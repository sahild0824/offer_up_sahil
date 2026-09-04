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

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"

# ---------------------------------------------------------------------------
# Tunables
# ---------------------------------------------------------------------------
# Ranking sources are grouped by outlet so one publisher never counts twice.
OUTLETS = {
    "fantasypros_ecr": ["fantasypros_ecr"],
    "espn": ["espn_ppr300", "espn_draft_rank", "espn_rank_aug24"],
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
    "fantasypros_ecr": 2.0,   # already a consensus of 100+ experts
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
    "sleeper_ppr": 1.0, "nfc_ppr": 1.0, "espn": 1.0, "yahoo": 1.0, "fantasypros_avg": 1.0,
    "fantasypros_cbs": 0.5, "fantasypros_rtsports": 0.5, "fantasypros_fantrax": 0.5, "fantasypros_espn": 0.25, "fantasypros_sleeper": 0.25,
    "underdog": 0.5, "rotowire_underdog": 0.25, "ffpc": 0.5, "draftsharks_half_consensus": 0.5,
    "sleeper_aug29": 0.5, "yahoo_aug25": 0.5, "nfc_ppr_aug28": 0.5,
    "udk_avg_pick": 0.5, "udk_sleeper_pick": 0.25, "udk_espn_pick": 0.25, "udk_yahoo_pick": 0.25, "udk_underdog_pick": 0.25,
}
ADP_PLATFORMS = ["sleeper_ppr", "nfc_ppr", "espn", "yahoo", "underdog", "ffpc", "fantasypros_cbs", "fantasypros_rtsports", "fantasypros_fantrax", "draftsharks_half_consensus"]

W = {
    "boom": {"upside": 0.25, "ceiling": 0.15, "mentions": 0.25, "factors": 0.15, "youth": 0.10, "value": 0.10},
    "bust": {"downside": 0.15, "floor": 0.10, "mentions": 0.25, "factors": 0.15, "age": 0.10, "reach": 0.10, "injury": 0.15},
    "risk": {"spread": 0.25, "adp_spread": 0.15, "uncertainty": 0.15, "injury": 0.25, "camp": 0.10, "situation": 0.10},
}
BASELINE = {"QB": 10, "RB": 22, "WR": 28, "TE": 10}          # 10-team VOLS + flex split
AGE_CLIFF = {"RB": (27, 29), "WR": (29, 31), "TE": (30, 32), "QB": (34, 36)}  # (at, past)
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
def ppr_points(r):
    g = lambda k: float(r.get(k) or 0)
    return (g("pass_yds") / 25 + g("pass_tds") * 4 - g("pass_ints") * 2 + g("rush_yds") / 10 + g("rush_tds") * 6
            + g("receptions") + g("reception_yds") / 10 + g("reception_tds") * 6 - g("fumbles") * 2)


