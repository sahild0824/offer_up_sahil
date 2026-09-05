#!/usr/bin/env python3
"""Derive market, projection, injury and team-context features from public GitHub datasets.

Sources (all verified reachable on 2026-09-05; see research/repos_survey.md):
  Danoodli/fantasy-drafter        FFC PPR ADP with stdev (7,681 drafts, Aug 28 - Sep 4), Sleeper ADP daily history,
                                   Sleeper stat-line projections, ESPN live player file (ADP, PPR rank, injury status, projections)
  najibismail95/...ADP-Comparison  daily ESPN / FantasyPros / Sleeper / Yahoo ADP snapshots Jul 27 - Sep 4
  srsavas42/fantasy-football-research  hierarchical-Bayesian PPR projections (p10 / p50 / p90, projected games, shares); Vegas win totals
  lhallee/fantasy-football-feature-discovery  calibrated missed-time injury probability, ML projections (frozen Aug 9)
  StrubeTube/the-lab              DraftKings win totals, PFF preseason O-line ranks, 2024-25 injury log by body part
  demansou/fantasy-football-26    2026 play-caller census with sources
  ffverse/ffopportunity           2025 expected fantasy points (efficiency / TD regression)
  nflverse roster_2026.csv        Sleeper id -> player crosswalk

Output: data/market_features.json  {players: {"<norm name>|<pos>": {...}}, teams: {...}, generated, notes}
Run:    python3 market_features.py [--fetch]
"""
import csv
import json
import re
import statistics
import sys
import unicodedata
import urllib.request
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAW = HERE / "data" / "raw" / "pull"
NFL = HERE / "data" / "raw" / "nflverse"
OUT = HERE / "data" / "market_features.json"
FILES = {
    "ffc-ppr.json": "https://raw.githubusercontent.com/Danoodli/fantasy-drafter/main/data/raw/ffc-ppr.json",
    "adp-history-ppr.json": "https://raw.githubusercontent.com/Danoodli/fantasy-drafter/main/data/raw/adp-history-ppr.json",
    "sleeper-projections.json": "https://raw.githubusercontent.com/Danoodli/fantasy-drafter/main/data/raw/sleeper-projections.json",
    "espn-kona.json": "https://raw.githubusercontent.com/Danoodli/fantasy-drafter/main/data/raw/espn-kona.json",
    "srsavas_2026_ppr.csv": "https://raw.githubusercontent.com/srsavas42/fantasy-football-research/main/projections/2026_ppr.csv",
    "vegas_win_totals_2026.csv": "https://raw.githubusercontent.com/srsavas42/fantasy-football-research/main/Vegas%20Win%20Totals/NFL%20Win%20Totals-export-2026-08-23.csv",
    "strube_team_context.json": "https://raw.githubusercontent.com/StrubeTube/the-lab/main/data/team_context.json",
    "strube_injury_recent.json": "https://raw.githubusercontent.com/StrubeTube/the-lab/main/data/injury_recent.json",
    "lhallee_rankings_2026.xlsx": "https://raw.githubusercontent.com/lhallee/fantasy-football-feature-discovery/main/outputs/fantasy_football_final_rankings_2026.xlsx",
    "najib_adp_snapshots.parquet": "https://raw.githubusercontent.com/najibismail95/Fantasy-Football-ADP-Comparison-Tool/main/data/silver/adp_snapshots.parquet",
    "najib_xref.parquet": "https://raw.githubusercontent.com/najibismail95/Fantasy-Football-ADP-Comparison-Tool/main/data/silver/player_xref.parquet",
    "ep_weekly_2025.csv": "https://github.com/ffverse/ffopportunity/releases/download/latest-data/ep_weekly_2025.csv",
    "demansou_playcaller_census.json": "https://raw.githubusercontent.com/demansou/fantasy-football-26/main/data/research/2026/playcaller_census.json",
    "ffc-half-ppr.json": "https://raw.githubusercontent.com/Danoodli/fantasy-drafter/main/data/raw/ffc-half-ppr.json",
    "ffc-standard.json": "https://raw.githubusercontent.com/Danoodli/fantasy-drafter/main/data/raw/ffc-standard.json",
}
POS = ("QB", "RB", "WR", "TE")
ESPN_TEAM = {1: "ATL", 2: "BUF", 3: "CHI", 4: "CIN", 5: "CLE", 6: "DAL", 7: "DEN", 8: "DET", 9: "GB", 10: "TEN", 11: "IND", 12: "KC", 13: "LV", 14: "LAR",
             15: "MIA", 16: "MIN", 17: "NE", 18: "NO", 19: "NYG", 20: "NYJ", 21: "PHI", 22: "ARI", 23: "PIT", 24: "LAC", 25: "SF", 26: "SEA", 27: "TB",
             28: "WAS", 29: "CAR", 30: "JAX", 33: "BAL", 34: "HOU"}
