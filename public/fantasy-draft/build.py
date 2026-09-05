#!/usr/bin/env python3
"""Build the scored player dataset for the Fourth Pick War Room app.

Inputs (all under ./data):
  rankings.json        26 ranking sources + 22 ADP feeds per player (see research/rankings_sources.md)
  risk.json            boom / bust / injury signals per player (see research/risk_sources.md)
  byes.json            team -> 2026 bye week
  adjustments.json     hand-curated 2026 context nudges (see research/context.md)
  strategy.json        the pick-4 plan rendered on the Plan tab
  model.json           prose + source list rendered on the Model tab
  raw/espn_projections_2026.csv, raw/cbs_projections_2026.csv   stat-line projections (PPR points computed here)
  raw/ffanalytics_projections_2026.csv                          floor / ceiling / uncertainty / age (standard scoring; used as ratios only)

Outputs:
  data/players.json    the scored dataset
  index.html           the JSON is injected into <script id="data">

Run:  python3 build.py

The model follows research/methodology.md:
  composite   outlet-grouped weighted mean of expert ranks (FantasyPros ECR counts double; stale or
              market-driven lists count half)
  tiers       new tier when the cumulative drop since the tier began exceeds the position's median
              cross-source spread (ffanalytics tier rule)
  value       ADP minus composite in picks, plus a log-space score 50 + 50*tanh(ln(ADP/rank)/ln 2)
  boom/bust   weighted raw signals converted to a within-position percentile (0-100)
  risk        expert spread, ADP spread, ffanalytics uncertainty, injury, camp and situation -> percentile
  VBD         PPR projection minus the 10-team replacement baseline (QB10 / RB22 / WR28 / TE10)
"""
import csv
import json
import math
import re
import statistics
import unicodedata
from datetime import date
from pathlib import Path

import situation

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"

# ---------------------------------------------------------------------------
# Tunables
# ---------------------------------------------------------------------------
# Ranking sources are grouped by outlet so one publisher never counts twice.
OUTLETS = {
    "fantasypros_ecr": ["fantasypros_ecr"],
    "espn": ["espn_ppr300", "espn_draft_rank", "espn_rank_aug24", "espn_live_ppr_rank"],
    "yahoo": ["yahoo_winks", "yahoo_boone"],
    "rotowire": ["rotowire_consensus", "rotowire_rank"],
    "rotoballer": ["rotoballer"],
    "draftsharks": ["draftsharks"],
    "flock": ["flock_consensus"],
    "nbc_rotoworld": ["nbc_rotoworld"],
    "lineupexperts": ["lineupexperts"],
    "fftoday": ["fftoday_krueger"],
    "prizepicks": ["prizepicks_hardy"],
    "bleacher_report": ["bleacher_report"],
    "etr": ["etr_auction_rank"],
    "bdge": ["bdge_top50"],
    "subvertadown": ["subvertadown"],
    "sleeper_rank": ["sleeper_rank"],
    "fantasylife_jul": ["fantasylife_consensus_jul28", "fantasylife_berry_jul28"],
    "fourfor4_jul": ["fourfor4_jul27"],
    "cbs_aug3": ["cbs_aug3"],
}
OUTLET_WEIGHT = {
    "fantasypros_ecr": 1.0,   # was 2.0; the backtest found ECR no more predictive than ADP and many outlets feed it (herding)
    "sleeper_rank": 0.5,      # platform default order, largely ADP-driven
    "subvertadown": 0.5,      # value-model board, not an analyst list
    "bdge": 0.5,              # top-50 only
    "etr": 0.75,              # derived from auction values
    "fantasylife_jul": 0.5,   # July snapshot
    "fourfor4_jul": 0.5,      # July snapshot
    "cbs_aug3": 0.5,          # early-August snapshot
    "lineupexperts": 0.75, "fftoday": 0.75, "prizepicks": 0.75, "bleacher_report": 0.75,
}
# ADP feeds: full-PPR redraft platforms count 1, other formats or older snapshots count less.
ADP_WEIGHT = {
    "espn_live": 3.0, "ffc_sep4": 1.0, "sleeper_live": 0.75, "fantasypros_live": 0.75, "yahoo_live": 0.5,   # Sept 4 feeds; the league drafts on ESPN
    "sleeper_ppr": 0.5, "nfc_ppr": 0.5, "espn": 0.25, "yahoo": 0.25, "fantasypros_avg": 0.5,
    "fantasypros_cbs": 0.5, "fantasypros_rtsports": 0.5, "fantasypros_fantrax": 0.5, "fantasypros_espn": 0.25, "fantasypros_sleeper": 0.25,
    "underdog": 0.5, "rotowire_underdog": 0.25, "ffpc": 0.5, "draftsharks_half_consensus": 0.5,
    "sleeper_aug29": 0.5, "yahoo_aug25": 0.5, "nfc_ppr_aug28": 0.5,
    "udk_avg_pick": 0.5, "udk_sleeper_pick": 0.25, "udk_espn_pick": 0.25, "udk_yahoo_pick": 0.25, "udk_underdog_pick": 0.25,
}
ADP_PLATFORMS = ["ffc_sep4", "espn_live", "sleeper_live", "fantasypros_live", "yahoo_live", "underdog", "ffpc", "fantasypros_cbs", "fantasypros_rtsports", "fantasypros_fantrax", "draftsharks_half_consensus"]

# Re-weighted after the 2016-2025 backtest (research/BACKTEST.md): expert spread and age are the strongest bust
# predictors, ADP-vs-ECR value helps boom for receivers, prior-year weekly volatility does not predict busts,
# and prior-year boom/bust-week rates are weak.
W = {
    "boom": {"upside": 0.15, "ceiling": 0.10, "hist_boom": 0.20, "mentions": 0.15, "factors": 0.10, "youth": 0.10, "value": 0.20},
    "bust": {"downside": 0.15, "floor": 0.10, "hist_bust": 0.10, "mentions": 0.20, "factors": 0.15, "age": 0.15, "reach": 0.0, "injury": 0.15},
    "risk": {"spread": 0.30, "adp_spread": 0.10, "uncertainty": 0.10, "consistency": 0.05, "injury": 0.20, "camp": 0.10, "situation": 0.15},
}
BASELINE = {"QB": 10, "RB": 22, "WR": 28, "TE": 10}          # 10-team VOLS + flex split
AGE_CLIFF = {"RB": (28, 29), "WR": (29, 31), "TE": (30, 32), "QB": (34, 36)}  # (at, past); RB moved 27 -> 28 per the backtest (age-28 RBs: hit 38%, bust 54%, PPG -3.3)
YOUTH = {"RB": [(23, 1.0), (24, 0.85), (25, 0.6), (26, 0.3)], "WR": [(23, 1.0), (24, 0.85), (25, 0.65), (26, 0.4), (27, 0.2)],
         "TE": [(24, 1.0), (25, 0.8), (26, 0.5), (27, 0.25)], "QB": [(25, 0.8), (27, 0.5), (29, 0.2)]}
