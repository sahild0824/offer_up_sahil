"""WR at 4, then what? RB-RB at 17 and 24 against the alternatives, same seeds, run-aware room."""
import numpy as np, montecarlo as mc
players = mc.load_players("espn", None)
ANCHOR = ["Chase Brown", "Omarion Hampton", "James Cook III", "De'Von Achane", "Saquon Barkley", "Kenneth Walker III", "Derrick Henry"]
NEXT_RB = ["Breece Hall", "Javonte Williams", "Quinshon Judkins", "D'Andre Swift", "Bucky Irving", "TreVeyon Henderson"]
WR3 = ["Nico Collins", "George Pickens", "Chris Olave", "DeVonta Smith"]
POLICIES = [
    ("RB-RB: anchor back at 17, best back at 24 (anchor, else next tier)",  {0: "Puka Nacua", 1: ANCHOR, 2: ANCHOR + NEXT_RB}),
    ("RB-RB but only anchors; if no 2nd anchor at 24 take Bowers, else WR", {0: "Puka Nacua", 1: ANCHOR, 2: ANCHOR + ["Brock Bowers"] + WR3}),
    ("RB at 17, Bowers at 24 if there, else WR",                              {0: "Puka Nacua", 1: ANCHOR, 2: ["Brock Bowers"] + WR3}),
    ("RB at 17, WR at 24",                                                    {0: "Puka Nacua", 1: ANCHOR, 2: WR3}),
    ("Bowers at 17, RB at 24 (anchor, else next tier)",                       {0: "Puka Nacua", 1: ["Brock Bowers"], 2: ANCHOR + NEXT_RB}),
    ("Bowers at 17, WR at 24",                                                {0: "Puka Nacua", 1: ["Brock Bowers"], 2: WR3}),
    ("Model's default",                                                       {0: "Puka Nacua"}),
]
print(f"{'policy':70s} {'lineup':>7s} {'floor':>6s} {'ceil':>6s}  {'2 backs by 24':>13s}")
for label, forced in POLICIES:
    r = mc.simulate(players, 10, 4, "balanced", "safe", 700, seed=77, forced=forced)
    v = np.array([x[0] for x in r["values"]]); fl = np.array([x[1] for x in r["values"]]); ce = np.array([x[2] for x in r["values"]])
    rb2 = sum(c for n, c in r["picks"][1].items() if n in ANCHOR + NEXT_RB) and sum(c for n, c in r["picks"][2].items() if n in ANCHOR + NEXT_RB)
    two = min(sum(c for n, c in r["picks"][1].items() if n in ANCHOR + NEXT_RB), sum(c for n, c in r["picks"][2].items() if n in ANCHOR + NEXT_RB)) / len(v)
    print(f"{label:70s} {v.mean():7.0f} {fl.mean():6.0f} {ce.mean():6.0f}  {two:13.0%}")
