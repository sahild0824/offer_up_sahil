#!/usr/bin/env python3
"""Weekly start/sit and waiver report from a roster file, a waiver file and data/weekly_2026.json.

    python3 weekly.py --week 2 roster.json waivers.json > week_2.md

How a player is projected for the week (each step is the choice the open-source survey
converged on; see research/open_source_survey.md):

  usage    = season consensus per game (players.json proj/17), pulled toward this season's
             EWMA of PPR points at weight n/(n+3) - one game moves it a quarter of the way,
             four games most of the way. A week his team played without him counts as zero.
  usage   *= matchup: clamp(implied_term * dvp_term * site_term, 0.88, 1.12), with
             implied_term = clamp(1 + 0.35*(team implied total / league avg - 1), 0.9, 1.1),
             dvp_term = 1 + 0.25*(defense-vs-position factor - 1), site_term 1.02 home / 0.98 away.
  expert   = FantasyPros weekly consensus projection (already matchup-aware).
  mean     = equal-weight average of usage and expert (equal weights beat accuracy weights
             in 64% of head-to-heads over twelve seasons - fantasy_quant), times the injury
             availability (Questionable 0.75, Doubtful 0.35, Out 0).
  spread   = lognormal with a position CV (QB .32, RB .52, WR .58, TE .62); floor and ceiling
             are the 20th and 80th percentiles; boom = P(> 1.5 x mean), bust = P(< 0.6 x mean).

The lineup maximizes the sum of means - "start your studs"; variance-seeking did not hold up
out of sample. Every starter is compared with the best bench alternative at that slot with
confidence Phi(gap / hypot(sd_a, sd_b)): under 55% is a coin flip, under 65% a lean.

Waiver value is the lineup delta from actually re-running the optimizer with the player
added, never his raw projection, in three buckets: season (improves the rest-of-season
lineup), week (improves this week only - a bye or injury filler), depth (beats your worst
bench player). Season selects, the week orders within it.
"""
import argparse
import json
import math
import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
SLOTS = [("QB", 1), ("RB", 2), ("WR", 2), ("TE", 1)]
FLEX_POS = ("RB", "WR", "TE")
CV = {"QB": 0.32, "RB": 0.52, "WR": 0.58, "TE": 0.62}
FORM_PRIOR_N = 3.0
LAST_WEEK = 17          # value rest-of-season through the fantasy playoffs
DST_NICK = {"cardinals": "ARI", "falcons": "ATL", "ravens": "BAL", "bills": "BUF", "panthers": "CAR", "bears": "CHI",
            "bengals": "CIN", "browns": "CLE", "cowboys": "DAL", "broncos": "DEN", "lions": "DET", "packers": "GB",
            "texans": "HOU", "colts": "IND", "jaguars": "JAX", "chiefs": "KC", "raiders": "LV", "chargers": "LAC",
            "rams": "LAR", "dolphins": "MIA", "vikings": "MIN", "patriots": "NE", "saints": "NO", "giants": "NYG",
            "jets": "NYJ", "eagles": "PHI", "steelers": "PIT", "49ers": "SF", "seahawks": "SEA", "buccaneers": "TB",
            "titans": "TEN", "commanders": "WAS"}


