#!/usr/bin/env python3
"""Monte Carlo draft simulator: opponents draft from ADP with noise, you follow a strategy, rosters are scored.

Each simulation
  1. draws a draft position for every player: X_i ~ Normal(ADP_i, sd_i), ADP from ESPN (the league's room)
     with Fantasy Football Calculator's per-player stdev (floored), so early picks are tight and late picks loose;
  2. runs a 10-team, 14-round snake draft: the nine opponents take the available player with the smallest X_i
     subject to roster rules (no second QB before round 10, no second TE before round 11, at most six RB / WR,
     K and D/ST in rounds 13-14 and sometimes 11-12), you pick at your slot with the strategy's scoring
     (research/scenario.py rules without the availability term, since availability is now simulated);
  3. scores your roster: the optimal starting lineup (QB, 2 RB, 2 WR, TE, FLEX) on projected PPR points,
     plus its floor (Bayesian p10) and ceiling (p90).

Outputs (scenarios/):
  montecarlo_summary.md      strategy comparison, first-pick comparison, per-round pick frequencies, availability table
  montecarlo_avail.json      P(available at each of your picks) per player, consumed by build.py for the app

Run:  python3 montecarlo.py [--sims 1500] [--teams 10] [--slot 4] [--room espn|blend]
"""
import argparse
import json
import math
import random
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

import numpy as np

import scenario as sc

HERE = Path(__file__).resolve().parent
OUT = HERE / "scenarios"
ROUNDS = 14          # QB, 2 RB, 2 WR, TE, FLEX, D/ST, K + 5 bench (GDL Fantasy; the IR slot is not drafted)
SKILL_ROUNDS = 12    # 7 skill starters + 5 bench; D/ST and K fill rounds 13-14
OPP_RULES = {"QB": (1, 10), "TE": (1, 11)}   # position -> (max before round, round from which a second is allowed)
OPP_CAPS = {"RB": 6, "WR": 6, "QB": 2, "TE": 2}
BENCH = 5
KDST_PROB = {11: 0.10, 12: 0.25, 13: 0.85, 14: 0.95}   # chance an opponent spends the pick on K / D/ST (outside our pool)
PRESETS = [("hero-rb", "balanced"), ("robust-rb", "balanced"), ("balanced", "balanced"), ("zero-rb", "balanced"),
           ("wr-heavy", "balanced"), ("hero-rb", "upside"), ("hero-rb", "safe")]
KEY_PLAYERS = ["Jahmyr Gibbs", "Bijan Robinson", "Ja'Marr Chase", "Puka Nacua", "Jaxon Smith-Njigba", "Amon-Ra St. Brown", "Christian McCaffrey", "Jonathan Taylor",
               "De'Von Achane", "Chase Brown", "James Cook III", "Kenneth Walker III", "Omarion Hampton", "Derrick Henry", "Ashton Jeanty", "Saquon Barkley",
               "Brock Bowers", "Trey McBride", "Colston Loveland", "Tyler Warren", "Josh Allen", "Lamar Jackson", "Jayden Daniels", "Drake Maye", "Joe Burrow", "Jalen Hurts",
               "Malik Nabers", "A.J. Brown", "Drake London", "Nico Collins", "DeVonta Smith", "Zay Flowers", "Garrett Wilson", "Breece Hall", "Jeremiyah Love", "MarShawn Lloyd"]


def load_players(room, path=None):
    P = json.loads(Path(path or (HERE / "data" / "players.json")).read_text())
    out = []
    for p in P:
        adp = p.get("espnAdp") if room == "espn" and p.get("espnAdp") is not None else p.get("adp")
        if adp is None:
            continue
        sd = max(1.0, p.get("adpSd") or 0.15 * adp)
        out.append({"id": p["id"], "name": p["name"], "pos": p["pos"], "comp": p["comp"], "adp": adp, "sd": sd, "proj": p.get("proj") or 0.0,
                    "floor": p.get("floorPts") if p.get("floorPts") is not None else (p.get("proj") or 0.0) * 0.6,
                    "ceil": p.get("ceilPts") if p.get("ceilPts") is not None else (p.get("proj") or 0.0) * 1.3,
                    "boom": p["boom"], "bust": p["bust"], "risk": p["risk"], "sit": p.get("sit", 50), "sos": p.get("sos") or {}, "posRank": p["posRank"], "bye": p.get("bye")})
    return out


