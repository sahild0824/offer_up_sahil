#!/usr/bin/env python3
"""Build the player dataset for the Fourth Pick War Room app.

Inputs (all in ./data):
  rankings.json     multi-source 2026 PPR overall ranks + ADP per player
  risk.json         boom / bust / injury signals per player
  byes.json         team -> 2026 bye week
  adjustments.json  hand-curated context nudges (new QB, holdout, role change ...)
  strategy.json     the pick-4 plan rendered on the Plan tab
  model.json        prose + formulas rendered on the Model tab, source list

Output:
  data/players.json  the scored dataset (for inspection)
  index.html         the JSON is injected into <script id="data">

Run:  python3 build.py
"""
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
# Tunable weights. Every score is 0-100. See model.json for the rationale.
# ---------------------------------------------------------------------------
W = {
    # composite: weight per ranking source (default 1). ECR already aggregates
    # 100+ experts, so it counts double.
    "source_weights": {"fantasypros_ecr": 2.0},
    # boom
    "boom": {"upside": 0.30, "mentions": 0.30, "factors": 0.20, "youth": 0.10, "value": 0.10},
    # bust
    "bust": {"downside": 0.20, "mentions": 0.30, "factors": 0.20, "age": 0.15, "reach": 0.10, "injury": 0.05},
    # risk / volatility
    "risk": {"spread": 0.35, "injury": 0.35, "camp": 0.15, "situation": 0.15},
    # tiers: new tier when the composite gap to the previous player exceeds
    # base + slope * composite (gaps naturally widen deeper in the draft).
    "tier_gap_base": 2.0,
    "tier_gap_slope": 0.06,
}

AGE_CLIFF = {  # position -> [(age, penalty 0..1)] evaluated top-down
    "RB": [(29, 1.0), (28, 0.85), (27, 0.55), (26, 0.25)],
    "WR": [(32, 1.0), (31, 0.8), (30, 0.55), (29, 0.25)],
    "TE": [(33, 1.0), (32, 0.7), (31, 0.4)],
    "QB": [(38, 0.9), (36, 0.5), (34, 0.2)],
}
YOUTH = {  # position -> [(max age, bonus)]
    "RB": [(23, 1.0), (24, 0.85), (25, 0.6), (26, 0.3)],
    "WR": [(23, 1.0), (24, 0.85), (25, 0.65), (26, 0.4), (27, 0.2)],
    "TE": [(24, 1.0), (25, 0.8), (26, 0.5), (27, 0.25)],
    "QB": [(25, 0.8), (27, 0.5), (29, 0.2)],
}
# Free-text labels from the research are matched by keyword, first hit wins.
INJ_LABEL = [("out for season", 1.0), ("out for year", 1.0), ("highest", 1.0), ("very high", 1.0), ("moderate-high", 0.7),
             ("high", 0.8), ("low-moderate", 0.35), ("moderate", 0.5), ("elevated", 0.65), ("medium", 0.5), ("average", 0.4),
             ("out", 0.9), ("suspension", 0.6), ("injured", 0.6), ("flagged", 0.55), ("very low", 0.1), ("low", 0.2)]
CAMP = [("healthy", 0.0), ("no reported", 0.0), ("out for season", 1.0), ("out for year", 1.0), ("exempt", 1.0), ("suspended", 1.0),
        ("pup", 1.0), ("ir,", 1.0), ("ir ", 1.0), ("out ", 1.0), ("holdout", 0.8), ("uncertain", 0.7), ("50/50", 0.6), ("questionable", 0.6),
        ("sprain", 0.6), ("injured", 0.6), ("minor", 0.5), ("healing", 0.4), ("returning from", 0.4), ("rehab", 0.4), ("managed", 0.3)]
SITUATION_WORDS = ["rookie", "new team", "new qb", "new oc", "new coach", "new offense", "committee", "timeshare", "contract", "holdout", "suspend", "trade"]


