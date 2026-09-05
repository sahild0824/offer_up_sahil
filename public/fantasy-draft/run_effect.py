"""Does modelling positional runs actually change availability, or is it decoration?

A/B the simulator with the run mechanic off and on, over the same seeds.
"""
import numpy as np, statistics as st
import montecarlo as mc

players = mc.load_players("espn", None)
by = {p["name"]: i for i, p in enumerate(players)}
WATCH = ["Chase Brown", "Omarion Hampton", "Kenneth Walker III", "Brock Bowers", "Trey McBride",
         "Drake Maye", "Jayden Daniels", "Tee Higgins", "Tucker Kraft", "Colston Loveland"]
SIMS = 800
out = {}
for label, pull in (("runs off", 0.0), ("runs on", 0.06)):
    mc.RUN_FRAC = pull
    r = mc.simulate(players, 10, 4, "robust-rb", "balanced", SIMS, seed=5)
    out[label] = r
    v = np.array([x[0] for x in r["values"]])
    print(f"{label:9s} lineup mean {v.mean():7.1f}  sd {v.std():5.1f}")

picks = out["runs on"]["my_picks"]
print(f"\n{'player':22s} {'pick':>5s} {'off':>7s} {'on':>7s} {'delta':>7s}")
for nm in WATCH:
    i = by.get(nm)
    if i is None:
        continue
    rd = 1 if nm in ("Chase Brown",) else None
    # report at the first of our picks where the two runs differ most
    best = max(range(len(picks)), key=lambda r: abs(out["runs off"]["avail"][r, i] - out["runs on"]["avail"][r, i]))
    a, b = out["runs off"]["avail"][best, i], out["runs on"]["avail"][best, i]
    print(f"{nm:22s} {picks[best]:5d} {a:7.0%} {b:7.0%} {b-a:+7.0%}")

# the real question: is the board less predictable?
for label in ("runs off", "runs on"):
    av = out[label]["avail"]
    mid = av[(av > 0.02) & (av < 0.98)]
    print(f"\n{label}: {mid.size} player-picks genuinely uncertain (2-98%)", end="")
print()
