"""Translate every ADP feed onto our league's scale before blending.

The board we draft on is ESPN, 10 teams, full PPR. The other feeds are useful for variance
reduction but several are measured in a different game: Underdog and Draft Sharks are half PPR,
FFPC is TE-premium, and the Fantasy Football Calculator / UDK feeds are 12-team. Blending them
raw imports their bias.

Method. Every feed is reduced to an ordinal rank over the players it shares with ESPN, so feeds
with different pick scales (12-team pick numbers, best-ball boards) are comparable. For each feed
and position we take the median of log(rank_feed) - log(rank_espn) over the shared players inside
the drafted range. The feed's own overall offset is then removed, leaving pure positional bias: "this feed ranks tight
ends x% later than it ranks everyone else, compared with ESPN". That is what gets corrected. Positions with too few shared players fall back to
the feed's overall offset.
"""
import json
import math
from collections import defaultdict
from pathlib import Path
from statistics import median

HERE = Path(__file__).parent
RANKINGS = json.loads((HERE / "data" / "rankings.json").read_text())
MARKET = json.loads((HERE / "data" / "market_features.json").read_text())
REF = "espn_live"
MAX_RANK = 160      # the drafted range in a 10-team, 14-round league is 140 picks
MIN_SHARED = 12     # per position, below this fall back to the feed's overall offset

FORMAT_NOTE = {
    "underdog": "half PPR, best ball", "rotowire_underdog": "half PPR, best ball",
    "udk_underdog_pick": "half PPR, best ball", "underdog_rank_aug24": "half PPR",
    "draftsharks_half_consensus": "half PPR", "yahoo_rank_aug24": "half PPR",
    "ffpc": "TE premium", "flock_ffpc_rank": "TE premium",
    "nfc_ppr": "full PPR, 12-team", "nfc_ppr_aug28": "full PPR, 12-team", "ffc_sep4": "full PPR, 12-team",
    "udk_avg_pick": "12-team", "udk_sleeper_pick": "12-team", "udk_espn_pick": "12-team", "udk_yahoo_pick": "12-team",
    "espn": "format-agnostic", "yahoo": "format-agnostic", "yahoo_aug25": "format-agnostic",
    "sleeper_aug29": "scoring not labelled", "subvertadown": "full PPR, 12-team",
}


def norm(s):
    return "".join(ch for ch in s.lower() if ch.isalnum() or ch == " ").strip()


# market_features is keyed "normalised name|POS"; map it back to the ranking spellings
MKT_NAME = {}
for _r in RANKINGS:
    MKT_NAME[f"{norm(_r['name'])}|{_r['pos']}"] = _r["name"]


def feed_values():
    """{feed: {player_name: raw value}} across rankings adp / adp_ranks and the live market feeds."""
    feeds = defaultdict(dict)
    for row in RANKINGS:
        nm = row["name"]
        for block in ("adp", "adp_ranks"):
            for k, v in (row.get(block) or {}).items():
                if isinstance(v, (int, float)) and v > 0:
                    feeds[k][nm] = float(v)
    for key, m in MARKET["players"].items():
        nm = MKT_NAME.get(key)
        if not nm:
            continue
        for k, v in (("espn_live", (m.get("espn") or {}).get("adp")), ("sleeper_live", (m.get("sleeper") or {}).get("adpPpr")),
                     ("ffc_live", m.get("ffc")), ("ffc_half", m.get("ffcHalf")), ("ffc_std", m.get("ffcStd")),
                     ("sleeper_adp", m.get("sleeperAdp"))):
            if isinstance(v, (int, float)) and v > 0:
                feeds[k][nm] = float(v)
    return feeds


def to_rank(vals):
    """Ordinal rank (1..n) so feeds on different pick scales are comparable."""
    return {nm: i + 1 for i, (nm, _) in enumerate(sorted(vals.items(), key=lambda kv: kv[1]))}


def main():
    feeds = feed_values()
    pos = {r["name"]: r["pos"] for r in RANKINGS}
    if REF not in feeds:
        raise SystemExit(f"no {REF} feed to calibrate against")

    out, report = {}, []
    for feed, vals in sorted(feeds.items()):
        if feed == REF or len(vals) < 40:
            continue
        # rank both feeds over the players they share, so coverage differences do not masquerade as bias
        common = [nm for nm in vals if nm in feeds[REF]]
        pool = [nm for nm in common if to_rank({k: feeds[REF][k] for k in common})[nm] <= MAX_RANK]
        if len(pool) < 30:
            continue
        rank = to_rank({nm: vals[nm] for nm in pool})
        ref_rank = to_rank({nm: feeds[REF][nm] for nm in pool})
        shared = pool
        d_all = [math.log(rank[nm]) - math.log(ref_rank[nm]) for nm in shared]
        overall = median(d_all)
        by_pos, n_by_pos = {}, {}
        for p in ("QB", "RB", "WR", "TE"):
            d = [math.log(rank[nm]) - math.log(ref_rank[nm]) for nm in shared if pos.get(nm) == p]
            n_by_pos[p] = len(d)
            by_pos[p] = median(d) if len(d) >= MIN_SHARED else overall
        out[feed] = {"overall": round(overall, 4), "byPos": {k: round(v - overall, 4) for k, v in by_pos.items()},
                     "n": len(shared), "nByPos": n_by_pos, "note": FORMAT_NOTE.get(feed, "")}
        report.append((feed, overall, by_pos, n_by_pos, FORMAT_NOTE.get(feed, "")))

    (HERE / "data" / "adp_calibration.json").write_text(json.dumps(
        {"reference": REF, "maxRank": MAX_RANK, "feeds": out}, indent=1))

    # A log offset of d means the feed ranks that position exp(d) times deeper than ESPN.
    # Report it at pick 40 so the number is readable in picks rather than log units.
    ANCHOR = 40
    print(f"Calibrated against {REF} (our draft platform: ESPN, 10 teams, full PPR).")
    print(f"Numbers are where each feed puts a player ESPN has at pick {ANCHOR}. Negative = the feed drafts him earlier.\n")
    print(f"{'feed':28s} {'n':>4s} {'QB':>7s} {'RB':>7s} {'WR':>7s} {'TE':>7s}   note")
    for feed, overall, by_pos, n_by_pos, note in sorted(report, key=lambda r: -abs(r[1])):
        cells = "".join(f"{ANCHOR * math.exp(by_pos[p] - overall) - ANCHOR:+7.1f}" for p in ("QB", "RB", "WR", "TE"))
        print(f"{feed:28s} {sum(n_by_pos.values()):4d} {cells}   {note}")
    print(f"\nwrote data/adp_calibration.json ({len(out)} feeds)")


if __name__ == "__main__":
    main()
