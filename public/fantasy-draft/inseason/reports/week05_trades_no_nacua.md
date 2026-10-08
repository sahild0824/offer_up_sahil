# Week 5 trades without Nacua (Thursday 10/8)

Puka Nacua is off the table: the Soaring Wings manager won't move him. This report searches
every other team for a trade.

**How it was checked**

- **Trade finder.** `trades.py --exclude "Puka Nacua"` on today's rosters
  (`examples/league_week05_thu.json`):
  - your side: Lamb in, Chase and Warren out, Cousins in the open spot;
  - Hurts so Good: Chase and Warren added.
- **Market values.** FantasyPros rest-of-season ranks, refreshed to the 10/2 scrape.
- **News file.** `examples/news_week05.json`, plus this sweep's sourced injury updates, saved as
  `examples/news_week05_trades.json`.
- **Research agents.** Five agents:
  - Kyren and Hakuna's needs;
  - Henry and Amon-Ra;
  - Olave, Collins, Jefferson and McBride;
  - your outgoing players;
  - Week 5 trade-value charts: CBS, Boone, RotoStreetJournal and FantasyPros buy/sell lists.
- **Exact injury scenarios.** An engine pass re-scored every candidate with exact injury scenarios.
  The finder collapses injuries to medians.
- **Three reviewers:**
  - acceptance: would that manager say yes?
  - news accuracy: re-checked against the official 10/7 practice reports;
  - math: an independent re-computation.

All gains are your best-lineup points over Weeks 6-17. The free move available without any
trade, dropping Montgomery for Loveland, is worth +10.3. Most two-for-one gains include it,
because the open spot gets the best free agent.

## Send

**1. Kyren Williams + Blake Corum for Chuba Hubbard + Breece Hall (Hakuna Mailata)**
- **Gain:** +38 for you; +49 for Kyren alone with Mark Andrews in the open spot. Hakuna gains
  +16.
- **Most likely yes.** Every chart values your side higher: CBS 47 vs 29, Boone 89 vs 60,
  RotoStreetJournal 3468 vs 2796.
- **His role.** Kyren is a clear lead back.
  - Out-snapped Corum 70 to 13 in Week 4, scoring 36.7 PPR.
  - Corum has no red-zone carry this year.
  - No 2026 injury report entries.
- **Breaks even** if Kyren falls to 77% of his projection.
- **Ask for Corum as a throw-in.** He is the handcuff, which the engine does not value. If they
  balk, drop Corum. Hold Montgomery back as the counter if they ask for Week 5 help.
- **Timing.** Kyren plays Monday night, and Hubbard is on bye with Hall out. Tell them they can
  accept after Monday's game.
- **Pitch:** "You get two starting backs for one. Hubbard is back in Week 6 next to Cook, and Hall
  takes your FLEX once his quad clears."

**2. Kenneth Walker III for Chase Brown + Tucker Kraft (Oh Saquon You See) - check their roster
first**
- **Gain:** +59 for you, the biggest single gain found; about +5 a week from Week 6.
- **Why them.** Their drafted TE, Colston Loveland, is on your waiver wire. Achane is out for the
  season.
  - They get Chase Brown as a starting RB and Kraft as their TE.
  - You add Loveland as your TE.
- **Their side.** The model has them at +42, and the market is 64 for 71, right at the 90% floor.
- **This hinges on their real roster.** It is still the draft roster. Only send it if they have no
  starting TE and Walker is still there.
- **Sensitivity:** Walker at 90% of his projection +34; at 80% +10.
- **Send after Sunday's games.** Walker is on bye this week (KC Week 5), and you need Brown and
  Kraft on Sunday.
- **Shares no player with #1.** Together they are +97 with Corum, or +107 without.

## Hold back (send only if #1 says no)

| Offer | You | Them | Note |
|---|---|---|---|
| Chris Olave for Hubbard + Pickens (Oh Saquon) | +51 | +4 | Most robust; breaks even at 75%. Send after tonight's game. Olave's Wednesday DNP was a rest day. |
| Derrick Henry for Hubbard + Pickens (Audubon) | +38 | +30 | Easiest Henry deal to sell (A.J. Brown is on IR). Audubon's roster is draft-based. |
| Derrick Henry for Chase Brown + Monangai (Audubon) | +37 | +37 | Even on CBS (38 v 38); sells Monangai before Swift is healthy. Conflicts with #2. |

**Henry risk:** he is 32, and Lamar Jackson has only an outside chance to play this week, so
Huntley may start. The engine cannot see a QB downgrade. At 80% of his projection, every Henry
deal is about zero.

## Skip

- **Justin Jefferson** (Teemo). Only about +2 a week, and his ankle was limited Wednesday.
  - Teemo's real need is a healthy RB, which Hall isn't.
  - If you try anyway, offer Hubbard + Pickens for Jefferson + Likely.
