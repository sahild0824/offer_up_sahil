#!/usr/bin/env python3
"""Derive per-player and per-team features from nflverse data (2024-2025 stats, 2026 rosters).

Produces data/nflverse_features.json with:
  players[<norm name>|<pos>] : age, team_2026, roster_status, draft capital, 2025 and 2024 usage,
                               weekly PPR boom / bust rates (FantasyPros thresholds), consistency
  teams[<team>]              : 2025 team volume, vacated targets / carries (departed and unavailable)
  defense[<team>][<pos>]     : 2025 PPR points allowed per game by position (schedule strength input)
  thresholds                 : the weekly boom / bust cut-offs that were used

Source files (GitHub release assets, downloadable with --fetch):
  https://github.com/nflverse/nflverse-data/releases/download/stats_player/stats_player_week_2025.csv
  .../stats_player/stats_player_week_2024.csv   .../stats_team/stats_team_reg_2025.csv
  .../players/players.csv   .../rosters/roster_2026.csv

Boom / bust follow FantasyPros' Boom-or-Bust report: a boom week scores at least the average weekly
score of the positional RB6 / WR6 / QB3 / TE3; a bust week scores at or below the weekly RB40 / WR56 /
QB18 / TE18. Two-season rates weight 2025 at 0.65 and 2024 at 0.35 (see research/methodology.md).
"""
import csv
import json
import re
import statistics
import sys
import unicodedata
import urllib.request
from collections import defaultdict
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAW = HERE / "data" / "raw" / "nflverse"
OUT = HERE / "data" / "nflverse_features.json"
BASE = "https://github.com/nflverse/nflverse-data/releases/download/"
FILES = {
    "stats_player_week_2025.csv": "stats_player/stats_player_week_2025.csv",
    "stats_player_week_2024.csv": "stats_player/stats_player_week_2024.csv",
    "stats_team_reg_2025.csv": "stats_team/stats_team_reg_2025.csv",
    "players.csv": "players/players.csv",
    "roster_2026.csv": "rosters/roster_2026.csv",
}
TEAM_FIX = {"LA": "LAR", "JAC": "JAX", "WSH": "WAS", "OAK": "LV", "SD": "LAC", "STL": "LAR"}
POS = ("QB", "RB", "WR", "TE")
BOOM_SLOT = {"QB": 3, "RB": 6, "WR": 6, "TE": 3}
BUST_SLOT = {"QB": 18, "RB": 40, "WR": 56, "TE": 18}
ROSTER_STATUS = {  # NFL status_description_abbr -> (availability label, flag)
    "A01": ("active", None), "E02": ("exempt list", "Exempt"), "R01": ("injured reserve", "IR"), "R48": ("injured reserve, designated to return", "IR"),
    "R04": ("reserve/PUP", "PUP"), "R05": ("non-football injury list", "NFI"), "R02": ("retired", "Retired"), "R03": ("did not report", "Holdout"),
    "W03": ("waived", "Cut"), "P01": ("practice squad", "PS"), "P06": ("practice squad (injured)", "PS"), "P07": ("practice squad (exception)", "PS"),
}


