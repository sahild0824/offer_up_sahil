"""Adversarial checks on the model's own output. Each one is a claim the board makes that could be
false; the test tries to break it."""
import json, math, statistics
from pathlib import Path
H = Path(__file__).parent
P = json.loads((H / "data" / "players.json").read_text())
PL = P["players"] if isinstance(P, dict) else P
BY = {p["name"]: p for p in PL}
opt = json.loads((H / "scenarios" / "optimal.json").read_text())
cal = json.loads((H / "data" / "adp_calibration.json").read_text())
ver = json.loads((H / "data" / "market_verdicts.json").read_text())

print("=" * 78)
print("A. Does the recommended chain actually survive? (branch A, robust RB)")
print("=" * 78)
for b in opt["branches"][:1]:
    chain = 1.0
    print(f"{'rd':>3s} {'pick':>5s}  {'player':22s} {'there':>6s} {'chain':>7s}")
    for pk in b["picks"]:
        chain *= pk["avail"]
        print(f"{pk['round']:3d} {pk['pick']:5d}  {pk['player']:22s} {pk['avail']:6.0%} {chain:7.2%}")
    print(f"\n  -> the exact 12-man roster the scenario prints occurs in {chain:.4%} of drafts.")
    print(f"  -> its projected {b['proj']} is therefore a conditional number, not an expectation.")

print()
print("=" * 78)
print("B. Is the calibration circular? (ESPN is both the 3x-weighted feed and the reference)")
print("=" * 78)
feeds = cal["feeds"]
print(f"  reference = {cal['reference']}, which also carries 3.0 weight in the blend (next highest 1.0).")
tot = 3.0 + 1.0 + 0.75 + 0.75 + 0.5
print(f"  ESPN's share of the fresh-feed weight: {3.0/tot:.0%}")
print("  Calibrating every other feed onto ESPN's positional structure removes exactly the")
print("  cross-platform disagreement the blend exists to capture. Measured below.")

print()
print("=" * 78)
print("C. How many players actually back each offset? (small n = noisy correction)")
print("=" * 78)
thin = []
for f, v in feeds.items():
    n = v.get("nByPos", {})
    for pos in ("QB", "TE"):
        if n.get(pos, 0) < 12:
            thin.append((f, pos, n.get(pos, 0)))
print(f"  feeds whose QB or TE offset fell back to the overall offset (n < 12): {len(thin)}")
for f, pos, n in thin[:8]:
    print(f"    {f:28s} {pos} n={n}")
qbn = [v["nByPos"].get("QB", 0) for v in feeds.values()]
ten = [v["nByPos"].get("TE", 0) for v in feeds.values()]
print(f"  median shared players per feed: QB {statistics.median(qbn):.0f}, TE {statistics.median(ten):.0f}")
print("  -> QB and TE offsets are the largest corrections AND rest on the fewest players.")

print()
print("=" * 78)
print("D. Scale mismatch: offsets fitted in rank space, applied to raw ADP values")
print("=" * 78)
print("  A 12-team feed's pick numbers run to ~192; ESPN's to ~140. The offset was measured after")
print("  rank-normalising, then multiplied against the RAW value. Effect at the deep end:")
for f in ("nfc_ppr", "underdog"):
    d = feeds[f]["byPos"]["TE"]
    for raw in (30, 90, 150):
        print(f"    {f:10s} TE raw {raw:3d} -> {raw*math.exp(-d):6.1f}  (moves {raw*math.exp(-d)-raw:+.1f})")
print("  -> the correction scales with the pick number, so a deep TE is moved several times")
print("     further than an early one, which the rank-space fit does not justify.")

print()
print("=" * 78)
print("E. Are the outlet counts independent evidence?")
print("=" * 78)
tot_for = sum(v["for"] for v in ver)
tot_ag = sum(v["against"] for v in ver)
print(f"  77 players, {tot_for} 'for' citations, {tot_ag} 'against' -> {tot_for/(tot_for+tot_ag):.0%} positive.")
lop = [v for v in ver if v["against"] == 0]
print(f"  players with ZERO recorded counter-argument: {len(lop)} ({len(lop)/len(ver):.0%})")
print("   ", ", ".join(v["name"] for v in lop[:8]))
print("  -> a search that finds reasons to draft someone will mostly surface bullish copy.")
print("     The for/against split measures what was written, not whether it is true.")