INJURY_PRIOR = {"RB": 0.40, "WR": 0.35, "TE": 0.35, "QB": 0.25}   # position base rates when nothing is known
INJ_LABEL = [("out for season", 1.0), ("out for year", 1.0), ("highest", 1.0), ("very high", 1.0), ("moderate-high", 0.7),
             ("high", 0.8), ("low-moderate", 0.35), ("moderate", 0.5), ("elevated", 0.65), ("medium", 0.5), ("average", 0.4),
             ("out", 0.9), ("suspension", 0.6), ("injured", 0.6), ("flagged", 0.55), ("very low", 0.1), ("low", 0.2)]
# (regex, score, flag) — first match wins
CAMP = [(r"\bhealthy\b|no reported", 0.0, None), (r"out for (the )?(season|year)", 1.0, "Out"), (r"exempt", 1.0, "Exempt"),
        (r"suspend", 1.0, "Suspended"), (r"\bpup\b", 1.0, "PUP"), (r"\bir\b|injured reserve", 1.0, "IR"),
        (r"out (at least|the first|first|\d+ games|\d+\+)", 1.0, "Out"), (r"holdout|holding out", 0.8, "Holdout"),
        (r"uncertain|50/50|questionable|doubtful", 0.65, "Questionable"), (r"sprain|fracture|surgery|injured", 0.6, "Injured"),
        (r"minor", 0.5, None), (r"healing|returning from|rehab|recover", 0.4, None), (r"managed|tightness|soreness", 0.3, None)]
SITUATION_WORDS = ["rookie", "new team", "new qb", "new oc", "new coach", "new offense", "new hc", "committee", "timeshare", "split",
                   "contract", "holdout", "suspend", "trade", "co-starter", "competition"]


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def clamp(x, lo=0.0, hi=1.0):
    return max(lo, min(hi, x))