def load_projections():
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
                out.setdefault((norm_name(r["name"]), r["pos"]), {})[src] = round(ppr_points(r), 1)
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
def main():
    rankings = load("rankings.json", [])
    risk = load("risk.json", [])
    byes = load("byes.json", {})
    adjustments = load("adjustments.json", {})
    strategy = load("strategy.json", {})
    model = load("model.json", {})
    proj = load_projections()
    ffa = load_ffa()

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

        # --- composite: average inside each outlet, then weighted across outlets ------------
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
        adps = {k: v for k, v in (r.get("adp") or {}).items() if v is not None}
        adp_pairs = [(v, ADP_WEIGHT.get(k, 0.25)) for k, v in adps.items()]
        adp = wmean(adp_pairs)
        plat = [adps[k] for k in ADP_PLATFORMS if k in adps]
        adp_sd = statistics.pstdev(plat) if len(plat) > 1 else None
        value = (adp - comp) if adp is not None else None
        value_score = 50 + 50 * math.tanh(math.log(adp / comp) / math.log(2)) if adp else None

        # --- projections / VBD ----------------------------------------------------------------
        proj_pts = statistics.mean(pj.values()) if pj else None
        proj_sd = statistics.pstdev(pj.values()) if len(pj) > 1 else None

        age = rk.get("age") or fa.get("age") or r.get("age")

        # --- signals --------------------------------------------------------------------------
        boom_mentions = (rk.get("boom_mentions") or []) + (rk.get("sleeper_mentions") or [])
        boom_factors = list(rk.get("boom_factors") or []) + list(ad.get("boom_factors") or [])
        bust_mentions = rk.get("bust_mentions") or []
        risk_factors = list(rk.get("risk_factors") or []) + list(ad.get("risk_factors") or [])
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
        injury = sum(inj_parts) / len(inj_parts) if inj_parts else None
        camp_text = rk.get("camp_status") or ad.get("camp_status")
        camp, camp_flag = camp_status(camp_text)
        sit = [f for f in risk_factors if any(w in f.lower() for w in SITUATION_WORDS)]

        players.append({
            "id": key.replace(" ", "-") + "-" + pos.lower(),
            "name": r["name"], "team": r["team"], "pos": pos,
            "bye": r.get("bye") or byes.get(r["team"]) or "?",
            "age": age,
            "comp": round(comp, 1), "n": len(outlet_ranks), "nRaw": len(raw_ranks), "best": best, "worst": worst, "sd": round(sd, 1),
            "sources": outlet_ranks, "ecrAvg": meta.get("fantasypros_ecr_avg"),
            "adp": round(adp, 1) if adp is not None else None, "adpN": len(adps), "adpSd": round(adp_sd, 1) if adp_sd is not None else None,
            "adpSources": {k: adps[k] for k in ADP_PLATFORMS if k in adps} or None,
            "value": round(value, 1) if value is not None else None, "valueScore": round(value_score) if value_score is not None else None,
            "proj": round(proj_pts) if proj_pts is not None else None, "projSources": pj or None, "projSd": round(proj_sd, 1) if proj_sd is not None else None,
            "ceilPts": round(proj_pts * fa["ceil_ratio"]) if proj_pts and fa.get("ceil_ratio") else None,
            "floorPts": round(proj_pts * fa["floor_ratio"]) if proj_pts and fa.get("floor_ratio") else None,
            "_sig": {
                "upside": (comp - best) / comp, "downside": (worst - comp) / comp,
                "ceil": (fa.get("ceil_ratio") or 1.0) - 1.0, "floor": 1.0 - (fa.get("floor_ratio") or 1.0),
                "boomMentions": boom_mentions, "boomFactors": boom_factors, "bustMentions": bust_mentions, "riskFactors": risk_factors,
                "injury": injury, "camp": camp, "campText": camp_text, "sit": sit,
                "uncertainty": fa.get("uncertainty"), "spread": sd / comp, "adpSpread": (adp_sd / adp) if adp and adp_sd is not None else None,
                "boomAdj": ad.get("boom_adj", 0), "bustAdj": ad.get("bust_adj", 0), "riskAdj": ad.get("risk_adj", 0),
                "note": ad.get("note") or rk.get("notes"), "flag": ad.get("flag") or camp_flag,
            },
        })

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
        pct_as = percentile_within([p for p in players if p["_sig"]["adpSpread"] is not None], lambda p: p["_sig"]["adpSpread"], pos)
        for p in players:
            if p["pos"] != pos:
                continue
            s = p["_sig"]
            bw, uw, rw = W["boom"], W["bust"], W["risk"]
            boom_raw = (bw["upside"] * pct_up(s["upside"]) / 100 + bw["ceiling"] * pct_ce(s["ceil"]) / 100
                        + bw["mentions"] * saturate(len(s["boomMentions"])) + bw["factors"] * saturate(len(s["boomFactors"]))
                        + bw["youth"] * youth_bonus(pos, p["age"]) + bw["value"] * clamp((p["value"] or 0) / 10.0) + s["boomAdj"])
            inj = s["injury"] if s["injury"] is not None else INJURY_PRIOR[pos]
            bust_raw = (uw["downside"] * pct_dn(s["downside"]) / 100 + uw["floor"] * pct_fl(s["floor"]) / 100
                        + uw["mentions"] * saturate(len(s["bustMentions"])) + uw["factors"] * saturate(len(s["riskFactors"]))
                        + uw["age"] * age_flag(pos, p["age"]) + uw["reach"] * clamp(-(p["value"] or 0) / 10.0) + uw["injury"] * inj + s["bustAdj"])
            unc = (s["uncertainty"] / 100.0) if s["uncertainty"] is not None else 0.5
            adp_sp = pct_as(s["adpSpread"]) / 100 if s["adpSpread"] is not None else 0.5
            risk_raw = (rw["spread"] * pct_sp(s["spread"]) / 100 + rw["adp_spread"] * adp_sp + rw["uncertainty"] * unc
                        + rw["injury"] * inj + rw["camp"] * s["camp"] + rw["situation"] * saturate(len(s["sit"]), 2.0) + s["riskAdj"])
            p["_raw"] = {"boom": boom_raw, "bust": bust_raw, "risk": risk_raw}
        pb = percentile_within([p for p in players if p["pos"] == pos], lambda p: p["_raw"]["boom"], pos)
        pu = percentile_within([p for p in players if p["pos"] == pos], lambda p: p["_raw"]["bust"], pos)
        pr = percentile_within([p for p in players if p["pos"] == pos], lambda p: p["_raw"]["risk"], pos)
        for p in players:
            if p["pos"] == pos:
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
            why_b.append(f"ffanalytics ceiling {p['ceilPts']} pts vs {p['proj']} projected")
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
        if p["floorPts"] and p["proj"] and p["proj"] - p["floorPts"] >= 0.10 * p["proj"]:
            why_u.append(f"ffanalytics floor {p['floorPts']} pts vs {p['proj']} projected")
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
        if rk.get("injury_risk_pct") is not None:
            why_r.append(f"Injury model: {rk['injury_risk_pct']:.0f}% chance of missing time")
        elif rk.get("injury_risk_label"):
            why_r.append("Injury risk: " + rk["injury_risk_label"])
        if rk.get("games_missed_last3"):
            why_r.append(f"Missed {rk['games_missed_last3']} games over the last three seasons")
        if s["camp"] >= 0.4:
            why_r.append("Status: " + s["campText"])
        if s["sit"]:
            why_r.append("Situation: " + "; ".join(s["sit"][:3]))

        flag = None
        big = max(5.0, 0.15 * comp)  # a 5-pick gap matters at pick 20, not at pick 120
        if s["flag"] and s["camp"] >= 0.6:
            flag = s["flag"]
        elif p["value"] is not None and p["value"] >= big:
            flag = "Value"
        elif p["value"] is not None and p["value"] <= -big:
            flag = "Reach"
        elif s["flag"]:
            flag = s["flag"]

        p.update({"boomWhy": why_b[:5], "bustWhy": why_u[:5], "riskWhy": why_r[:5], "flag": flag, "note": s["note"]})

    # --- report -------------------------------------------------------------------------------
    print(f"players scored: {len(players)}   with projections: {used_proj}   with risk signals: {len(used_risk)}/{len(risk)}   with adjustments: {len(used_adj)}/{len(adj_by)}")
    print("unmatched risk rows:", sorted(set(risk_by) - used_risk))
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
    for s in model.get("sources", []):
        if s.get("key") in counts:
            s["count"] = counts[s["key"]]
    for pos in ("QB", "RB", "WR", "TE"):
        g = [p for p in players if p["pos"] == pos]
        print(f"{pos}: {len(g)} players, tiers {max(p['tier'] for p in g)}, top: " + ", ".join(f"{p['name']} {p['comp']}" for p in g[:5]))

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
            "weights": W, "outletWeights": OUTLET_WEIGHT, "baselines": BASELINE,
        },
    }
    (DATA / "players.json").write_text(json.dumps(out["players"], indent=1))

    html_path = HERE / "index.html"
    html = html_path.read_text()
    blob = json.dumps(out, separators=(",", ":")).replace("</", "<\\/")
    new_html, n = re.subn(r'(<script id="data" type="application/json">)(.*?)(</script>)', lambda m: m.group(1) + "\n" + blob + "\n" + m.group(3), html, flags=re.S)
    assert n == 1, "data script block not found"
    html_path.write_text(new_html)
    print(f"wrote index.html ({len(new_html) // 1024} KB)")


if __name__ == "__main__":
    main()