print()
print("=" * 78)
print("F. Do the model and the market ever actually disagree, or is the model just ADP?")
print("=" * 78)
import statistics as st
pairs = [(p["comp"], p["adp"]) for p in PL if p.get("comp") and p.get("adp") and p["adp"] <= 140]
n = len(pairs)
mc = st.mean([a for a, _ in pairs]); ma = st.mean([b for _, b in pairs])
cov = sum((a-mc)*(b-ma) for a, b in pairs)/n
r = cov/(st.pstdev([a for a,_ in pairs])*st.pstdev([b for _,b in pairs]))
print(f"  composite vs blended ADP, drafted range: r = {r:.3f} (n={n})")
gaps = [abs(p["adp"]-p["comp"]) for p in PL if p.get("comp") and p.get("adp") and p["adp"] <= 140]
print(f"  median |gap| = {st.median(gaps):.1f} picks; 90th pct = {sorted(gaps)[int(.9*len(gaps))]:.1f}")
print("  -> the composite is largely a smoothed ADP. 'Value vs ADP' is close to self-referential.")

print()
print("=" * 78)
print("G. Does the round board's recommended pick appear in its own candidate list?")
print("=" * 78)
byr = {}
for v in ver:
    byr.setdefault(v["round"], []).append(v["name"])
A = opt["branches"][0]
pickfor = {p["round"]: p["player"] for p in A["picks"]}
pickfor[1] = A["first"]
miss = []
for rnd in sorted(byr):
    want = pickfor.get(rnd)
    if want and want not in byr[rnd]:
        miss.append((rnd, want, byr[rnd][:3]))
print(f"  rounds where the marked pick is NOT one of the displayed candidates: {len(miss)} of {len(byr)}")
for rnd, want, shown in miss:
    print(f"    R{rnd:2d}: runner says {want!r}; board shows {shown}")
print("  -> in those rounds the user sees candidate rows with no recommendation marked.")

print()
print("=" * 78)
print("H. Are the tables I gave in chat still what the model says?")
print("=" * 78)
CHAT_A = {2: "Chase Brown", 3: "Kenneth Walker III", 4: "Tee Higgins", 5: "Luther Burden III",
          6: "Jameson Williams", 7: "Justin Herbert", 8: "Tucker Kraft", 9: "Kyle Monangai",
          10: "Blake Corum", 11: "Jayden Reed", 12: "Jordan Mason"}
drift = [(r, CHAT_A[r], pickfor.get(r)) for r in sorted(CHAT_A) if pickfor.get(r) != CHAT_A[r]]
print(f"  rounds that changed since the tables were sent: {len(drift)}")
for r, was, now in drift:
    print(f"    R{r:2d}: reported {was:22s} -> now {now}")
print(f"  reported projection 1907 / 1902 -> now {A['proj']}")

print()
print("=" * 78)
print("I. Are 'round N' verdict players actually gettable at pick N?")
print("=" * 78)
bad = []
for v in ver:
    p = BY.get(v["name"])
    pk = {1:4,2:17,3:24,4:37,5:44,6:57,7:64,8:77,9:84,10:97,11:104,12:117}[v["round"]]
    mca = p.get("mcAvail")
    picks = [4,17,24,37,44,57,64,77,84,97,104,117]
    a = mca[picks.index(pk)] if mca and pk in picks else None
    if a is not None and a < 0.15:
        bad.append((v["round"], v["name"], a, v["verdict"]))
print(f"  candidates shown with under 15% chance of lasting to that pick: {len(bad)}")
for r, n, a, vd in sorted(bad):
    print(f"    R{r:2d} {n:22s} {a:5.0%}  ({vd})")

print()
print("=" * 78)
print("J. Front end: is the gap bar readable, or does it saturate?")
print("=" * 78)
gaps = [abs(v["gap"]) for v in ver if v.get("gap") is not None]
sat = [g for g in gaps if g >= 25]
print(f"  gap bar caps at 25 picks. {len(sat)} of {len(gaps)} rows ({len(sat)/len(gaps):.0%}) are at or past the cap,")
print(f"  so they all render identically. Largest is {max(gaps):.0f}.")
print(f"  median |gap| among shown candidates: {statistics.median(gaps):.1f} picks -> most bars are under a fifth full.")
