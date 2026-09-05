#!/usr/bin/env python3
"""Backtest the draft model's signals against 2016-2025 outcomes.

Inputs (data/raw/nflverse and data/raw/bt; --fetch downloads what is missing):
  stats_player_week_{2015..2025}.csv   nflverse weekly stats (actual PPR points, usage)
  roster_{2016..2025}.csv              nflverse rosters (team, birth date, experience, draft slot)
  fp_adp_{2016..2025}.csv              FantasyPros overall PPR ADP, preseason (srsavas42 mirror)
  db_fpecr.parquet                     FantasyPros ECR history 2020-2026 with sd / best / worst (DynastyProcess)
  vegas_*.csv                          Vegas season win totals 2003-2025 (srsavas42 mirror)

For every drafted player-season (ADP inside the top 180) we know, before the season:
  ADP, positional ADP rank, ECR (2020+), expert spread / best / worst (2020+), age, years of experience,
  rookie and draft slot, team change, prior-season PPG / games / boom-week rate / bust-week rate / weekly CV,
  Vegas win total, and the share of the team's prior-season targets or carries that had left.
And after the season: positional finish by total PPR points, games played, PPG.

Outcomes
  hit    finished inside the positional starter line (QB 12, RB 24, WR 24, TE 12 in a 10-team league with flex)
  boom   finished as an elite scorer (top 5 RB / WR, top 3 QB / TE) OR beat his ADP positional rank by 6 spots
         (3 for QB / TE) while finishing inside the starter line
  bust   finished outside the starter line AND at least 6 spots (3 QB / TE) worse than his ADP positional rank,
         or played 10 games or fewer   (both an absolute miss and a relative miss, so a first-round pick who
         slips two spots is not a bust)

Outputs research/BACKTEST.md (tables) and data/backtest_priors.json (measured rates the model can use).
Run:  python3 backtest.py [--fetch]
"""
import csv
import json
import math
import re
import statistics
import sys
import unicodedata
import urllib.request
from collections import defaultdict
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
NFL = HERE / "data" / "raw" / "nflverse"
BT = HERE / "data" / "raw" / "bt"
YEARS = list(range(2016, 2026))
POS = ("QB", "RB", "WR", "TE")
STARTER = {"QB": 12, "RB": 24, "WR": 24, "TE": 12}
BOOM_GAP = {"QB": 3, "RB": 6, "WR": 6, "TE": 3}
BOOM_SLOT = {"QB": 3, "RB": 6, "WR": 6, "TE": 3}
BUST_SLOT = {"QB": 18, "RB": 40, "WR": 56, "TE": 18}
TEAM_FIX = {"LA": "LAR", "JAC": "JAX", "WSH": "WAS", "OAK": "LV", "SD": "LAC", "STL": "LAR"}
FULL = {"Arizona Cardinals": "ARI", "Atlanta Falcons": "ATL", "Baltimore Ravens": "BAL", "Buffalo Bills": "BUF", "Carolina Panthers": "CAR", "Chicago Bears": "CHI",
        "Cincinnati Bengals": "CIN", "Cleveland Browns": "CLE", "Dallas Cowboys": "DAL", "Denver Broncos": "DEN", "Detroit Lions": "DET", "Green Bay Packers": "GB",
        "Houston Texans": "HOU", "Indianapolis Colts": "IND", "Jacksonville Jaguars": "JAX", "Kansas City Chiefs": "KC", "Las Vegas Raiders": "LV", "Los Angeles Chargers": "LAC",
        "Los Angeles Rams": "LAR", "Miami Dolphins": "MIA", "Minnesota Vikings": "MIN", "New England Patriots": "NE", "New Orleans Saints": "NO", "New York Giants": "NYG",
        "New York Jets": "NYJ", "Philadelphia Eagles": "PHI", "Pittsburgh Steelers": "PIT", "San Francisco 49ers": "SF", "Seattle Seahawks": "SEA", "Tampa Bay Buccaneers": "TB",
        "Tennessee Titans": "TEN", "Washington Commanders": "WAS", "Washington Football Team": "WAS", "Washington Redskins": "WAS"}
URLS = {
    **{f"stats_player_week_{y}.csv": f"https://github.com/nflverse/nflverse-data/releases/download/stats_player/stats_player_week_{y}.csv" for y in range(2015, 2026)},
    **{f"roster_{y}.csv": f"https://github.com/nflverse/nflverse-data/releases/download/rosters/roster_{y}.csv" for y in range(2016, 2026)},
}
BT_URLS = {
    **{f"fp_adp_{y}.csv": f"https://raw.githubusercontent.com/srsavas42/fantasy-football-research/main/ADP/FantasyPros_{y}_Overall_ADP_Rankings.csv" for y in YEARS},
    "db_fpecr.parquet": "https://raw.githubusercontent.com/dynastyprocess/data/master/files/db_fpecr.parquet",
    "vegas_2003_2022_win_totals.csv": "https://raw.githubusercontent.com/srsavas42/fantasy-football-research/main/Vegas%20Win%20Totals/2003_2022_win_totals.csv",
    **{f"vegas_{y}_nfl_regular_season_win_total_odds.csv": f"https://raw.githubusercontent.com/srsavas42/fantasy-football-research/main/Vegas%20Win%20Totals/{y}_nfl_regular_season_win_total_odds.csv" for y in (2023, 2024, 2025)},
}


