#!/usr/bin/env python3
"""Find trades that improve your season lineup AND look fair to the other manager.

    python3 trades.py --week 4 league.json [--news news.json] [--waivers waivers.json]

league.json: {"me": "<your team>", "teams": {"<team>": ["Player Name", ...], ...}} - skill players
only (QB/RB/WR/TE); names resolve with the intake matcher.

For every other team, every 1-for-1, 2-for-1, 1-for-2 and 2-for-2 swap is scored three ways:

  you       the change in your season lineup (weeks after this one through 17, byes and
            news absences included - weekly.py's week-by-week optimizer). Getting back fewer
            players than you send opens a spot, filled with the best free agent from --waivers;
            getting back more forces your cheapest drop.
  them      the same for their roster. A trade only survives if it does not hurt them: the
            best offers solve a problem they have (a hole from an injury, a bye crunch).
  market    FantasyPros rest-of-season overall rank as a trade-chart value, 80*exp(-rank/40),
            discounted for news since the scrape. The side taking two-for-one counts its
            second player at half (a roster spot is not free). They must receive at least 90%
            of what they give up, or the offer reads as a lowball.

Rosters are what you say they are; a stale roster gives stale answers.
"""
import argparse
import csv
import itertools
import json
import math
import sys
from pathlib import Path

import intake
import weekly

HERE = Path(__file__).resolve().parent
ROS_CSV = HERE.parent / "data" / "ros_overall.csv"
SLOTS = weekly.SLOTS
FLEX_POS = weekly.FLEX_POS


def market_values(E):
    """Trade-chart value by (norm name, pos) from the FantasyPros ROS overall ranks."""
    vals = {}
    if not ROS_CSV.exists():
        print(f"!! {ROS_CSV} missing - market check disabled", file=sys.stderr)
        return vals, None
    with open(ROS_CSV) as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        vals[weekly.norm_name(r["player"]) + "|" + r["pos"]] = 80.0 * math.exp(-int(r["rank"]) / 40.0)
    return vals, rows[0].get("scrape_date") if rows else None


def lineup_week(pool):
    """pool: list of (pos, pts). Best lineup total for one week (QB, 2 RB, 2 WR, TE, FLEX)."""
    by = {"QB": [], "RB": [], "WR": [], "TE": []}
    for pos, v in pool:
        if pos in by:
            by[pos].append(v)
    for v in by.values():
        v.sort(reverse=True)
    total, rest = 0.0, []
    for pos, k in SLOTS:
        total += sum(by[pos][:k])
        if pos in FLEX_POS:
            rest += by[pos][k:]
    return total + (max(rest) if rest else 0.0)


class Valuer:
    def __init__(self, E, first_week):
        self.E = E
        self.weeks = list(range(first_week, weekly.LAST_WEEK + 1))
        self.cache = {}

    def points(self, key):
        """key = (name, pos) -> per-scenario list of per-week points."""
        if key not in self.cache:
            p = self.E.project(key[0], key[1])
            self.cache[key] = [[self.E.week_points(p, w, sc) for w in self.weeks] for _, sc in self.E.scenarios]
        return self.cache[key]

    def season(self, roster):
        tot = 0.0
        for si, (pr, _) in enumerate(self.E.scenarios):
            for wi in range(len(self.weeks)):
                tot += pr * lineup_week([(k[1], self.points(k)[si][wi]) for k in roster])
        return tot

    def cheapest_drop(self, roster, protect=()):
        base = self.season(roster)
        best = None
        for k in roster:
            if k in protect:
                continue
            loss = base - self.season([x for x in roster if x != k])
            if best is None or loss < best[0]:
                best = (loss, k)
        return best