def my_score(p, rnd, profile, strategy, roster, sit_w=0.10, sos_w=0.04):
    k = sc.PROFILES[profile]
    s = -math.log(p["comp"])
    s += k["boom"] * (p["boom"] - 50) / 100
    s -= k["bust"] * (p["bust"] - 50) / 100
    s -= k["risk"] * (p["risk"] - 50) / 100
    s += sit_w * (p["sit"] - 50) / 100
    if p["sos"].get("playoffsZ") is not None:
        s += sos_w * p["sos"]["playoffsZ"]
    s += sc.strategy_adj(strategy, rnd, p["pos"])
    s += sc.need_adj(roster, rnd, p["pos"], 10)
    return s


def lineup_value(roster, key):
    by = defaultdict(list)
    for p in roster:
        by[p["pos"]].append(p[key])
    for pos in by:
        by[pos].sort(reverse=True)
    take = lambda pos, n: sum(by[pos][:n])
    val = take("QB", 1) + take("RB", 2) + take("WR", 2) + take("TE", 1)
    flex_c = [(by["RB"][2] if len(by["RB"]) > 2 else 0, "RB"), (by["WR"][2] if len(by["WR"]) > 2 else 0, "WR"), (by["TE"][1] if len(by["TE"]) > 1 else 0, "TE")]
    flex, fpos = max(flex_c)
    used = {"QB": 1, "RB": 2, "WR": 2, "TE": 1}; used[fpos] += 1
    leftovers = sorted((v for pos in ("QB", "RB", "WR", "TE") for v in by[pos][used[pos]:]), reverse=True)
    bench = sum(leftovers[:BENCH])
    return val + flex + 0.25 * bench   # the five bench slots count a quarter: injuries and byes make depth matter in head-to-head


