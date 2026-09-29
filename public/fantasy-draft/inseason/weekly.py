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

News (optional --news news.json) covers what the box scores cannot see yet: a player ruled
out for N weeks or the season. He projects to zero for those weeks, and NEWS_KEEP (0.7) of his
per-game role is handed to his healthy same-position teammates in proportion to their recent
snap share, capped at NEWS_CAP (0.9) of his role - the vacated-opportunity rule, so a handcuff
is valued as the starter he is about to be rather than the backup the data still shows.

    {"out": [{"name": "Breece Hall", "pos": "RB", "weeks": 1, "note": "quad, week-to-week"},
             {"name": "De'Von Achane", "pos": "RB", "weeks": "season", "note": "torn ACL"},
             {"name": "Travis Etienne", "pos": "RB", "weeks": 3, "heirs": {"Alvin Kamara": 0.65, "Kendre Miller": 0.35}}]}

"heirs" overrides the snap-share split when the reporting names who takes the work. "weeks"
may also be a spread of outcomes for a week-to-week injury, {"1": 0.45, "2": 0.35, "4": 0.2}:
the season lineup is then averaged over every combination, so a backup earns credit in the
scenarios where he would actually start.

Rest-of-season value is never a raw points total. The optimizer is re-run for every remaining
week through Week 17 - byes zeroed, absences zeroed, heirs promoted - and a bench player is
worth what the season lineup loses without him. That is what makes a backup quarterback worth
exactly his starter's bye week, and a handcuff worth exactly the weeks he would start.

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
# Prior for a player with no preseason number and no current FantasyPros projection: a weekly
# replacement-level starter. Three games move him halfway from here to his form, so a
# 90%-catch-rate month is shrunk rather than taken at face value.
REPLACEMENT = {"QB": 14.0, "RB": 6.0, "WR": 7.0, "TE": 5.0}
NEWS_KEEP = 0.7         # share of a missing player's role that stays inside his position group
NEWS_CAP = 0.9          # an heir's role tops out at this fraction of the missing player's role
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
    def __init__(self, week, news=None):
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
        self.byes = self.W.get("byes") or {}
        if not self.byes:
            print("!! weekly_2026.json has no bye table; rerun ingest.py so rest-of-season values see byes", file=sys.stderr)
        self.out, self.heirs = {}, {}
        self._apply_news(news or {})

    # ---- news: players ruled out, and who inherits their role ----------------------------
    def _role_value(self, wp, pos):
        """Per-game role worth, before matchup: the same prior-plus-form blend project() uses."""
        base_p = self.P_by_name.get(norm_name(wp["name"]) + "|" + pos)
        base = (base_p["proj"] / 17.0) if base_p and base_p.get("proj") else None
        form = wp.get("form") or {}
        n = form.get("games") or 0
        if base is None and n:
            base = REPLACEMENT.get(pos)
        ewma, ep = form.get("ewma_pts"), form.get("ewma_ep")
        target = 0.5 * ewma + 0.5 * ep if (ewma is not None and ep) else ewma
        if base is not None and target is not None and n:
            w = n / (n + FORM_PRIOR_N)
            return (1 - w) * base + w * target
        return target if target is not None else (base or 0.0)

    def _apply_news(self, news):
        for o in news.get("out", []):
            pos, g = o.get("pos"), None
            for cand in ([pos] if pos else ["RB", "WR", "TE", "QB"]):
                g = self.gsis_for(o["name"], cand)
                if g:
                    pos = cand
                    break
            if not g or g not in self.W["players"]:
                print(f"!! news: no 2026 player matches {o['name']!r}", file=sys.stderr)
                continue
            # "weeks" is a count, "season", or a spread of outcomes {"1": 0.5, "2": 0.3, "5": 0.2}
            wk = o.get("weeks", 1)
            spread = wk if isinstance(wk, dict) else {wk: 1.0}
            tot = sum(float(v) for v in spread.values()) or 1.0
            dist = [(self.weeks_left if k == "season" else max(1, min(int(k), self.weeks_left)), float(v) / tot)
                    for k, v in spread.items()]
            self.out[g] = {"dist": dist, "weeks": max(k for k, _ in dist), "note": o.get("note") or "out",
                           "pos": pos, "season": all(k >= self.weeks_left for k, _ in dist), "heirs": o.get("heirs")}
        for g, o in self.out.items():
            wp = self.W["players"][g]
            vac = self._role_value(wp, o["pos"])
            if o["heirs"]:
                # the beat reporters know the depth chart better than last month's snap shares
                named = {self.gsis_for(n, o["pos"]): float(w) for n, w in o["heirs"].items()}
                mates = [(h, self.W["players"][h]) for h in named if h in self.W["players"]]
                wts = {h: named[h] for h, _ in mates}
            else:
                mates = [(h, q) for h, q in self.W["players"].items()
                         if h != g and h not in self.out and q.get("team") == wp.get("team") and q.get("pos") == o["pos"]
                         and (q.get("form") or {}).get("games") and q.get("status") in (None, "ACT", "A01")]
                wts = {h: max((q.get("form") or {}).get("ewma_snap_pct") or 0.0, 0.05) for h, q in mates}
            tot = sum(wts.values()) or 1.0
            for h, q in mates:
                own = self._role_value(q, o["pos"])
                extra = min(own + NEWS_KEEP * vac * wts[h] / tot, max(own, NEWS_CAP * vac)) - own
                if extra >= 0.5:
                    hr = self.heirs.setdefault(h, {"extra": 0.0, "parts": [], "from": []})
                    hr["extra"] += extra
                    hr["parts"].append((g, extra))
                    hr["from"].append(wp["name"])
        # One scenario per combination of uncertain return dates, so a handcuff is valued in
        # the weeks he would actually start rather than against an averaged-out starter.
        self.scenarios = [(1.0, {})]
        combos = math.prod(len(o["dist"]) for o in self.out.values())
        if combos <= 64:
            for g, o in self.out.items():
                if len(o["dist"]) > 1:
                    self.scenarios = [(pr * q, {**sc, g: k}) for pr, sc in self.scenarios for k, q in o["dist"]]
        else:
            print(f"!! news: {combos} return-date combinations; using each player's median instead", file=sys.stderr)
            med = {}
            for g, o in self.out.items():
                acc = 0.0
                for k, q in sorted(o["dist"]):
                    acc += q
                    if acc >= 0.5:
                        med[g] = k
                        break
            self.scenarios = [(1.0, med)]

    # ---- projection ---------------------------------------------------------------------
    @staticmethod
    def _status_avail(wp):
        """Availability from the injury report and roster status (not news)."""
        inj = (wp or {}).get("injury") or {}
        avail = inj.get("avail", 1.0) if inj.get("status") else 1.0
        if ((wp or {}).get("status") or "ACT") in ("RES", "IR", "PUP", "INA"):
            avail = 0.0
        return avail

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
        if base is None and ((wp or {}).get("form") or {}).get("games"):
            base = REPLACEMENT.get(pos)
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
        # An heir's preseason number and his box scores both describe the backup job, so the
        # inherited work is added on top of whatever we believed about him, not blended in.
        rate = usage
        heir = self.heirs.get(g) if g else None
        extra = heir["extra"] if heir and usage is not None else 0.0
        if extra:
            usage += extra
            notes.append(f"INHERITS +{extra:.1f}/gm while {', '.join(heir['from'])} out")
        if usage is not None and n:
            notes.append((f"wk1: {form.get('last_pts', 0):.1f} pts" if n == 1
                          else f"wk1-{self.week - 1} avg {form.get('mean_pts', 0):.1f}, last {form.get('last_pts', 0):.1f}"))
        if role_shift:
            notes.append(f"ROLE UP: {ep_ew:.0f} expected pts/gm vs {base:.0f} preseason")

        # matchup
        matchup = 1.0
        if tm.get("bye"):
            av = self._status_avail(wp)
            bye_notes = ["BYE"] + ([f"OUT ({self.out[g]['note']})"] if g in self.out else [])
            p = {"mean": 0.0, "floor": 0.0, "ceil": 0.0, "sd": 0.0, "bye": True, "team": team, "opp": None,
                 "notes": bye_notes, "avail": 0.0, "parts": {}, "g": g, "rate": rate,
                 "avail_future": 1.0 if g in self.out else avail_ros(av)}
            p["ros"] = self.season_points(p) if rate is not None else None
            return p
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
        out = self.out.get(g) if g else None
        if out:
            avail = 0.0
            span = ("season" if out["season"] else f"{out['weeks']} wk" if len(out["dist"]) == 1
                    else "/".join(f"{k} wk {q:.0%}" for k, q in sorted(out["dist"])))
            notes.append(f"OUT ({out['note']}) - {span}")
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

        res = {"mean": mean, "mean_if_plays": mean_if_plays, "floor": floor, "ceil": ceil, "sd": sd,
                "boom": boom, "bust": bust, "avail": avail, "team": team, "opp": opp, "bye": False, "notes": notes,
                "parts": {"base": base, "ewma": ewma, "n": n, "usage_adj": usage_adj, "expert": expert,
                          "matchup": matchup, "implied": tm.get("implied"), "dvp": dvp_f},
                "g": g, "rate": rate, "avail_future": 1.0 if out else avail_ros(avail)}
        res["ros"] = self.season_points(res) if rate is not None else None
        return res

    # ---- the rest of the season, one week at a time -----------------------------------------
    def out_weeks(self, g, sc):
        o = self.out.get(g)
        return 0 if not o else sc.get(g, o["weeks"])

    def week_points(self, p, w, sc=None):
        """Expected points in week w under return-date scenario sc. This week is the full
        projection (matchup, injury tag); later weeks are the per-game rate, zero on his bye and
        while news has him out, plus whatever role he inherits while the player ahead is out."""
        if p is None:
            return 0.0
        if w == self.week:
            return p["mean"]
        if self.byes.get(p.get("team")) == w:
            return 0.0
        sc = sc or {}
        g = p.get("g")
        if g in self.out and w < self.week + self.out_weeks(g, sc):
            return 0.0
        r = (p.get("rate") or 0.0) * p.get("avail_future", 1.0)
        for src, extra in (self.heirs.get(g) or {}).get("parts", []):
            if w < self.week + self.out_weeks(src, sc):
                r += extra
        return r

    def season_points(self, p):
        return sum(pr * sum(self.week_points(p, w, sc) for w in range(self.week, LAST_WEEK + 1))
                   for pr, sc in self.scenarios)

    def season_lineup(self, scored):
        """Sum over the remaining weeks of the best lineup that week, averaged over return-date
        scenarios. A backup is worth exactly the weeks he would start - a bye, an injury - which
        is what a roster spot buys."""
        live = [(e, p) for e, p in scored if p is not None]
        total = 0.0
        for pr, sc in self.scenarios:
            for w in range(self.week, LAST_WEEK + 1):
                pool = [(e, {"mean": self.week_points(p, w, sc)}) for e, p in live]
                total += pr * self.total(self.best_lineup(pool)[0])
        return total

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
    fp_note = f"FantasyPros consensus scraped {W.get('fp_scrape_date')}"
    if W.get("fp_rows_stale") and not W.get("fp_rows_this_week"):
        fp_note = (f"**no FantasyPros consensus** - the {W.get('fp_scrape_date')} scrape is for another week, "
                   f"so projections are usage and matchup only")
    say(f"_Built {W['generated']} from nflverse through week {W['weeks_done'][-1] if W['weeks_done'] else 0}, {fp_note}, Vegas lines from nflverse games.csv._\n")

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
    # What each bench player is worth to THIS roster: the season lineup total with him, minus
    # without him. A backup quarterback scores nothing until the starter's bye, then everything.
    base_ros = E.season_lineup(scored)
    drop_cost = {id(e): base_ros - E.season_lineup([x for x in scored if x[0] is not e]) for e, p in bench}
    say("## Bench\n")
    say("| Player | Proj | Floor-Ceil | ROS pts | Lineup pts lost if dropped | Notes |")
    say("|---|---|---|---|---|---|")
    for e, p in sorted(bench, key=lambda x: -x[1]["mean"]):
        ros = f"{p['ros']:.0f}" if p.get("ros") is not None else "-"
        say(f"| {e['name']} ({e['pos']}) | {p['mean']:.1f} | {p['floor']:.0f}-{p['ceil']:.0f} | {ros} | {drop_cost[id(e)]:.1f} | {'; '.join(p['notes'][:3])} |")
    unscored = [e for e, p in scored if p is None and e["pos"] not in ("K", "DST")]
    for e in unscored:
        say(f"| {e['name']} ({e['pos']}) | ? | | | | no data - not in the model or no 2026 stats yet |")
    say("")

    # ---- WAIVERS -------------------------------------------------------------------------
    say("## Waivers\n")
    base_total = E.total(starters)
    droppable = [(e, p) for e, p in bench if p is not None]
    # The cheapest drop is the bench player whose loss costs the season lineup the least - not
    # the one with the fewest raw points, which would cut the quarterback who covers a bye.
    if droppable:
        drop_e, drop_p = min(droppable, key=lambda x: (drop_cost[id(x[0])], x[1]["ros"] or 0))
    else:
        drop_e = drop_p = None
    # Rest-of-season value is a LINEUP delta, week by week: the optimizer re-run for every
    # remaining week with the add in and each possible drop out, byes and injuries included.
    # Each add is paired with whichever drop leaves the best season lineup.
    has_qb = any(e2["pos"] == "QB" for e2, p2 in scored if p2 is not None)
    rows = []
    for e in waivers["players"]:
        e = dict(e); e["slot"] = "BE"
        p = E.project(e["name"], e["pos"], e.get("team"))
        if p is None:
            rows.append((e, None, None, None, "no data", None))
            continue
        best = None
        for de, dp in (droppable or [(None, None)]):
            after = [(e2, p2) for e2, p2 in scored if e2 is not de] + [(e, p)]
            rd = E.season_lineup(after) - base_ros
            if best is None or rd > best[0] + 1e-9 or (abs(rd - best[0]) <= 1e-9 and de is drop_e):
                best = (rd, de, dp, after)
        ros_delta, de, dp, after = best
        wk_delta = E.total(E.best_lineup(after)[0]) - base_total
        # the season total includes this week; the buckets ask about the weeks after it, or a
        # one-week filler would read as a season-long upgrade
        later_delta = ros_delta - wk_delta
        raw_ros_edge = (p["ros"] or 0) - ((dp or {}).get("ros") or 0) if dp else (p["ros"] or 0)
        if later_delta > 0.5 and wk_delta > 0.5:
            bucket = "season"
        elif later_delta > 0.5:
            bucket = "season-later"
        elif wk_delta > 0.5:
            bucket = "week"
        elif raw_ros_edge > 0 and (e["pos"] != "QB" or not has_qb):
            bucket = "depth"
        else:
            bucket = "pass"
        rows.append((e, p, wk_delta, later_delta, bucket, de))
    order = {"season": 0, "season-later": 1, "week": 2, "depth": 3, "pass": 4, "no data": 5}
    rows.sort(key=lambda r: (order.get(r[4], 9), -(r[3] or 0), -(r[2] or 0), -(r[1]["mean"] if r[1] else 0)))
    if drop_e:
        say(f"Cheapest drop: **{drop_e['name']}** ({drop_e['pos']}) - losing him costs your season lineup "
            f"{drop_cost[id(drop_e)]:.1f} points, the least on your bench.\n")
    say(f"| # | Add | Drop | This week | +lineup this wk | +lineup wk {week + 1}-{LAST_WEEK} | Bucket | Notes |")
    say("|---|---|---|---|---|---|---|---|")
    rank = 0
    for e, p, wkd, rosd, bucket, de in rows:
        if bucket in ("pass", "no data"):
            continue
        rank += 1
        say(f"| {rank} | **{e['name']}** ({e['pos']}, {p['team'] or e.get('team') or '?'}) | {de['name'] if de else '-'} | {p['mean']:.1f} | {wkd:+.1f} | {rosd:+.1f} | {bucket} | {'; '.join(p['notes'][:3])} |")
    if rank == 0:
        say("| - | nobody on the wire improves this roster | | | | | | |")
    passed = [e["name"] for e, p, wkd, rosd, b, de in rows if b == "pass"]
    if passed:
        say("\nNot worth a roster spot - no drop from your bench improves your lineup this week or later: " + ", ".join(passed) + ".")
    nodata = [e["name"] for e, p, wkd, rosd, b, de in rows if b == "no data"]
    if nodata:
        say(f"\nNo data for: " + ", ".join(nodata) + " - not in the model and no 2026 stat line; treat as unknowns.")
    say(f"\n_Rest of season is Weeks {week + 1}-{LAST_WEEK}, one lineup per week, with byes and known absences zeroed; each add is paired with the drop that leaves the best lineup over Weeks {week}-{LAST_WEEK}. Buckets: **season** = improves your rest-of-season lineup and this week; **season-later** = better rest-of-season but not this week; **week** = a one-week filler; **depth** = more raw points than the drop but never starts for you. Priority order is the table order._\n")

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
        if t and (t in fp_dst or not fp_dst):
            d = dict(fp_dst.get(t, {"name": e["name"]}))
            d["name"] = f"**{d.get('name', t)} (mine)**"
            say(dst_row(t, d))
        else:
            say(f"| {e['name']} (mine) | not found in FP | | | |")
    if fp_dst:
        streams = sorted(((t, d) for t, d in fp_dst.items() if d.get("ecr") is not None), key=lambda x: x[1]["ecr"])[:6]
    else:
        # no current consensus: rank by the signal that carries D/ST scoring, the opponent's implied total
        streams = sorted(((t, {"name": t}) for t, tm in E.teams.items() if tm.get("opp_implied") is not None),
                         key=lambda x: E.teams[x[0]]["opp_implied"])[:8]
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
    ap.add_argument("--news", help="JSON of players ruled out (see the module docstring)")
    a = ap.parse_args()
    roster = json.load(open(a.roster))
    waivers = json.load(open(a.waivers)) if a.waivers else {"players": []}
    E = Engine(a.week, json.load(open(a.news)) if a.news else None)
    print(report(a.week, roster, waivers, E))


if __name__ == "__main__":
    main()