def norm_name(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = s.lower().replace("'", "").replace(".", "").replace("-", " ")
    s = re.sub(r"\b(jr|sr|ii|iii|iv|v)\b", "", s)
    return re.sub(r"\s+", " ", s).strip()


def load(name, default):
    p = DATA / name
    if not p.exists():
        print(f"  ! {name} missing, using default")
        return default
    with p.open() as f:
        return json.load(f)


def saturate(n, k=3.0):
    """0..1, rising with count but never flat: 1 -> .28, 3 -> .63, 5 -> .81, 10 -> .96"""
    return 1.0 - math.exp(-n / k)


def keyword_score(text, table, default):
    s = (text or "").lower()
    for k, v in table:
        if k in s:
            return v
    return default


def camp_status(text):
    """-> (score 0..1, flag or None) from free-text camp status."""
    s = (text or "").lower()
    if not s:
        return 0.0, None
    # drop negated mentions such as "avoided PUP", "off IR", "activated from PUP"
    s = re.sub(r"(avoided|avoid|off|not on|removed from|activated from|came off|cleared from|out of|no)\s+(the\s+)?(pup|ir|injured reserve|exempt list)\b", "", s)
    for pat, v, flag in CAMP:
        if re.search(pat, s):
            return v, flag
    return 0.3, None


def youth_bonus(pos, age):
    if age is None:
        return 0.0
    for a, b in YOUTH.get(pos, []):
        if age <= a:
            return b
    return 0.0


def age_flag(pos, age):
    if age is None or pos not in AGE_CLIFF:
        return 0.0
    at, past = AGE_CLIFF[pos]
    return 1.0 if age >= past else 0.5 if age >= at else 0.0


def wmean(pairs):
    tw = sum(w for _, w in pairs)
    return sum(v * w for v, w in pairs) / tw if tw else None


def wstdev(pairs):
    m = wmean(pairs)
    tw = sum(w for _, w in pairs)
    return math.sqrt(sum(w * (v - m) ** 2 for v, w in pairs) / tw) if tw and len(pairs) > 1 else 0.0


def percentile_within(players, key_fn, pos):
    """Percent rank (0-100) of key_fn(p) among players at the same position."""
    vals = sorted(key_fn(p) for p in players if p["pos"] == pos)
    n = len(vals)

    def pct(v):
        below = sum(1 for x in vals if x < v)
        equal = sum(1 for x in vals if x == v)
        return 100.0 * (below + 0.5 * equal) / n if n else 50.0
    return pct


# ---------------------------------------------------------------------------
# projections
# ---------------------------------------------------------------------------
REC_W = {"ppr": 1.0, "half": 0.5, "std": 0.0}   # points per reception by scoring format
FORMATS = ("ppr", "half", "std")


def stat_points(st, w):
    """Fantasy points from a stat line with reception weight w (ESPN scoring: 25 pass yds, 4 pass TD, -2 INT, 10 yds, 6 TD, -2 fumble)."""
    g = lambda k: float(st.get(k) or 0)
    return (g("passYds") / 25 + g("passTD") * 4 - g("ints") * 2 + g("rushYds") / 10 + g("rushTD") * 6
            + g("rec") * w + g("recYds") / 10 + g("recTD") * 6 - g("fum") * 2)


def load_projections():
    """Stat lines from the CBS (and older ESPN) exports: {(name, pos): {src: stats}}."""
    out = {}
    for src, fname in (("espn", "espn_projections_2026.csv"), ("cbs", "cbs_projections_2026.csv")):
        p = DATA / "raw" / fname
        if not p.exists():
            continue
        with p.open() as f:
            for r in csv.DictReader(f):
                r["pos"] = (r["pos"] or "").split(",")[0].strip()
                if r["pos"] not in ("QB", "RB", "WR", "TE"):
                    continue
                if not any(r.get(k) for k in ("pass_yds", "rush_yds", "reception_yds")):
                    continue
                g = lambda k: float(r.get(k) or 0)
                out.setdefault((norm_name(r["name"]), r["pos"]), {})[src] = {"passYds": g("pass_yds"), "passTD": g("pass_tds"), "ints": g("pass_ints"), "rushYds": g("rush_yds"), "rushTD": g("rush_tds"),
                                                                             "rec": g("receptions"), "recYds": g("reception_yds"), "recTD": g("reception_tds"), "fum": g("fumbles")}
    return out


def load_ffa():
    out = {}
    p = DATA / "raw" / "ffanalytics_projections_2026.csv"
    if not p.exists():
        return out
    with p.open() as f:
        for r in csv.DictReader(f):
            pos = r["Position Bucket"]
            if pos not in ("QB", "RB", "WR", "TE"):
                continue
            try:
                pts = float(r["Points"])
                fl, ce = float(r["Floor"]), float(r["Ceiling"])
                unc = float(r["Uncertainty"]) if r["Uncertainty"] else None
                age = int(float(r["Age"])) if r["Age"] else None
            except ValueError:
                continue
            if pts <= 0:
                continue
            out[(norm_name(r["Player"]), pos)] = {"ceil_ratio": ce / pts, "floor_ratio": fl / pts, "uncertainty": unc, "age": age,
                                                  "sd_ratio": (float(r["SD"]) / pts) if r["SD"] else None}
    return out


# ---------------------------------------------------------------------------
def build(scoring="ppr", mc_tag=""):
    w_rec = REC_W[scoring]
    rankings = load("rankings.json", [])
    risk = load("risk.json", [])
    byes = load("byes.json", {})
    adjustments = load("adjustments.json", {})
    strategy = load("strategy.json", {})
    model = load("model.json", {})
    proj = load_projections()
    ffa = load_ffa()
    team_env = {r["team"]: r for r in load("team_env.json", [])} if (DATA / "team_env.json").exists() else {}
    sos = load("sos.json", {}).get("teams", {}) if (DATA / "sos.json").exists() else {}
    opp_rows = load("opportunity.json", []) if (DATA / "opportunity.json").exists() else []
    opp_by = {}
    for o in opp_rows:
        opp_by[norm_name(o["name"]) + "|" + (o.get("pos") or "").upper()] = o
    used_opp = set()
    mkt = load("market_features.json", {})
    mkt_players = mkt.get("players", {})
    mkt_teams = mkt.get("teams", {})
    NEW_HC_2026 = {"ARI", "ATL", "BAL", "BUF", "CLE", "LV", "MIA", "NYG", "PIT", "TEN"}   # research/context.md
    TEAMS32 = set(byes)
    for t, m in mkt_teams.items():
        if t not in TEAMS32:
            continue
        row = team_env.setdefault(t, {"team": t})
        cz = m.get("census") or {}
        row.setdefault("hc", cz.get("head_coach") or m.get("hcListed"))
        row.setdefault("oc", cz.get("offensive_coordinator"))
        row.setdefault("playcaller", cz.get("play_caller"))
        row.setdefault("playcaller_evidence", cz.get("evidence_summary"))
        row.setdefault("hc_new", t in NEW_HC_2026)
        if row.get("vegas_wins") is None:
            row["vegas_wins"] = m.get("vegasWins") if m.get("vegasWins") is not None else m.get("dkWins")
        if row.get("oline_rank") is None:
            row["oline_rank"] = m.get("olineRank")
    league_env = situation.team_env_scores(team_env) if team_env else {"implied": [], "wins": [], "oline": []}
    nfl = load("nflverse_features.json", {})
    nfl_players = nfl.get("players", {})
    nfl_teams = nfl.get("teams", {})
    team_changes, status_conflicts = [], []

    risk_by = {norm_name(r["name"]): r for r in risk}
    adj_by = {norm_name(k): v for k, v in adjustments.items() if not k.startswith("_")}
    used_risk, used_adj, used_proj = set(), set(), 0

    players = []
    for r in rankings:
        raw_ranks = {k: v for k, v in (r.get("ranks") or {}).items() if v is not None and not k.endswith("_posrank")}
        if not raw_ranks:
            continue
        pos = r["pos"].upper()
        key = norm_name(r["name"])
        rk = risk_by.get(key, {})
        ad = adj_by.get(key, {})
        fa = ffa.get((key, pos), {})
        pj = proj.get((key, pos), {})
        used_risk.add(key) if rk else None
        used_adj.add(key) if ad else None
        used_proj += 1 if pj else 0
        nv = nfl_players.get(key + "|" + pos, {})
        team_code = r["team"]
        if nv.get("team_2026") and nv["team_2026"] != team_code and nv.get("roster_status") in ("ACT", "RES", "EXE"):
            team_changes.append(f"{r['name']}: {team_code} -> {nv['team_2026']}")
            team_code = nv["team_2026"]
        s25 = nv.get("s2025") or {}
        s24 = nv.get("s2024") or {}
        games_missed = None
        if s25 or s24:
            games_missed = (17 - s25["games"] if s25 else 17) + ((17 - s24["games"]) if s24 else 0) if (s25 and not nv.get("rookie")) else None
            if s25 and not s24:
                games_missed = 17 - s25["games"]
        tctx = nfl_teams.get(team_code, {})

        # --- composite: average inside each outlet, then weighted across outlets ------------
        mk_early = mkt_players.get(key + "|" + pos, {})
        if (mk_early.get("espn") or {}).get("pprRank"):
            raw_ranks = dict(raw_ranks, espn_live_ppr_rank=mk_early["espn"]["pprRank"])
        outlet_ranks = {}
        for outlet, keys in OUTLETS.items():
            vals = [raw_ranks[k] for k in keys if k in raw_ranks]
            if vals:
                outlet_ranks[outlet] = round(statistics.mean(vals), 1)
        pairs = [(v, OUTLET_WEIGHT.get(o, 1.0)) for o, v in outlet_ranks.items()]
        comp = wmean(pairs)
        sd = wstdev(pairs)
        meta = r.get("meta") or {}
        best = min([min(outlet_ranks.values())] + ([meta["fantasypros_best"]] if meta.get("fantasypros_best") else []))
        worst = max([max(outlet_ranks.values())] + ([meta["fantasypros_worst"]] if meta.get("fantasypros_worst") else []))

        # --- ADP ------------------------------------------------------------------------------
        mk = mkt_players.get(key + "|" + pos, {})
        adps = {}
        if (mk.get("espn") or {}).get("adp"):
            adps["espn_live"] = mk["espn"]["adp"]          # ESPN leagues of every format; the league's own room
        if scoring == "ppr":
            if mk.get("ffc"):
                adps["ffc_sep4"] = mk["ffc"]["adp"]
            if (mk.get("sleeperAdp") or {}).get("latest"):
                adps["sleeper_live"] = mk["sleeperAdp"]["latest"]
            for src, dst in (("fantasypros", "fantasypros_live"), ("yahoo", "yahoo_live")):
                a = (mk.get("adpLatest") or {}).get(src)
                if a and a.get("adp") and a.get("date", "") >= "2026-09-01":
                    adps[dst] = a["adp"]
            for k, v in (r.get("adp") or {}).items():
                if v is None:
                    continue
                if k == "draftsharks_half_consensus":      # feed is round.pick for a 12-team draft, e.g. 6.2 = round 6, pick 2
                    rd, pk = divmod(round(v * 10), 10)
                    v = (rd - 1) * 12 + (pk if pk else 10)
                if v > 300:                                # undrafted placeholders (701, 3054 ...)
                    continue
                adps[k] = v
            fresh = {"ffc_sep4", "espn_live", "sleeper_live", "fantasypros_live", "yahoo_live"}
            n_fresh = sum(1 for k in adps if k in fresh)
            # when three or more Sept 4 feeds exist, the older feeds add lag, not information
            adp_pairs = [(v, ADP_WEIGHT.get(k, 0.25) * (0.1 if (n_fresh >= 3 and k not in fresh) else 1.0)) for k, v in adps.items()]
            ffc_row = mk.get("ffc")
        else:
            ffc_key, sl_key = ("ffcHalf", "adpHalf") if scoring == "half" else ("ffcStd", "adpStd")
            ffc_row = mk.get(ffc_key)
            if ffc_row:
                adps["ffc_" + scoring] = ffc_row["adp"]
            if (mk.get("sleeper") or {}).get(sl_key):
                adps["sleeper_" + scoring] = mk["sleeper"][sl_key]
            if scoring == "half":
                a = (mk.get("adpLatest") or {}).get("yahoo")     # Yahoo defaults to half PPR
                if a and a.get("adp") and a.get("date", "") >= "2026-09-01":
                    adps["yahoo_live"] = a["adp"]
                for k in ("underdog", "draftsharks_half_consensus"):
                    v = (r.get("adp") or {}).get(k)
                    if v is not None and k == "draftsharks_half_consensus":
                        rd, pk = divmod(round(v * 10), 10); v = (rd - 1) * 12 + (pk if pk else 10)
                    if v is not None and v <= 300:
                        adps[k] = v
            fmt_w = {"espn_live": 2.0, "ffc_" + scoring: 1.5, "sleeper_" + scoring: 1.5, "yahoo_live": 1.0, "underdog": 1.0, "draftsharks_half_consensus": 0.5}
            adp_pairs = [(v, fmt_w.get(k, 0.1)) for k, v in adps.items()]
        adp = wmean(adp_pairs)
        plat = [adps[k] for k in (ADP_PLATFORMS if scoring == "ppr" else list(adps)) if k in adps]
        adp_sd = statistics.pstdev(plat) if len(plat) > 1 else None
        ffc_sd = (ffc_row or {}).get("stdev")
        if ffc_sd is not None and ((ffc_row or {}).get("n") or 0) >= 50:
            adp_sd = round(max(ffc_sd, 0.5 * (adp_sd or 0)), 1)   # within-draft spread from FFC drafts, floored by half the cross-site spread
        trend = mk.get("adpTrend") or {}
        adp_d7, adp_d30 = trend.get("d7"), trend.get("d30")
        value = (adp - comp) if adp is not None else None
        value_score = 50 + 50 * math.tanh(math.log(adp / comp) / math.log(2)) if adp else None

        # --- projections / VBD ----------------------------------------------------------------
        stat_lines = dict(pj)                                   # cbs (+ older espn export)
        if (mk.get("espn") or {}).get("stats"):
            stat_lines["espn"] = mk["espn"]["stats"]            # live Sept 4 file replaces the older ESPN export
        if (mk.get("sleeper") or {}).get("stats"):
            stat_lines["sleeper"] = mk["sleeper"]["stats"]
        pj = {src: round(stat_points(st, w_rec), 1) for src, st in stat_lines.items()}
        pj_ppr = {src: round(stat_points(st, 1.0), 1) for src, st in stat_lines.items()}
        bayes = dict(mk.get("bayes") or {})
        if bayes.get("p50"):
            pj_ppr["bayes"] = bayes["p50"]
            if scoring != "ppr" and bayes.get("recEst") is not None and bayes["p50"] > 0:
                shift = (1.0 - w_rec) * bayes["recEst"]
                ratio = max(0.0, (bayes["p50"] - shift) / bayes["p50"])
                bayes = dict(bayes, p50=round(bayes["p50"] - shift, 1), p10=round(bayes["p10"] * ratio, 1), p90=round(bayes["p90"] * ratio, 1))
            pj["bayes"] = bayes["p50"]
        proj_pts = statistics.mean(pj.values()) if pj else None
        proj_ppr = statistics.mean(pj_ppr.values()) if pj_ppr else None
        proj_sd = statistics.pstdev(pj.values()) if len(pj) > 1 else None
        lh = mk.get("lhallee") or {}
        espn = mk.get("espn") or {}
        ep = mk.get("ep2025") or {}

        age = nv.get("age") or rk.get("age") or fa.get("age") or r.get("age")

        # --- signals --------------------------------------------------------------------------
        boom_mentions = (rk.get("boom_mentions") or []) + (rk.get("sleeper_mentions") or [])
        pre = "Before the move: " if nv.get("moved") else ""   # article notes for traded / signed players describe the old team
        boom_factors = [pre + f for f in (rk.get("boom_factors") or [])] + list(ad.get("boom_factors") or [])
        bust_mentions = rk.get("bust_mentions") or []
        risk_factors = [pre + f for f in (rk.get("risk_factors") or [])] + list(ad.get("risk_factors") or [])
        pct = rk.get("injury_risk_pct")
        inj_parts = []
        if pct is not None:
            inj_parts.append(clamp(pct / 60.0))
        elif rk.get("injury_risk_label"):
            ls = keyword_score(rk["injury_risk_label"], INJ_LABEL, None)
            if ls is not None:
                inj_parts.append(ls)
        if rk.get("games_missed_last3") is not None:
            inj_parts.append(clamp(rk["games_missed_last3"] / 18.0))
        if games_missed is not None and not nv.get("rookie"):
            inj_parts.append(clamp(games_missed / 12.0))
        if lh.get("injProb") is not None:
            inj_parts += [clamp((lh["injProb"] - 0.15) / 0.55)] * 2   # calibrated missed-time probability (AUC 0.75) counts double
        if mk.get("gamesOut2425"):
            inj_parts.append(clamp(mk["gamesOut2425"] / 12.0))
        injury = sum(inj_parts) / len(inj_parts) if inj_parts else None
        ESPN_STATUS = {"OUT": 1.0, "INJURY_RESERVE": 1.0, "SUSPENSION": 1.0, "DOUBTFUL": 0.8, "QUESTIONABLE": 0.6, "DAY_TO_DAY": 0.4}
        espn_camp = ESPN_STATUS.get(str(espn.get("injuryStatus") or "").upper(), 0.0)
        if ep.get("diffPct") is not None and ep["diffPct"] >= 0.15 and ep["games"] >= 10:
            risk_factors.append(f"Scored {ep['diffPct']:.0%} above expected fantasy points in 2025 (touchdown / efficiency regression risk)")
        elif ep.get("diffPct") is not None and ep["diffPct"] <= -0.12 and ep["games"] >= 10:
            boom_factors.append(f"Scored {-ep['diffPct']:.0%} below expected fantasy points in 2025 (positive regression candidate)")
        if bayes.get("games") is not None and bayes["games"] < 12 and not nv.get("rookie"):
            risk_factors.append(f"Bayesian model projects only {bayes['games']:.1f} games")
        if adp_d7 is not None and adp_d7 >= 8:
            risk_factors.append(f"ADP fell {adp_d7:.0f} picks in the last week (market reacting to news)")
        elif adp_d7 is not None and adp_d7 <= -8:
            boom_factors.append(f"ADP rose {-adp_d7:.0f} picks in the last week (market buying)")
        camp_text = ad.get("camp_status") or rk.get("camp_status")   # hand-curated context (newer, cross-checked) wins over article snippets
        camp, camp_flag = camp_status(camp_text)
        if espn_camp > camp and not (nv.get("status_code") == "A01" and espn_camp >= 1.0):
            camp = max(camp, espn_camp)
            camp_text = camp_text or f"ESPN status: {espn.get('injuryStatus')}"
        roster_flag = nv.get("status_flag")
        if roster_flag in ("Exempt", "IR", "PUP", "NFI", "Holdout", "Retired"):
            camp, camp_flag = 1.0, roster_flag
            camp_text = "Week 1 roster: " + nv.get("availability", roster_flag)
        elif nv.get("status_code") == "A01" and camp >= 0.8:
            status_conflicts.append(f"{r['name']}: adjustments say '{camp_text}' but the Week 1 roster lists him active")
            camp, camp_flag = 0.4, None
            camp_text = "Listed active on the Week 1 roster; earlier reports said " + (ad.get("camp_status") or rk.get("camp_status") or "")
            ad = dict(ad, bust_adj=0.0, flag=None)
        if nv.get("status_code") == "A01":
            # percentile ranking amplifies hand nudges; for players the roster confirms active, cap them
            ad = dict(ad, boom_adj=max(-0.05, min(0.05, ad.get("boom_adj", 0))), bust_adj=max(-0.05, min(0.05, ad.get("bust_adj", 0))), risk_adj=max(-0.05, min(0.05, ad.get("risk_adj", 0))))   # roster is authoritative: drop the reported-out flag
        if pos in ("WR", "TE") and (tctx.get("vacated_target_share") or 0) >= 0.25:
            boom_factors.append(f"{team_code} vacated {tctx['vacated_target_share'] * 100:.0f}% of its 2025 targets ({tctx['vacated_targets']})")
        if pos == "RB" and (tctx.get("vacated_carry_share") or 0) >= 0.30:
            boom_factors.append(f"{team_code} vacated {tctx['vacated_carry_share'] * 100:.0f}% of its 2025 carries ({tctx['vacated_carries']})")
        if nv.get("rookie"):
            risk_factors.append("Rookie: no NFL usage history")
            if nv.get("draft_number") and nv["draft_number"] <= 32:
                boom_factors.append(f"First-round draft capital (pick {nv['draft_number']})")
        if nv.get("moved"):
            risk_factors.append(f"New team in 2026 ({nv.get('team_2025')} to {team_code}): backs and receivers who changed teams busted 7-8 points more often, 2016-25")
        if pos == "RB" and s25 and s25.get("games", 0) >= 12 and s25.get("total") and s25.get("total") >= 0:
            pass
        if pos == "RB" and nv.get("s2025") and (nv["s2025"].get("ppg") or 0) >= 18 and (nv["s2025"].get("games") or 0) >= 12:
            risk_factors.append("Coming off an elite RB season: prior-year top-3 RBs repeated a top-3 finish 23% of the time and lost 4.5 PPG on average, 2016-25")
        sit = [f for f in risk_factors if any(w in f.lower() for w in SITUATION_WORDS)]

        opp_row = opp_by.get(key + "|" + pos)
        if opp_row:
            used_opp.add(key + "|" + pos)
        sit_raw, sit_parts, sit_why, env_block, chg_block, sos_block, sit_uncertain = situation.compute(
            pos, team_code, team_env.get(team_code), opp_row, sos.get(team_code), tctx, league_env,
            arrival=bool(nv.get("moved")), rookie=bool(nv.get("rookie")), draft_no=nv.get("draft_number"), years_exp=nv.get("years_exp"))
        if ad.get("clear_uncertain"):
            sit_uncertain = False
        if sit_uncertain:
            risk_factors.append("2026 role unresolved: " + (opp_row.get("note") or "competition or scheme still unsettled"))
            sit = [f for f in risk_factors if any(w in f.lower() for w in SITUATION_WORDS)]
        if chg_block and (chg_block.get("coaching") or 0) != 0:
            sit.append("coaching change")
        players.append({
            "id": key.replace(" ", "-") + "-" + pos.lower(),
            "chg": chg_block, "sos": sos_block, "sitWhy": sit_why, "sitParts": sit_parts,
            "name": r["name"], "team": team_code, "pos": pos,
            "bye": byes.get(team_code) or r.get("bye") or "?",
            "age": age,
            "comp": round(comp, 1), "n": len(outlet_ranks), "nRaw": len(raw_ranks), "best": best, "worst": worst, "sd": round(sd, 1),
            "sources": outlet_ranks, "ecrAvg": meta.get("fantasypros_ecr_avg"),
            "adp": round(adp, 1) if adp is not None else None, "adpN": len(adps), "adpSd": round(adp_sd, 1) if adp_sd is not None else None,
            "adpSources": {k: adps[k] for k in ADP_PLATFORMS if k in adps} or None,
            "value": round(value, 1) if value is not None else None, "valueScore": round(value_score) if value_score is not None else None,
            "proj": round(proj_pts) if proj_pts is not None else None, "projSources": pj or None, "projSd": round(proj_sd, 1) if proj_sd is not None else None,
            "ceilPts": round(bayes["p90"]) if bayes.get("p90") else (round(proj_pts * fa["ceil_ratio"]) if proj_pts and fa.get("ceil_ratio") else None),
            "floorPts": round(bayes["p10"]) if bayes.get("p10") is not None else (round(proj_pts * fa["floor_ratio"]) if proj_pts and fa.get("floor_ratio") else None),
            "espnAdp": espn.get("adp"), "espnRank": espn.get("pprRank"),
            "market": {"adpD7": adp_d7, "adpD30": adp_d30, "ffcSd": ffc_sd, "ffcN": (mk.get("ffc") or {}).get("n"), "ffcRange": [mk["ffc"]["high"], mk["ffc"]["low"]] if mk.get("ffc") else None,
                       "espnStatus": espn.get("injuryStatus"), "espnOwned": espn.get("pctOwned"), "injProb": lh.get("injProb"), "projGames": bayes.get("games"),
                       "epDiff": ep.get("diffPct"), "injuryLog": mk.get("injuryLog")} if mk else None,
            "hist": {
                "games25": s25.get("games"), "ppg25": s25.get("ppg"), "boom25": s25.get("boom_rate"), "bust25": s25.get("bust_rate"), "cv25": s25.get("cv"),
                "targets25": s25.get("targets"), "tgtShare25": s25.get("target_share"), "carries25": s25.get("carries"), "carryShare25": s25.get("carry_share"),
                "games24": s24.get("games"), "ppg24": s24.get("ppg"), "boomRate": nv.get("boom_rate"), "bustRate": nv.get("bust_rate"), "gamesMissed": games_missed,
                "rookie": nv.get("rookie"), "draftNo": nv.get("draft_number"), "rosterStatus": nv.get("availability"),
            } if nv else None,
            "teamCtx": {"vacTgtShare": tctx.get("vacated_target_share"), "vacCarShare": tctx.get("vacated_carry_share"), "vacTgt": tctx.get("vacated_targets"), "vacCar": tctx.get("vacated_carries"), "departed": tctx.get("departed"), "unavailable": tctx.get("unavailable")} if tctx else None,
            "_sig": {
                "sitRaw": sit_raw, "sitUncertain": sit_uncertain,
                "histBoom": (nv.get("rates_by_format", {}).get(scoring) or {}).get("boom_rate", nv.get("boom_rate")) if scoring != "ppr" else nv.get("boom_rate"),
                "histBust": (nv.get("rates_by_format", {}).get(scoring) or {}).get("bust_rate", nv.get("bust_rate")) if scoring != "ppr" else nv.get("bust_rate"),
                "projPpr": proj_ppr,
                "cv": s25.get("cv") if s25 and s25.get("games", 0) >= 6 else None,
                "upside": (comp - best) / comp, "downside": (worst - comp) / comp,
                "ceil": (bayes["p90"] / bayes["p50"] - 1.0) if bayes.get("p50") and bayes.get("p90") else ((fa.get("ceil_ratio") or 1.0) - 1.0),
                "floor": (1.0 - bayes["p10"] / bayes["p50"]) if bayes.get("p50") and bayes.get("p10") is not None else (1.0 - (fa.get("floor_ratio") or 1.0)),
                "boomMentions": boom_mentions, "boomFactors": boom_factors, "bustMentions": bust_mentions, "riskFactors": risk_factors,
                "injury": injury, "camp": camp, "campText": camp_text, "sit": sit,
                "uncertainty": fa.get("uncertainty"), "spread": sd / comp, "adpSpread": (adp_sd / adp) if adp and adp_sd is not None else None,
                "boomAdj": ad.get("boom_adj", 0), "bustAdj": ad.get("bust_adj", 0), "riskAdj": ad.get("risk_adj", 0),
                "note": ad.get("note") or rk.get("notes"), "flag": ad.get("flag") or camp_flag,
            },
        })

    if scoring != "ppr":
        # Expert ranks are full PPR. Shift each player's composite by how his projection rank moves under this
        # format (70% credited), so backs rise and target-heavy receivers / tight ends fall in half and standard.
        have = [p for p in players if p["proj"] is not None and p["_sig"].get("projPpr") is not None]
        # value over the positional baseline in each format, so the shift respects scarcity (the WR baseline drops too)
        def vbd_map(key):
            out = {}
            for pos in ("QB", "RB", "WR", "TE"):
                g = sorted((p for p in have if p["pos"] == pos), key=lambda p: -(p[key] if key == "proj" else p["_sig"][key]))
                base = (g[BASELINE[pos] - 1][key] if key == "proj" else g[BASELINE[pos] - 1]["_sig"][key]) if len(g) >= BASELINE[pos] else 0
                for p in g:
                    out[p["id"]] = (p[key] if key == "proj" else p["_sig"][key]) - base
            return out
        v_fmt, v_ppr = vbd_map("proj"), vbd_map("projPpr")
        order_fmt = {pid: i for i, pid in enumerate(sorted(v_fmt, key=lambda k: -v_fmt[k]), 1)}
        order_ppr = {pid: i for i, pid in enumerate(sorted(v_ppr, key=lambda k: -v_ppr[k]), 1)}
        for p in have:
            delta = 0.5 * (order_fmt[p["id"]] - order_ppr[p["id"]])
            p["comp"] = round(max(1.0, p["comp"] + delta), 1)
            p["value"] = round(p["adp"] - p["comp"], 1) if p["adp"] is not None else None
            p["valueScore"] = round(50 + 50 * math.tanh(math.log(p["adp"] / p["comp"]) / math.log(2))) if p["adp"] else None
            p["_sig"]["upside"] = (p["comp"] - p["best"]) / p["comp"]
            p["_sig"]["downside"] = (p["worst"] - p["comp"]) / p["comp"]
            p["_sig"]["spread"] = p["sd"] / p["comp"]
    players.sort(key=lambda p: p["comp"])

    # --- positional rank, VBD baselines, tiers ---------------------------------------------
    for pos in ("QB", "RB", "WR", "TE"):
        group = [p for p in players if p["pos"] == pos]
        projs = sorted((p["proj"] for p in group if p["proj"] is not None), reverse=True)
        base = projs[BASELINE[pos] - 1] if len(projs) >= BASELINE[pos] else (projs[-1] if projs else 0)
        tier, start, prev = 1, None, None
        for i, p in enumerate(group, 1):
            p["posRank"] = i
            p["vbd"] = round(p["proj"] - base) if p["proj"] is not None else None
            # local spread: median sd of the neighbours (+-5 positional ranks), so tiers widen
            # deeper in the draft where experts disagree more
            nb = group[max(0, i - 6): i + 5]
            T = max(3.0, statistics.median(q["sd"] for q in nb))
            if start is not None and (p["comp"] - start > T or p["comp"] - prev > 0.75 * T):
                tier += 1
                start = p["comp"]
            if start is None:
                start = p["comp"]
            p["tier"] = tier
            prev = p["comp"]

    # --- within-position percentiles for the skewed signals --------------------------------
    for pos in ("QB", "RB", "WR", "TE"):
        pct_up = percentile_within(players, lambda p: p["_sig"]["upside"], pos)
        pct_dn = percentile_within(players, lambda p: p["_sig"]["downside"], pos)
        pct_ce = percentile_within(players, lambda p: p["_sig"]["ceil"], pos)
        pct_fl = percentile_within(players, lambda p: p["_sig"]["floor"], pos)
        pct_sp = percentile_within(players, lambda p: p["_sig"]["spread"], pos)
        pct_hb = percentile_within([p for p in players if p["_sig"]["histBoom"] is not None], lambda p: p["_sig"]["histBoom"], pos)
        pct_hu = percentile_within([p for p in players if p["_sig"]["histBust"] is not None], lambda p: p["_sig"]["histBust"], pos)
        pct_cv = percentile_within([p for p in players if p["_sig"]["cv"] is not None], lambda p: p["_sig"]["cv"], pos)
        pct_sit = percentile_within(players, lambda p: p["_sig"]["sitRaw"], pos)
        pct_as = percentile_within([p for p in players if p["_sig"]["adpSpread"] is not None], lambda p: p["_sig"]["adpSpread"], pos)
        for p in players:
            if p["pos"] != pos:
                continue
            s = p["_sig"]
            bw, uw, rw = W["boom"], W["bust"], W["risk"]
            hb = pct_hb(s["histBoom"]) / 100 if s["histBoom"] is not None else 0.5
            hu = pct_hu(s["histBust"]) / 100 if s["histBust"] is not None else 0.5
            cvp = pct_cv(s["cv"]) / 100 if s["cv"] is not None else 0.5
            sit_up = max(0.0, s["sitRaw"]) + 0.5 * (p["sitParts"].get("variance") or 0.0); sit_dn = max(0.0, -s["sitRaw"]) + 0.5 * (p["sitParts"].get("variance") or 0.0)
            boom_raw = (0.12 * sit_up / 0.5) + (bw["upside"] * pct_up(s["upside"]) / 100 + bw["ceiling"] * pct_ce(s["ceil"]) / 100 + bw["hist_boom"] * hb
                        + bw["mentions"] * saturate(len(s["boomMentions"])) + bw["factors"] * saturate(len(s["boomFactors"]))
                        + bw["youth"] * youth_bonus(pos, p["age"]) + bw["value"] * clamp((p["value"] or 0) / 10.0) + s["boomAdj"])
            inj = s["injury"] if s["injury"] is not None else INJURY_PRIOR[pos]
            bust_raw = (0.12 * sit_dn / 0.5) + (uw["downside"] * pct_dn(s["downside"]) / 100 + uw["floor"] * pct_fl(s["floor"]) / 100 + uw["hist_bust"] * hu
                        + uw["mentions"] * saturate(len(s["bustMentions"])) + uw["factors"] * saturate(len(s["riskFactors"]))
                        + uw["age"] * age_flag(pos, p["age"]) + uw["reach"] * clamp(-(p["value"] or 0) / 10.0) + uw["injury"] * inj + s["bustAdj"])
            unc = (s["uncertainty"] / 100.0) if s["uncertainty"] is not None else 0.5
            adp_sp = pct_as(s["adpSpread"]) / 100 if s["adpSpread"] is not None else 0.5
            risk_raw = (0.10 * (1.0 if s["sitUncertain"] else 0.0)) + (rw["spread"] * pct_sp(s["spread"]) / 100 + rw["adp_spread"] * adp_sp + rw["uncertainty"] * unc + rw["consistency"] * cvp
                        + rw["injury"] * inj + rw["camp"] * s["camp"] + rw["situation"] * saturate(len(s["sit"]), 2.0) + s["riskAdj"])
            p["_raw"] = {"boom": boom_raw, "bust": bust_raw, "risk": risk_raw}
        pb = percentile_within([p for p in players if p["pos"] == pos], lambda p: p["_raw"]["boom"], pos)
        pu = percentile_within([p for p in players if p["pos"] == pos], lambda p: p["_raw"]["bust"], pos)
        pr = percentile_within([p for p in players if p["pos"] == pos], lambda p: p["_raw"]["risk"], pos)
        for p in players:
            if p["pos"] == pos:
                p["sit"] = round(max(1, min(99, 50 + 100 * p["_sig"]["sitRaw"])))   # linear, 50 = neutral; raw is capped at +-0.35 so the score spans 15-85
                p["boom"] = round(pb(p["_raw"]["boom"]))
                p["bust"] = round(pu(p["_raw"]["bust"]))
                p["risk"] = round(pr(p["_raw"]["risk"]))

    # --- explanations + flags ---------------------------------------------------------------
    for p in players:
        s = p["_sig"]
        comp, best, worst = p["comp"], p["best"], p["worst"]
        why_b = []
        if (comp - best) / comp >= 0.25 and comp - best >= 3:
            why_b.append(f"Most bullish source has him #{int(best)}, {comp - best:.0f} spots above the composite")
        if p["ceilPts"] and p["proj"] and p["ceilPts"] - p["proj"] >= 0.08 * p["proj"]:
            why_b.append(f"Ceiling {p['ceilPts']} pts vs {p['proj']} projected" + (" (Bayesian p90)" if (p.get("market") or {}).get("projGames") else " (ffanalytics)"))
        if p["hist"] and p["hist"]["boomRate"] is not None and p["hist"]["games25"]:
            why_b.append(f"Boom weeks (top-{ {'QB': 3, 'RB': 6, 'WR': 6, 'TE': 3}[p['pos']]} scoring) in {p['hist']['boomRate'] * 100:.0f}% of games, 2024-25 weighted")
        if s["boomMentions"]:
            why_b.append("Breakout/sleeper pick by " + ", ".join(s["boomMentions"][:4]))
        why_b += s["boomFactors"]
        if youth_bonus(p["pos"], p["age"]) >= 0.6:
            why_b.append(f"Age {p['age']}: still on the ascending side of the curve")
        if p["value"] is not None and p["value"] >= 3:
            why_b.append(f"Market lets him fall {p['value']:.0f} picks past his composite rank")

        why_u = []
        if worst >= 250 and comp < 150:
            why_u.append("Some experts leave him off their boards entirely")
        elif (worst - comp) / comp >= 0.25 and worst - comp >= 3:
            why_u.append(f"Most bearish source has him #{int(worst)}, {worst - comp:.0f} spots below the composite")
        if p["floorPts"] is not None and p["proj"] and p["proj"] - p["floorPts"] >= 0.10 * p["proj"]:
            why_u.append(f"Floor {p['floorPts']} pts vs {p['proj']} projected" + (" (Bayesian p10)" if (p.get("market") or {}).get("projGames") else " (ffanalytics)"))
        if p["hist"] and p["hist"]["bustRate"] is not None and p["hist"]["games25"]:
            why_u.append(f"Bust weeks (below the startable line) in {p['hist']['bustRate'] * 100:.0f}% of games, 2024-25 weighted")
        if s["bustMentions"]:
            why_u.append("On bust/avoid lists from " + ", ".join(s["bustMentions"][:4]))
        why_u += s["riskFactors"]
        if age_flag(p["pos"], p["age"]) >= 0.5:
            why_u.append(f"Age {p['age']}: at or past the historical {p['pos']} decline point")
        if p["value"] is not None and p["value"] <= -3:
            why_u.append(f"Market drafts him {-p['value']:.0f} picks earlier than his composite rank")

        why_r = []
        if p["sd"] >= 0.25 * comp and p["sd"] >= 2:
            why_r.append(f"Sources disagree: ±{p['sd']:.1f} places (#{int(best)} to #{int(worst)})")
        if p["adpSd"] is not None and p["adp"] and p["adpSd"] >= 0.2 * p["adp"] and p["adpSd"] >= 2:
            why_r.append(f"Platforms disagree on ADP: ±{p['adpSd']:.1f} picks")
        if s["uncertainty"] is not None and s["uncertainty"] >= 60:
            why_r.append(f"ffanalytics projection uncertainty {s['uncertainty']:.0f}/99")
        rk = risk_by.get(norm_name(p["name"]), {})
        mkb = p.get("market") or {}
        if mkb.get("injProb") is not None:
            why_r.append(f"Calibrated injury model: {mkb['injProb']:.0%} chance of missing time (AUC 0.75)")
        if mkb.get("ffcSd") is not None and mkb.get("ffcN"):
            why_r.append(f"Drafted anywhere from pick {mkb['ffcRange'][0]} to {mkb['ffcRange'][1]} across {mkb['ffcN']} FFC drafts (±{mkb['ffcSd']})")
        if rk.get("injury_risk_pct") is not None:
            why_r.append(f"Injury model: {rk['injury_risk_pct']:.0f}% chance of missing time")
        elif rk.get("injury_risk_label"):
            why_r.append("Injury risk: " + rk["injury_risk_label"])
        if p["hist"] and p["hist"]["gamesMissed"]:
            why_r.append(f"Missed {p['hist']['gamesMissed']} regular-season games in 2024-25")
        elif rk.get("games_missed_last3"):
            why_r.append(f"Missed {rk['games_missed_last3']} games over the last three seasons")
        if s["cv"] is not None and s["cv"] >= 0.6:
            why_r.append(f"Week-to-week swing: 2025 scores varied ±{s['cv'] * 100:.0f}% of his average")
        if s["camp"] >= 0.4:
            why_r.append("Status: " + s["campText"])
        if s["sit"]:
            why_r.append("Situation: " + "; ".join(s["sit"][:3]))

        flag = None
        big = max(6.0, 0.20 * comp)  # a 6-pick gap matters at pick 20, not at pick 120
        if s["flag"] and s["camp"] >= 0.6:
            flag = s["flag"]
        elif (p.get("market") or {}).get("adpD7") is not None and abs(p["market"]["adpD7"]) >= max(8, 0.12 * comp) and comp <= 150:
            flag = "Falling" if p["market"]["adpD7"] > 0 else "Rising"
        elif p["value"] is not None and p["value"] >= big and comp <= 170:
            flag = "Value"
        elif p["value"] is not None and p["value"] <= -big and comp <= 170 and (p["adp"] or 999) < 160:
            flag = "Reach"
        elif s["flag"]:
            flag = s["flag"]

        p.update({"boomWhy": why_b[:5], "bustWhy": why_u[:5], "riskWhy": why_r[:5], "flag": flag, "note": s["note"]})

    # --- report -------------------------------------------------------------------------------
    print(f"players scored: {len(players)}   with projections: {used_proj}   with risk signals: {len(used_risk)}/{len(risk)}   with adjustments: {len(used_adj)}/{len(adj_by)}")
    print("unmatched risk rows:", sorted(set(risk_by) - used_risk))
    print("nflverse matched:", sum(1 for p in players if p["hist"]), "of", len(players), "| team changes from Week 1 roster:", team_changes)
    print("status conflicts (roster active vs reported out):", status_conflicts)
    print(f"situation inputs: team_env {len(team_env)} teams, sos {len(sos)} teams, opportunity rows matched {len(used_opp)}/{len(opp_by)}")
    if opp_by:
        print("unmatched opportunity rows:", sorted(set(opp_by) - used_opp)[:15])
    print("unmatched adjustments:", sorted(set(adj_by) - used_adj))
    counts = {}
    for p in players:
        for k in p["sources"]:
            counts[k] = counts.get(k, 0) + 1
        for k in (p["adpSources"] or {}):
            counts["adp_" + k] = counts.get("adp_" + k, 0) + 1
        for k in (p["projSources"] or {}):
            counts["proj_" + k] = counts.get("proj_" + k, 0) + 1
        if p["ceilPts"] is not None:
            counts["ffa"] = counts.get("ffa", 0) + 1
        if norm_name(p["name"]) in used_risk:
            counts["risk"] = counts.get("risk", 0) + 1
        if norm_name(p["name"]) in used_adj:
            counts["context"] = counts.get("context", 0) + 1
        if p.get("hist"):
            counts["nflverse"] = counts.get("nflverse", 0) + 1
        if p.get("sos"):
            counts["sos"] = counts.get("sos", 0) + 1
        if team_env.get(p["team"]):
            counts["team_env"] = counts.get("team_env", 0) + 1
        if p.get("chg"):
            counts["opportunity"] = counts.get("opportunity", 0) + 1
        mkb = p.get("market") or {}
        if mkb.get("injProb") is not None:
            counts["lhallee"] = counts.get("lhallee", 0) + 1
        if mkb.get("epDiff") is not None:
            counts["ffopportunity"] = counts.get("ffopportunity", 0) + 1
        if team_env.get(p["team"], {}).get("playcaller"):
            counts["census"] = counts.get("census", 0) + 1
        if team_env.get(p["team"], {}).get("vegas_wins") is not None:
            counts["vegas"] = counts.get("vegas", 0) + 1
    for s in model.get("sources", []):
        if s.get("key") in counts:
            s["count"] = counts[s["key"]]
    for pos in ("QB", "RB", "WR", "TE"):
        g = [p for p in players if p["pos"] == pos]
        print(f"{pos}: {len(g)} players, tiers {max(p['tier'] for p in g)}, top: " + ", ".join(f"{p['name']} {p['comp']}" for p in g[:5]))

    mc_path = HERE / "scenarios" / f"montecarlo_avail{mc_tag}.json"
    mc = json.loads(mc_path.read_text()) if mc_path.exists() else None
    if mc:
        for p in players:
            if p["id"] in mc["players"]:
                p["mcAvail"] = mc["players"][p["id"]]
        print(f"monte carlo availability attached for {sum(1 for p in players if p.get('mcAvail'))} players ({mc['sims']} sims, {mc['room']} room, slot {mc['slot']})")
    out = {
        "players": [{k: v for k, v in p.items() if not k.startswith("_")} for p in players],
        "strategy": strategy,
        "meta": {
            "updated": date.today().isoformat(),
            "sourceNames": model.get("sourceNames", {}),
            "adpNames": model.get("adpNames", {}),
            "sources": model.get("sources", []),
            "unavailable": model.get("unavailable", []),
            "model": {"intro": model.get("intro", ""), "sections": model.get("sections", [])},
            "weights": W, "situationWeights": situation.SW, "outletWeights": OUTLET_WEIGHT, "baselines": BASELINE,
            "mc": {"teams": mc["teams"], "slot": mc["slot"], "room": mc["room"], "sims": mc["sims"], "picks": mc["picks"], "generated": mc["generated"], "strategies": mc.get("strategies"), "best": mc.get("best"), "first": mc.get("first"), "rounds": mc.get("rounds")} if mc else None,
            "teams": {t: {"hc": r.get("hc"), "hcNew": r.get("hc_new"), "oc": r.get("oc"), "ocNew": r.get("oc_new"), "playcaller": r.get("playcaller"), "scheme": r.get("scheme_notes"),
                          "passRate": r.get("pass_rate_tendency"), "pace": r.get("pace_tendency"), "rbUsage": r.get("rb_usage"), "qb": r.get("qb"), "qbNew": r.get("qb_new"), "qbTier": r.get("qb_tier"),
                          "qbNote": r.get("qb_note"), "vegasWins": r.get("vegas_wins"), "impliedPpg": r.get("implied_ppg"), "olineRank": r.get("oline_rank"), "arrivals": r.get("arrivals"),
                          "departures": r.get("departures"), "verdict": r.get("env_verdict"), "bye": byes.get(t)} for t, r in team_env.items()},
        },
    }
    (DATA / f"players_{scoring}.json").write_text(json.dumps(out["players"], indent=1))
    return out


OVERLAY_FIELDS = ("comp", "adp", "adpSd", "adpSources", "value", "valueScore", "proj", "projSources", "vbd", "floorPts", "ceilPts",
                  "boom", "bust", "risk", "sit", "tier", "posRank", "flag", "mcAvail", "boomWhy", "bustWhy", "riskWhy")


def main():
    outs = {}
    for fmt in FORMATS:
        print(f"=== scoring format: {fmt}")
        outs[fmt] = build(fmt, "" if fmt == "ppr" else "_" + fmt)
    base = outs["ppr"]
    by_id = {fmt: {p["id"]: p for p in outs[fmt]["players"]} for fmt in FORMATS}
    for p in base["players"]:
        p["alt"] = {fmt: {k: by_id[fmt][p["id"]].get(k) for k in OVERLAY_FIELDS} for fmt in ("half", "std") if p["id"] in by_id[fmt]}
    base["meta"]["scoring"] = {"base": "ppr", "formats": list(FORMATS), "recWeights": REC_W,
                               "mc": {fmt: outs[fmt]["meta"].get("mc") for fmt in FORMATS}}
    (DATA / "players.json").write_text(json.dumps([{k: v for k, v in p.items() if k != "alt"} for p in base["players"]], indent=1))

    html_path = HERE / "index.html"
    html = html_path.read_text()
    blob = json.dumps(base, separators=(",", ":")).replace("</", "<\\/")
    new_html, n = re.subn(r'(<script id="data" type="application/json">)(.*?)(</script>)', lambda m: m.group(1) + "\n" + blob + "\n" + m.group(3), html, flags=re.S)
    assert n == 1, "data script block not found"
    html_path.write_text(new_html)
    print(f"wrote index.html ({len(new_html) // 1024} KB) with half / standard overlays")


if __name__ == "__main__":
    main()