def simulate(players, teams, slot, strategy, profile, sims, seed=7, forced_first=None):
    rng = np.random.default_rng(seed)
    n = len(players)
    adp = np.array([p["adp"] for p in players]); sd = np.array([p["sd"] for p in players])
    idx_by_id = {p["id"]: i for i, p in enumerate(players)}
    my_picks = sc.my_picks(teams, slot, ROUNDS)
    avail_count = np.zeros((SKILL_ROUNDS, n))
    pick_counter = [Counter() for _ in range(SKILL_ROUNDS)]
    values = []
    for _ in range(sims):
        X = rng.normal(adp, sd)
        order = np.argsort(X)
        taken = np.zeros(n, dtype=bool)
        rosters = [[] for _ in range(teams)]
        my_roster = []
        ptr = 0
        for pick in range(1, teams * ROUNDS + 1):
            rnd = (pick - 1) // teams + 1
            pos_in_round = (pick - 1) % teams + 1
            team_ix = pos_in_round - 1 if rnd % 2 else teams - pos_in_round
            if pick in my_picks:
                r_ix = my_picks.index(pick)
                if r_ix >= SKILL_ROUNDS:
                    continue  # K / D/ST
                avail_count[r_ix] += ~taken
                cands = [players[i] for i in range(n) if not taken[i]]
                if forced_first and r_ix == 0:
                    f = [p for p in cands if p["name"] == forced_first]
                    choice = f[0] if f else max(cands, key=lambda p: my_score(p, rnd, profile, strategy, my_roster))
                else:
                    choice = max(cands, key=lambda p: my_score(p, rnd, profile, strategy, my_roster))
                taken[idx_by_id[choice["id"]]] = True
                my_roster.append(choice)
                pick_counter[r_ix][choice["name"]] += 1
                continue
            if rnd in KDST_PROB and rng.random() < KDST_PROB[rnd]:
                continue
            ros = rosters[team_ix]
            cnt = Counter(p["pos"] for p in ros)
            chosen = None
            for i in order:
                if taken[i]:
                    continue
                pos = players[i]["pos"]
                if pos in OPP_RULES and cnt[pos] >= OPP_RULES[pos][0] and rnd < OPP_RULES[pos][1]:
                    continue
                if cnt[pos] >= OPP_CAPS[pos]:
                    continue
                chosen = i
                break
            if chosen is None:
                continue
            taken[chosen] = True
            ros.append(players[chosen])
        values.append((lineup_value(my_roster, "proj"), lineup_value(my_roster, "floor"), lineup_value(my_roster, "ceil"),
                       Counter(p["pos"] for p in my_roster)))
    avail = avail_count / sims
    return {"values": values, "avail": avail, "picks": pick_counter, "my_picks": my_picks[:SKILL_ROUNDS]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sims", type=int, default=1500)
    ap.add_argument("--teams", type=int, default=10)
    ap.add_argument("--slot", type=int, default=4)
    ap.add_argument("--room", choices=("espn", "blend"), default="espn")
    ap.add_argument("--players", default=None, help="players json to simulate (default data/players.json)")
    ap.add_argument("--tag", default="", help="suffix for output files, e.g. _half")
    a = ap.parse_args()
    players = load_players(a.room, a.players)
    OUT.mkdir(exist_ok=True)
    L = [f"# Monte Carlo draft simulation ({a.sims} drafts per strategy)\n",
         f"Generated {datetime.now():%Y-%m-%d %H:%M}. {a.teams} teams, slot {a.slot}, snake, 14 rounds (QB, 2 RB, 2 WR, TE, FLEX, D/ST, K, 5 bench); opponents draft from {a.room.upper()} ADP with each player's measured spread and simple roster rules; your picks follow the strategy preset. Roster score = optimal lineup (QB, 2 RB, 2 WR, TE, FLEX) on projected points plus a quarter of the best five bench players (bench depth matters in head-to-head); floor and ceiling use the Bayesian p10 / p90. All 12 skill rounds are simulated and reported.\n"]

    # --- strategy comparison ---------------------------------------------------------------------
    L.append("## 1. Strategy comparison\n")
    L.append("| strategy | profile | lineup proj (mean) | p10 of runs | p90 of runs | floor lineup | ceiling lineup | avg RB / WR / QB / TE drafted |")
    L.append("|---|---|---|---|---|---|---|---|")
    results = {}
    strat_rows = []
    for strategy, profile in PRESETS:
        r = simulate(players, a.teams, a.slot, strategy, profile, a.sims)
        results[(strategy, profile)] = r
        v = np.array([x[0] for x in r["values"]]); fl = np.array([x[1] for x in r["values"]]); ce = np.array([x[2] for x in r["values"]])
        mix = Counter()
        for x in r["values"]:
            mix.update(x[3])
        k = len(r["values"])
        L.append(f"| {strategy} | {profile} | {v.mean():.0f} | {np.quantile(v, 0.1):.0f} | {np.quantile(v, 0.9):.0f} | {fl.mean():.0f} | {ce.mean():.0f} | {mix['RB']/k:.1f} / {mix['WR']/k:.1f} / {mix['QB']/k:.1f} / {mix['TE']/k:.1f} |")
        strat_rows.append({"strategy": strategy, "profile": profile, "mean": round(float(v.mean())), "p10": round(float(np.quantile(v, 0.1))), "p90": round(float(np.quantile(v, 0.9))), "floor": round(float(fl.mean())), "ceil": round(float(ce.mean())), "mix": {pos: round(mix[pos] / k, 1) for pos in ("RB", "WR", "QB", "TE")}})
    best = max(results, key=lambda key: np.mean([x[0] for x in results[key]["values"]]))
    L.append(f"\nBest mean lineup: **{best[0]} / {best[1]}**. Differences under ~10 points are noise at this sample size.\n")

    # --- first pick comparison (hero-rb / balanced) ----------------------------------------------------
    L.append("## 2. Who to take at your first pick (when available)\n")
    L.append("Forcing each candidate at pick 4 whenever he is on the board, then drafting normally (hero-rb / balanced). Rows are only comparable on the runs where the candidate was available.\n")
    L.append("| forced pick | available in % of runs | lineup proj (mean) | floor lineup | ceiling lineup |")
    L.append("|---|---|---|---|---|")
    base = results[("hero-rb", "balanced")]
    name_ix = {p["name"]: i for i, p in enumerate(players)}
    first_rows = []
    for cand in ["Jahmyr Gibbs", "Bijan Robinson", "Ja'Marr Chase", "Puka Nacua", "Jaxon Smith-Njigba", "Amon-Ra St. Brown", "Jonathan Taylor", "Christian McCaffrey"]:
        if cand not in name_ix:
            continue
        r = simulate(players, a.teams, a.slot, "hero-rb", "balanced", max(400, a.sims // 3), seed=11, forced_first=cand)
        av = base["avail"][0, name_ix[cand]]
        v = np.array([x[0] for x in r["values"]]); fl = np.array([x[1] for x in r["values"]]); ce = np.array([x[2] for x in r["values"]])
        L.append(f"| {cand} | {av * 100:.0f}% | {v.mean():.0f} | {fl.mean():.0f} | {ce.mean():.0f} |")
        first_rows.append({"player": cand, "id": players[name_ix[cand]]["id"], "avail": round(float(av), 3), "mean": round(float(v.mean())), "floor": round(float(fl.mean())), "ceil": round(float(ce.mean()))})
    L.append("")

    # --- per-round pick frequencies (hero-rb / balanced and robust-rb) ----------------------------------
    round_freq = {}
    for key in (("hero-rb", "balanced"), ("robust-rb", "balanced"), ("balanced", "balanced")):
        r = results[key]
        round_freq[f"{key[0]}/{key[1]}"] = [[[n, round(c / a.sims, 3)] for n, c in r["picks"][i].most_common(4)] for i in range(len(r["my_picks"]))]
        L.append(f"## 3. Most frequent picks by round: {key[0]} / {key[1]}\n")
        L.append("| Rd | Pick | #1 | #2 | #3 | #4 |")
        L.append("|---|---|---|---|---|---|")
        for i, pk in enumerate(r["my_picks"]):
            top = r["picks"][i].most_common(4)
            cells = [f"{n} ({c / a.sims * 100:.0f}%)" for n, c in top] + [""] * (4 - len(top))
            L.append(f"| {i + 1} | {pk} | " + " | ".join(cells) + " |")
        L.append("")

    # --- availability of key players at your picks ------------------------------------------------------
    L.append("## 4. Chance key players are still there at your picks (simulated, ESPN room)\n")
    picks = base["my_picks"]
    L.append("| player | pos | ADP used | " + " | ".join(f"#{p}" for p in picks) + " |")
    L.append("|---|---|---|" + "---|" * len(picks))
    for nm in KEY_PLAYERS:
        if nm not in name_ix:
            continue
        i = name_ix[nm]
        row = [f"{base['avail'][r, i] * 100:.0f}%" for r in range(len(picks))]
        L.append(f"| {nm} | {players[i]['pos']} | {players[i]['adp']:.1f} | " + " | ".join(row) + " |")
    L.append("")

    # --- availability json for the app ----------------------------------------------------------------
    avail_json = {"teams": a.teams, "slot": a.slot, "room": a.room, "sims": a.sims, "picks": base["my_picks"], "generated": datetime.now().isoformat(timespec="minutes"),
                  "strategies": strat_rows, "best": f"{best[0]}/{best[1]}", "first": first_rows, "rounds": round_freq,
                  "players": {p["id"]: [round(float(base["avail"][r, i]), 3) for r in range(len(base["my_picks"]))] for i, p in enumerate(players)}}
    (OUT / f"montecarlo_avail{a.tag}.json").write_text(json.dumps(avail_json))
    (OUT / f"montecarlo_summary{a.tag}.md").write_text("\n".join(L))
    print("\n".join(L))


if __name__ == "__main__":
    main()