ESPN_POS = {1: "QB", 2: "RB", 3: "WR", 4: "TE"}
TEAM_FIX = {"LA": "LAR", "JAC": "JAX", "WSH": "WAS"}


def norm_name(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode()
    s = s.lower().replace("'", "").replace(".", "").replace("-", " ")
    s = re.sub(r"\b(jr|sr|ii|iii|iv|v)\b", "", s)
    return re.sub(r"\s+", " ", s).strip()


def fetch():
    RAW.mkdir(parents=True, exist_ok=True)
    for name, url in FILES.items():
        if not (RAW / name).exists():
            print("downloading", name)
            urllib.request.urlretrieve(url, RAW / name)


def jload(name):
    with (RAW / name).open() as f:
        return json.load(f)


def ppr(passyds=0, passtd=0, ints=0, rushyds=0, rushtd=0, rec=0, recyds=0, rectd=0, fum=0):
    return passyds / 25 + passtd * 4 - ints * 2 + rushyds / 10 + rushtd * 6 + rec + recyds / 10 + rectd * 6 - fum * 2


def main():
    if "--fetch" in sys.argv or not all((RAW / n).exists() for n in FILES):
        fetch()
    import pandas as pd

    # Sleeper id -> (name, pos) from the nflverse Week 1 roster, then the ADP tool's crosswalk
    sleeper = {}
    with (NFL / "roster_2026.csv").open(newline="") as f:
        for r in csv.DictReader(f):
            if r.get("sleeper_id") and r["position"] in POS:
                sleeper[r["sleeper_id"]] = (r["full_name"], r["position"])
    xref = pd.read_parquet(RAW / "najib_xref.parquet")
    for _, r in xref.iterrows():
        sid = str(r["player_id"])
        if sid not in sleeper and r.get("source_name"):
            sleeper[sid] = (r["source_name"], None)

    P = defaultdict(dict)

    def key_for(name, pos):
        return norm_name(name) + "|" + pos

    # --- FFC ADP with stdev ----------------------------------------------------------------------
    ffc = jload("ffc-ppr.json")
    for r in ffc["players"]:
        if r["position"] in POS:
            P[key_for(r["name"], r["position"])]["ffc"] = {"adp": r["adp"], "stdev": r["stdev"], "high": r["high"], "low": r["low"], "n": r["times_drafted"]}
    ffc_meta = ffc["meta"]
    for fname, key in (("ffc-half-ppr.json", "ffcHalf"), ("ffc-standard.json", "ffcStd")):
        for r in jload(fname)["players"]:
            if r["position"] in POS:
                P[key_for(r["name"], r["position"])][key] = {"adp": r["adp"], "stdev": r["stdev"], "n": r["times_drafted"]}

    # --- Sleeper ADP history (PPR) -> 7-day trend ------------------------------------------------
    hist = jload("adp-history-ppr.json")
    days = sorted(hist)
    latest, prior = days[-1], days[max(0, len(days) - 8)]
    for sid, adp in hist[latest].items():
        nm = sleeper.get(sid)
        if not nm:
            continue
        old = hist[prior].get(sid)
        for pos in ([nm[1]] if nm[1] else POS):
            k = key_for(nm[0], pos)
            P[k].setdefault("sleeperAdp", {})["latest"] = adp
            if old is not None:
                P[k]["sleeperAdp"]["d7"] = round(adp - old, 1)
                P[k]["sleeperAdp"]["window"] = f"{prior} to {latest}"

    # --- Sleeper projections --------------------------------------------------------------------
    sp = jload("sleeper-projections.json")
    for sid, v in sp.items():
        nm = sleeper.get(sid)
        if not nm or not v.get("stats"):
            continue
        st = v["stats"]
        pts = ppr(st.get("passYds", 0), st.get("passTD", 0), st.get("passInt", 0), st.get("rushYds", 0), st.get("rushTD", 0), st.get("receptions", 0), st.get("recYds", 0), st.get("recTD", 0), st.get("fumblesLost", 0))
        if pts < 20:
            continue
        for pos in ([nm[1]] if nm[1] else POS):
            P[key_for(nm[0], pos)]["sleeper"] = {"projPpr": round(pts, 1), "adpPpr": (v.get("adp") or {}).get("ppr"), "adpHalf": (v.get("adp") or {}).get("half-ppr"), "adpStd": (v.get("adp") or {}).get("standard"),
                                                 "stats": {"passYds": st.get("passYds", 0), "passTD": st.get("passTD", 0), "ints": st.get("passInt", 0), "rushYds": st.get("rushYds", 0), "rushTD": st.get("rushTD", 0),
                                                           "rec": st.get("receptions", 0), "recYds": st.get("recYds", 0), "recTD": st.get("recTD", 0), "fum": st.get("fumblesLost", 0)}}

    # --- ESPN live player file ------------------------------------------------------------------
    kona = jload("espn-kona.json")
    kona_rows = kona.get("players") if isinstance(kona, dict) else kona
    for row in kona_rows:
        pl = row.get("player", row)
        pos = ESPN_POS.get(pl.get("defaultPositionId"))
        if not pos:
            continue
        team = ESPN_TEAM.get(pl.get("proTeamId"))
        proj = next((s for s in pl.get("stats", []) if s.get("seasonId") == 2026 and s.get("statSourceId") == 1 and s.get("statSplitTypeId") == 0), None)
        pts = None; stats = None
        if proj and proj.get("stats"):
            st = {int(k): v for k, v in proj["stats"].items()}
            pts = round(ppr(st.get(3, 0), st.get(4, 0), st.get(20, 0), st.get(24, 0), st.get(25, 0), st.get(53, 0), st.get(42, 0), st.get(43, 0), st.get(72, 0)), 1)
            stats = {"passYds": st.get(3, 0), "passTD": st.get(4, 0), "ints": st.get(20, 0), "rushYds": st.get(24, 0), "rushTD": st.get(25, 0), "rec": st.get(53, 0), "recYds": st.get(42, 0), "recTD": st.get(43, 0), "fum": st.get(72, 0)}
        own = pl.get("ownership") or {}
        rk = ((pl.get("draftRanksByRankType") or {}).get("PPR") or {}).get("rank")
        P[key_for(pl["fullName"], pos)]["espn"] = {
            "team": team, "adp": own.get("averageDraftPosition"), "adpChangePct": own.get("averageDraftPositionPercentChange"), "pctOwned": own.get("percentOwned"),
            "pprRank": rk, "injuryStatus": pl.get("injuryStatus"), "projPpr": pts, "auction": own.get("auctionValueAverage"), "stats": stats,
        }

    # --- daily multi-source ADP snapshots -> latest per source + 7/30-day trend --------------------
    na = pd.read_parquet(RAW / "najib_adp_snapshots.parquet")
    na["captured_at"] = pd.to_datetime(na["captured_at"]).dt.date
    last_day = na["captured_at"].max()
    d7 = last_day - timedelta(days=7)
    d30 = last_day - timedelta(days=30)
    na = na[na["adp"].notna() & (na["adp"] < 400)]
    grp = na.groupby(["player_id", "source"])
    for (sid, src), g in grp:
        nm = sleeper.get(str(sid))
        if not nm:
            continue
        g = g.sort_values("captured_at")
        lat = g.iloc[-1]
        old7 = g[g["captured_at"] <= d7]
        old30 = g[g["captured_at"] <= d30]
        for pos in ([nm[1]] if nm[1] else POS):
            k = key_for(nm[0], pos)
            d = P[k].setdefault("adpLatest", {})
            d[src.lower()] = {"adp": round(float(lat["adp"]), 1), "date": str(lat["captured_at"])}
            if len(old7):
                d[src.lower()]["d7"] = round(float(lat["adp"]) - float(old7.iloc[-1]["adp"]), 1)
            if len(old30):
                d[src.lower()]["d30"] = round(float(lat["adp"]) - float(old30.iloc[-1]["adp"]), 1)
    for k, v in P.items():
        al = v.get("adpLatest")
        if al:
            t7 = [x["d7"] for x in al.values() if "d7" in x]
            t30 = [x["d30"] for x in al.values() if "d30" in x]
            v["adpTrend"] = {"d7": round(statistics.mean(t7), 1) if t7 else None, "d30": round(statistics.mean(t30), 1) if t30 else None, "asOf": str(last_day)}

    # --- Bayesian projections --------------------------------------------------------------------
    sr = pd.read_csv(RAW / "srsavas_2026_ppr.csv")
    for _, r in sr.iterrows():
        if r["position"] not in POS:
            continue
        P[key_for(r["player_name"], r["position"])]["bayes"] = {
            "proj": round(float(r["projection"]), 1), "p10": round(float(r["p10"]), 1), "p50": round(float(r["p50"]), 1), "p90": round(float(r["p90"]), 1),
            "games": round(float(r["projected_games"]), 1), "tgtShare": round(float(r["target_share"]), 3) if pd.notna(r["target_share"]) else None,
            "recEst": round(float(r["targets"]) * float(r["catch_rate"]), 1) if pd.notna(r.get("targets")) and pd.notna(r.get("catch_rate")) else None,
            "carShare": round(float(r["carry_share"]), 3) if pd.notna(r["carry_share"]) else None, "team": r["team"],
        }

    # --- lhallee: injury probability + ML projection (frozen Aug 9) ---------------------------------
    x = pd.ExcelFile(RAW / "lhallee_rankings_2026.xlsx")
    df = x.parse("ALL")
    col = {c.lower(): c for c in df.columns}
    for _, r in df.iterrows():
        pos = str(r.get(col.get("pos", "Pos"), ""))
        if pos not in POS:
            continue
        ip = r.get("Missed-Time Injury Probability")
        P[key_for(str(r["Player"]), pos)]["lhallee"] = {
            "injProb": round(float(ip), 3) if pd.notna(ip) else None, "pred": round(float(r["Projected 2026 Points"]), 1) if pd.notna(r.get("Projected 2026 Points")) else None,
            "p10": round(float(r["Points P10"]), 1) if pd.notna(r.get("Points P10")) else None, "p90": round(float(r["Points P90"]), 1) if pd.notna(r.get("Points P90")) else None,
            "band": r.get("Injury Risk Band"), "listing": r.get("Current Injury Listing (screen date)"),
        }

    # --- injury log 2024-25 by body part (Sleeper ids) --------------------------------------------
    ir = jload("strube_injury_recent.json")
    for sid, items in ir.items():
        nm = sleeper.get(sid)
        if not nm:
            continue
        log = [{"y": i["y"], "part": i["p"], "out": i["o"], "tier": i["t"]} for i in items if i.get("o", 0) > 0 or i.get("t") == "long"]
        for pos in ([nm[1]] if nm[1] else POS):
            P[key_for(nm[0], pos)]["injuryLog"] = log[:6]
            P[key_for(nm[0], pos)]["gamesOut2425"] = sum(i["o"] for i in items)

    # --- expected points 2025 (ffopportunity) ----------------------------------------------------
    ep = defaultdict(lambda: {"actual": 0.0, "exp": 0.0, "g": 0})
    with (RAW / "ep_weekly_2025.csv").open(newline="") as f:
        for r in csv.DictReader(f):
            if r.get("position") not in POS:
                continue
            try:
                a, e = float(r["total_fantasy_points"] or 0), float(r["total_fantasy_points_exp"] or 0)
            except ValueError:
                continue
            k = key_for(r["full_name"], r["position"])
            ep[k]["actual"] += a
            ep[k]["exp"] += e
            ep[k]["g"] += 1
    for k, v in ep.items():
        if v["g"] >= 6 and v["exp"] > 40:
            P[k]["ep2025"] = {"actual": round(v["actual"], 1), "expected": round(v["exp"], 1), "diffPct": round((v["actual"] - v["exp"]) / v["exp"], 3), "games": v["g"]}

    # --- teams: Vegas, O-line, play-callers ---------------------------------------------------------
    teams = defaultdict(dict)
    with (RAW / "vegas_win_totals_2026.csv").open(newline="") as f:
        rows = list(csv.reader(f))
        hdr = rows[0]
        i_team, i_coach, i_total = hdr.index("Team"), hdr.index("Coach"), hdr.index("Vegas Total")
        for r in rows[1:]:
            if len(r) <= i_total or not r[i_team]:
                continue
            t = TEAM_FIX.get(r[i_team], r[i_team])
            try:
                teams[t]["vegasWins"] = float(r[i_total])
                teams[t]["hcListed"] = r[i_coach]
            except ValueError:
                pass
    tc = jload("strube_team_context.json")
    for t, v in tc.get("teams", {}).items():
        t = TEAM_FIX.get(t, t)
        teams[t]["dkWins"] = v.get("wins")
        teams[t]["olineRank"] = v.get("oline")
    census = jload("demansou_playcaller_census.json")
    census_rows = census.get("teams") or census.get("entries") or census.get("data") or []
    if isinstance(census_rows, dict):
        census_rows = [dict(v, team=k) for k, v in census_rows.items()]
    for row in census_rows:
        t = TEAM_FIX.get(row.get("team") or row.get("team_abbr") or "", row.get("team") or row.get("team_abbr") or "")
        if t:
            teams[t]["census"] = {k: v for k, v in row.items() if k != "team"}

    # keep only players in the rankings universe (drops the four-position fallback rows for unknown ids)
    universe = set()
    rk_path = HERE / "data" / "rankings.json"
    if rk_path.exists():
        for r in json.loads(rk_path.read_text()):
            universe.add(key_for(r["name"], r["pos"].upper()))
        P = {k: v for k, v in P.items() if k in universe}
    out = {
        "generated": date.today().isoformat(),
        "notes": {"ffc": f"FFC {ffc_meta['type']} {ffc_meta['teams']}-team, {ffc_meta['total_drafts']} drafts {ffc_meta['start_date']} to {ffc_meta['end_date']}",
                  "adpSnapshots": f"daily ESPN / FantasyPros / Sleeper / Yahoo ADP through {last_day}", "sleeperHistory": f"{days[0]} to {days[-1]}",
                  "census": f"play-caller census as of {census.get('as_of')}"},
        "players": {k: v for k, v in P.items() if v},
        "teams": dict(teams),
    }
    OUT.write_text(json.dumps(out, indent=0))
    cov = defaultdict(int)
    for v in out["players"].values():
        for k in v:
            cov[k] += 1
    print("players with any feature:", len(out["players"]), dict(cov))
    print("teams:", len(teams), "sample", {k: teams[k] for k in list(teams)[:2]})
    print("census keys sample:", (census_rows[0].keys() if census_rows else None), "| census top-level:", list(census.keys()))
    print("wrote", OUT.relative_to(HERE), f"({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
