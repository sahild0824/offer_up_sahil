#!/usr/bin/env python3
"""Run a draft scenario and save a simple "top 4 targets per round" table.

Examples
  python3 scenario.py                                   # 10 teams, slot 4, balanced/balanced
  python3 scenario.py --strategy hero-rb --profile upside
  python3 scenario.py --strategy zero-rb --profile safe --name zero_rb_safe
  python3 scenario.py --taken "Ja'Marr Chase,Bijan Robinson" --mine "Justin Jefferson" --start-round 2
  python3 scenario.py --teams 12 --slot 7

Outputs scenarios/<name>.md and scenarios/<name>.csv and prints the table.

The pick score lives in log-rank space so every knob is proportional: a 4-spot gap at pick 4
matters as much as a 40-spot gap at pick 40.
  score = -ln(composite)
          + k_boom * (boom - 50)/100  - k_bust * (bust - 50)/100  - k_risk * (risk - 50)/100
          + strategy adjustment for (round, position)     (e.g. +0.25 = "treat as 25% better")
          + roster-need adjustment
          - (1 - P(available at this pick)) * 0.5
Players are only candidates for a pick when P(available) >= --min-avail (default 0.30).
The #1 target of each round is assumed drafted, so later rounds reflect roster build-up.
"""
import argparse
import csv
import json
import math
import re
import unicodedata
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "data" / "players.json"
OUT = HERE / "scenarios"

PROFILES = {  # log-rank units per 100 points of score
    "safe": {"boom": 0.15, "bust": 0.50, "risk": 0.30},
    "balanced": {"boom": 0.30, "bust": 0.35, "risk": 0.15},
    "upside": {"boom": 0.60, "bust": 0.20, "risk": 0.05},
}

# strategy -> list of (round range, {pos: log-rank adjustment}); +0.25 ~ "25% better", -2 ~ "never"
STRATEGIES = {
    "balanced": [],
    "hero-rb": [((1, 1), {"WR": 0.15}), ((2, 2), {"RB": 0.35}), ((3, 5), {"WR": 0.10}), ((6, 9), {"RB": 0.15})],   # anchor WR at 4, bell-cow at 17
    "zero-rb": [((1, 5), {"RB": -2.0, "WR": 0.15, "TE": 0.10}), ((6, 12), {"RB": 0.35})],
    "robust-rb": [((1, 3), {"RB": 0.30}), ((4, 6), {"WR": 0.15})],
    "wr-heavy": [((1, 4), {"WR": 0.25, "RB": -0.15}), ((5, 8), {"RB": 0.20})],
}

STARTERS = {"QB": 1, "RB": 2, "WR": 2, "TE": 1}  # + 1 flex
CAPS = {"QB": 2, "RB": 6, "WR": 6, "TE": 2}
FLEX_FILL_ROUND = 6  # by this round the flex (RB/WR #3 combined) should be filled


