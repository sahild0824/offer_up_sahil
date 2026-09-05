"""Turn the round-by-round research into structured per-player rows.

The four research sweeps (research/rounds_*.md) are narrative. This encodes them as data: for each
player on a round list, how many distinct outlets argued for and against him, the resulting verdict,
and the one line that decides it. Joined with the model, that gives a signed model-vs-market gap
that can be sorted and charted instead of read.

verdict: consensus  = the market's own pick at that slot
         value      = the market says he is cheaper than he should be
         split      = outlets are genuinely divided
         fade       = most outlets say pass at this price
         reach      = he goes several rounds later than this slot
"""
import json
from pathlib import Path

HERE = Path(__file__).parent

# (player, round, for, against, verdict, note)  -- counts are distinct outlets in research/rounds_*.md
V = [
 ("Jahmyr Gibbs", 1, 6, 0, "consensus", "Near-unanimous 1.01; CBS calls passing on him at 1 a league-losing mistake."),
 ("Bijan Robinson", 1, 6, 1, "consensus", "Field Yates' RB1; five more 20-point PPR games than Gibbs over two years."),
 ("Ja'Marr Chase", 1, 5, 2, "consensus", "WR1 on five boards; only knock is Burrow's health and a minor knee hyperextension."),
 ("Puka Nacua", 1, 4, 4, "split", "The industry default at 1.04, but side work Aug 31 and an open NFL review with no Week 1 deadline."),
 ("Jaxon Smith-Njigba", 1, 3, 1, "consensus", "FantasyPros No. 7 and the accepted fallback; FTN fades him slightly on the coordinator change."),
 ("Amon-Ra St. Brown", 1, 3, 0, "value", "4for4 and the Footballguys thread list him at 4-6; PFN calls him one of the safest picks in fantasy."),
 ("Jonathan Taylor", 1, 3, 1, "value", "ADP 1.07 everywhere; elite floor, conditional ceiling. Nobody puts him at 4 in PPR."),
 ("Christian McCaffrey", 1, 2, 3, "fade", "SI lists him among three early-round busts; even PFN wants him at 7-8, and 4for4 only in standard."),
 ("Chase Brown", 2, 6, 1, "consensus", "The most-endorsed round-2 back: CBS 'perfect second-round pick', PFN 'belongs at the 1/2 turn'."),
 ("Omarion Hampton", 2, 3, 2, "split", "Underdog No. 15 and named Week 1 starter, but Yahoo's 'RB16 on RB16 usage' and FTN's cold water."),
 ("Kenneth Walker III", 2, 3, 2, "split", "PFF names him a pick-4 target; PFN says his price is steamed up after the Super Bowl MVP run."),
 ("De'Von Achane", 2, 2, 3, "split", "Yates RB5 and the clear upside play, but Miami cut Tua and Hill and traded Waddle."),
 ("James Cook III", 2, 2, 2, "reach", "Consensus RB5 but he comes off boards at the 1-2 turn, so he rarely reaches 17."),
 ("Derrick Henry", 2, 3, 2, "fade", "Age 32, no receiving floor; no back since 2000 has averaged 16 a game at 32 or older."),
 ("Saquon Barkley", 2, 2, 2, "split", "ETR prefers him to Jefferson and Lamb; FTN calls him the worst pick of round 1."),
 ("Ashton Jeanty", 2, 1, 4, "fade", "Ankle sprain Aug 23, DNP Sept 2. Yahoo: everything points to him playing except practice."),
 ("Brock Bowers", 3, 4, 2, "split", "CBS and Yahoo say as early as mid round 2; ten picks ahead of the FFC and Underdog boards."),
 ("Drake London", 3, 5, 2, "consensus", "Karabell tier 1, but Tua struggled so badly in camp that Penix may start."),
 ("Nico Collins", 3, 5, 2, "consensus", "Karabell tier 1 and the target tree just thinned: Higgins tore an ACL, Dell out four games."),
 ("A.J. Brown", 3, 4, 1, "value", "Now a Patriot with Vrabel and Maye; PFN sees top-five upside if the touchdowns bounce back."),
 ("Chris Olave", 3, 2, 0, "value", "Karabell tier 2 and one of FTN's best-pick-of-the-round names; we were missing him."),
 ("George Pickens", 3, 3, 3, "split", "The most-cited regression call in this range, but our model has him at bust 21."),
 ("Malik Nabers", 3, 3, 5, "fade", "Would not commit to Week 1; DK Network calls him the biggest unknown in football."),
 ("Breece Hall", 3, 2, 2, "split", "Reich wants to run, but RotoBaller asks if he is overvalued and the Jets' QB room is shaky."),
 ("Tee Higgins", 4, 6, 1, "value", "PFN ranks him WR14 against a WR19 ADP; SI picks him over both Wilson and Egbuka."),
 ("Zay Flowers", 4, 4, 1, "value", "Heath Cummings' top draft target; RotoWire leans him over Higgins specifically in PPR."),
 ("Garrett Wilson", 4, 3, 2, "split", "Karabell WR10 on a 30% target share, but Geno Smith may not change much."),
 ("Tetairoa McMillan", 4, 3, 2, "split", "Undisputed Carolina WR1; the whole bet is whether you trust Bryce Young."),
 ("DeVonta Smith", 4, 3, 2, "value", "With A.J. Brown gone CBS expects his best season; Yahoo also lists him among WR busts."),
 ("Ladd McConkey", 5, 3, 1, "value", "4for4 calls him a bargain at WR20; McDaniel arrives and Keenan Allen left for the Colts."),
 ("Colston Loveland", 5, 4, 1, "consensus", "TE3 at ADP 48 with the upside to be the TE1; Chicago's schedule is the caution."),
 ("Emeka Egbuka", 5, 3, 3, "split", "League-winning upside, but three weeks without practice on turf toe and SI cut him to WR26."),
 ("Quinshon Judkins", 5, 3, 3, "split", "Fantasy Life's perfect mid-round back; CBS wants the later side of 4-6, PFN says priced too high."),
 ("Rome Odunze", 5, 2, 1, "value", "Bears WR1 after the DJ Moore trade; the Sept 3 practice exit was cramps."),
 ("Travis Hunter", 5, 2, 2, "reach", "ADP 69 and Jacksonville plans to use him more as a defensive back."),
 ("Lamar Jackson", 5, 2, 2, "fade", "ADP 56 with a career-worst 26.8 rushing yards a game; FantasyPros ran the case against."),
 ("Cam Skattebo", 5, 1, 4, "fade", "SI's most overvalued player, a Rotoworld top fade, on PFF's avoid list."),
 ("Luther Burden III", 6, 2, 0, "value", "Ben Johnson said he is buying stock; slot receivers have always produced in his offense."),
 ("MarShawn Lloyd", 6, 4, 1, "value", "Bumped 60 spots to top-65 after Jacobs went on the exempt list; over-under about six games."),
 ("Drake Maye", 6, 4, 0, "consensus", "350.9 points last season and he added A.J. Brown and Doubs; the tier's best name."),
 ("Jayden Daniels", 6, 3, 2, "split", "Rushing edge over Burrow, but knee, hamstring and elbow limited him to seven games in 2025."),
 ("Joe Burrow", 6, 2, 2, "value", "ADP drifted from the late 50s into the 70s and 80s; missed seven games in two of three years."),
 ("Jalen Hurts", 6, 3, 1, "split", "Fantasy Life priority target; new coordinator and no A.J. Brown is the sticking point."),
 ("Bucky Irving", 6, 3, 2, "split", "NBC and PFN say rebound; CBS's Cummings has him on the do-not-draft list."),
 ("Chris Godwin Jr.", 6, 0, 2, "reach", "ADP 128. Yahoo: the name is more valuable than the projection."),
 ("Harold Fannin Jr.", 7, 3, 0, "value", "ESPN's unquestioned No. 1 in Cleveland, TE4 in two ranking sets, four TE1 weeks in his last five."),
 ("Tucker Kraft", 7, 4, 2, "consensus", "Cleared for full contact and will play Week 1, but zero preseason snaps and a slow-ramp warning."),
 ("Justin Herbert", 7, 2, 1, "value", "Reworked mechanics under McDaniel; CBS puts him in the rounds 6-7 QB group."),
 ("Caleb Williams", 7, 3, 1, "value", "QB8 last year and rising; SI says there is little reason to force the first name from this tier."),
 ("Sam LaPorta", 8, 2, 2, "split", "Petzing's arrival is the case; ADP 111 and a summer hip scare are the caution."),
 ("Kyle Pitts Sr.", 8, 2, 1, "value", "Fair from the middle of round 7 in full PPR, but the advice is explicitly do not chase him."),
 ("Jaylen Warren", 8, 2, 0, "value", "ADP slipped into the late 80s with his starting role intact; Draft Sharks calls it exceptional value."),
 ("Jadarian Price", 8, 3, 1, "value", "Slid toward pick 90 on preseason caution; Charbonnet's knee opens the job."),
 ("TreVeyon Henderson", 8, 2, 2, "split", "ADP fell from the mid-40s to the late 80s on the ankle; cleared, but Stevenson grades better."),
 ("Bhayshul Tuten", 8, 2, 2, "fade", "PFN: his ADP spiked on opportunity, not production."),
 ("Blake Corum", 9, 6, 1, "consensus", "The most-cited handcuff in football: 39% of carries and 55% inside the five from week 10 on."),
 ("Kyler Murray", 9, 5, 0, "value", "Going in the 10th round and a QB1 in points per game every year he has played eight games."),
 ("George Kittle", 9, 4, 2, "split", "Activated from PUP with a legitimate chance at Week 1; our model still has him at bust 99."),
 ("Stefon Diggs", 9, 5, 2, "split", "NFL.com's tenth-round sleeper; he is 33 and our model has him at boom 20, bust 98."),
 ("Dalton Kincaid", 9, 3, 1, "value", "Led all tight ends in targets and points per route in 2025 with the Bills ready to expand his role."),
 ("Jordan Mason", 10, 5, 1, "value", "PFF sleeper with weekly must-start upside behind a 31-year-old Aaron Jones."),
 ("Isaiah Likely", 10, 4, 0, "value", "Followed Harbaugh to the Giants and projects as the No. 2 target behind Nabers."),
 ("Jaxson Dart", 10, 3, 1, "value", "FantasyPros lists him among five QB2s with a real path to a top-five finish; ADP is this exact pick."),
 ("Matthew Stafford", 10, 2, 2, "reach", "ADP 75-76 makes him a round-8 name, and his 7.7% touchdown rate has to regress."),
 ("Josh Downs", 10, 2, 2, "split", "ESPN calls him a lower-risk flier; the Keenan Allen signing and a calf injury cut the ceiling."),
 ("Tyler Allgeier", 11, 3, 2, "value", "A Week 1 flex if Jeremiyah Love (50-50) sits, but blocked again once Love is healthy."),
 ("Jonathon Brooks", 11, 2, 0, "value", "ESPN's bust-to-boom candidate at ADP 125 with Carolina confident in the recovery."),
 ("Kyle Monangai", 11, 4, 1, "split", "An elite handcuff on talent, but week-to-week with a knee and may miss Week 1."),
 ("RJ Harvey", 11, 2, 2, "fade", "Dobbins sits atop the depth chart and Denver drafted Jonah Coleman; he is a passing-down back."),
 ("Keaton Mitchell", 11, 3, 3, "fade", "Six straight practices missed; Hampton is the clear lead back."),
 ("Rachaad White", 11, 1, 3, "fade", "Croskey-Merritt has the edge, and White has had a hamstring since Aug 19."),
 ("Ja'Kobi Lane", 12, 6, 1, "value", "Baltimore's new No. 2 opposite Flowers with stated red-zone usage, at ADP 172."),
 ("Caleb Douglas", 12, 5, 1, "value", "Played 100% of Miami's first-team snaps on the starters' lone preseason drive; Week 1 starter."),
 ("De'Zhaun Stribling", 12, 5, 1, "split", "Zooming up boards since Pearsall's season-ending injury, but Deebo Samuel is back."),
 ("Mike Washington Jr.", 12, 4, 1, "value", "CBS: one of the best handcuffs in fantasy, an immediate volume RB2 if Jeanty misses time."),
 ("Kaelon Black", 12, 5, 0, "value", "The only healthy back behind McCaffrey and he handled the starters' workload in preseason."),
 ("Chris Rodriguez Jr.", 12, 2, 1, "fade", "Just 2.9% of his touches are receptions, which caps him badly in full PPR."),
]

