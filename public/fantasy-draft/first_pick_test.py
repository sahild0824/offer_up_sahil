"""Force each candidate at pick 4, then draft the rest with the current best build, under the
run-aware simulator. Answers "why not a running back at 4" with the model as it is now."""
import numpy as np, montecarlo as mc
players = mc.load_players("espn", None)
by = {p["name"]: i for i, p in enumerate(players)}
base = mc.simulate(players, 10, 4, "balanced", "safe", 600, seed=41)
print(f"{'forced at 4':22s} {'there':>6s} {'lineup':>7s} {'floor':>6s} {'ceil':>6s}  {'RB/WR drafted':>13s}")
rows = []
for cand in ["Jonathan Taylor", "Christian McCaffrey", "James Cook III", "De'Von Achane", "Puka Nacua", "Ja'Marr Chase", "Jaxon Smith-Njigba", "Amon-Ra St. Brown"]:
    r = mc.simulate(players, 10, 4, "balanced", "safe", 600, seed=41, forced_first=cand)
    v = np.array([x[0] for x in r["values"]]); fl = np.array([x[1] for x in r["values"]]); ce = np.array([x[2] for x in r["values"]])
    mix = sum((x[3] for x in r["values"]), start=__import__("collections").Counter())
    k = len(r["values"])
    av = base["avail"][0, by[cand]]
    rows.append((cand, av, v.mean(), fl.mean(), ce.mean(), mix["RB"]/k, mix["WR"]/k))
for cand, av, m, f, c, rb, wr in sorted(rows, key=lambda x: -x[2]):
    print(f"{cand:22s} {av:6.0%} {m:7.0f} {f:6.0f} {c:6.0f}  {rb:5.1f} / {wr:4.1f}")