def norm_name(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode()
    s = s.lower().replace("'", "").replace(".", "").replace("-", " ")
    s = re.sub(r"\b(jr|sr|ii|iii|iv|v)\b", "", s)
    return re.sub(r"\s+", " ", s).strip()


def phi(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def clamp(x, lo, hi):
    return max(lo, min(hi, x))


# ---------------------------------------------------------------------------------------------
class Engine:
    def __init__(self, week):
        self.week = week
        self.W = json.load(open(DATA / "weekly_2026.json"))
        if self.W["week"] != week:
            print(f"!! weekly_2026.json was built for week {self.W['week']}, not {week}; rerun ingest.py --week {week}", file=sys.stderr)
        pl = json.load(open(DATA / "players.json"))
        self.P = {p["id"]: p for p in (pl["players"] if isinstance(pl, dict) else pl)}
        self.P_by_name = {norm_name(p["name"]) + "|" + p["pos"]: p for p in self.P.values()}
        self.teams = self.W["teams"]
        imp = [t["implied"] for t in self.teams.values() if t.get("implied")]
        self.avg_implied = sum(imp) / len(imp) if imp else 22.0
        self.weeks_left = max(1, LAST_WEEK - week + 1)

    # ---- projection ---------------------------------------------------------------------
    def gsis_for(self, name, pos):
        return self.W["by_name"].get(norm_name(name) + "|" + pos)

    def project(self, name, pos, team_hint=None):
        """Return a dict with mean / floor / ceiling / parts, or None for K and DST."""
        if pos in ("K", "DST"):
            return None
        g = self.gsis_for(name, pos)
        wp = self.W["players"].get(g) if g else None
        base_p = self.P_by_name.get(norm_name(name) + "|" + pos)
        team = (wp or {}).get("team") or (base_p or {}).get("team") or team_hint
        tm = self.teams.get(team, {}) if team else {}
        notes = []

        # season consensus per game; for a player the draft model never scored (a rookie or a
        # backup who just broke out) the FantasyPros weekly number stands in as the prior, so
        # one loud week is still shrunk toward something rather than taken at face value
        base = (base_p["proj"] / 17.0) if base_p and base_p.get("proj") else None
        fp = (wp or {}).get("fp") or {}
        expert = fp.get("proj")
        prior_is_expert = False
        if base is None and expert is not None:
            base, prior_is_expert = expert, True
        # this season's form
        form = (wp or {}).get("form") or {}
        n = form.get("games") or 0
        ewma = form.get("ewma_pts")
        w_form = n / (n + FORM_PRIOR_N) if n else 0.0
        # Role shift: the preseason number is stale when this season's usage is worth far more.
        # Expected points from play-by-play (ffopportunity) measure the role without the TD
        # noise, so a player whose EP runs 1.5x his preseason per-game baseline has changed
        # jobs - a rookie starting, a backup promoted - and the usage is the fresher fact.
        ep_ew = form.get("ewma_ep")
        role_shift = bool(base is not None and ep_ew and base > 0 and ep_ew >= 1.5 * base and ep_ew >= 8.0)
        if role_shift:
            w_form = max(w_form, 0.45)
        # The form target is half actual points, half expected points from usage. Expected
        # points strip out touchdown luck - a 3-TD day on 20 carries is worth its 20 carries -
        # so a hot week moves the projection by what the role was worth, not what it scored.
        target = ewma
        if ewma is not None and ep_ew:
            target = 0.5 * ewma + 0.5 * ep_ew
        if base is not None and target is not None and n:
            usage = (1 - w_form) * base + w_form * target
        elif target is not None and n:
            usage = target
        else:
            usage = base
        if usage is not None and n:
            notes.append((f"wk1: {form.get('last_pts', 0):.1f} pts" if n == 1
                          else f"wk1-{self.week - 1} avg {form.get('mean_pts', 0):.1f}, last {form.get('last_pts', 0):.1f}"))
        if role_shift:
            notes.append(f"ROLE UP: {ep_ew:.0f} expected pts/gm vs {base:.0f} preseason")

        # matchup
        matchup = 1.0
        if tm.get("bye"):
            return {"mean": 0.0, "floor": 0.0, "ceil": 0.0, "sd": 0.0, "bye": True, "team": team, "opp": None,
                    "notes": ["BYE"], "avail": 0.0, "parts": {}}
        opp = tm.get("opp")
        if tm.get("implied") and self.avg_implied:
            implied_term = clamp(1 + 0.35 * (tm["implied"] / self.avg_implied - 1), 0.9, 1.1)
        else:
            implied_term = 1.0
        dvp_f = ((self.teams.get(opp) or {}).get("dvp_factor") or {}).get(pos) if opp else None
        dvp_term = 1 + 0.25 * (dvp_f - 1) if dvp_f else 1.0
        site_term = 1.02 if tm.get("home") else (0.98 if tm.get("home") is False else 1.0)
        matchup = clamp(implied_term * dvp_term * site_term, 0.88, 1.12)
        usage_adj = usage * matchup if usage is not None else None

        # expert weekly projection
        fp = (wp or {}).get("fp") or {}
        expert = fp.get("proj")

        ests = [x for x in (usage_adj, expert) if x is not None]
        if not ests:
            return None
        mean_if_plays = sum(ests) / len(ests)

        inj = (wp or {}).get("injury") or {}
        avail = inj.get("avail", 1.0) if inj.get("status") else 1.0
        if inj.get("status"):
            notes.append(f"{inj['status']}{' (' + inj['injury'] + ')' if inj.get('injury') else ''}"
                         + (" - report is from last week" if inj.get("stale") else ""))
        status = (wp or {}).get("status")
        if status and status not in ("ACT", "A01"):
            notes.append(f"roster status {status}")
            if status in ("RES", "IR", "PUP", "INA"):
                avail = 0.0
        mean = mean_if_plays * avail

        cv = CV.get(pos, 0.55)
        s2 = math.log(1 + cv * cv)
        sig = math.sqrt(s2)
        if mean > 0:
            mu = math.log(mean) - s2 / 2
            floor, ceil = math.exp(mu - 0.8416 * sig), math.exp(mu + 0.8416 * sig)
            boom = 1 - phi((math.log(1.5 * mean) - mu) / sig)
            bust = phi((math.log(0.6 * mean) - mu) / sig)
        else:
            floor = ceil = boom = bust = 0.0
        sd = mean * cv

        wk = (wp or {}).get("weeks", {}).get(str(self.week - 1), {}) if wp else {}
        if wk.get("snap_pct") is not None:
            notes.append(f"{int(round(wk['snap_pct'] * 100))}% snaps")
        if pos in ("WR", "TE") and wk.get("targets") is not None:
            notes.append(f"{int(wk['targets'])} tgt" + (f" ({int(round(wk['target_share'] * 100))}% share)" if wk.get("target_share") else ""))
        if pos == "RB" and wk.get("carries") is not None:
            notes.append(f"{int(wk['carries'])} car / {int(wk.get('targets') or 0)} tgt")
        if wk.get("ep") is not None and wk.get("pts") is not None:
            d = wk["pts"] - wk["ep"]
            if abs(d) >= 5:
                notes.append(f"{'+' if d > 0 else ''}{d:.0f} vs expected pts" + (" - TD-inflated" if d > 0 else " - unlucky"))
        if fp.get("pos_rank"):
            notes.append(f"FP {fp['pos_rank']}" + (f" {fp['grade']}" if fp.get("grade") else ""))
        if opp:
            notes.append(f"{'vs' if tm.get('home') else '@'} {opp}" + (f", DvP x{dvp_f:.2f}" if dvp_f else "")
                         + (f", implied {tm['implied']:.1f}" if tm.get("implied") else ""))

        return {"mean": mean, "mean_if_plays": mean_if_plays, "floor": floor, "ceil": ceil, "sd": sd,
                "boom": boom, "bust": bust, "avail": avail, "team": team, "opp": opp, "bye": False, "notes": notes,
                "parts": {"base": base, "ewma": ewma, "n": n, "usage_adj": usage_adj, "expert": expert,
                          "matchup": matchup, "implied": tm.get("implied"), "dvp": dvp_f},
                "ros": (self._ros(base, target, w_form) * avail_ros(avail)) if (base or target) else None}

    def _ros(self, base, target, w_form):
        if base is not None and target is not None and w_form:
            per = (1 - w_form) * base + w_form * target
        else:
            per = base if base is not None else target
        return per * self.weeks_left

    # ---- lineup ------------------------------------------------------------------------
    @staticmethod
    def best_lineup(scored):
        """scored: list of (entry, proj). Returns (starters as list of (slot, entry, proj), bench)."""
        pool = [(e, p) for e, p in scored if p is not None and e["pos"] in ("QB",) + FLEX_POS]
        used, starters = set(), []
        for pos, k in SLOTS:
            c = sorted([(e, p) for e, p in pool if e["pos"] == pos and id(e) not in used], key=lambda x: -x[1]["mean"])[:k]
            for e, p in c:
                used.add(id(e)); starters.append((pos, e, p))
        fx = sorted([(e, p) for e, p in pool if e["pos"] in FLEX_POS and id(e) not in used], key=lambda x: -x[1]["mean"])[:1]
        for e, p in fx:
            used.add(id(e)); starters.append(("FLEX", e, p))
        bench = [(e, p) for e, p in pool if id(e) not in used]
        return starters, bench

    @staticmethod
    def total(starters):
        return sum(p["mean"] for _, _, p in starters)


def avail_ros(avail):
    # a one-week injury tag should barely move rest-of-season value; an IR/out tag should
    return 1.0 if avail >= 0.75 else (0.85 if avail > 0 else 0.5)


# ---------------------------------------------------------------------------------------------
def conf_label(gap, sd_a, sd_b):
    s = math.hypot(sd_a, sd_b)
    c = phi(gap / s) if s else 1.0
    return c, ("coin flip" if c < 0.55 else "lean" if c < 0.65 else "clear")


def fmt(p):
    return f"{p['mean']:.1f}" if p else "-"


def report(week, roster, waivers, E):
    out = []
    W = E.W
    say = out.append
    say(f"# Week {week} - start/sit and waivers")
    say(f"_Built {W['generated']} from nflverse through week {W['weeks_done'][-1] if W['weeks_done'] else 0}, FantasyPros consensus scraped {W.get('fp_scrape_date')}, Vegas lines from nflverse games.csv._\n")

    # ---- score the roster ----------------------------------------------------------------
    scored = []
    for e in roster["players"]:
        e = dict(e)
        p = E.project(e["name"], e["pos"], e.get("team"))
        scored.append((e, p))
    starters, bench = E.best_lineup(scored)
    current = {e["slot"]: e for e in roster["players"] if e.get("slot") not in (None, "BE", "BN")}

    # ---- START THIS ------------------------------------------------------------------------
    say("## Start this\n")
    say("| Slot | Player | Proj | Floor-Ceil | Why |")
    say("|---|---|---|---|---|")
    for slot, e, p in starters:
        changed = ""
        cur = [x for x in roster["players"] if x.get("slot") == slot or (slot in ("RB", "WR") and x.get("slot") == slot)]
        if e.get("slot") in ("BE", "BN"):
            changed = " **(from bench)**"
        say(f"| {slot} | **{e['name']}**{changed} | {p['mean']:.1f} | {p['floor']:.0f}-{p['ceil']:.0f} | {'; '.join(p['notes'][:4])} |")
    say(f"\nLineup total: **{E.total(starters):.1f}** projected.\n")

    moves = [(slot, e) for slot, e, p in starters if e.get("slot") in ("BE", "BN")]
    benched = [e for e, p in bench if e.get("slot") not in (None, "BE", "BN")]
    if moves or benched:
        say("**Changes from your current lineup:** "
            + "; ".join([f"start {e['name']} at {slot}" for slot, e in moves] + [f"bench {e['name']}" for e in benched]) + ".\n")
    else:
        say("Your current lineup is already the best one.\n")

    # ---- CLOSE CALLS --------------------------------------------------------------------
    say("## Close calls\n")
    say("Each starter against the best bench player who could take his slot. Under 55% is a coin flip - overrule with a reason.\n")
    say("| Slot | Starter | vs bench | Gap | Confidence |")
    say("|---|---|---|---|---|")
    any_close = False
    for slot, e, p in starters:
        eligible = [(be, bp) for be, bp in bench if (be["pos"] == e["pos"] if slot != "FLEX" else be["pos"] in FLEX_POS)]
        if not eligible:
            continue
        be, bp = max(eligible, key=lambda x: x[1]["mean"])
        gap = p["mean"] - bp["mean"]
        c, lab = conf_label(gap, p["sd"], bp["sd"])
        flag = "" if lab == "clear" else f" **{lab}**"
        if lab != "clear":
            any_close = True
        say(f"| {slot} | {e['name']} {p['mean']:.1f} | {be['name']} {bp['mean']:.1f} | +{gap:.1f} | {c * 100:.0f}%{flag} |")
    if not any_close:
        say("\nNo coin flips this week - the lineup is clear-cut.")
    say("")

    # ---- BENCH ---------------------------------------------------------------------------
    say("## Bench\n")
    say("| Player | Proj | Floor-Ceil | ROS | Notes |")
    say("|---|---|---|---|---|")
    for e, p in sorted(bench, key=lambda x: -x[1]["mean"]):
        say(f"| {e['name']} ({e['pos']}) | {p['mean']:.1f} | {p['floor']:.0f}-{p['ceil']:.0f} | {p['ros']:.0f} | {'; '.join(p['notes'][:3])} |")
    unscored = [e for e, p in scored if p is None and e["pos"] not in ("K", "DST")]
    for e in unscored:
        say(f"| {e['name']} ({e['pos']}) | ? | | | no data - not in the model or no 2026 stats yet |")
    say("")

    # ---- WAIVERS -------------------------------------------------------------------------
    say("## Waivers\n")
    base_total = E.total(starters)
    droppable = [(e, p) for e, p in bench if p is not None]
    if droppable:
        drop_e, drop_p = min(droppable, key=lambda x: (x[1]["ros"] or 0))
    else:
        drop_e = drop_p = None
    # Rest-of-season value is a LINEUP delta too: the same optimizer run on rest-of-season
    # totals, with the add in and the drop out. Raw points would rank a backup quarterback
    # above a starting-caliber receiver - a QB2 never starts in a one-quarterback league.
    def ros_pool(sc):
        return [(e2, {"mean": (p2["ros"] or 0.0), "sd": 0.0}) for e2, p2 in sc if p2 is not None]
    base_ros = E.total(E.best_lineup(ros_pool(scored))[0])
    has_qb = any(e2["pos"] == "QB" for e2, p2 in scored if p2 is not None)
    rows = []
    for e in waivers["players"]:
        e = dict(e); e["slot"] = "BE"
        p = E.project(e["name"], e["pos"], e.get("team"))
        if p is None:
            rows.append((e, None, None, None, "no data"))
            continue
        after = [(e2, p2) for e2, p2 in scored if e2 is not drop_e] + [(e, p)]
        wk_delta = E.total(E.best_lineup(after)[0]) - base_total
        ros_delta = E.total(E.best_lineup(ros_pool(after))[0]) - base_ros
        raw_ros_edge = (p["ros"] or 0) - ((drop_p or {}).get("ros") or 0) if drop_p else (p["ros"] or 0)
        if ros_delta > 0.5 and wk_delta > 0.5:
            bucket = "season"
        elif ros_delta > 0.5:
            bucket = "season-later"
        elif wk_delta > 0.5:
            bucket = "week"
        elif raw_ros_edge > 0 and (e["pos"] != "QB" or not has_qb):
            bucket = "depth"
        else:
            bucket = "pass"
        rows.append((e, p, wk_delta, ros_delta, bucket))
    order = {"season": 0, "season-later": 1, "week": 2, "depth": 3, "pass": 4, "no data": 5}
    rows.sort(key=lambda r: (order.get(r[4], 9), -(r[3] or 0), -(r[1]["mean"] if r[1] else 0)))
    if drop_e:
        say(f"Drop candidate: **{drop_e['name']}** ({drop_e['pos']}, {drop_p['mean']:.1f} this week, {drop_p['ros']:.0f} rest of season) - lowest rest-of-season value on your bench.\n")
    say("| # | Add | This week | +lineup this wk | ROS vs drop | Bucket | Notes |")
    say("|---|---|---|---|---|---|---|")
    rank = 0
    for e, p, wkd, rosd, bucket in rows:
        if bucket in ("pass", "no data"):
            continue
        rank += 1
        say(f"| {rank} | **{e['name']}** ({e['pos']}, {p['team'] or e.get('team') or '?'}) | {p['mean']:.1f} | {wkd:+.1f} | {rosd:+.0f} | {bucket} | {'; '.join(p['notes'][:3])} |")
    if rank == 0:
        say("| - | nobody on the wire improves this roster | | | | | |")
    passed = [e["name"] for e, p, wkd, rosd, b in rows if b == "pass"]
    if passed:
        say(f"\nNot worth a spot over {drop_e['name'] if drop_e else 'your bench'}: " + ", ".join(passed) + ".")
    nodata = [e["name"] for e, p, wkd, rosd, b in rows if b == "no data"]
    if nodata:
        say(f"\nNo data for: " + ", ".join(nodata) + " - not in the model and no 2026 stat line; treat as unknowns.")
    say("\n_Buckets: **season** = improves your rest-of-season lineup and this week; **season-later** = better rest-of-season but not this week; **week** = a one-week filler; **depth** = beats your worst bench player only. Priority order is the table order._\n")

    # ---- K and D/ST ----------------------------------------------------------------------
    say("## Kicker and D/ST\n")
    my_dst = [e for e in roster["players"] if e["pos"] == "DST"]
    my_k = [e for e in roster["players"] if e["pos"] == "K"]
    fp_dst, fp_k = W.get("fp_dst", {}), W.get("fp_k", {})
    def dst_row(t, d):
        tm = E.teams.get(t, {})
        oi = tm.get("opp_implied")
        return f"| {d.get('name', t)} | {d.get('pos_rank', '-')} {d.get('grade') or ''} | {d.get('proj') if d.get('proj') is not None else '-'} | {'vs' if tm.get('home') else '@'} {tm.get('opp', '-')} | {f'{oi:.1f}' if oi else '-'} |"
    say("| D/ST | FP rank | FP proj | Opp | Opp implied |")
    say("|---|---|---|---|---|")
    for e in my_dst:
        t = DST_NICK.get(norm_name(e["name"]).split()[0], None) or next((k for k in DST_NICK.values() if k.lower() in norm_name(e["name"])), None)
        if t and t in fp_dst:
            say("**mine** " + dst_row(t, fp_dst[t]))
        else:
            say(f"| {e['name']} (mine) | not found in FP | | | |")
    streams = sorted(((t, d) for t, d in fp_dst.items() if d.get("ecr") is not None), key=lambda x: x[1]["ecr"])[:6]
    for t, d in streams:
        say(dst_row(t, d))
    say("\n_D/ST scoring is mostly the opponent and the line: a low opponent implied total is the signal. Kickers are not streamable - the week-to-week spread is noise - so keep yours unless he loses his job._\n")
    if my_k:
        for e in my_k:
            k = fp_k.get(norm_name(e["name"]))
            say(f"K **{e['name']}**: " + (f"FP {k['pos_rank']} {k.get('grade') or ''}, proj {k.get('proj')}" if k else "not found in FP rankings") + ".")
    say("")

    # ---- WATCH LIST ----------------------------------------------------------------------
    say("## Watch before kickoff\n")
    watch = []
    for e, p in scored:
        if p and p.get("avail", 1.0) < 1.0 and not p.get("bye"):
            pivot = ""
            slot = next((s for s, se, sp in starters if se is e), None)
            if slot:
                alt = [(be, bp) for be, bp in bench if (be["pos"] == e["pos"] if slot != "FLEX" else be["pos"] in FLEX_POS)]
                if alt:
                    be, bp = max(alt, key=lambda x: x[1]["mean"])
                    pivot = f" If out: **{be['name']}** ({bp['mean']:.1f})."
            watch.append(f"- **{e['name']}** - {[n for n in p['notes'] if any(s in n for s in ('Questionable', 'Doubtful', 'Out'))][0] if any('Questionable' in n or 'Doubtful' in n or 'Out' in n for n in p['notes']) else 'injury flag'}. Projected {p['mean']:.1f} ({p['mean_if_plays']:.1f} if he plays).{pivot}")
    if watch:
        out.extend(watch)
    else:
        say("No injury designations on your roster.")
    stale = [e["name"] for e, p in scored if p and any("last week" in n for n in p["notes"])]
    if stale:
        say(f"\n_Reports for {', '.join(stale)} are from last week; this week's designations land Wed-Fri._")
    say("")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--week", type=int, required=True)
    ap.add_argument("roster")
    ap.add_argument("waivers", nargs="?")
    a = ap.parse_args()
    roster = json.load(open(a.roster))
    waivers = json.load(open(a.waivers)) if a.waivers else {"players": []}
    E = Engine(a.week)
    print(report(a.week, roster, waivers, E))


if __name__ == "__main__":
    main()