- **Nico Collins** (Rowan). +33, but it goes to about zero with a hamstring re-injury. It also
  forces Rowan to drop Bucky Irving.
- **Trey McBride** (Soaring Wings). An overpay (152%). The ARI bye stacks with Lamb and Pickens
  in Week 14.
- **Zay Flowers.** +12, foot and hamstring, and Huntley may be at QB.
- **Rashee Rice**, and anything built on Monangai + Montgomery. These are the two-bench-players
  packages Liza already said she won't take.
- **Kenneth Walker for Chase Brown + Hubbard.** It costs Oh Saquon their RB depth. Use the Kraft
  version.

## Before sending

- **Cancel any pending offer that shares a player.**
  - The Smith + Hall for Nacua offer, and any older Kyren offer, must go before #1.
  - An accepted trade can't be withdrawn, and two accepted offers with the same player can't
    both process.
- **Open the Oh Saquon You See and Audubon Condors rosters on ESPN.** Both files are still the
  draft rosters.
- **Thursday and Friday practice reports were not out when this ran.** Re-check Olave, Hall,
  Smith and Monangai before sending anything that includes them.

## Corrections from the reviewers (folded in above)

- D'Andre Swift was not benched. Ben Johnson denied it, and Swift has a hip/knee injury.
- The players absorbing Smith's targets are Wicks, Lemon and Ertz, not Goedert. Goedert is out
  for Week 5 with the MCL.
- The Ekeler-to-Carolina risk for Hubbard is stale. Jonathon Brooks (IR) is about a Week 9-11
  return.
- Lamar Jackson's ankle is worse than the news file assumed.
- Fixed in `trades.py`: wire fills skipped only your own roster, so players on other rosters
  (Cousins, Lemon, Loveland) could be added for free. Fills now skip anyone on any roster in the
  league file.
- Removed from the league file, because both are on the 10/8 wire screenshots:
  - Loveland from Oh Saquon;
  - Lemon from Soaring Wings.

## Finder output (Nacua excluded, corrected wire)

_Season lineup points over Weeks 6-17; market values from FantasyPros ROS overall ranks scraped 2026-10-02, discounted for news. Your baseline: 1298 points._

| Team | You give | You get | You +pts | They +pts | Market (they get / give) | Note |
|---|---|---|---|---|---|---|
| Oh Saquon You See | Chase Brown, Tucker Kraft | Kenneth Walker III | +58.5 | +41.6 | 64 / 71 | you add Colston Loveland from the wire |
| Oh Saquon You See | Chase Brown, Tucker Kraft | Amon-Ra St. Brown | +40.2 | +76.7 | 64 / 67 | you add Colston Loveland from the wire |
| Hakuna Mailata | Chuba Hubbard, Breece Hall | Kyren Williams | +48.6 | +17.7 | 33 / 33 | you add Mark Andrews from the wire |
| Audubon Condors | Chase Brown, Kyle Monangai | Derrick Henry | +37.2 | +37.2 | 63 / 54 | you add Colston Loveland from the wire |
| Oh Saquon You See | Chuba Hubbard, George Pickens | Chris Olave | +52.8 | +4.3 | 56 / 58 | you add Mark Andrews from the wire |
| Audubon Condors | Chuba Hubbard, George Pickens | Derrick Henry | +39.6 | +28.6 | 56 / 54 | you add Devaughn Vele from the wire |
| Audubon Condors | Breece Hall, George Pickens | Derrick Henry | +46.5 | +9.8 | 60 / 54 | you add Devaughn Vele from the wire |
| Hakuna Mailata | Chuba Hubbard, Breece Hall | Kyren Williams, Blake Corum | +38.1 | +17.7 | 33 / 36 |  |
| Hakuna Mailata | Chuba Hubbard, Breece Hall | Kyren Williams, MarShawn Lloyd | +38.1 | +17.7 | 33 / 34 |  |
| Teemo | Breece Hall, George Pickens | Isaiah Likely, Justin Jefferson | +37.6 | +9.6 | 60 / 59 |  |
| Teemo | Chuba Hubbard, George Pickens | Isaiah Likely, Justin Jefferson | +31.8 | +17.6 | 56 / 59 |  |
| Teemo | Breece Hall, George Pickens | T.J. Hockenson, Justin Jefferson | +29.7 | +17.5 | 60 / 58 |  |
| Soaring Wings | Chase Brown, Tucker Kraft | Dontayvion Wicks, Trey McBride | +28.0 | +20.7 | 64 / 42 |  |
| Soaring Wings | Chase Brown, Tucker Kraft | Trey McBride, Tyler Shough | +28.5 | +14.3 | 64 / 43 |  |
| Rowan's Rowdy Team | Chuba Hubbard, DeVonta Smith | Nico Collins | +32.7 | +4.3 | 49 / 49 | you add Colston Loveland from the wire |
| Soaring Wings | Chase Brown, Tucker Kraft | Trey McBride, Travis Etienne Jr. | +28.0 | +12.4 | 64 / 45 |  |
| Rowan's Rowdy Team | Chuba Hubbard, DeVonta Smith | Nico Collins, Michael Mayer | +31.8 | +4.3 | 49 / 49 |  |
| Quinshon Chud-Wins | Kyle Monangai, Tucker Kraft | Juwan Johnson | +21.4 | +11.4 | 9 / 5 | you add Colston Loveland from the wire |
| Rowan's Rowdy Team | Chase Brown, Kirk Cousins | Nico Collins | +26.0 | +1.7 | 61 / 49 | you add Jordan Love from the wire |
| Quinshon Chud-Wins | Kyle Monangai, George Pickens | Christian Watson, Juwan Johnson | +23.8 | +0.6 | 49 / 37 |  |
| Quinshon Chud-Wins | Kyle Monangai, DeVonta Smith | Christian Watson, George Kittle | +21.9 | +3.1 | 43 / 39 |  |
| NW BIRDIES | Kyle Monangai, Tucker Kraft | Harold Fannin Jr. | +18.9 | +5.7 | 9 / 8 | you add Colston Loveland from the wire |
| NW BIRDIES | Chuba Hubbard, DeVonta Smith | Zay Flowers | +12.5 | +3.6 | 49 / 51 | you add Colston Loveland from the wire |
| NW BIRDIES | Kyle Monangai, David Montgomery | Bhayshul Tuten | +10.3 | +6.4 | 22 / 22 | you add Colston Loveland from the wire |
| Hurts so Good | Kyle Monangai, Kirk Cousins | Jayden Daniels | +10.1 | +5.2 | 4 / 4 | you add Colston Loveland from the wire |
| Hurts so Good | Kyle Monangai, David Montgomery | Rashee Rice | +10.3 | +2.9 | 22 / 24 | you add Colston Loveland from the wire |
| Hurts so Good | Kyle Monangai, David Montgomery | Jameson Williams | +10.3 | +2.9 | 22 / 18 | you add Colston Loveland from the wire |

