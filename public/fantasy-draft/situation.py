"""2026 situation layer: team environment, opportunity change, schedule.

Inputs (all optional; missing files degrade gracefully):
  data/team_env.json     per-team coaching, play-caller tendencies, QB tier, Vegas, O-line, arrivals/departures
  data/sos.json          per-team, per-position strength of schedule (full / early / playoffs) from nflverse 2024-25
  data/opportunity.json  per-player 2026 change drivers (opportunity, competition, QB, coaching, uncertainty)

compute(...) returns a raw situation score (roughly -1 .. +1), the explanation lines, and the display blocks.
The raw score is turned into a within-position percentile by build.py. Weights live in SW.

Design (see research/methods_2026.md): experts and ADP already price the headline moves, so the layer
does not move the composite rank. It widens or narrows the range of outcomes (boom / bust / risk) and
adds the pieces the market prices least: schedule (playoff weeks as a tiebreaker), vacated opportunity,
play-caller tendency and unresolved situations.
"""
import statistics

SW = {
    "env": 0.35,        # team offensive environment (Vegas, QB tier, O-line, play-caller tendency)
    "change": 0.35,     # 2026 opportunity / competition / QB / coaching change for the player
    "vacated": 0.15,    # share of 2025 volume the team vacated (data, nflverse)
    "schedule": 0.15,   # 0.4 full-season + 0.6 fantasy playoffs (weeks 15-17), both small by design
}
QB_TIER = {1: 0.6, 2: 0.25, 3: -0.1, 4: -0.5}
PASS_RATE = {"high": 1.0, "mid": 0.0, "low": -1.0}


def _z(value, values):
    vals = [v for v in values if v is not None]
    if value is None or len(vals) < 4:
        return 0.0
    m, sd = statistics.mean(vals), statistics.pstdev(vals)
    return (value - m) / sd if sd else 0.0


def _clamp(x, lo=-1.0, hi=1.0):
    return max(lo, min(hi, x))


def team_env_scores(team_env):
    """Pre-compute league z-scores for Vegas / implied points / O-line so each team's env is relative."""
    rows = list(team_env.values())
    return {
        "implied": [r.get("implied_ppg") for r in rows],
        "wins": [r.get("vegas_wins") for r in rows],
        "oline": [r.get("oline_rank") for r in rows],
    }


