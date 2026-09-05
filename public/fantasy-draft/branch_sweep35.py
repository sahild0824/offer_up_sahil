"""For each draft-day branch, run every strategy / profile and rank the resulting roster.

Answers "what is the optimal team" per branch instead of assuming a build.
"""
import itertools, json, subprocess, re, sys
from pathlib import Path

BRANCHES = {
    "A": dict(mine="Puka Nacua", taken="", label="Nacua is cleared and there at 4"),
    "B": dict(mine="Ja'Marr Chase", taken="", label="Chase falls to 4"),
    "C": dict(mine="Bijan Robinson", taken="", label="Bijan or Gibbs falls to 4"),
    "D": dict(mine="", taken="Puka Nacua,Ja'Marr Chase,Jahmyr Gibbs,Bijan Robinson", label="Nacua out or gone, Chase gone"),
}
AVOID = "Christian McCaffrey,Ashton Jeanty,Jeremiyah Love,Kyren Williams,Travis Etienne Jr.,Cam Skattebo,Carnell Tate,Davante Adams"
STRATS = ["balanced", "hero-rb", "zero-rb", "robust-rb", "wr-heavy"]
PROFILES = ["safe", "balanced", "upside"]

rows = []
for key, b in BRANCHES.items():
    for st, pr in itertools.product(STRATS, PROFILES):
        name = f"_swp35_{key}_{st}_{pr}".replace("-", "")
        cmd = [sys.executable, "scenario.py", "--strategy", st, "--profile", pr, "--avoid", AVOID,
               "--min-avail", "0.35", "--name", name]
        if b["mine"]:
            cmd += ["--mine", b["mine"]]
        if b["taken"]:
            cmd += ["--taken", b["taken"]]
        subprocess.run(cmd, capture_output=True, check=True)
        md = Path(f"scenarios/{name}.md").read_text()
        proj = float(re.search(r"Projected: \*\*(\d+)\*\*", md).group(1))
        floor = float(re.search(r"Floor \(p10\): \*\*(\d+)\*\*", md).group(1))
        ceil = float(re.search(r"Ceiling \(p90\): \*\*(\d+)\*\*", md).group(1))
        roster = re.findall(r"^\d+\. (.+?) — (\w+)\d+", md, re.M)
        rows.append(dict(branch=key, strategy=st, profile=pr, proj=proj, floor=floor, ceil=ceil,
                         roster=[n for n, _ in roster], mix=[p for _, p in roster], file=name))

json.dump(rows, open("scenarios/branch_sweep35.json", "w"), indent=1)
for key, b in BRANCHES.items():
    sub = sorted([r for r in rows if r["branch"] == key], key=lambda r: -r["proj"])
    print(f"\n=== {key}: {b['label']} ===")
    for r in sub[:4]:
        print(f"  {r['strategy']:10s} {r['profile']:8s} proj {r['proj']:.0f}  floor {r['floor']:.0f}  ceil {r['ceil']:.0f}")
    best = sub[0]
    print(f"  best -> {best['strategy']}/{best['profile']}: {', '.join(best['roster'][:6])} ...")