## Follow-up: Chase Brown + George Pickens for Kenneth Walker III + Chris Olave (Oh Saquon)

These numbers come from the exact-scenario engine. A follow-up research pass and an adversarial
verifier checked them.

**The 2-for-2 as asked.**
- **For you:** +116 over Weeks 6-17, about +10 a week, and +12.7 in Week 6.
- **It is a lowball.** CBS has their side at 55 vs 89 (62%), RotoStreetJournal at about 61%, and
  FantasyPros ranks at 85%.
- **Their lineup loses 123-133** whatever TE or waiver back you assume they added. Walker and
  Olave simply outscore Brown and Pickens by about 11 a week.
- **No 2-for-2 from your roster reaches the 90% fairness floor.**

**Walker health.** He is clean: no 2026 injury designation.
- He is a bellcow: 18-24 carries and 68-82% of snaps, with 27.5 PPR a game.
- His KC bye was Week 5, so there is none left.
- Playoff schedule: NE, SF, @LAC.

**Olave health.** He was limited Thursday 10/8 with a foot injury (Wednesday was a rest day).
Check Friday's designation.

**Counter that keeps the Kyren offer alive.** Hubbard and Hall are both in the Hakuna offer.

| Offer to Oh Saquon | You | Them | Market | With Kyren deal too |
|---|---|---|---|---|
| Brown + Pickens + DeVonta Smith | +112 | -103 | 105% FP-rank weighting; CBS 77 v 89 | +150 total |
| Brown + Pickens + Monangai + Smith (if they counter) | +98 after Kyren | -72 | 107% | +136 total |
| Brown + Pickens + Hubbard (only if no Kyren deal) | +114 | -75 | 94%; CBS 80 v 89 | conflicts |

**Corrections to earlier advice.**
- **The Brown + Pickens + Hall version is not fair** on raw chart sums: CBS 87%, RSJ 81%. The
  finder's "97%" counts the extra players at half value.
- **Kenneth Walker for Chase Brown + Kraft (offer #2 above) only helps them if they have no TE.**
  With any TE it is about -45 for them, so check their roster first.

**Timing.** Send after Sunday's games.
- Pickens plays tonight and Brown plays Sunday, but Walker is on bye.
- An accepted trade that clears before Sunday costs you about 8.6 in Week 5.
- A 3-for-2 needs an open spot on their roster, for example Achane to IR.
