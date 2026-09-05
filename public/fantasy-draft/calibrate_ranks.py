"""Same translation check for the ranking lists: is any of them not really full PPR?

Each list is compared with the full-PPR consensus (FantasyPros PPR ECR) over the players they
share, ranked within that shared set. A list published in half PPR or TE premium shows up as a
systematic positional tilt; a genuine full-PPR list sits near zero on every position.
"""
import json, math
from statistics import median
from pathlib import Path

R = json.loads((Path(__file__).parent / "data" / "rankings.json").read_text())
REF, MAX_RANK, MIN_SHARED, ANCHOR = "fantasypros_ecr", 160, 10, 40
pos = {r["name"]: r["pos"] for r in R}
feeds = {}
for row in R:
    for k, v in (row.get("ranks") or {}).items():
        if isinstance(v, (int, float)) and v > 0 and not k.endswith("_posrank"):
            feeds.setdefault(k, {})[row["name"]] = float(v)

rank = lambda d: {n: i + 1 for i, (n, _) in enumerate(sorted(d.items(), key=lambda kv: kv[1]))}
out, rep = {}, []
for feed, vals in feeds.items():
    if feed == REF:
        continue
    common = [n for n in vals if n in feeds[REF]]
    ref_all = rank({n: feeds[REF][n] for n in common})
    pool = [n for n in common if ref_all[n] <= MAX_RANK]
    if len(pool) < 30:
        continue
    fr, rr = rank({n: vals[n] for n in pool}), rank({n: feeds[REF][n] for n in pool})
    d_all = [math.log(fr[n]) - math.log(rr[n]) for n in pool]
    overall = median(d_all)
    by = {}
    for p in ("QB", "RB", "WR", "TE"):
        d = [math.log(fr[n]) - math.log(rr[n]) for n in pool if pos.get(n) == p]
        by[p] = (median(d) - overall) if len(d) >= MIN_SHARED else 0.0
    tilt = max(abs(v) for v in by.values())
    out[feed] = {"byPos": {k: round(v, 4) for k, v in by.items()}, "n": len(pool), "tilt": round(tilt, 4)}
    rep.append((feed, by, len(pool), tilt))

(Path(__file__).parent / "data" / "rank_calibration.json").write_text(json.dumps({"reference": REF, "feeds": out}, indent=1))
print(f"Ranking lists vs {REF} (full PPR). Picks a player at ESPN pick {ANCHOR} would move; near zero = same format.\n")
print(f"{'list':34s} {'n':>4s} {'QB':>7s} {'RB':>7s} {'WR':>7s} {'TE':>7s}  verdict")
for feed, by, n, tilt in sorted(rep, key=lambda r: -r[3]):
    cells = "".join(f"{ANCHOR * math.exp(by[p]) - ANCHOR:+7.1f}" for p in ("QB", "RB", "WR", "TE"))
    v = "OFF FORMAT" if tilt > 0.35 else ("tilted" if tilt > 0.18 else "full PPR")
    print(f"{feed:34s} {n:4d} {cells}  {v}")
print(f"\nwrote data/rank_calibration.json ({len(out)} lists)")