def norm_name(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode()
    s = s.lower().replace("'", "").replace(".", "").replace("-", " ")
    s = re.sub(r"\b(jr|sr|ii|iii|iv|v)\b", "", s)
    return re.sub(r"\s+", " ", s).strip()


def team(t):
    return TEAM_FIX.get(t, t)


def fetch():
    RAW.mkdir(parents=True, exist_ok=True)
    for name, path in FILES.items():
        dest = RAW / name
        if dest.exists():
            continue
        print("downloading", name)
        urllib.request.urlretrieve(BASE + path, dest)


def load_csv(name):
    with (RAW / name).open(newline="") as f:
        return list(csv.DictReader(f))


def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def season_features(rows, year):
    """rows = weekly player stats for one season. Returns per-player dict and thresholds."""
    reg = [r for r in rows if r["season_type"] == "REG" and r["position"] in POS]
    # weekly positional cut-offs
    by_week = defaultdict(lambda: defaultdict(list))
    for r in reg:
        by_week[int(r["week"])][r["position"]].append(num(r["fantasy_points_ppr"]))
    thr = {}
    for pos in POS:
        booms, busts = [], []
        for wk, d in by_week.items():
            pts = sorted(d[pos], reverse=True)
            if len(pts) >= BUST_SLOT[pos]:
                booms.append(pts[BOOM_SLOT[pos] - 1])
                busts.append(pts[BUST_SLOT[pos] - 1])
        thr[pos] = {"boom": round(statistics.mean(booms), 1), "bust": round(statistics.mean(busts), 1)}
    # team volume per week for shares
    team_wk = defaultdict(lambda: defaultdict(float))
    for r in reg:
        t = team(r["team"])
        team_wk[(t, int(r["week"]))]["targets"] += num(r["targets"])
        team_wk[(t, int(r["week"]))]["carries"] += num(r["carries"])
    players = {}
    for r in reg:
        if num(r["targets"]) + num(r["carries"]) + num(r["attempts"]) == 0:
            continue  # did not play
        key = (r["player_id"], r["position"])
        p = players.setdefault(key, {"name": r["player_display_name"], "pos": r["position"], "team": team(r["team"]), "weeks": [], "targets": 0, "carries": 0, "receptions": 0,
                                     "rec_yds": 0, "rush_yds": 0, "tds": 0, "team_targets": 0, "team_carries": 0, "pass_att": 0, "rush_att": 0})
        pts = num(r["fantasy_points_ppr"])
        p["weeks"].append(pts)
        p["team"] = team(r["team"])  # last team of the season
        p["targets"] += num(r["targets"]); p["carries"] += num(r["carries"]); p["receptions"] += num(r["receptions"])
        p["rec_yds"] += num(r["receiving_yards"]); p["rush_yds"] += num(r["rushing_yards"])
        p["tds"] += num(r["rushing_tds"]) + num(r["receiving_tds"]) + num(r["passing_tds"])
        p["pass_att"] += num(r["attempts"])
        tw = team_wk[(team(r["team"]), int(r["week"]))]
        p["team_targets"] += tw["targets"]; p["team_carries"] += tw["carries"]
    out = {}
    for (pid, pos), p in players.items():
        w = p["weeks"]
        g = len(w)
        boom = sum(1 for x in w if x >= thr[pos]["boom"]) / g
        bust = sum(1 for x in w if x <= thr[pos]["bust"]) / g
        mean = statistics.mean(w)
        sd = statistics.pstdev(w) if g > 1 else 0.0
        out[(pid, pos)] = {
            "name": p["name"], "pos": pos, "team": p["team"], "games": g, "ppg": round(mean, 1), "total": round(sum(w), 1),
            "boom_rate": round(boom, 3), "bust_rate": round(bust, 3), "weekly_sd": round(sd, 1), "cv": round(sd / mean, 3) if mean > 0 else None,
            "targets": int(p["targets"]), "target_share": round(p["targets"] / p["team_targets"], 3) if p["team_targets"] else None,
            "carries": int(p["carries"]), "carry_share": round(p["carries"] / p["team_carries"], 3) if p["team_carries"] else None,
            "receptions": int(p["receptions"]), "rec_yds": int(p["rec_yds"]), "rush_yds": int(p["rush_yds"]), "tds": int(p["tds"]), "pass_att": int(p["pass_att"]),
            "year": year,
        }
    return out, thr


def defense_allowed(rows):
    """PPR points allowed per game by defense x position (REG season)."""
    acc = defaultdict(lambda: defaultdict(float))
    games = defaultdict(set)
    for r in rows:
        if r["season_type"] != "REG" or r["position"] not in POS:
            continue
        opp = team(r["opponent_team"])
        acc[opp][r["position"]] += num(r["fantasy_points_ppr"])
        games[opp].add(r["game_id"])
    return {t: {pos: round(acc[t][pos] / len(games[t]), 1) for pos in POS} for t in acc if games[t]}


def main():
    if "--fetch" in sys.argv or not all((RAW / n).exists() for n in FILES):
        fetch()
    wk25 = load_csv("stats_player_week_2025.csv")
    wk24 = load_csv("stats_player_week_2024.csv")
    players_csv = load_csv("players.csv")
    roster = load_csv("roster_2026.csv")
    team_reg = load_csv("stats_team_reg_2025.csv")

    f25, thr25 = season_features(wk25, 2025)
    f24, thr24 = season_features(wk24, 2024)
    defense = defense_allowed(wk25)

    # players.csv: birth dates and draft capital by gsis_id
    info = {}
    for r in players_csv:
        info[r["gsis_id"]] = r
    # 2026 roster by gsis_id (week 1)
    ros = {}
    for r in roster:
        if r["position"] in POS or r["depth_chart_position"] in POS:
            ros[r["gsis_id"]] = r

    today = date(2026, 9, 1)

    def age_of(r):
        bd = r.get("birth_date")
        if not bd:
            return None
        y, m, d = (int(x) for x in bd.split("-"))
        return today.year - y - ((today.month, today.day) < (m, d))

    # --- per player ------------------------------------------------------------------------
    players = {}
    ids = set(k[0] for k in f25) | set(k[0] for k in f24) | set(ros)
    for pid in ids:
        r26 = ros.get(pid)
        s25 = next((v for (i, p), v in f25.items() if i == pid), None)
        s24 = next((v for (i, p), v in f24.items() if i == pid), None)
        meta = info.get(pid, {})
        pos = (r26 or {}).get("position") or (s25 or s24 or {}).get("pos") or meta.get("position")
        if pos not in POS:
            continue
        name = (r26 or {}).get("full_name") or (s25 or s24 or {}).get("name") or meta.get("display_name")
        if not name:
            continue
        key = norm_name(name) + "|" + pos
        if s25 and s24:
            boom = 0.65 * s25["boom_rate"] + 0.35 * s24["boom_rate"]
            bust = 0.65 * s25["bust_rate"] + 0.35 * s24["bust_rate"]
        else:
            boom = (s25 or s24 or {}).get("boom_rate")
            bust = (s25 or s24 or {}).get("bust_rate")
        status_code = (r26 or {}).get("status_description_abbr")
        avail, flag = ROSTER_STATUS.get(status_code, (None, None))
        draft_no = (r26 or {}).get("draft_number") or ""
        players[key] = {
            "name": name, "pos": pos, "gsis_id": pid,
            "age": age_of(r26 or meta) if (r26 or meta) else None,
            "team_2026": team((r26 or {}).get("team")) if r26 else None,
            "team_2025": (s25 or {}).get("team"),
            "moved": bool(r26 and s25 and team(r26["team"]) != s25["team"]),
            "roster_status": (r26 or {}).get("status"), "status_code": status_code, "availability": avail, "status_flag": flag,
            "years_exp": int((r26 or {}).get("years_exp") or 0) if r26 else None,
            "rookie": bool(r26 and (r26.get("years_exp") or "0") == "0"),
            "draft_number": int(draft_no) if draft_no.isdigit() else None,
            "s2025": s25, "s2024": s24,
            "boom_rate": round(boom, 3) if boom is not None else None,
            "bust_rate": round(bust, 3) if bust is not None else None,
        }

    # --- per team: 2025 volume and 2026 vacated volume ---------------------------------------
    teams = {}
    tr = {team(r["team"]): r for r in team_reg}
    for t in sorted(set(v["team"] for v in f25.values())):
        row = tr.get(t, {})
        vac_t_dep = vac_c_dep = vac_t_un = vac_c_un = tot_t = tot_c = 0
        departed, unavailable = [], []
        for (pid, pos), s in f25.items():
            if s["team"] != t:
                continue
            tot_t += s["targets"]; tot_c += s["carries"]
            r26 = ros.get(pid)
            now = team(r26["team"]) if r26 else None
            code = (r26 or {}).get("status_description_abbr")
            if now != t:
                vac_t_dep += s["targets"]; vac_c_dep += s["carries"]
                if s["targets"] >= 20 or s["carries"] >= 40:
                    departed.append(f"{s['name']} ({s['targets']} tgt, {s['carries']} car)")
            elif code and code != "A01":
                vac_t_un += s["targets"]; vac_c_un += s["carries"]
                if s["targets"] >= 20 or s["carries"] >= 40:
                    unavailable.append(f"{s['name']} ({ROSTER_STATUS.get(code, (code,))[0]}; {s['targets']} tgt, {s['carries']} car)")
        teams[t] = {
            "targets_2025": tot_t, "carries_2025": tot_c,
            "pass_att_2025": int(num(row.get("attempts"))), "rush_att_2025": int(num(row.get("carries"))),
            "vacated_targets": vac_t_dep, "vacated_carries": vac_c_dep, "unavailable_targets": vac_t_un, "unavailable_carries": vac_c_un,
            "vacated_target_share": round(vac_t_dep / tot_t, 3) if tot_t else None, "vacated_carry_share": round(vac_c_dep / tot_c, 3) if tot_c else None,
            "departed": departed[:8], "unavailable": unavailable[:6],
        }

    out = {"generated": date.today().isoformat(), "thresholds": {"2025": thr25, "2024": thr24}, "players": players, "teams": teams, "defense_ppr_allowed_2025": defense}
    OUT.write_text(json.dumps(out, indent=0))
    print(f"players {len(players)}  teams {len(teams)}  defenses {len(defense)}")
    print("weekly thresholds 2025:", thr25)
    print("wrote", OUT.relative_to(HERE), f"({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
