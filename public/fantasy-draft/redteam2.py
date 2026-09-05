import json, statistics as st
from pathlib import Path
H = Path(__file__).parent
R = json.loads((H / "data" / "rankings.json").read_text())
M = json.loads((H / "data" / "market_features.json").read_text())["players"]
norm = lambda s: "".join(c for c in s.lower() if c.isalnum() or c == " ").strip()
NAME = {f"{norm(r['name'])}|{r['pos']}": r["name"] for r in R}
espn = {}
for k, m in M.items():
    n = NAME.get(k)
    a = (m.get("espn") or {}).get("adp")
    if n and a: espn[n] = a
ffc = {r["name"]: (r.get("adp") or {}).get("nfc_ppr") for r in R if (r.get("adp") or {}).get("nfc_ppr")}
shared = [n for n in ffc if n in espn and espn[n] <= 140]
print("K. Is the 12-team raw pick scale actually inflated vs ESPN? (tests finding D)")
print(f"   shared players inside ESPN's drafted range: {len(shared)}")
print(f"   mean raw ADP  ESPN {st.mean([espn[n] for n in shared]):6.1f}   FFC 12-team {st.mean([ffc[n] for n in shared]):6.1f}")
print(f"   ratio FFC/ESPN = {st.mean([ffc[n]/espn[n] for n in shared]):.3f}")
print("   -> if this is ~1.0 the raw scales already agree and D is cosmetic; if ~1.2 the blend")
print("      is averaging two different pick scales and D is a real defect.")

print()
print("L. Do the simulated opponents respond to positional runs?")
src = (H / "montecarlo.py").read_text()
print("   opponent rule set in montecarlo.py:")
for line in src.split("\n"):
    if line.startswith(("OPP_RULES", "OPP_CAPS", "KDST_PROB")):
        print("    ", line.split("#")[0].strip())
print("   Opponents draw X ~ Normal(ADP, sd) once per draft and take the smallest available,")
print("   subject to caps. Nothing in that loop reacts to what has just been taken, so a run on")
print("   a position cannot start. Real rooms run; availability variance is therefore understated.")

print()
print("M. How stale is the evidence the board is built on?")
print("   Feeds dated Aug 24-29 still carrying weight in a Sept 5 board:")
for k in ("draftsharks_half_consensus", "underdog", "ffpc", "sleeper_aug29", "yahoo_aug25",
          "udk_avg_pick", "nfc_ppr_aug28", "rotowire_underdog"):
    print(f"     {k}")
print("   build.py down-weights these to 0.1x when 3+ Sept 4 feeds exist, which is the right")
print("   instinct, but they still shape the calibration offsets, which are NOT recency-weighted.")