def resolve(names, players):
    out = []
    for n in names:
        p, _ = intake.match(n, players)
        if not p:
            print(f"!! no match for {n!r}", file=sys.stderr)
            continue
        if p["pos"] in ("QB", "RB", "WR", "TE"):
            out.append((p["name"], p["pos"]))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--week", type=int, required=True)
    ap.add_argument("league")
    ap.add_argument("--news")
    ap.add_argument("--waivers", help="waivers.json from intake.py, to fill a spot a 2-for-1 opens")
    ap.add_argument("--first-week", type=int, help="first week the trade counts (default: next week)")
    ap.add_argument("--top", type=int, default=3)
    ap.add_argument("--json", help="also write every surviving trade to this file")
    a = ap.parse_args()

    E = weekly.Engine(a.week, json.load(open(a.news)) if a.news else None)
    V = Valuer(E, a.first_week or a.week + 1)
    mv, scrape = market_values(E)
    players = intake.load_players()
    league = json.load(open(a.league))
    me = league["me"]
    rosters = {t: resolve(ns, players) for t, ns in league["teams"].items()}
    fa = []
    if a.waivers:
        fa = [(e["name"], e["pos"]) for e in json.load(open(a.waivers))["players"] if e["pos"] in ("QB", "RB", "WR", "TE")]

    def market(k):
        v = mv.get(weekly.norm_name(k[0]) + "|" + k[1], 1.0)
        g = E.gsis_for(*k)
        o = E.out.get(g)
        if o:   # news since the scrape: pay for the weeks he will actually play
            exp_out = sum(w * q for w, q in o["dist"])
            v *= max(0.0, 1 - exp_out / E.weeks_left)
        return v

    def received(ks):
        vs = sorted((market(k) for k in ks), reverse=True)
        return vs[0] + 0.5 * sum(vs[1:]) if len(ks) > 1 else (vs[0] if vs else 0.0)

    mine = rosters[me]
    my_base = V.season(mine)
    base = {t: V.season(r) for t, r in rosters.items() if t != me}

    def my_after(give, get):
        r = [k for k in mine if k not in give] + list(get)
        note = ""
        extra = len(get) - len(give)
        if extra > 0:
            for _ in range(extra):
                loss, k = V.cheapest_drop(r, protect=get)
                r.remove(k)
                note += f"; you drop {k[0]}"
        elif extra < 0 and fa:
            for _ in range(-extra):
                gain, k = max(((V.season(r + [f]) - V.season(r), f) for f in fa if f not in r), default=(0, None))
                if k and gain > 0.05:
                    r.append(k)
                    note += f"; you add {k[0]} from the wire"
        return V.season(r), note

    def their_after(t, give, get):
        r = [k for k in rosters[t] if k not in get] + list(give)
        return V.season(r)

    results = []
    for t, theirs in rosters.items():
        if t == me:
            continue
        for ng, nr in ((1, 1), (2, 1), (1, 2), (2, 2)):
            for give in itertools.combinations(mine, ng):
                for get in itertools.combinations(theirs, nr):
                    # market: they must get at least 90% of what they give, and I should not
                    # pay more than 150% (a lopsided offer is a signal to the room, not a trade)
                    they_get, they_give = received(give), received(get)
                    if they_get < 0.9 * they_give or they_get > 1.5 * they_give + 3:
                        continue
                    mine_after, note = my_after(give, get)
                    d_me = mine_after - my_base
                    if d_me < 2.0:
                        continue
                    d_them = their_after(t, give, get) - base[t]
                    if d_them < 0:
                        continue
                    results.append({"team": t, "give": [k[0] for k in give], "get": [k[0] for k in get],
                                    "d_me": d_me, "d_them": d_them, "they_get": they_get, "they_give": they_give,
                                    "note": note.lstrip("; ")})

    wk = f"Weeks {V.weeks[0]}-{V.weeks[-1]}"
    print(f"# Trade finder - Week {a.week}\n")
    print(f"_Season lineup points over {wk}; market values from FantasyPros ROS overall ranks scraped {scrape}, "
          f"discounted for news. Your baseline: {my_base:.0f} points._\n")
    results.sort(key=lambda r: -(r["d_me"] + 0.5 * min(r["d_them"], r["d_me"])))
    print("| Team | You give | You get | You +pts | They +pts | Market (they get / give) | Note |")
    print("|---|---|---|---|---|---|---|")
    shown = {}
    for r in results:
        if shown.get(r["team"], 0) >= a.top:
            continue
        shown[r["team"]] = shown.get(r["team"], 0) + 1
        print(f"| {r['team']} | {', '.join(r['give'])} | {', '.join(r['get'])} | {r['d_me']:+.1f} | {r['d_them']:+.1f} | "
              f"{r['they_get']:.0f} / {r['they_give']:.0f} | {r['note']} |")
    if not results:
        print("| - | no trade helps both sides at a fair price | | | | | |")
    if a.json:
        json.dump(results, open(a.json, "w"), indent=1)


if __name__ == "__main__":
    main()