def clamp(x, lo=0.0, hi=1.0):
    return max(lo, min(hi, x))


def norm_name(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = s.lower().replace("'", "").replace(".", "").replace("-", " ")
    s = re.sub(r"\b(jr|sr|ii|iii|iv)\b", "", s)
    return re.sub(r"\s+", " ", s).strip()


def load(name, default):
    p = DATA / name
    if not p.exists():
        print(f"  ! {name} missing, using default")
        return default
    with p.open() as f:
        return json.load(f)


def age_penalty(pos, age):
    if age is None:
        return 0.0
    for a, pen in AGE_CLIFF.get(pos, []):
        if age >= a:
            return pen
    return 0.0


def youth_bonus(pos, age):
    if age is None:
        return 0.0
    for a, b in YOUTH.get(pos, []):
        if age <= a:
            return b
    return 0.0


def camp_score(status):
    if not status:
        return 0.0
    s = status.lower()
    for k, v in CAMP:
        if k in s:
            return v
    return 0.3


def label_score(label):
    s = (label or "").lower()
    for k, v in INJ_LABEL:
        if k in s:
            return v
    return None


def saturate(n, k=3.0):
    """0..1, rising with n but never saturating outright: 1 -> .28, 3 -> .63, 5 -> .81, 10 -> .96"""
    return 1.0 - math.exp(-n / k)


def injury_norm(r):
    pct = r.get("injury_risk_pct")
    lab = (r.get("injury_risk_label") or "").lower()
    gm = r.get("games_missed_last3")
    parts = []
    if pct is not None:
        parts.append(clamp(pct / 60.0))
    elif lab and label_score(lab) is not None:
        parts.append(label_score(lab))
    if gm is not None:
        parts.append(clamp(gm / 18.0))
    return sum(parts) / len(parts) if parts else None


def main():
    rankings = load("rankings.json", [])
    risk = load("risk.json", [])
    byes = load("byes.json", {})
    adjustments = load("adjustments.json", {})
    strategy = load("strategy.json", {})
    model = load("model.json", {})

    risk_by = {norm_name(r["name"]): r for r in risk}
    adj_by = {norm_name(k): v for k, v in adjustments.items()}
    used_risk, used_adj = set(), set()

    players = []
    for r in rankings:
        ranks = {k: v for k, v in (r.get("ranks") or {}).items() if v is not None and not k.endswith("_posrank")}
        if not ranks:
            continue
        key = norm_name(r["name"])
        rk = risk_by.get(key, {})
        ad = adj_by.get(key, {})
        if rk:
            used_risk.add(key)
        if ad:
            used_adj.add(key)

        # --- composite -----------------------------------------------------
        wsum = sum(W["source_weights"].get(k, 1.0) for k in ranks)
        comp = sum(v * W["source_weights"].get(k, 1.0) for k, v in ranks.items()) / wsum
        vals = list(ranks.values())
        best, worst = min(vals), max(vals)
        sd = statistics.pstdev(vals) if len(vals) > 1 else 0.0

        adps = {k: v for k, v in (r.get("adp") or {}).items() if v is not None}
        adp = statistics.mean(adps.values()) if adps else None
        value = (adp - comp) if adp is not None else None

        pos = r["pos"].upper()
        age = rk.get("age") or r.get("age")
        scale = 0.5 * comp + 5.0  # rank distances mean less deeper in the draft

        # --- boom ----------------------------------------------------------
        boom_mentions = len(rk.get("boom_mentions") or []) + len(rk.get("sleeper_mentions") or [])
        boom_factors = list(rk.get("boom_factors") or []) + list(ad.get("boom_factors") or [])
        bw = W["boom"]
        boom_parts = {
            "upside": bw["upside"] * clamp((comp - best) / scale),
            "mentions": bw["mentions"] * saturate(boom_mentions),
            "factors": bw["factors"] * saturate(len(boom_factors)),
            "youth": bw["youth"] * youth_bonus(pos, age),
            "value": bw["value"] * clamp((value or 0) / 10.0),
        }
        boom = 100 * clamp(sum(boom_parts.values()) + ad.get("boom_adj", 0))

        # --- bust ----------------------------------------------------------
        bust_mentions = len(rk.get("bust_mentions") or [])
        risk_factors = list(rk.get("risk_factors") or []) + list(ad.get("risk_factors") or [])
        inj = injury_norm(rk)
        uw = W["bust"]
        bust_parts = {
            "downside": uw["downside"] * clamp((worst - comp) / scale),
            "mentions": uw["mentions"] * saturate(bust_mentions),
            "factors": uw["factors"] * saturate(len(risk_factors)),
            "age": uw["age"] * age_penalty(pos, age),
            "reach": uw["reach"] * clamp(-(value or 0) / 10.0),
            "injury": uw["injury"] * (inj or 0),
        }
        bust = 100 * clamp(sum(bust_parts.values()) + ad.get("bust_adj", 0))

        # --- risk / volatility ---------------------------------------------
        camp = camp_score(rk.get("camp_status") or ad.get("camp_status"))
        sit_hits = sum(1 for f in risk_factors if any(w in f.lower() for w in SITUATION_WORDS))
        rw = W["risk"]
        risk_parts = {
            "spread": rw["spread"] * clamp(sd / (0.35 * comp + 3.0)),
            "injury": rw["injury"] * (inj if inj is not None else 0.35),
            "camp": rw["camp"] * camp,
            "situation": rw["situation"] * clamp(sit_hits / 2.0),
        }
        risk_score = 100 * clamp(sum(risk_parts.values()) + ad.get("risk_adj", 0))

        # --- explanations --------------------------------------------------
        boom_why = []
        if comp - best >= 0.25 * scale:
            boom_why.append(f"Most bullish source has him #{int(best)}, {comp - best:.0f} spots above consensus")
        if boom_mentions:
            boom_why.append("Named a breakout/sleeper by " + ", ".join((rk.get("boom_mentions") or []) + (rk.get("sleeper_mentions") or [])))
        boom_why += boom_factors
        if youth_bonus(pos, age) >= 0.6:
            boom_why.append(f"Age {age}: still on the ascending side of the curve")
        if value is not None and value >= 3:
            boom_why.append(f"Market lets him fall {value:.0f} picks past his composite rank")

        bust_why = []
        if worst - comp >= 0.25 * scale:
            bust_why.append(f"Most bearish source has him #{int(worst)}, {worst - comp:.0f} spots below consensus")
        if bust_mentions:
            bust_why.append("On bust/avoid lists from " + ", ".join(rk.get("bust_mentions") or []))
        bust_why += risk_factors
        if age_penalty(pos, age) >= 0.5:
            bust_why.append(f"Age {age}: past the historical {pos} decline point")
        if value is not None and value <= -3:
            bust_why.append(f"Market drafts him {-value:.0f} picks earlier than his composite rank")

        risk_why = []
        if sd >= 0.5 * (0.35 * comp + 3.0):
            risk_why.append(f"Sources disagree: spread of ±{sd:.1f} places (#{int(best)} to #{int(worst)})")
        if rk.get("injury_risk_pct") is not None:
            risk_why.append(f"Injury model: {rk['injury_risk_pct']:.0f}% chance of missing time")
        elif rk.get("injury_risk_label"):
            risk_why.append(f"Injury risk rated {rk['injury_risk_label']}")
        if rk.get("games_missed_last3"):
            risk_why.append(f"Missed {rk['games_missed_last3']} games over the last three seasons")
        if camp >= 0.5:
            risk_why.append("Camp status: " + (rk.get("camp_status") or ad.get("camp_status")))
        if sit_hits:
            risk_why.append("Situation change: " + "; ".join(f for f in risk_factors if any(w in f.lower() for w in SITUATION_WORDS)))

        flag = None
        if camp >= 0.8:
            flag = (rk.get("camp_status") or ad.get("camp_status") or "").split(":")[0][:14]
        elif value is not None and value >= 4:
            flag = "Value"
        elif value is not None and value <= -4:
            flag = "Reach"
        elif ad.get("flag"):
            flag = ad["flag"]

        players.append({
            "id": key.replace(" ", "-"),
            "name": r["name"], "team": r["team"], "pos": pos,
            "bye": r.get("bye") or byes.get(r["team"]) or "?",
            "age": age,
            "comp": round(comp, 1), "n": len(ranks), "best": best, "worst": worst, "sd": round(sd, 1),
            "sources": ranks,
            "adp": round(adp, 1) if adp is not None else None, "adpN": len(adps), "adpSources": adps or None,
            "value": round(value, 1) if value is not None else None,
            "boom": round(boom), "bust": round(bust), "risk": round(risk_score),
            "boomWhy": boom_why[:5], "bustWhy": bust_why[:5], "riskWhy": risk_why[:5],
            "flag": flag,
            "note": ad.get("note") or rk.get("notes"),
            "_parts": {"boom": boom_parts, "bust": bust_parts, "risk": risk_parts},
        })

    # --- positional rank + tiers ------------------------------------------
    players.sort(key=lambda p: p["comp"])
    for pos in ("QB", "RB", "WR", "TE"):
        group = [p for p in players if p["pos"] == pos]
        tier, prev = 1, None
        for i, p in enumerate(group, 1):
            p["posRank"] = i
            if prev is not None and (p["comp"] - prev) > W["tier_gap_base"] + W["tier_gap_slope"] * p["comp"]:
                tier += 1
            p["tier"] = tier
            prev = p["comp"]

    # --- report ------------------------------------------------------------
    missing_risk = [p["name"] for p in players if norm_name(p["name"]) not in used_risk]
    print(f"players scored: {len(players)}")
    print(f"risk signals matched: {len(used_risk)}/{len(risk)}  unmatched risk rows: {sorted(set(risk_by) - used_risk)[:20]}")
    print(f"adjustments matched: {len(used_adj)}/{len(adj_by)}  unmatched: {sorted(set(adj_by) - used_adj)}")
    print(f"players without risk signals: {len(missing_risk)} e.g. {missing_risk[:12]}")

    source_counts = {}
    for p in players:
        for k in p["sources"]:
            source_counts[k] = source_counts.get(k, 0) + 1
        for k in (p["adpSources"] or {}):
            source_counts[k] = source_counts.get(k, 0) + 1
    print("source coverage:", json.dumps(source_counts, indent=0))

    for s in model.get("sources", []):
        if s.get("key") in source_counts:
            s["count"] = source_counts[s["key"]]

    out = {
        "players": [{k: v for k, v in p.items() if k != "_parts"} for p in players],
        "strategy": strategy,
        "meta": {
            "updated": date.today().isoformat(),
            "sourceNames": model.get("sourceNames", {}),
            "sources": model.get("sources", []),
            "unavailable": model.get("unavailable", []),
            "model": {"intro": model.get("intro", ""), "sections": model.get("sections", [])},
            "weights": W,
        },
    }
    (DATA / "players.json").write_text(json.dumps(players, indent=1))

    html_path = HERE / "index.html"
    html = html_path.read_text()
    blob = json.dumps(out, separators=(",", ":")).replace("</", "<\\/")
    new_html, n = re.subn(r'(<script id="data" type="application/json">)(.*?)(</script>)', lambda m: m.group(1) + "\n" + blob + "\n" + m.group(3), html, flags=re.S)
    assert n == 1, "data script block not found"
    html_path.write_text(new_html)
    print(f"wrote index.html ({len(new_html) // 1024} KB)")


if __name__ == "__main__":
    main()
