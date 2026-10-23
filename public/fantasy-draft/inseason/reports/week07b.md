# Week 7 plan, Friday 10/23 (real rosters)

**How this was built**
- **Rosters:** all ten rosters from the Thursday-night screenshots (`examples/league_week07b.json`).
- **Data:** refreshed with the FantasyPros Week 7 scrape (10/22).
- **Engine:** `reports/week07b_engine.md` and `reports/week07b_trades_finder.md`, plus exact
  injury-scenario checks of every trade idea. Gains are lineup points over Weeks 8-17.
- **Research agents:** two.
  - **Lineup news:** Wednesday-Thursday practice reports. Friday designations were not posted yet,
    and DAL and PHI post theirs Saturday.
  - **Waivers and trades:** CBS (Dave Richard) and RotoStreetJournal Week 7 trade charts.

**Where you stand**
- 4-2. The Week 7 opponent is Hakuna Mailata; ESPN gives you 61%.
- **Surplus:** three QBs (Love, Goff, Lamar).
- **Weak spots:**
  - TE: Kraft is 9.4 a game and his bye is Week 11.
  - RB depth: Hall has missed Weeks 4-6, Monangai is O, and Hubbard's role shrinks when Brooks
    returns (around Weeks 9-11).
- **Bye problems ahead:**
  - Week 10: Smith and Waddle.
  - Week 11: Kraft and Love.
  - Week 14: Lamb and Pickens.

## Week 7 lineup

| Slot | Player | Note |
|---|---|---|
| QB | **Jordan Love** | Experts rank him above Goff this week. Sore back, but full practice Thursday. Lamar is ~50% on a limited ankle. |
| RB | Chase Brown, Chuba Hubbard | |
| WR | Pickens, DeVonta Smith | Pickens: shoulder, limited, beat writer not worried, ~90%. Smith: DNP Thursday (hamstring + toe), ~60%. |
| TE | Kraft | |
| FLEX | Lamb | |
| D/ST | Steelers | |
| K | Butker | |

**Bench:** Goff, Lamar, Hall (~35%), Waddle (chest, ~90%), Harrison Jr.

**The one decision: Smith, by Sun 1:05 PM PT** (Waddle's kickoff). Nobody on your bench plays
Monday, so this is the last chance to protect the Monday WR slots.
- If Smith is Doubtful or Out on Saturday's report, or misses practice again, start **Waddle**
  instead.
- Do the same for Pickens if he is unexpectedly Doubtful.

**If the Love trade below goes through before Sunday,** start **Goff**.

## Waivers

1. **Drop Marvin Harrison Jr.** (19% of snaps, 3.9 a game) **and add Ollie Gordon II.**
   - He is Miami's lead back: 18-88-1 in Week 5 and FantasyPros RB20 this week, with his bye
     already done.
   - The engine sees him as depth only, so the gain is insurance, not points. But you are
     thin at RB: Hall has missed Weeks 4-6, Monangai is out, and Brooks returns to cut into
     Hubbard's work.
2. **Week 11 TE.** If the Likely trade below fails, use a later spot on **Brenton Strange** (+10.1).
   - Other options: Juwan Johnson or Mark Andrews.
   - **Not** Higbee or Hunter Henry: both are on bye in Week 11 too.
3. **Skip Kamara.** He is 31, has a back injury, and is in a three-way committee once Etienne
   returns.

## Trades: turn the extra QBs into a TE and a better RB

| # | Offer | You (Wks 8-17) | Them (engine) | Charts (they get / give) |
|---|---|---|---|---|
| 1 | **Teemo: Love + Waddle for Isaiah Likely** | +57.9 | -2.3 | CBS 16 / 18 |
| 1b | Teemo: Love + Monangai for Likely (or add Monangai to #1 as a sweetener) | +56.5 | +19.5 | CBS ~10 / 18 |
| 2 | **Hakuna: Hubbard + Hall for Kyren Williams** (your pending offer) | +22 raw / +38 adjusted | +30 / +12 | CBS 57 / 36 (generous) |
| 2b | Hakuna: Hubbard + Waddle for Kyren (if Waddle isn't used in #1) | +24 / +39 | +1 / -18 | CBS 42 / 36 |
| 3 | Audubon: Lamar + Chase Brown for Derrick Henry (if Hakuna says no) | +27.8 | +10.4 | CBS 34 / 35 |
| 4 | Audubon: Love for Colston Loveland (cheap Week 11 TE fix if Teemo says no) | +15.7 | +2.8 | CBS 7 / ~4 |

"Adjusted" accounts for Hubbard losing work once Brooks returns. **#1 and #2 together: +75 raw,
+91 adjusted** (Likely for Love + Monangai combined with Kyren for Hubbard + Waddle; the same
total holds for the Love + Waddle and Hubbard + Harrison Jr. pairing).

**Why Likely**
- He averages 18.2 PPR on 9.8 targets: a WR2-level TE.
- His NYG bye is Week 8, when Kraft covers; Kraft's bye is Week 11, when Likely covers.
- Teemo dropped Lamar, so Caleb Williams is their only QB (CHI bye Week 10).
- Davante Adams is on IR, so Waddle fills a real WR hole for them.
- **Pitch:** "You need a QB for Caleb's bye and a WR with Adams out. You have two starting TEs
  with Hockenson back."

**Why Kyren**
- Hakuna has only three WRs and the Week 7 byes.
- Hubbard is at his peak trade value: CBS 33, more than Brown or Hall.
- Kyren is FantasyPros ROS #16 vs Hubbard's #27.
- Hall is unlikely to play this week, so the offer is cheap for you to keep open.

**Skip**
- **Kraft + Waddle for LaPorta.** Even on the charts, but NW BIRDIES lose 31 in the engine.
- **Kraft + Lamar for McBride.** Soaring loses 42.
- **Lamar + Pickens for Olave.** Only +8 for you.
- **Goff + Pickens for Olave.** -18 for you.
- **Goff for anything.** He is your best QB the rest of the way.

## The plan to win the league

1. **Convert the QB surplus** into Likely (TE) and the RB surplus into Kyren. That means
   **Love, Waddle, Hubbard and Hall out; Likely and Kyren in.** You keep Goff as QB1 and
   Lamar as backup or trade bait.
2. **Rebuild RB depth from the wire:** Gordon now. Monangai comes back in Weeks 8-9.
3. **Bye map after the trades**
   - **Week 8:** NYG (Likely) and HOU. Kraft covers.
   - **Week 10:** PHI (Smith). Gordon and Kyren cover.
   - **Week 11:** GB (Kraft) and LAR (Kyren). Likely and Gordon cover.
   - **Week 14:** DAL (Lamb and Pickens). This is the one to plan for: get WR depth (Downs or
     Keenan Allen) before Week 14.
4. **Revisit Lamar after his first healthy game.** He is a strong trade chip for a QB-needy
   team (Audubon after Hurts; Oh Saquon for Stroud's Week 8 bye).
