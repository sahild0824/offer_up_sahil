"""Rounds 2-3 with Brock Bowers on the board: force each policy, same seeds, run-aware room."""
import numpy as np, montecarlo as mc
from collections import Counter
players = mc.load_players("espn", None)
by = {p["name"]: i for i, p in enumerate(players)}
RB = ["Chase Brown", "Omarion Hampton", "Kenneth Walker III"]
POLICIES = [
    ("Model's default (no forcing)",              {0: "Puka Nacua"}),
    ("Bowers at 17 whenever there",               {0: "Puka Nacua", 1: "Brock Bowers"}),
    ("Bowers at 24 whenever there (not at 17)",   {0: "Puka Nacua", 2: "Brock Bowers"}),
    ("RB at 17 if Brown/Hampton/Walker, else Bowers; Bowers at 24 if still there", {0: "Puka Nacua", 1: RB + ["Brock Bowers"], 2: ["Brock Bowers"]}),
    ("RB at 17 if there else Collins; Bowers at 24 if there", {0: "Puka Nacua", 1: RB + ["Nico Collins"], 2: ["Brock Bowers"]}),
    ("WR-WR at 17 and 24, never Bowers early",   {0: "Puka Nacua", 1: ["Nico Collins", "George Pickens"], 2: ["George Pickens", "Nico Collins", "DeVonta Smith"]}),
]
print(f"{'policy':78s} {'lineup':>7s} {'floor':>6s} {'ceil':>6s}  {'Bowers landed':>13s}")
for label, forced in POLICIES:
    r = mc.simulate(players, 10, 4, "balanced", "safe", 700, seed=77, forced=forced)
    v = np.array([x[0] for x in r["values"]]); fl = np.array([x[1] for x in r["values"]]); ce = np.array([x[2] for x in r["values"]])
    got = sum(r["picks"][i]["Brock Bowers"] for i in (1, 2)) / len(v)
    print(f"{label:78s} {v.mean():7.0f} {fl.mean():6.0f} {ce.mean():6.0f}  {got:13.0%}")