def main():
    players = json.loads((HERE / "data" / "players.json").read_text())
    P = {p["name"]: p for p in (players["players"] if isinstance(players, dict) else players)}
    rows, missing = [], []
    for name, rnd, nfor, nagainst, verdict, note in V:
        p = P.get(name)
        if not p:
            missing.append(name)
            continue
        total = nfor + nagainst
        lean = (nfor - nagainst) / total if total else 0.0        # -1 all against .. +1 all for
        adp, comp = p.get("adp"), p.get("comp")
        gap = round(adp - comp, 1) if adp and comp else None       # + = market lets him fall past our rank
        rows.append({"name": name, "id": p["id"], "pos": p["pos"], "round": rnd,
                     "for": nfor, "against": nagainst, "lean": round(lean, 2), "verdict": verdict, "note": note,
                     "comp": comp, "adp": adp, "gap": gap,
                     "boom": p.get("boom"), "bust": p.get("bust"), "risk": p.get("risk"), "sit": p.get("sit"),
                     "proj": p.get("proj")})
    if missing:
        raise SystemExit(f"unmatched players: {missing}")
    # Finding 8 of research/red_team_2.md: a search for reasons to draft someone returns bullish
    # copy, so raw counts are a coverage measure, not a verdict. The corpus runs about two thirds
    # positive; scoring each player against that base rate is what makes "well liked" mean
    # anything, and a player nobody argued against is marked uncontested rather than unanimous.
    BF, BA = sum(r["for"] for r in rows), sum(r["against"] for r in rows)
    base = BF / (BF + BA) if (BF + BA) else 0.5
    for r in rows:
        tot = r["for"] + r["against"]
        share = r["for"] / tot if tot else base
        r["baseRate"] = round(base, 3)
        r["lean"] = round(share - base, 2)          # + = better liked than the corpus average
        r["uncontested"] = r["against"] == 0 and r["for"] >= 2
    rows.sort(key=lambda r: (r["round"], -r["lean"]))
    (HERE / "data" / "market_verdicts.json").write_text(json.dumps(rows, indent=1))
    print(f"{len(rows)} players across rounds {min(r['round'] for r in rows)}-{max(r['round'] for r in rows)}")
    from collections import Counter
    print("verdicts:", dict(Counter(r["verdict"] for r in rows)))
    print(f"corpus base rate: {rows[0]['baseRate']:.0%} of citations are positive; lean is measured against that")
    print(f"uncontested (no counter-argument found): {sum(1 for r in rows if r['uncontested'])} players")
    print("\nBest liked relative to the base rate:")
    for r in sorted(rows, key=lambda r: -r["lean"])[:5]:
        print(f"  R{r['round']:2d} {r['name']:24s} {r['for']}-{r['against']}  lean {r['lean']:+.2f}")
    print("Most contested:")
    for r in sorted(rows, key=lambda r: r["lean"])[:5]:
        print(f"  R{r['round']:2d} {r['name']:24s} {r['for']}-{r['against']}  lean {r['lean']:+.2f}")
    print("\nBiggest model-vs-market gaps (+ = market lets him fall past our composite):")
    for r in sorted(rows, key=lambda r: -abs(r["gap"] or 0))[:10]:
        print(f"  R{r['round']:2d} {r['name']:24s} {r['verdict']:9s} comp {r['comp']:6.1f} adp {r['adp']:6.1f} gap {r['gap']:+6.1f}")
    print("\nwrote data/market_verdicts.json")


if __name__ == "__main__":
    main()
