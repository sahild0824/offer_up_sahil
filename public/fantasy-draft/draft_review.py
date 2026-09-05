"""Review the real GDL Fantasy draft (Sept 5) against the model, pick by pick.

Board transcribed from the ESPN roster view. Overall pick = (round-1)*10 + slot-in-round.
Team 10's exact order is cut off in the screenshot; its players are placed at its picks in
ADP order, which only affects who is 'gone' at the margins.
"""
import json, sys
import scenario as sc

USER = "Kai and his Guy"
picks = {}  # overall pick -> (team, player)
def add(team, entries):
    for rp, name in entries:
        r, p = rp.split("."); picks[(int(r) - 1) * 10 + int(p)] = (team, name)

add("Audubon", [("7.1","Dak Prescott"),("1.1","Bijan Robinson"),("4.10","Breece Hall"),("3.1","A.J. Brown"),("6.10","Luther Burden III"),("2.10","Trey McBride"),("5.1","Quinshon Judkins"),("8.10","Josh Jacobs"),("9.1","Parker Washington"),("10.10","Brian Thomas Jr."),("11.1","Brock Purdy"),("12.10","Jayden Reed")])
add("NW Birdies", [("8.9","Justin Herbert"),("5.2","D'Andre Swift"),("6.9","TreVeyon Henderson"),("1.2","Puka Nacua"),("2.9","Drake London"),("3.2","Brock Bowers"),("4.9","Zay Flowers"),("7.2","Jameson Williams"),("9.2","Jaylen Warren"),("10.9","Trevor Lawrence"),("11.2","Kyle Monangai"),("12.9","Matthew Stafford")])
add("Rowan's", [("8.8","Jaxson Dart"),("1.3","Jahmyr Gibbs"),("2.8","Jeremiyah Love"),("3.3","Chris Olave"),("4.8","Tee Higgins"),("5.3","Colston Loveland"),("6.8","Jadarian Price"),("7.3","Mike Evans"),("9.3","Michael Wilson"),("10.8","Travis Hunter"),("11.3","Rachaad White"),("12.8","Quentin Johnston")])
add(USER, [("9.4","Caleb Williams"),("2.7","Derrick Henry"),("3.4","Kenneth Walker III"),("1.4","Ja'Marr Chase"),("4.7","Ladd McConkey"),("7.4","Kyle Pitts Sr."),("5.4","Davante Adams"),("6.7","Rome Odunze"),("8.7","Michael Pittman Jr."),("10.7","J.K. Dobbins"),("11.4","Jake Ferguson"),("12.7","Isaiah Likely")])
add("Soaring Wings", [("5.5","Lamar Jackson"),("2.6","Ashton Jeanty"),("4.6","Travis Etienne Jr."),("1.5","Jaxon Smith-Njigba"),("3.5","Nico Collins"),("7.5","Harold Fannin Jr."),("6.6","DJ Moore"),("8.6","Kenneth Gainwell"),("10.6","Jakobi Meyers"),("11.5","Matthew Golden"),("12.6","Khalil Shakir"),("13.5","Mark Andrews")])
add("Tejis", [("6.5","Jalen Hurts"),("1.6","Jonathan Taylor"),("2.5","Saquon Barkley"),("3.6","Rashee Rice"),("4.5","Tetairoa McMillan"),("7.6","George Kittle"),("5.6","Cam Skattebo"),("8.5","Courtland Sutton"),("9.6","Wan'Dale Robinson"),("10.5","Aaron Jones Sr."),("11.6","Jordan Addison"),("13.6","Jacory Croskey-Merritt")])
add("Oh Saquon", [("6.4","Joe Burrow"),("1.7","James Cook III"),("2.4","Omarion Hampton"),("3.7","George Pickens"),("4.4","Emeka Egbuka"),("7.7","Sam LaPorta"),("5.7","Jaylen Waddle"),("8.4","DK Metcalf"),("9.7","Rico Dowdle"),("10.4","Stefon Diggs"),("11.7","Chris Godwin Jr."),("12.4","Makai Lemon")])
add("Teemo", [("3.8","Josh Allen"),("1.8","Christian McCaffrey"),("2.3","Chase Brown"),("4.3","Malik Nabers"),("6.3","Terry McLaurin"),("9.8","Tucker Kraft"),("5.8","Bucky Irving"),("7.8","Marvin Harrison Jr."),("8.3","David Montgomery"),("10.3","MarShawn Lloyd"),("11.8","Dallas Goedert"),("12.3","Blake Corum")])
add("Hakuna", [("6.2","Drake Maye"),("4.2","Javonte Williams"),("7.9","Tony Pollard"),("1.9","Justin Jefferson"),("2.2","CeeDee Lamb"),("5.9","Tyler Warren"),("3.9","Garrett Wilson"),("8.2","Christian Watson"),("9.9","Chuba Hubbard"),("10.2","Jonathon Brooks"),("11.9","Patrick Mahomes II"),("12.2","RJ Harvey")])
# team 10: picks 10,11,30,31,50,51,70,71,90,91,110,111 -- order inferred from ADP
add("Hurts", [("1.10","De'Von Achane"),("2.1","Amon-Ra St. Brown"),("3.10","Kyren Williams"),("4.1","DeVonta Smith"),("5.10","Jayden Daniels"),("6.1","Bhayshul Tuten"),("7.10","Travis Kelce"),("8.1","Carnell Tate"),("9.10","Rhamondre Stevenson"),("10.1","Bo Nix"),("11.10","Alec Pierce"),("12.1","Josh Downs")])

