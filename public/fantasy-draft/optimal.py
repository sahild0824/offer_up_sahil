"""Consolidate the four draft-day branches into one round-by-round plan.

Each branch runs the strategy that won the sweep for it; rows are the runner's pick plus its
simulated availability and the best fallback. Rounds 13-14 (D/ST, K) come from the research.
"""
import csv, json, re
from pathlib import Path

OUT = Path("scenarios")
BR = [
    ("A", "branch_A_nacua", "Nacua is the best man left and is cleared to play", "balanced, safe", "53% of boards"),
    ("B", "branch_B_chase", "Chase falls to 4", "balanced, safe", "44% of boards"),
    ("C", "branch_C_rb_falls", "Gibbs or Bijan falls to 4", "WR heavy, safe", "2% of boards"),
    ("D", "branch_D_nacua_out", "Nacua is out or suspended and Chase is gone", "balanced, safe", "only if Nacua is scratched"),
]
FIRST = {"A": "Puka Nacua", "B": "Ja'Marr Chase", "C": "Bijan Robinson", "D": None}
LATE = [(13, 124, "D/ST — Chargers", "host ARI and LV in weeks 1-2, the consensus best opener; Chiefs, Packers, Bears next"),
        (14, 137, "K — Brandon Aubrey", "the one kicker experts take early; our 3/4/5-point distance tiers reward his range")]
probs = json.load(open(OUT / "branch_probs.json"))
doc = ["# The optimal team, four draft-day branches\n",
       "10 teams, slot 4, full PPR, head-to-head, 14 rounds (QB, 2 RB, 2 WR, TE, FLEX, D/ST, K, 5 bench).",
       "Each branch runs every strategy and profile; the one shown won its branch on projected lineup value.",
       "Availability is from 2,000 simulated ESPN drafts, and no pick below 35% likely to be there is recommended.\n",
       "## Which branch fires at pick 4\n",
       "Following the decision order Gibbs > Bijan > Chase > Nacua, over 3,000 simulated drafts:\n",
       "| Branch | Frequency |", "|---|---|"] + [f"| {k} | {v:.0%} |" for k, v in json.load(open(OUT / "branch_freq.json")).items()] + [
       "",
       "One of the four is on the board at pick 4 in every single simulated draft, so branch D is not a board",
       "outcome at all: it only fires if Nacua is scratched or suspended and Chase is already gone.\n",
       "## What survives to each of your picks\n",
       "| Group at your pick | at least 1 | at least 2 | mean left |", "|---|---|---|---|"]
for lab in ("elite4 @4", "anchorRB @17", "anchorRB @24", "eliteTE @24", "WRt1 @24", "QBtier @57", "QBtier @64", "QBnext @97", "midTE @77"):
    v = probs[lab]
    doc.append(f"| {lab} | {v['p1']:.0%} | {v['p2']:.0%} | {v['mean']:.2f} |")
doc.append("")
summary = []
for key, fname, label, strat, prob in BR:
    md = (OUT / f"{fname}.md").read_text()
    proj = re.search(r"Projected: \*\*(\d+)\*\*", md).group(1)
    floor = re.search(r"Floor \(p10\): \*\*(\d+)\*\*", md).group(1)
    ceil = re.search(r"Ceiling \(p90\): \*\*(\d+)\*\*", md).group(1)
    rows = list(csv.DictReader((OUT / f"{fname}.csv").open()))
    picks, alts = {}, {}
    for r in rows:
        rnd = int(r["round"])
        if r["slot"] == "1":
            picks[rnd] = r
        elif rnd not in alts:
            alts[rnd] = r
    doc += [f"## Scenario {key}: {label}", "",
            f"**{strat}** · {prob} · projected lineup **{proj}** (floor {floor}, ceiling {ceil})", "",
            "| Rd | Pick | Take | Pos | There | Fallback |", "|---|---|---|---|---|---|"]
    if FIRST[key]:
        doc.append(f"| 1 | 4 | **{FIRST[key]}** | — | this branch | see the other branches |")
    for rnd in sorted(picks):
        p, a = picks[rnd], alts.get(rnd)
        doc.append(f"| {rnd} | {p['pick']} | **{p['player']}** | {p['pos']}{p['pos_rank']} {p['team']} | {float(p['p_available']):.0%} | "
                   + (f"{a['player']} ({float(a['p_available']):.0%})" if a else "—") + " |")
    for rnd, pick, who, why in LATE:
        doc.append(f"| {rnd} | {pick} | **{who}** | — | — | {why} |")
    doc.append("")
    summary.append((key, label, strat, proj, floor, ceil))
doc = ["# The optimal team, four draft-day branches\n"] + doc[1:]
doc += ["## Scenarios ranked", "", "| Branch | Situation | Build | Projected | Floor | Ceiling |", "|---|---|---|---|---|---|"]
for key, label, strat, proj, floor, ceil in sorted(summary, key=lambda x: -int(x[3])):
    doc.append(f"| {key} | {label} | {strat} | {proj} | {floor} | {ceil} |")
doc.append("")
(OUT / "OPTIMAL.md").write_text("\n".join(doc))

# machine-readable twin for the app
js = {"freq": json.load(open(OUT / "branch_freq.json")), "survives": probs, "branches": []}
for key, fname, label, strat, prob in BR:
    md = (OUT / f"{fname}.md").read_text()
    rows = list(csv.DictReader((OUT / f"{fname}.csv").open()))
    picks = {int(r["round"]): r for r in rows if r["slot"] == "1"}
    alts = {}
    for r in rows:
        rnd = int(r["round"])
        if r["slot"] != "1" and rnd not in alts:
            alts[rnd] = r
    b = {"key": key, "label": label, "strategy": strat, "freq": prob,
         "proj": int(re.search(r"Projected: \*\*(\d+)\*\*", md).group(1)),
         "floor": int(re.search(r"Floor \(p10\): \*\*(\d+)\*\*", md).group(1)),
         "ceil": int(re.search(r"Ceiling \(p90\): \*\*(\d+)\*\*", md).group(1)),
         "first": FIRST[key], "picks": []}
    for rnd in sorted(picks):
        p, a = picks[rnd], alts.get(rnd)
        b["picks"].append({"round": rnd, "pick": int(p["pick"]), "player": p["player"], "pos": p["pos"],
                           "avail": float(p["p_available"]),
                           "alt": a["player"] if a else None, "altAvail": float(a["p_available"]) if a else None})
    js["branches"].append(b)
(OUT / "optimal.json").write_text(json.dumps(js, indent=1))
print("\n".join(doc))