def norm_name(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode()
    s = s.lower().replace("'", "").replace(".", "").replace("-", " ")
    s = re.sub(r"\b(jr|sr|ii|iii|iv|v)\b", "", s)
    return re.sub(r"\s+", " ", s).strip()


def team(t):
    return TEAM_FIX.get(t, t)


def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def fetch():
    NFL.mkdir(parents=True, exist_ok=True)
    BT.mkdir(parents=True, exist_ok=True)
    for name, url in URLS.items():
        if not (NFL / name).exists():
            print("downloading", name)
            urllib.request.urlretrieve(url, NFL / name)
    for name, url in BT_URLS.items():
        if not (BT / name).exists():
            print("downloading", name)
            urllib.request.urlretrieve(url, BT / name)


# ---------------------------------------------------------------------------------------------
# season stats
# ---------------------------------------------------------------------------------------------
def season_stats(year):
    """Per (player_id, pos): games, total, ppg, boom_rate, bust_rate, cv, targets, carries, target_share, team (last)."""
    rows = []
    with (NFL / f"stats_player_week_{year}.csv").open(newline="") as f:
        for r in csv.DictReader(f):
            if r["season_type"] == "REG" and r["position"] in POS:
                rows.append(r)
    by_week = defaultdict(lambda: defaultdict(list))
    for r in rows:
        by_week[int(r["week"])][r["position"]].append(num(r["fantasy_points_ppr"]))
    thr = {}
    for pos in POS:
        booms, busts = [], []
        for wk, d in by_week.items():
            pts = sorted(d[pos], reverse=True)
            if len(pts) >= BUST_SLOT[pos]:
                booms.append(pts[BOOM_SLOT[pos] - 1])
                busts.append(pts[BUST_SLOT[pos] - 1])
        thr[pos] = (statistics.mean(booms), statistics.mean(busts))
    team_wk = defaultdict(lambda: [0.0, 0.0])
    for r in rows:
        tw = team_wk[(team(r["team"]), int(r["week"]))]
        tw[0] += num(r["targets"])
        tw[1] += num(r["carries"])
    P = {}
    for r in rows:
        if num(r["targets"]) + num(r["carries"]) + num(r["attempts"]) == 0:
            continue
        k = (r["player_id"], r["position"])
        p = P.setdefault(k, {"name": r["player_display_name"], "pos": r["position"], "weeks": [], "targets": 0.0, "carries": 0.0, "tt": 0.0, "tc": 0.0, "team": team(r["team"])})
        p["weeks"].append(num(r["fantasy_points_ppr"]))
        p["targets"] += num(r["targets"]); p["carries"] += num(r["carries"])
        tw = team_wk[(team(r["team"]), int(r["week"]))]
        p["tt"] += tw[0]; p["tc"] += tw[1]
        p["team"] = team(r["team"])
    out = {}
    for k, p in P.items():
        w = p["weeks"]; g = len(w); m = statistics.mean(w); sd = statistics.pstdev(w) if g > 1 else 0.0
        b, u = thr[p["pos"]]
        out[k] = {"name": p["name"], "pos": p["pos"], "team": p["team"], "games": g, "total": sum(w), "ppg": m,
                  "boom_rate": sum(1 for x in w if x >= b) / g, "bust_rate": sum(1 for x in w if x <= u) / g, "cv": sd / m if m > 0 else None,
                  "targets": p["targets"], "carries": p["carries"], "target_share": p["targets"] / p["tt"] if p["tt"] else None, "carry_share": p["carries"] / p["tc"] if p["tc"] else None}
    # positional finish ranks by total
    for pos in POS:
        ranked = sorted([k for k in out if out[k]["pos"] == pos], key=lambda k: -out[k]["total"])
        for i, k in enumerate(ranked, 1):
            out[k]["fin"] = i
    return out


def roster(year):
    R = {}
    with (NFL / f"roster_{year}.csv").open(newline="") as f:
        for r in csv.DictReader(f):
            if r.get("position") in POS and r.get("gsis_id") and r["gsis_id"] not in R:
                R[r["gsis_id"]] = r
    return R


def parse_adp(year):
    """FantasyPros overall ADP -> list of (norm name, pos, adp, pos_rank, team or None)."""
    out = []
    with (BT / f"fp_adp_{year}.csv").open(newline="") as f:
        for r in csv.DictReader(f):
            raw = r.get("Player (Bye)") or r.get("Player") or ""
            m = re.match(r"^(.*?)(?:\s{2,}([A-Z]{2,3})\s*\((\d+)\))?\s*$", raw)
            name = (m.group(1) if m else raw).strip()
            tm = m.group(2) if m and m.group(2) else (r.get("Team") or None)
            pm = re.match(r"^([A-Z]+)(\d+)$", r.get("POS", ""))
            if not pm or pm.group(1) not in POS:
                continue
            try:
                adp = float(r.get("AVG") or r.get("Rank"))
            except (TypeError, ValueError):
                continue
            out.append((norm_name(name), pm.group(1), adp, int(pm.group(2)), team(tm) if tm else None))
    return out


def load_ecr():
    df = pd.read_parquet(BT / "db_fpecr.parquet", columns=["fp_page", "player", "pos", "team", "ecr", "sd", "best", "worst", "scrape_date"])
    df = df[df["fp_page"] == "/nfl/rankings/ppr-cheatsheets.php"].copy()
    df["scrape_date"] = pd.to_datetime(df["scrape_date"])
    out = {}
    for y in range(2020, 2026):
        d = df[(df["scrape_date"].dt.year == y) & (df["scrape_date"].dt.month == 9) & (df["scrape_date"].dt.day <= 8)]
        if d.empty:
            continue
        d = d[d["scrape_date"] == d["scrape_date"].max()]
        for _, r in d.iterrows():
            if r["pos"] in POS:
                out[(y, norm_name(r["player"]), r["pos"])] = {"ecr": float(r["ecr"]), "sd": float(r["sd"]) if pd.notna(r["sd"]) else None, "best": float(r["best"]), "worst": float(r["worst"])}
    return out


def load_vegas():
    V = {}
    with (BT / "vegas_2003_2022_win_totals.csv").open(newline="") as f:
        for r in csv.DictReader(f):
            V[(int(r["season"]), team(r["team"]))] = float(r["line"])
    for y in (2023, 2024, 2025):
        with (BT / f"vegas_{y}_nfl_regular_season_win_total_odds.csv").open(newline="") as f:
            for r in csv.DictReader(f):
                t = FULL.get(r["Team"])
                if t:
                    V[(y, t)] = float(r["Win Total"])
    return V


# ---------------------------------------------------------------------------------------------
# numpy stats helpers
# ---------------------------------------------------------------------------------------------
def rank(a):
    a = np.asarray(a, dtype=float)
    order = a.argsort()
    r = np.empty(len(a)); r[order] = np.arange(1, len(a) + 1)
    # average ties
    _, inv, counts = np.unique(a, return_inverse=True, return_counts=True)
    sums = np.zeros(len(counts)); np.add.at(sums, inv, r)
    return sums[inv] / counts[inv]


def spearman(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    m = ~(np.isnan(x) | np.isnan(y))
    if m.sum() < 5:
        return float("nan")
    rx, ry = rank(x[m]), rank(y[m])
    return float(np.corrcoef(rx, ry)[0, 1])


def auc(score, y):
    score, y = np.asarray(score, float), np.asarray(y, int)
    m = ~np.isnan(score)
    score, y = score[m], y[m]
    if y.sum() == 0 or y.sum() == len(y):
        return float("nan")
    r = rank(score)
    n1 = y.sum(); n0 = len(y) - n1
    return float((r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def logistic_fit(X, y, l2=1.0, iters=50):
    """IRLS logistic regression with L2 on standardized features. Returns (coef, intercept, mean, sd)."""
    X = np.asarray(X, float); y = np.asarray(y, float)
    mu = np.nanmean(X, axis=0); sd = np.nanstd(X, axis=0); sd[sd == 0] = 1
    Z = (X - mu) / sd
    Z = np.nan_to_num(Z)
    A = np.hstack([np.ones((len(Z), 1)), Z])
    w = np.zeros(A.shape[1])
    R = np.eye(A.shape[1]) * l2; R[0, 0] = 0
    for _ in range(iters):
        p = 1 / (1 + np.exp(-A @ w))
        W = p * (1 - p)
        H = A.T @ (A * W[:, None]) + R
        g = A.T @ (y - p) - R @ w
        step = np.linalg.solve(H, g)
        w = w + step
        if np.abs(step).max() < 1e-6:
            break
    return w[1:], w[0], mu, sd


def logistic_score(X, coef, b, mu, sd):
    Z = np.nan_to_num((np.asarray(X, float) - mu) / sd)
    return 1 / (1 + np.exp(-(Z @ coef + b)))


# ---------------------------------------------------------------------------------------------
def main():
    if "--fetch" in sys.argv or not all((NFL / n).exists() for n in URLS) or not all((BT / n).exists() for n in BT_URLS):
        fetch()
    ecr = load_ecr()
    vegas = load_vegas()
    stats = {y: season_stats(y) for y in range(2015, 2026)}
    rosters = {y: roster(y) for y in YEARS}
    today = date(2026, 9, 1)

    rows = []
    for y in YEARS:
        S, S0, R, R0 = stats[y], stats[y - 1], rosters[y], rosters.get(y - 1, {})
        by_name = {(norm_name(v["name"]), v["pos"]): k for k, v in S.items()}
        by_name0 = {(norm_name(v["name"]), v["pos"]): k for k, v in S0.items()}
        ros_by_name = {(norm_name(r["full_name"]), r["position"]): r for r in R.values()}
        # team vacated share for season y from y-1 stats and y roster
        team_tot = defaultdict(lambda: [0.0, 0.0]); team_vac = defaultdict(lambda: [0.0, 0.0])
        for (pid, pos), s in S0.items():
            team_tot[s["team"]][0] += s["targets"]; team_tot[s["team"]][1] += s["carries"]
            now = team(R[pid]["team"]) if pid in R else None
            if now != s["team"]:
                team_vac[s["team"]][0] += s["targets"]; team_vac[s["team"]][1] += s["carries"]
        loose = {}
        for (nm, ps), k in by_name.items():
            parts = nm.split()
            if parts:
                loose.setdefault((parts[-1], parts[0][:1], ps), []).append(k)
        unmatched = []
        for name, pos, adp, adp_pos, tm in parse_adp(y):
            if adp > 180:
                continue
            key = by_name.get((name, pos))
            if key is None:
                parts = name.split()
                cands = loose.get((parts[-1], parts[0][:1], pos), []) if parts else []
                if len(cands) == 1:
                    key = cands[0]
                elif adp <= 120:
                    unmatched.append(name)
            act = S.get(key) if key else None
            ros = ros_by_name.get((name, pos))
            pid = ros["gsis_id"] if ros else (key[0] if key else None)
            prior = S0.get((pid, pos)) if pid else None
            if prior is None:
                k0 = by_name0.get((name, pos))
                prior = S0.get(k0) if k0 else None
            tm_now = team(ros["team"]) if ros else (act["team"] if act else tm)
            tm_prev = prior["team"] if prior else None
            age = None
            if ros and ros.get("birth_date"):
                try:
                    by, bm, bd = (int(x) for x in ros["birth_date"].split("-"))
                    age = y - by - ((9, 1) < (bm, bd))
                except ValueError:
                    pass
            yexp = int(ros["years_exp"]) if ros and (ros.get("years_exp") or "").isdigit() else None
            dn = int(ros["draft_number"]) if ros and (ros.get("draft_number") or "").isdigit() else None
            e = ecr.get((y, name, pos))
            vac = team_vac.get(tm_now); tot = team_tot.get(tm_now)
            vac_share = None
            if vac and tot:
                vac_share = (vac[0] / tot[0]) if pos != "RB" and tot[0] else ((vac[1] / tot[1]) if tot[1] else None)
            fin = act["fin"] if act else 999
            games = act["games"] if act else 0
            rows.append({
                "season": y, "name": name, "pos": pos, "adp": adp, "adp_pos": adp_pos, "round": int((adp - 1) // 12) + 1, "team": tm_now,
                "ecr": e["ecr"] if e else None, "ecr_sd": e["sd"] if e else None, "ecr_best": e["best"] if e else None, "ecr_worst": e["worst"] if e else None,
                "age": age, "years_exp": yexp, "rookie": 1 if (yexp == 0) else 0, "draft_no": dn, "moved": 1 if (tm_prev and tm_now and tm_prev != tm_now and yexp != 0) else 0,
                "prior_ppg": prior["ppg"] if prior else None, "prior_games": prior["games"] if prior else None, "prior_boom": prior["boom_rate"] if prior else None,
                "prior_bust": prior["bust_rate"] if prior else None, "prior_cv": prior["cv"] if prior else None, "prior_fin": prior["fin"] if prior else None,
                "prior_tshare": prior["target_share"] if prior else None, "prior_carries": prior["carries"] if prior else None,
                "vegas": vegas.get((y, tm_now)), "vac_share": vac_share,
                "fin": fin, "games": games, "total": act["total"] if act else 0.0, "ppg": act["ppg"] if act else 0.0,
            })
        if unmatched:
            print(f"{y}: {len(unmatched)} top-120 ADP names without a stats match (counted as zero-game seasons): {unmatched[:8]}")
    df = pd.DataFrame(rows)
    df["hit"] = (df["fin"] <= df["pos"].map(STARTER)).astype(int)
    elite = df["pos"].map({"QB": 3, "RB": 5, "WR": 5, "TE": 3})
    df["boom"] = ((df["fin"] <= elite) | ((df["adp_pos"] - df["fin"] >= df["pos"].map(BOOM_GAP)) & (df["fin"] <= df["pos"].map(STARTER)))).astype(int)
    df["bust"] = (((df["fin"] > df["pos"].map(STARTER)) & (df["fin"] - df["adp_pos"] >= df["pos"].map(BOOM_GAP))) | (df["games"] <= 10)).astype(int)
    df["beat_adp"] = (df["fin"] <= df["adp_pos"]).astype(int)
    df["ecr_gap"] = df["ecr_worst"] - df["ecr_best"]
    df["value"] = df["adp"] - df["ecr"]
    df["prior_missed"] = 17 - df["prior_games"]
    df["ppg_delta"] = df["ppg"] - df["prior_ppg"]
    df.to_csv(BT / "player_seasons.csv", index=False)

    L = []
    pr = L.append
    pr("# Backtest of the draft model's signals, 2016-2025\n")
    pr(f"Generated {date.today().isoformat()}. {len(df)} player-seasons with a preseason FantasyPros ADP inside the top 180 "
       f"(QB {int((df.pos=='QB').sum())}, RB {int((df.pos=='RB').sum())}, WR {int((df.pos=='WR').sum())}, TE {int((df.pos=='TE').sum())}); "
       f"{int(df.ecr.notna().sum())} of them (2020-2025) also carry a preseason expert consensus with spread, best and worst. "
       "Outcomes are positional finishes by total PPR points from nflverse game logs. Definitions are in the script header.\n")

    # --- 1. ADP vs ECR predictiveness ---------------------------------------------------------------
    pr("## 1. How predictive are ADP and the expert consensus?\n")
    pr("Spearman rank correlation between the preseason number and the actual positional finish (higher is better), drafted players only.\n")
    pr("| position | ADP → finish (2016-25) | ADP → finish (2020-25) | ECR → finish (2020-25) | 50/50 blend (2020-25) | n (2020-25) |")
    pr("|---|---|---|---|---|---|")
    d20 = df[df.ecr.notna()].copy()
    d20["blend"] = 0.5 * d20["adp"] + 0.5 * d20["ecr"]
    for pos in POS:
        a = df[df.pos == pos]; b = d20[d20.pos == pos]
        pr(f"| {pos} | {spearman(a.adp, a.fin):.3f} | {spearman(b.adp, b.fin):.3f} | {spearman(b.ecr, b.fin):.3f} | {spearman(b.blend, b.fin):.3f} | {len(b)} |")
    pr(f"| all | {spearman(df.adp, df.fin):.3f} | {spearman(d20.adp, d20.fin):.3f} | {spearman(d20.ecr, d20.fin):.3f} | {spearman(d20.blend, d20.fin):.3f} | {len(d20)} |")
    pr("")
    pr("By season (all positions, ECR years):\n")
    pr("| season | ADP | ECR | blend | n |")
    pr("|---|---|---|---|---|")
    for y in sorted(d20.season.unique()):
        b = d20[d20.season == y]
        pr(f"| {y} | {spearman(b.adp, b.fin):.3f} | {spearman(b.ecr, b.fin):.3f} | {spearman(b.blend, b.fin):.3f} | {len(b)} |")
    pr("")
    # value picks: ADP later than ECR
    pr("Does the gap between ADP and ECR carry information? Players the market takes later than the experts rank them (value) vs earlier (reach), 2020-25:\n")
    pr("| group | n | hit rate | beat-ADP rate | bust rate |")
    pr("|---|---|---|---|---|")
    for lab, sel in (("value ≥ 10 picks", d20.value >= 10), ("within ±10", d20.value.abs() < 10), ("reach ≥ 10 picks", d20.value <= -10)):
        g = d20[sel]
        pr(f"| {lab} | {len(g)} | {g.hit.mean():.2f} | {g.beat_adp.mean():.2f} | {g.bust.mean():.2f} |")
    pr("")

    # --- 2. hit / boom / bust by round -----------------------------------------------------------------
    pr("## 2. Hit, boom and bust rates by ADP round and position (12-team rounds, 2016-25)\n")
    priors = {"round_pos": {}}
    pr("| round | pos | n | hit (starter line) | boom | bust | avg games |")
    pr("|---|---|---|---|---|---|---|")
    for rd in range(1, 16):
        for pos in POS:
            g = df[(df["round"] == rd) & (df.pos == pos)]
            if len(g) < 8:
                continue
            priors["round_pos"][f"{rd}|{pos}"] = {"n": int(len(g)), "hit": round(g.hit.mean(), 3), "boom": round(g.boom.mean(), 3), "bust": round(g.bust.mean(), 3)}
            pr(f"| {rd} | {pos} | {len(g)} | {g.hit.mean():.2f} | {g.boom.mean():.2f} | {g.bust.mean():.2f} | {g.games.mean():.1f} |")
    pr("")

    # --- 3. univariate signal tests --------------------------------------------------------------------
    pr("## 3. Does each signal move the boom or bust rate? (within position, ADP top 120)\n")
    pr("Each row compares a slice against the rest of its position after controlling for ADP band (rounds 1-3, 4-6, 7-10). Lift is the slice's rate minus the matched base rate, in percentage points.\n")
    top = df[df.adp <= 120].copy()
    top["band"] = pd.cut(top["round"], [0, 3, 6, 10], labels=["R1-3", "R4-6", "R7-10"])

    def lift(sel, label):
        out = []
        for pos in POS:
            g = top[top.pos == pos]
            s = g[sel(g)]
            if len(s) < 25:
                continue
            base_b = base_u = 0.0; wsum = 0
            for band, gb in g.groupby("band", observed=True):
                sb = gb[sel(gb)]
                if len(sb):
                    base_b += gb.boom.mean() * len(sb); base_u += gb.bust.mean() * len(sb); wsum += len(sb)
            if not wsum:
                continue
            out.append((pos, len(s), s.boom.mean() - base_b / wsum, s.bust.mean() - base_u / wsum, s.boom.mean(), s.bust.mean()))
        return label, out

    tests = [
        lift(lambda g: g.age >= 29, "age ≥ 29"),
        lift(lambda g: (g.age == 27) | (g.age == 28), "age 27-28"),
        lift(lambda g: g.age <= 24, "age ≤ 24"),
        lift(lambda g: g.years_exp == 1, "year 2 (second season)"),
        lift(lambda g: g.years_exp == 2, "year 3"),
        lift(lambda g: g.rookie == 1, "rookie"),
        lift(lambda g: (g.rookie == 1) & (g.draft_no <= 32), "rookie, first-round pick"),
        lift(lambda g: g.moved == 1, "changed teams"),
        lift(lambda g: g.prior_boom >= 0.35, "prior-year boom-week rate ≥ 35%"),
        lift(lambda g: g.prior_boom <= 0.10, "prior-year boom-week rate ≤ 10%"),
        lift(lambda g: g.prior_bust >= 0.30, "prior-year bust-week rate ≥ 30%"),
        lift(lambda g: g.prior_missed >= 4, "missed ≥ 4 games prior year"),
        lift(lambda g: g.prior_games == 17, "played all 17 prior year"),
        lift(lambda g: g.prior_cv >= 0.65, "prior-year weekly CV ≥ 0.65 (volatile)"),
        lift(lambda g: g.prior_fin <= 6, "prior-year top-6 finish"),
        lift(lambda g: g.vegas >= 10, "Vegas win total ≥ 10"),
        lift(lambda g: g.vegas <= 6.5, "Vegas win total ≤ 6.5"),
        lift(lambda g: (g.vac_share >= 0.35) & (g.moved == 0) & (g.rookie == 0), "incumbent on team that vacated ≥ 35%"),
        lift(lambda g: (g.vac_share >= 0.35) & ((g.moved == 1) | (g.rookie == 1)), "arrival/rookie on team that vacated ≥ 35%"),
        lift(lambda g: g.ecr_sd >= g.ecr_sd.quantile(0.75), "expert spread in top quartile (2020+)"),
        lift(lambda g: g.ecr_sd <= g.ecr_sd.quantile(0.25), "expert spread in bottom quartile (2020+)"),
        lift(lambda g: (g.ecr - g.ecr_best) >= 0.3 * g.ecr, "most bullish expert ≥ 30% above consensus (2020+)"),
        lift(lambda g: (g.ecr_worst - g.ecr) >= 0.3 * g.ecr, "most bearish expert ≥ 30% below consensus (2020+)"),
        lift(lambda g: g.value >= 8, "ADP ≥ 8 picks later than ECR (2020+)"),
        lift(lambda g: g.value <= -8, "ADP ≥ 8 picks earlier than ECR (2020+)"),
    ]
    pr("| signal | pos | n | boom lift | bust lift | boom rate | bust rate |")
    pr("|---|---|---|---|---|---|---|")
    signal_lifts = {}
    for label, out in tests:
        for pos, n, lb, lu, rb, ru in out:
            pr(f"| {label} | {pos} | {n} | {lb * 100:+.1f} | {lu * 100:+.1f} | {rb:.2f} | {ru:.2f} |")
            signal_lifts.setdefault(label, {})[pos] = {"n": int(n), "boom_lift": round(lb, 3), "bust_lift": round(lu, 3)}
    priors["signal_lifts"] = signal_lifts
    pr("")

    # --- 4. specific claims ---------------------------------------------------------------------
    pr("## 4. Specific claims the model leans on\n")
    wr = top[(top.pos == "WR") & top.prior_ppg.notna() & (top.prior_games >= 8)]
    mv, st = wr[wr.moved == 1], wr[wr.moved == 0]
    pr(f"- **Receivers who change teams.** PPG change vs prior year: moved {mv.ppg_delta.mean():+.2f} (n={len(mv)}, {100 * (mv.ppg_delta < 0).mean():.0f}% declined) vs stayed {st.ppg_delta.mean():+.2f} (n={len(st)}, {100 * (st.ppg_delta < 0).mean():.0f}% declined).")
    rb = top[(top.pos == "RB") & top.prior_ppg.notna() & (top.prior_games >= 8)]
    for lab, sel in (("RB age ≤ 25", rb.age <= 25), ("RB age 26", rb.age == 26), ("RB age 27", rb.age == 27), ("RB age 28", rb.age == 28), ("RB age ≥ 29", rb.age >= 29)):
        g = rb[sel]
        if len(g) >= 10:
            pr(f"- **{lab}.** PPG change {g.ppg_delta.mean():+.2f}, hit rate {g.hit.mean():.2f}, bust rate {g.bust.mean():.2f} (n={len(g)}).")
    rb1 = top[(top.pos == "RB") & (top.prior_fin <= 3)]
    pr(f"- **Prior-year top-3 RBs** (n={len(rb1)}): repeated a top-3 finish {100 * (rb1.fin <= 3).mean():.0f}% of the time, finished top-12 {100 * (rb1.fin <= 12).mean():.0f}%, PPG change {rb1.ppg_delta.mean():+.2f}.")
    y2 = top[(top.pos == "WR") & (top.years_exp == 1)]
    y3 = top[(top.pos == "WR") & (top.years_exp == 2)]
    vet = top[(top.pos == "WR") & (top.years_exp >= 4)]
    pr(f"- **Breakouts by experience (WR, boom as defined).** Year 2: {y2.boom.mean():.2f} (n={len(y2)}), year 3: {y3.boom.mean():.2f} (n={len(y3)}), 5th season or later: {vet.boom.mean():.2f} (n={len(vet)}).")
    inc = top[(top.moved == 0) & (top.rookie == 0) & top.vac_share.notna() & top.prior_tshare.notna() & (top.pos.isin(["WR", "TE"]))]
    pr(f"- **Vacated targets vs incumbent growth (WR/TE).** Spearman between the team's vacated target share and the incumbent's PPG change: {spearman(inc.vac_share, inc.ppg_delta):.3f} (n={len(inc)}).")
    d = d20[d20.adp <= 120]
    pr(f"- **Expert disagreement as a variance signal (2020-25, top 120).** Spearman between expert spread and |finish − ECR positional rank|: {spearman(d.ecr_sd, (d.fin - d.adp_pos).abs()):.3f}; between spread and bust: {spearman(d.ecr_sd, d.bust):.3f}; between spread and boom: {spearman(d.ecr_sd, d.boom):.3f}.")
    v = top[top.vegas.notna()]
    pr(f"- **Vegas win total.** Spearman with total PPR points for drafted players: {spearman(v.vegas, v.total):.3f} (n={len(v)}); with finish rank residual after ADP (finish − ADP positional rank): {spearman(v.vegas, v.fin - v.adp_pos):.3f}.")
    pb = top[top.prior_boom.notna()]
    pr(f"- **Prior-year boom-week rate.** Spearman with boom: {spearman(pb.prior_boom, pb.boom):.3f}; prior bust-week rate with bust: {spearman(pb.prior_bust, pb.bust):.3f}; prior games missed with bust: {spearman(pb.prior_missed, pb.bust):.3f}.")
    pr("")

    # --- 5. multivariate fits, walk-forward --------------------------------------------------------------
    pr("## 5. Fitted boom and bust models, walk-forward\n")
    pr("Logistic regression (L2, standardized inputs) trained on 2016-2023 and scored on 2024-2025 held out. Baseline = ADP positional rank alone. AUC 0.5 is coin-flip.\n")
    feats_all = ["adp_pos", "age", "years_exp", "rookie", "moved", "prior_ppg", "prior_missed", "prior_boom", "prior_bust", "prior_cv", "vegas", "vac_share"]
    feats_ecr = feats_all + ["ecr_sd", "ecr_gap", "value"]
    fitted = {}
    pr("| target | position | features | train n | test n | AUC ADP-only | AUC model | top-decile rate | base rate |")
    pr("|---|---|---|---|---|---|---|---|---|")
    for target in ("boom", "bust"):
        for pos in ("RB", "WR", "QB", "TE", "ALL"):
            for feats, tag, minyear in ((feats_all, "ADP + history", 2016), (feats_ecr, "+ expert spread (2020+)", 2020)):
                sub = top if pos == "ALL" else top[top.pos == pos]
                sub = sub[sub.season >= minyear]
                tr, te = sub[sub.season <= 2023], sub[sub.season >= 2024]
                if len(tr) < 80 or len(te) < 30 or te[target].sum() < 5:
                    continue
                Xtr = tr[feats].astype(float).values; Xte = te[feats].astype(float).values
                coef, b, mu, sd = logistic_fit(Xtr, tr[target].values, l2=2.0)
                s = logistic_score(Xte, coef, b, mu, sd)
                a_model = auc(s, te[target].values)
                a_adp = auc(-te.adp_pos.values if target == "boom" else te.adp_pos.values, te[target].values)
                thr = np.quantile(s, 0.9)
                topdec = te[target].values[s >= thr].mean()
                pr(f"| {target} | {pos} | {tag} | {len(tr)} | {len(te)} | {a_adp:.3f} | {a_model:.3f} | {topdec:.2f} | {te[target].mean():.2f} |")
                fitted[f"{target}|{pos}|{tag}"] = {"features": feats, "coef_std": [round(float(c), 3) for c in coef], "intercept": round(float(b), 3),
                                                     "auc_model": round(a_model, 3), "auc_adp": round(a_adp, 3), "test_n": int(len(te))}
    pr("")
    pr("Standardized coefficients (sign and size tell you what the fit actually uses), ALL positions, 2016-2023 training:\n")
    for target in ("boom", "bust"):
        for tag in ("ADP + history", "+ expert spread (2020+)"):
            f = fitted.get(f"{target}|ALL|{tag}")
            if not f:
                continue
            pairs = sorted(zip(f["features"], f["coef_std"]), key=lambda t: -abs(t[1]))
            pr(f"- **{target}, {tag}:** " + ", ".join(f"{k} {v:+.2f}" for k, v in pairs))
    pr("")

    # --- 6. hand-weight proxy vs fitted ---------------------------------------------------------------
    pr("## 6. The app's hand-set weights vs the fitted model (2020-25, top 120)\n")
    d = d20[d20.adp <= 120].copy()
    d["scale"] = 0.5 * d.ecr + 5
    proxy_boom = (0.20 * ((d.ecr - d.ecr_best) / d.scale).clip(0, 1) + 0.20 * d.prior_boom.fillna(d.prior_boom.median()) / 0.5
                  + 0.10 * (d.age <= 24).astype(float) + 0.10 * (d.value / 10).clip(0, 1))
    proxy_bust = (0.10 * ((d.ecr_worst - d.ecr) / d.scale).clip(0, 1) + 0.15 * d.prior_bust.fillna(d.prior_bust.median()) / 0.5
                  + 0.10 * ((d.age >= 29) & (d.pos == "RB")).astype(float) + 0.05 * (-d.value / 10).clip(0, 1) + 0.15 * (d.prior_missed.fillna(2) / 12).clip(0, 1))
    pr(f"- Hand-weight proxy (only the inputs that exist historically: disagreement, prior boom/bust rates, age, value, games missed): boom AUC {auc(proxy_boom, d.boom):.3f}, bust AUC {auc(proxy_bust, d.bust):.3f} on 2020-25.")
    te = d[d.season >= 2024]
    if len(te):
        pr(f"- Same proxy on the 2024-25 holdout: boom AUC {auc(proxy_boom[d.season >= 2024], te.boom):.3f}, bust AUC {auc(proxy_bust[d.season >= 2024], te.bust):.3f}, vs ADP-only {auc(-te.adp_pos, te.boom):.3f} / {auc(te.adp_pos, te.bust):.3f}.")
    pr("")

    # --- 7. measured priors for the model ---------------------------------------------------------------
    age_tbl = {}
    for pos in POS:
        g = top[top.pos == pos]
        age_tbl[pos] = {str(a): {"n": int(len(gg)), "bust": round(gg.bust.mean(), 3), "boom": round(gg.boom.mean(), 3)} for a, gg in g.groupby("age") if len(gg) >= 15}
    exp_tbl = {}
    for pos in POS:
        g = top[top.pos == pos]
        exp_tbl[pos] = {str(int(e)): {"n": int(len(gg)), "boom": round(gg.boom.mean(), 3), "bust": round(gg.bust.mean(), 3)} for e, gg in g.groupby("years_exp") if len(gg) >= 15}
    priors.update({"age": age_tbl, "years_exp": exp_tbl, "fitted": fitted, "definitions": {"hit": STARTER, "boom_gap": BOOM_GAP, "bust": "fin >= 2*adp_pos or games <= 10"},
                   "generated": date.today().isoformat(), "seasons": YEARS})
    (HERE / "data" / "backtest_priors.json").write_text(json.dumps(priors, indent=1))

    pr("## 7. What this means for the model\n")
    pr("See the summary in the chat and `data/backtest_priors.json` for the measured round, age and experience tables. Coefficients above are on standardized inputs; the app's hand weights are compared in section 6.\n")
    (HERE / "research" / "BACKTEST.md").write_text("\n".join(L))
    print("\n".join(L))


if __name__ == "__main__":
    main()