players = json.loads(sc.DATA.read_text())
byn = {sc.norm_name(p["name"]): p for p in players}
def find(n):
    p = byn.get(sc.norm_name(n))
    if p: return p
    c = [q for q in players if sc.norm_name(n) in sc.norm_name(q["name"]) or sc.norm_name(q["name"]) in sc.norm_name(n)]
    return c[0] if len(c) == 1 else None

my_picks = sc.my_picks(10, 4, 12)
roster, taken = [], set()
total_gap = 0.0
print(f"{'pick':>4s} {'you took':24s} {'proj':>4s} {'bust':>4s}   {'model’s best there':24s} {'proj':>4s} {'bust':>4s}  {'Δproj':>5s}")
for overall in sorted(picks):
    team, name = picks[overall]
    p = find(name)
    if team != USER:
        if p: taken.add(p["id"])
        continue
    rnd = my_picks.index(overall) + 1
    cands = []
    for q in players:
        if q["id"] in taken or q["id"] in {r["id"] for r in roster}: continue
        s, _ = sc.pick_score(q, rnd, overall, "safe", "balanced", roster, 10, 0.10, 0.04)
        cands.append((s, q))
    cands.sort(key=lambda t: -t[0])
    best = cands[0][1]
    top3 = ", ".join(q["name"] for _, q in cands[:3])
    if p is None:
        print(f"{overall:4d} {name:24s} {'?':>4s}      (not in the model pool)"); continue
    d = (best["proj"] or 0) - (p["proj"] or 0)
    mark = "" if best["id"] == p["id"] else ("  ←" if d >= 15 else "")
    print(f"{overall:4d} {p['name']:24s} {p['proj']:4d} {p['bust']:4d}   {best['name']:24s} {best['proj']:4d} {best['bust']:4d}  {d:+5d}{mark}")
    print(f"     top 3 available: {top3}")
    roster.append(p); taken.add(p["id"])

print()
def summary(label, ros):
    v = sc.lineup_value(ros, "proj"); f = sc.lineup_value(ros, "floorPts"); c = sc.lineup_value(ros, "ceilPts")
    from collections import Counter
    mix = " ".join(f"{k}{n}" for k, n in sorted(Counter(p["pos"] for p in ros).items()))
    print(f"{label:58s} lineup {v[0]:5.0f}  floor {f[0]:4.0f}  ceiling {c[0]:5.0f}   {mix}")
    return v[0]

def replay(keep_rounds):
    """Keep your real picks for the first `keep_rounds` rounds, then let the model choose at each of
    your later picks from whatever was actually still on the board in this room. Your own later
    picks are treated as taken by someone else at their ADP."""
    ros, tk = [], set()
    # players you really took but the replay does not keep would not have lasted: someone else
    # takes them at their ADP, so the counterfactual cannot quietly get Henry in round 6
    mine_unkept = [find(n) for o, (t, n) in picks.items() if t == USER and my_picks.index(o) + 1 > keep_rounds]
    ghosts = {round(p["adp"]): p for p in mine_unkept if p and p.get("adp")}
    for overall in sorted(set(picks) | set(ghosts)):
        for g_pick, g in ghosts.items():
            if g_pick <= overall and g["id"] not in tk and g["id"] not in {r["id"] for r in ros}:
                tk.add(g["id"])
        if overall not in picks:
            continue
        team, name = picks[overall]; p = find(name)
        if team != USER:
            if p: tk.add(p["id"])
            continue
        rnd = my_picks.index(overall) + 1
        if rnd <= keep_rounds:
            if p: ros.append(p); tk.add(p["id"])
            continue
        cands = []
        for q in players:
            if q["id"] in tk or q["id"] in {r["id"] for r in ros}: continue
            sc_, _ = sc.pick_score(q, rnd, overall, "safe", "balanced", ros, 10, 0.10, 0.04)
            cands.append((sc_, q))
        best = max(cands, key=lambda t: t[0])[1]
        ros.append(best); tk.add(best["id"])
    return ros

print()
actual = summary("Your actual roster", roster)
for k, lab in ((4, "Your first 4 picks kept, model from round 5 on"), (3, "Your first 3 picks kept, model from round 4 on"), (1, "Chase at 4 kept, model from round 2 on")):
    r = replay(k)
    summary(lab, r)
    print("      " + ", ".join(f"R{i+1} {p['name']}" for i, p in enumerate(r) if i >= k))
