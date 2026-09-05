"""Mutually exclusive frequencies for the pick-4 decision, following the plan's order:
Gibbs > Bijan > Chase > Nacua > Smith-Njigba / St. Brown."""
import json
import montecarlo as mc

players = mc.load_players("espn", None)
by = {p["name"]: p["id"] for p in players}
probe = {n: (4, [by[n]]) for n in ("Jahmyr Gibbs", "Bijan Robinson", "Ja'Marr Chase", "Puka Nacua")}
SIMS = 3000
r = mc.simulate(players, 10, 4, "hero-rb", "balanced", SIMS, seed=101, probe=probe)
h = r["probe"]
n = len(h["Puka Nacua"])
branch = {"C (Gibbs or Bijan)": 0, "B (Chase)": 0, "A (Nacua)": 0, "D (none of them)": 0}
for i in range(n):
    if h["Jahmyr Gibbs"][i] or h["Bijan Robinson"][i]:
        branch["C (Gibbs or Bijan)"] += 1
    elif h["Ja'Marr Chase"][i]:
        branch["B (Chase)"] += 1
    elif h["Puka Nacua"][i]:
        branch["A (Nacua)"] += 1
    else:
        branch["D (none of them)"] += 1
out = {k: round(v / n, 3) for k, v in branch.items()}
print(f"{SIMS} simulated drafts, pick 4, following the decision order:\n")
for k, v in out.items():
    print(f"  {k:22s} {v:5.0%}")
print("\nNote: branch A also requires Nacua to be cleared to play; the simulation only models the board.")
json.dump(out, open("scenarios/branch_freq.json", "w"), indent=1)
