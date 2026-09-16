#!/usr/bin/env python3
"""Pull the week's in-season inputs and write data/weekly_2026.json for weekly.py.

Every source is free, keyless and verified reachable from this sandbox (2026-09-16):

  nflverse releases (github.com/nflverse/nflverse-data)
    stats_player/stats_player_week_2026.csv   per-player weekly box score, target_share, wopr, PPR pts
    snap_counts/snap_counts_2026.csv          offense_snaps / offense_pct (PFR ids)
    injuries/injuries_2026.csv                official practice + game-status reports
    schedules/games.csv                       spread_line, total_line, roof for upcoming weeks
    weekly_rosters/roster_weekly_2026.csv     status (ACT / RES / INA), espn_id
  ffverse (github.com/ffverse/ffopportunity)
    ep_weekly_2026.csv                        expected fantasy points from play-by-play
  DynastyProcess mirror (raw.githubusercontent.com/dynastyprocess/data)
    fp_latest_weekly.csv                      FantasyPros weekly ECR, start/sit grade, r2p projection
    db_playerids.csv                          fantasypros_id / pfr_id / gsis_id / espn_id bridge

Joins run on gsis_id. Snap counts bridge pfr_id -> gsis_id and FantasyPros bridges
fantasypros_id -> gsis_id through db_playerids, with a name+position fallback for each.
The draft model's players.json is bridged through the existing nflverse_features.json,
whose keys are "<norm name>|<pos>" and carry gsis_id.

    python3 ingest.py --week 2            # use cached files in data/raw/inseason
    python3 ingest.py --week 2 --fetch    # download fresh copies first

Defense-vs-position follows the shrinkage the open-source survey converged on: the 2025
per-game base is blended with the 2026 running average at weight n/(n+4) and the resulting
multiplier is clamped to [0.8, 1.2]. Recent form is an EWMA with half-life 2 weeks, and a
week a player's team played without him counts as zero, not as missing.
"""
import argparse
import csv
import io
import json
import math
import re
import sys
import time
import unicodedata
import urllib.request
from collections import defaultdict
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
RAW = DATA / "raw" / "inseason"
OUT = DATA / "weekly_2026.json"
SEASON = 2026

NFLV = "https://github.com/nflverse/nflverse-data/releases/download/"
DP = "https://raw.githubusercontent.com/dynastyprocess/data/master/files/"
SOURCES = {
    "stats_player_week_2026.csv": NFLV + "stats_player/stats_player_week_2026.csv",
    "snap_counts_2026.csv": NFLV + "snap_counts/snap_counts_2026.csv",
    "injuries_2026.csv": NFLV + "injuries/injuries_2026.csv",
    "games.csv": NFLV + "schedules/games.csv",
    "roster_weekly_2026.csv": NFLV + "weekly_rosters/roster_weekly_2026.csv",
    "ep_weekly_2026.csv": "https://github.com/ffverse/ffopportunity/releases/download/latest-data/ep_weekly_2026.csv",
    "fp_latest_weekly.csv": DP + "fp_latest_weekly.csv",
    "db_playerids.csv": DP + "db_playerids.csv",
}
POS = ("QB", "RB", "WR", "TE")
TEAM_FIX = {"LA": "LAR", "JAC": "JAX", "WSH": "WAS", "OAK": "LV", "SD": "LAC", "STL": "LAR", "LVR": "LV"}
EWMA_HALF_LIFE = 2.0
DVP_PRIOR_N = 4.0
DVP_CLAMP = (0.8, 1.2)
INJURY_AVAIL = {"out": 0.0, "doubtful": 0.35, "questionable": 0.75}


def norm_name(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode()
    s = s.lower().replace("'", "").replace(".", "").replace("-", " ")
    s = re.sub(r"\b(jr|sr|ii|iii|iv|v)\b", "", s)
    return re.sub(r"\s+", " ", s).strip()


def team(t):
    t = (t or "").strip().upper()
    return TEAM_FIX.get(t, t)


def fnum(v, default=None):
    try:
        if v in (None, "", "NA", "NaN"):
            return default
        return float(v)
    except ValueError:
        return default


def fetch(name, url, retries=4):
    RAW.mkdir(parents=True, exist_ok=True)
    dest = RAW / name
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "fourth-pick-war-room/inseason"})
            with urllib.request.urlopen(req, timeout=120) as r:
                dest.write_bytes(r.read())
            print(f"  fetched {name}  ({dest.stat().st_size // 1024} KB)", file=sys.stderr)
            return dest
        except Exception as e:  # noqa: BLE001
            wait = 2 ** i
            print(f"  {name}: {e} (retry in {wait}s)", file=sys.stderr)
            time.sleep(wait)
    raise SystemExit(f"could not fetch {name} from {url}")