def compute(pos, team, env_row, opp_row, sos_row, team_ctx, league, arrival=False, rookie=False, draft_no=None, years_exp=None):
    """arrival / rookie / draft_no / years_exp come from the nflverse roster; they gate the evidence-based priors."""
    why, parts = [], {}
    env_row = env_row or {}
    opp_row = opp_row or {}
    sos_row = sos_row or {}
    team_ctx = team_ctx or {}

    # --- team environment ------------------------------------------------------------------
    e = 0.0
    if env_row:
        pts_z = _z(env_row.get("implied_ppg"), league["implied"]) if env_row.get("implied_ppg") is not None else _z(env_row.get("vegas_wins"), league["wins"])
        qb = QB_TIER.get(env_row.get("qb_tier"), 0.0)
        ol = -_z(env_row.get("oline_rank"), league["oline"]) if env_row.get("oline_rank") is not None else 0.0   # rank 1 = best
        pr_key = str(env_row.get("pass_rate_tendency") or "").split()[0].lower() if env_row.get("pass_rate_tendency") else ""
        pr = PASS_RATE.get(pr_key, 0.0)
        if pos in ("WR", "TE"):
            e = 0.40 * _clamp(pts_z / 2) + 0.35 * qb + 0.10 * _clamp(ol / 2) + 0.15 * pr
        elif pos == "RB":
            rb_use = {"bellcow": 0.4, "committee": -0.4}.get(str(env_row.get("rb_usage") or "").lower(), 0.0)
            e = 0.40 * _clamp(pts_z / 2) + 0.10 * qb + 0.25 * _clamp(ol / 2) - 0.10 * pr + 0.15 * rb_use
        else:  # QB: environment is weapons + O-line + pass volume
            e = 0.45 * _clamp(pts_z / 2) + 0.20 * _clamp(ol / 2) + 0.35 * pr
        parts["env"] = round(e, 2)
        if env_row.get("implied_ppg") is not None:
            why.append(f"Vegas implies {env_row['implied_ppg']:.1f} points per game" + (f" ({env_row['vegas_wins']} wins)" if env_row.get("vegas_wins") else ""))
        elif env_row.get("vegas_wins") is not None:
            why.append(f"Vegas win total {env_row['vegas_wins']}")
        if env_row.get("qb_note"):
            why.append(f"QB: {env_row['qb']} (tier {env_row.get('qb_tier')}) — {env_row['qb_note']}")
        if env_row.get("hc_new") or env_row.get("oc_new"):
            who = []
            if env_row.get("hc_new"):
                who.append(f"new HC {env_row.get('hc')}")
            if env_row.get("oc_new"):
                who.append(f"new OC {env_row.get('oc')}")
            why.append(", ".join(who) + (f": {env_row['scheme_notes']}" if env_row.get("scheme_notes") else ""))
        if env_row.get("oline_rank"):
            why.append(f"Offensive line ranked {env_row['oline_rank']} of 32")

    # --- opportunity / change --------------------------------------------------------------
    c = 0.0
    uncertain = bool(opp_row.get("uncertain"))
    if opp_row:
        o = opp_row.get("opportunity_change") or 0
        k = opp_row.get("competition_change") or 0
        q = opp_row.get("qb_change") or 0
        h = opp_row.get("coaching_change") or 0
        qb_w = {"WR": 0.5, "TE": 0.5, "RB": 0.25, "QB": 0.0}[pos]
        c = _clamp((0.5 * o + 0.25 * k + qb_w * q + 0.25 * h) / 2)
        parts["change"] = round(c, 2)
        for lab, v in (("Opportunity", o), ("Competition", k), ("QB change", q), ("Coaching change", h)):
            if v:
                why.append(f"{lab} {'+' if v > 0 else ''}{v}")
        why += list(opp_row.get("drivers") or [])[:3]
        if opp_row.get("proj_target_share_2026") is not None:
            why.append(f"Projected 2026 target share {opp_row['proj_target_share_2026']:.0%}")

    # --- vacated volume (nflverse) -----------------------------------------------------------
    # Evidence: vacated targets do not predict incumbents' growth (R^2 < 0.01, Dynasty Football Factory; ff-edge weight ~0),
    # but they matter for arrivals and for rookies with draft capital. So the opening only counts for those players.
    v = 0.0
    share = team_ctx.get("vacated_target_share" if pos in ("WR", "TE", "QB") else "vacated_carry_share")
    if share is not None and (arrival or (rookie and draft_no and draft_no <= 100)):
        v = _clamp((share - 0.2) / 0.25, 0.0, 1.0)   # 20% vacated is normal churn; 45% is a big opening
        parts["vacated"] = round(v, 2)
        if v > 0:
            why.append(f"Arrives into a room that vacated {share:.0%} of its 2025 {'targets' if pos != 'RB' else 'carries'}")

    # --- evidence-based priors (research/methods_2026.md) --------------------------------------
    prior = 0.0
    if pos in ("WR", "TE") and years_exp is not None:
        if years_exp == 1:
            prior += 0.15; why.append("Year-2 receiver: ~15% breakout base rate (RotoViz)")
        elif years_exp == 2:
            prior += 0.10; why.append("Year-3 receiver: ~10% breakout base rate")
    if rookie and draft_no and draft_no <= 32:
        prior += 0.12; why.append("First-round rookie: 71% of first-round RBs finish top-24; first-round WRs average ~100 targets")
    if arrival and pos == "WR":
        prior -= 0.10; why.append("Receivers who change teams decline ~2 PPG on average (77% decline)")
    parts["priors"] = round(prior, 2)

    # --- schedule ----------------------------------------------------------------------------
    s = 0.0
    sp = (sos_row.get("sos") or {}).get(pos) or {}
    if sp:
        s = _clamp((0.4 * (sp.get("full_z") or 0) + 0.6 * (sp.get("playoffs_z") or 0)) / 2)
        parts["schedule"] = round(s, 2)

    raw = SW["env"] * e + SW["change"] * c + SW["vacated"] * v + SW["schedule"] * s + prior
    # Route the larger half of situational change into variance rather than the mean (methods sanity rule 2):
    # the caller adds |change| to both boom and bust; the mean effect is capped at about +-0.35 raw.
    raw = max(-0.35, min(0.35, raw))
    parts["variance"] = round(abs(c) * 0.5 + (0.25 if uncertain else 0.0), 2)
    env_block = {
        "hc": env_row.get("hc"), "hcNew": env_row.get("hc_new"), "oc": env_row.get("oc"), "ocNew": env_row.get("oc_new"), "playcaller": env_row.get("playcaller"),
        "scheme": env_row.get("scheme_notes"), "passRate": env_row.get("pass_rate_tendency"), "pace": env_row.get("pace_tendency"), "rbUsage": env_row.get("rb_usage"),
        "qb": env_row.get("qb"), "qbNew": env_row.get("qb_new"), "qbTier": env_row.get("qb_tier"), "qbNote": env_row.get("qb_note"),
        "vegasWins": env_row.get("vegas_wins"), "impliedPpg": env_row.get("implied_ppg"), "olineRank": env_row.get("oline_rank"),
        "arrivals": env_row.get("arrivals"), "departures": env_row.get("departures"), "verdict": env_row.get("env_verdict"),
    } if env_row else None
    chg_block = {
        "opportunity": opp_row.get("opportunity_change"), "competition": opp_row.get("competition_change"), "qb": opp_row.get("qb_change"),
        "coaching": opp_row.get("coaching_change"), "uncertain": uncertain, "drivers": opp_row.get("drivers"), "note": opp_row.get("note"),
        "projShare": opp_row.get("proj_target_share_2026"), "projTouches": opp_row.get("proj_touches_2026"),
    } if opp_row else None
    sos_block = {
        "full": sp.get("full"), "early": sp.get("early"), "playoffs": sp.get("playoffs"), "fullZ": sp.get("full_z"), "playoffsZ": sp.get("playoffs_z"),
        "playoffOpp": sos_row.get("playoff_opponents"), "opponents": sos_row.get("opponents_ha") or sos_row.get("opponents"),
    } if sp else None
    return raw, parts, why[:8], env_block, chg_block, sos_block, uncertain
