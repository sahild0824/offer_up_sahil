"""Joint probabilities for the draft's branch points, from the same simulated ESPN room.

The per-player availability table gives marginals; the decisions at 4, 17, 24 and 57 depend on
whether *any* member of a tier survives, which only the joint distribution answers.
"""
import json
from collections import Counter
import montecarlo as mc

players = mc.load_players("espn", None)
by = {p["name"]: p["id"] for p in players}
G = lambda *names: [by[n] for n in names if n in by]

ELITE4 = G("Jahmyr Gibbs", "Bijan Robinson", "Ja'Marr Chase", "Puka Nacua")
ANCHOR_RB = G("De'Von Achane", "Chase Brown", "James Cook III", "Kenneth Walker III", "Omarion Hampton", "Derrick Henry", "Saquon Barkley")
WR_T1 = G("Drake London", "Nico Collins", "A.J. Brown", "Chris Olave", "Malik Nabers", "George Pickens")
QB_TIER = G("Jayden Daniels", "Drake Maye", "Joe Burrow", "Jalen Hurts")
QB_NEXT = G("Justin Herbert", "Caleb Williams", "Trevor Lawrence", "Jaxson Dart", "Kyler Murray", "Matthew Stafford")
TE_ELITE = G("Brock Bowers", "Trey McBride")
TE_MID = G("Colston Loveland", "Tyler Warren", "Tucker Kraft", "Harold Fannin Jr.", "Sam LaPorta")

probe = {
    "elite4 @4": (4, ELITE4), "anchorRB @17": (17, ANCHOR_RB), "anchorRB @24": (24, ANCHOR_RB),
    "eliteTE @17": (17, TE_ELITE), "eliteTE @24": (24, TE_ELITE), "WRt1 @24": (24, WR_T1),
    "QBtier @44": (44, QB_TIER), "QBtier @57": (57, QB_TIER), "QBtier @64": (64, QB_TIER),
    "QBnext @77": (77, QB_NEXT), "QBnext @97": (97, QB_NEXT),
    "midTE @44": (44, TE_MID), "midTE @57": (57, TE_MID), "midTE @64": (64, TE_MID), "midTE @77": (77, TE_MID),
}
SIMS = 2000
r = mc.simulate(players, 10, 4, "hero-rb", "balanced", SIMS, seed=23, probe=probe)
out = {}
print(f"{SIMS} simulated ESPN drafts, 10 teams, slot 4\n")
print(f"{'group at your pick':22s} {'>=1':>6s} {'>=2':>6s} {'>=3':>6s}   mean")
for lab, hits in r["probe"].items():
    n = len(hits)
    row = {k: sum(1 for h in hits if h >= k) / n for k in (1, 2, 3)}
    out[lab] = {"p1": round(row[1], 3), "p2": round(row[2], 3), "p3": round(row[3], 3), "mean": round(sum(hits) / n, 2)}
    print(f"{lab:22s} {row[1]:6.0%} {row[2]:6.0%} {row[3]:6.0%}   {sum(hits)/n:.2f}")
json.dump(out, open("scenarios/branch_probs.json", "w"), indent=1)
print("\nsaved scenarios/branch_probs.json")