def read_csv(name):
    path = RAW / name
    if not path.exists():
        raise SystemExit(f"missing {path}; run with --fetch")
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# ---------------------------------------------------------------------------------------------
def build(week, fetch_first):
    if fetch_first:
        print("fetching sources", file=sys.stderr)
        for name, url in SOURCES.items():
            fetch(name, url)

    stats = [r for r in read_csv("stats_player_week_2026.csv") if r.get("season_type") == "REG"]
    snaps = read_csv("snap_counts_2026.csv")
    injuries = read_csv("injuries_2026.csv")
    games = [g for g in read_csv("games.csv") if g.get("season") == str(SEASON)]
    rosters = read_csv("roster_weekly_2026.csv")
    ep = read_csv("ep_weekly_2026.csv")
    fp = read_csv("fp_latest_weekly.csv")
    ids = read_csv("db_playerids.csv")
    feats = json.load(open(DATA / "nflverse_features.json"))
    dvp_base = feats["defense_ppr_allowed_2025"]

    # ---- id bridges -----------------------------------------------------------------------
    pfr_to_gsis, fp_to_gsis, name_to_gsis = {}, {}, {}
    for r in ids:
        g = r.get("gsis_id") or ""
        if not g:
            continue
        if r.get("pfr_id"):
            pfr_to_gsis[r["pfr_id"]] = g
        if r.get("fantasypros_id"):
            fp_to_gsis[r["fantasypros_id"]] = g
        if r.get("name") and r.get("position"):
            name_to_gsis[norm_name(r["name"]) + "|" + r["position"].upper()] = g

    # ---- games: schedule, lines, implied totals for the target week -----------------------
    played_weeks = sorted({int(g["week"]) for g in games if g.get("home_score") not in ("", None, "NA")})
    weeks_done = [w for w in played_weeks if w < week]
    teams = {}
    for g in games:
        if int(g["week"]) != week:
            continue
        home, away = team(g["home_team"]), team(g["away_team"])
        spread, total = fnum(g.get("spread_line")), fnum(g.get("total_line"))
        home_it = away_it = None
        if spread is not None and total is not None:
            home_it, away_it = (total + spread) / 2, (total - spread) / 2
        common = {"total": total, "spread_home": spread, "roof": g.get("roof"), "surface": g.get("surface"),
                  "gameday": g.get("gameday"), "gametime": g.get("gametime"), "game_id": g.get("game_id")}
        teams[home] = {**common, "opp": away, "home": True, "implied": home_it, "opp_implied": away_it}
        teams[away] = {**common, "opp": home, "home": False, "implied": away_it, "opp_implied": home_it}
    all_teams = sorted({team(g["home_team"]) for g in games} | {team(g["away_team"]) for g in games})
    for t in all_teams:
        teams.setdefault(t, {"opp": None, "home": None, "implied": None, "opp_implied": None, "total": None,
                             "spread_home": None, "roof": None, "bye": True})

    # which teams played in each completed week (for absence = 0)
    played_in = defaultdict(set)
    for g in games:
        w = int(g["week"])
        if w in weeks_done:
            played_in[w].add(team(g["home_team"]))
            played_in[w].add(team(g["away_team"]))

    # ---- defense vs position: 2025 base blended with 2026 to date -------------------------
    allowed = defaultdict(lambda: defaultdict(float))     # def team -> pos -> pts allowed
    games_by_def = defaultdict(set)
    for r in stats:
        w = int(r["week"])
        if w not in weeks_done or r.get("position") not in POS:
            continue
        d = team(r.get("opponent_team"))
        allowed[d][r["position"]] += fnum(r.get("fantasy_points_ppr"), 0.0)
        games_by_def[d].add(w)
    dvp = {}
    for t in all_teams:
        n = len(games_by_def.get(t, ()))
        wgt = n / (n + DVP_PRIOR_N)
        dvp[t] = {}
        for pos in POS:
            base = fnum((dvp_base.get(t) or {}).get(pos))
            cur = allowed[t][pos] / n if n else None
            if base is None and cur is None:
                dvp[t][pos] = None
            elif base is None:
                dvp[t][pos] = cur
            elif cur is None:
                dvp[t][pos] = base
            else:
                dvp[t][pos] = wgt * cur + (1 - wgt) * base
    dvp_factor = {}
    for pos in POS:
        vals = [dvp[t][pos] for t in all_teams if dvp[t].get(pos) is not None]
        mean = sum(vals) / len(vals) if vals else None
        for t in all_teams:
            v = dvp[t].get(pos)
            f = None if (v is None or not mean) else max(DVP_CLAMP[0], min(DVP_CLAMP[1], v / mean))
            dvp_factor.setdefault(t, {})[pos] = f
    for t in all_teams:
        teams[t]["dvp_pts_allowed"] = dvp[t]
        teams[t]["dvp_factor"] = dvp_factor[t]
        teams[t]["dvp_games"] = len(games_by_def.get(t, ()))

    # ---- players: weekly lines ------------------------------------------------------------
    players = {}
    def P(gsis, name, pos, tm):
        p = players.get(gsis)
        if p is None:
            p = players[gsis] = {"gsis_id": gsis, "name": name, "pos": pos, "team": team(tm), "weeks": {},
                                 "form": {}, "injury": None, "fp": None, "status": None}
        return p

    for r in stats:
        w = int(r["week"])
        if w not in weeks_done or r.get("position") not in POS:
            continue
        p = P(r["player_id"], r.get("player_display_name"), r["position"], r.get("team"))
        p["weeks"][str(w)] = {
            "opp": team(r.get("opponent_team")), "pts": fnum(r.get("fantasy_points_ppr"), 0.0),
            "targets": fnum(r.get("targets"), 0.0), "target_share": fnum(r.get("target_share")),
            "air_yards_share": fnum(r.get("air_yards_share")), "wopr": fnum(r.get("wopr")),
            "carries": fnum(r.get("carries"), 0.0), "receptions": fnum(r.get("receptions"), 0.0),
            "rec_yds": fnum(r.get("receiving_yards"), 0.0), "rush_yds": fnum(r.get("rushing_yards"), 0.0),
            "pass_yds": fnum(r.get("passing_yards"), 0.0), "tds": (fnum(r.get("receiving_tds"), 0.0)
                                                                    + fnum(r.get("rushing_tds"), 0.0)
                                                                    + fnum(r.get("passing_tds"), 0.0)),
            "snap_pct": None, "ep": None,
        }

    for r in ep:
        w = int(r["week"])
        if w not in weeks_done:
            continue
        g = r.get("player_id")
        if g in players and str(w) in players[g]["weeks"]:
            players[g]["weeks"][str(w)]["ep"] = fnum(r.get("total_fantasy_points_exp"))

    snap_miss = 0
    for r in snaps:
        w = int(r["week"])
        if w not in weeks_done or r.get("position") not in POS:
            continue
        g = pfr_to_gsis.get(r.get("pfr_player_id")) or name_to_gsis.get(norm_name(r.get("player")) + "|" + r["position"])
        if g in players and str(w) in players[g]["weeks"]:
            players[g]["weeks"][str(w)]["snap_pct"] = fnum(r.get("offense_pct"))
            players[g]["weeks"][str(w)]["snaps"] = fnum(r.get("offense_snaps"))
        else:
            snap_miss += 1

    # roster status (latest week available)
    latest_roster = {}
    for r in rosters:
        g = r.get("gsis_id")
        if not g:
            continue
        w = int(r["week"])
        if w <= week and (g not in latest_roster or w >= latest_roster[g][0]):
            latest_roster[g] = (w, r)
    for g, (w, r) in latest_roster.items():
        if g in players:
            players[g]["status"] = r.get("status")
            players[g]["team"] = team(r.get("team"))
            players[g]["espn_id"] = r.get("espn_id") or None

    # ---- recent form: EWMA half-life 2, absence = 0 when the team played -------------------
    alpha = 1 - 0.5 ** (1 / EWMA_HALF_LIFE)
    for g, p in players.items():
        ew = n = 0
        ew_pts = ew_snap = ew_tgt = ew_car = ew_ep = None
        pts_list = []
        for w in weeks_done:
            wk = p["weeks"].get(str(w))
            if wk is None:
                if p["team"] not in played_in[w]:
                    continue                                   # bye: skip
                pts, snap, tgt, car, epv = 0.0, 0.0, 0.0, 0.0, 0.0   # absent: zero
                p["weeks"][str(w)] = {"absent": True, "pts": 0.0, "snap_pct": 0.0, "targets": 0.0, "carries": 0.0}
            else:
                pts, snap, tgt, car, epv = wk["pts"], wk.get("snap_pct") or 0.0, wk.get("targets") or 0.0, wk.get("carries") or 0.0, wk.get("ep") or 0.0
            pts_list.append(pts)
            def upd(prev, x):
                return x if prev is None else (1 - alpha) * prev + alpha * x
            ew_pts, ew_snap, ew_tgt, ew_car, ew_ep = upd(ew_pts, pts), upd(ew_snap, snap), upd(ew_tgt, tgt), upd(ew_car, car), upd(ew_ep, epv)
            n += 1
        p["form"] = {"games": n, "ewma_pts": ew_pts, "ewma_snap_pct": ew_snap, "ewma_targets": ew_tgt,
                     "ewma_carries": ew_car, "ewma_ep": ew_ep, "last_pts": pts_list[-1] if pts_list else None,
                     "mean_pts": (sum(pts_list) / len(pts_list)) if pts_list else None}

    # ---- injuries: the latest report row per player for the target week (else prior) ------
    inj_rows = defaultdict(list)
    for r in injuries:
        if r.get("gsis_id"):
            inj_rows[r["gsis_id"]].append(r)
    for g, rows in inj_rows.items():
        rows.sort(key=lambda r: (int(r["week"]), r.get("date_modified") or ""))
        cur = [r for r in rows if int(r["week"]) == week]
        r = cur[-1] if cur else rows[-1]
        status = (r.get("report_status") or "").strip()
        avail = INJURY_AVAIL.get(status.lower(), 1.0) if status else 1.0
        entry = {"week": int(r["week"]), "status": status or None, "practice": r.get("practice_status") or None,
                 "injury": r.get("report_primary_injury") or None, "avail": avail, "stale": int(r["week"]) < week}
        if g in players:
            players[g]["injury"] = entry
        else:
            P(g, r.get("full_name"), r.get("position"), r.get("team"))["injury"] = entry

    # ---- FantasyPros weekly ECR / grade / projection --------------------------------------
    fp_miss = 0
    page_pos = {"qb": "QB", "ppr-rb": "RB", "ppr-wr": "WR", "ppr-te": "TE", "k": "K", "dst": "DST"}
    fp_dst, fp_k = {}, {}
    for r in fp:
        pos = page_pos.get(r.get("page"))
        if not pos:
            continue
        entry = {"ecr": fnum(r.get("ecr")), "sd": fnum(r.get("sd")), "rank": fnum(r.get("rank")),
                 "pos_rank": r.get("pos_rank"), "grade": r.get("start_sit_grade") or None,
                 "proj": fnum(r.get("r2p_pts")), "opp": r.get("player_opponent"), "owned": fnum(r.get("player_owned_avg")),
                 "scrape_date": r.get("scrape_date")}
        if pos == "DST":
            fp_dst[team(r.get("team"))] = {**entry, "name": r.get("player_name")}
            continue
        if pos == "K":
            fp_k[norm_name(r.get("player_name"))] = {**entry, "name": r.get("player_name"), "team": team(r.get("team"))}
            continue
        g = fp_to_gsis.get(r.get("fantasypros_id")) or name_to_gsis.get(norm_name(r.get("player_name")) + "|" + pos)
        if g:
            P(g, r.get("player_name"), pos, r.get("team"))["fp"] = entry
        else:
            fp_miss += 1

    # ---- bridge to the draft model's names ------------------------------------------------
    by_name = {}
    for key, f in feats["players"].items():
        if f.get("gsis_id") and f["gsis_id"] in players:
            by_name[key] = f["gsis_id"]
    for g, p in players.items():
        by_name.setdefault(norm_name(p["name"]) + "|" + p["pos"], g)

    out = {
        "generated": date.today().isoformat(), "season": SEASON, "week": week, "weeks_done": weeks_done,
        "ewma_half_life": EWMA_HALF_LIFE, "dvp_prior_n": DVP_PRIOR_N, "dvp_clamp": DVP_CLAMP,
        "fp_scrape_date": (fp[0].get("scrape_date") if fp else None),
        "teams": teams, "players": players, "by_name": by_name, "fp_dst": fp_dst, "fp_k": fp_k,
        "coverage": {"players": len(players), "with_snaps": sum(1 for p in players.values() if any(w.get("snap_pct") is not None for w in p["weeks"].values())),
                     "with_fp": sum(1 for p in players.values() if p["fp"]), "with_injury": sum(1 for p in players.values() if p["injury"]),
                     "snap_rows_unmatched": snap_miss, "fp_rows_unmatched": fp_miss, "by_name": len(by_name)},
    }
    OUT.write_text(json.dumps(out, indent=1))
    print(f"wrote {OUT}  week {week}  weeks_done={weeks_done}  coverage={json.dumps(out['coverage'])}", file=sys.stderr)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--week", type=int, required=True, help="the week you are setting a lineup for")
    ap.add_argument("--fetch", action="store_true", help="download fresh source files first")
    ap.add_argument("--raw", type=Path, default=None, help="directory holding the source CSVs (default data/raw/inseason)")
    a = ap.parse_args()
    global RAW
    if a.raw:
        RAW = a.raw
    build(a.week, a.fetch)


if __name__ == "__main__":
    main()