def norm_name(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = s.lower().replace("'", "").replace(".", "").replace("-", " ")
    s = re.sub(r"\b(jr|sr|ii|iii|iv)\b", "", s)
    return re.sub(r"\s+", " ", s).strip()


def my_picks(teams, slot, rounds):
    return [((r - 1) * teams + slot) if r % 2 else (r * teams - slot + 1) for r in range(1, rounds + 1)]


def p_avail(adp, pick, adp_sd=None):
    if adp is None:
        return 0.5
    s = max(1.6, 0.55 * max(adp_sd or 0.0, 0.15 * adp))
    return 1 / (1 + math.exp((pick - adp) / s))


def strategy_adj(strategy, rnd, pos):
    adj = 0
    for (lo, hi), table in STRATEGIES[strategy]:
        if lo <= rnd <= hi:
            adj += table.get(pos, 0)
    return adj


def need_adj(roster, rnd, pos, teams):
    """Roster-construction nudges (log-rank units) for a 1-QB league."""
    count = {p: sum(1 for x in roster if x["pos"] == p) for p in STARTERS}
    adj = 0.0
    if count[pos] >= CAPS[pos]:
        return -3.0
    if pos == "QB":
        if count["QB"] >= 1:
            adj -= 1.5 if rnd < 12 else 0.2
        elif rnd <= 3:
            adj -= 0.4  # the research: do not pay the Allen tax in a 10-team one-QB league
    if pos == "TE":
        if count["TE"] >= 1:
            adj -= 1.2 if rnd < 11 else 0.2
        elif rnd <= 2:
            adj -= 0.15  # elite TE is a pivot, not the plan
    if pos in ("RB", "WR"):
        starters_short = STARTERS[pos] - count[pos]
        if starters_short > 0 and rnd >= 4:
            adj += 0.10 * starters_short
        if count["RB"] + count["WR"] < 5 and rnd >= FLEX_FILL_ROUND:
            adj += 0.05
        if count[pos] >= 5:
            adj -= 0.30
    if pos == "QB" and count["QB"] == 0 and rnd >= 9:
        adj += 0.15 + 0.10 * (rnd - 9)
    if pos == "TE" and count["TE"] == 0 and rnd >= 8:
        adj += 0.12 + 0.10 * (rnd - 8)
    return adj


def pick_score(p, rnd, pick, profile, strategy, roster, teams, sit_w=0.0, sos_w=0.0):
    k = PROFILES[profile]
    s = -math.log(p["comp"])
    s += k["boom"] * (p["boom"] - 50) / 100
    s -= k["bust"] * (p["bust"] - 50) / 100
    s -= k["risk"] * (p["risk"] - 50) / 100
    if p.get("sit") is not None:
        s += sit_w * (p["sit"] - 50) / 100
    if p.get("sos") and p["sos"].get("playoffsZ") is not None:
        s += sos_w * p["sos"]["playoffsZ"]
    s += strategy_adj(strategy, rnd, p["pos"])
    s += need_adj(roster, rnd, p["pos"], teams)
    pa = p_avail(p["adp"], pick, p.get("adpSd"))
    s -= (1 - pa) * 0.5
    return s, pa


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--teams", type=int, default=10)
    ap.add_argument("--slot", type=int, default=4)
    ap.add_argument("--rounds", type=int, default=14)
    ap.add_argument("--strategy", choices=sorted(STRATEGIES), default="balanced")
    ap.add_argument("--profile", choices=sorted(PROFILES), default="balanced")
    ap.add_argument("--min-avail", type=float, default=0.30, help="only list players at least this likely to be there")
    ap.add_argument("--taken", default="", help="comma-separated names already drafted by others")
    ap.add_argument("--mine", default="", help="comma-separated names already on your roster (in order)")
    ap.add_argument("--start-round", type=int, default=None, help="first round to plan (default: after your --mine picks)")
    ap.add_argument("--top", type=int, default=4)
    ap.add_argument("--sit-weight", type=float, default=0.10, help="log-rank units per 100 points of 2026 situation score (0 to ignore)")
    ap.add_argument("--sos-weight", type=float, default=0.04, help="log-rank units per z-score of fantasy-playoff schedule strength (weeks 15-17)")
    ap.add_argument("--name", default=None, help="scenario file name (default derived from settings)")
    a = ap.parse_args()

    players = json.loads(DATA.read_text())
    by_norm = {norm_name(p["name"]): p for p in players}

    def resolve(csv_names):
        out = []
        for n in [x.strip() for x in csv_names.split(",") if x.strip()]:
            p = by_norm.get(norm_name(n))
            if not p:
                cands = [q for q in players if norm_name(n) in norm_name(q["name"])]
                if len(cands) == 1:
                    p = cands[0]
            if not p:
                raise SystemExit(f"unknown player: {n!r}")
            out.append(p)
        return out

    taken = resolve(a.taken)
    roster = resolve(a.mine)
    gone = {p["id"] for p in taken} | {p["id"] for p in roster}
    picks = my_picks(a.teams, a.slot, a.rounds)
    start = a.start_round or (len(roster) + 1)

    rows = []
    for rnd in range(start, a.rounds + 1):
        pick = picks[rnd - 1]
        cands = []
        for p in players:
            if p["id"] in gone:
                continue
            s, pa = pick_score(p, rnd, pick, a.profile, a.strategy, roster, a.teams, a.sit_weight, a.sos_weight)
            if pa < a.min_avail:
                continue
            cands.append((s, pa, p))
        cands.sort(key=lambda t: -t[0])
        top = cands[: a.top]
        rows.append((rnd, pick, top))
        if top:
            roster.append(top[0][2])
            gone.add(top[0][2]["id"])

    name = a.name or f"{a.teams}team_slot{a.slot}_{a.strategy}_{a.profile}".replace("-", "")
    OUT.mkdir(exist_ok=True)

    def cell(t):
        s, pa, p = t
        return f"{p['name']} ({p['pos']}{p['posRank']}, comp {p['comp']:.0f}, {pa * 100:.0f}%, 2026 {p.get('sit', '–')})"

    hdr = f"# Scenario: {name}\n\n"
    hdr += f"- League: {a.teams} teams, slot {a.slot}, full PPR snake, picks {', '.join('#' + str(x) for x in picks)}\n"
    hdr += f"- Strategy: **{a.strategy}** · risk profile: **{a.profile}** · min availability {a.min_avail:.0%} · 2026 situation weight {a.sit_weight} · playoff-schedule weight {a.sos_weight}\n"
    if taken:
        hdr += f"- Already gone: {', '.join(p['name'] for p in taken)}\n"
    if a.mine:
        hdr += f"- Your roster coming in: {', '.join(p['name'] for p in resolve(a.mine))}\n"
    hdr += f"- Generated {datetime.now():%Y-%m-%d %H:%M}\n\n"
    hdr += "Cell = player (position rank, composite rank, chance still on the board at that pick). "
    hdr += "The #1 target each round is assumed drafted before planning the next round.\n\n"

    cols = ["Rd", "Pick"] + [f"#{i + 1}" for i in range(a.top)]
    md = hdr + "| " + " | ".join(cols) + " |\n|" + "|".join(["---"] * len(cols)) + "|\n"
    for rnd, pick, top in rows:
        cells = [cell(t) for t in top] + [""] * (a.top - len(top))
        md += f"| {rnd} | {pick} | " + " | ".join(cells) + " |\n"

    final = [p for p in roster]
    md += "\n## Resulting roster if you take the #1 target every round\n\n"
    for i, p in enumerate(final, 1):
        md += f"{i}. {p['name']} — {p['pos']}{p['posRank']} {p['team']} (bye {p['bye']}) · comp {p['comp']} · proj {p.get('proj') or '–'} · VBD {p.get('vbd') if p.get('vbd') is not None else '–'} · boom {p['boom']} / bust {p['bust']} / risk {p['risk']}\n"
    counts = {pos: sum(1 for p in final if p["pos"] == pos) for pos in ("QB", "RB", "WR", "TE")}
    md += "\nPosition mix: " + ", ".join(f"{k} {v}" for k, v in counts.items()) + "\n"

    (OUT / f"{name}.md").write_text(md)
    with (OUT / f"{name}.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["round", "pick", "slot", "player", "pos", "pos_rank", "team", "bye", "composite", "adp", "p_available", "proj", "vbd", "boom", "bust", "risk", "situation", "playoff_sos_rank", "score"])
        for rnd, pick, top in rows:
            for i, (s, pa, p) in enumerate(top, 1):
                w.writerow([rnd, pick, i, p["name"], p["pos"], p["posRank"], p["team"], p["bye"], p["comp"], p["adp"], round(pa, 2), p.get("proj"), p.get("vbd"), p["boom"], p["bust"], p["risk"], p.get("sit"), (p.get("sos") or {}).get("playoffs"), round(s, 3)])

    print(md)
    print(f"saved scenarios/{name}.md and .csv")


if __name__ == "__main__":
    main()
