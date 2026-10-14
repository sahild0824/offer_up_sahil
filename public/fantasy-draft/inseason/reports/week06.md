# Week 6 plan (Wednesday 10/14)

You are 3-2 after the Week 5 loss. This week's opponent is Oh Saquon You See (2-3).

**Byes:** CIN, DET, MIA and MIN. That costs you Goff, Chase Brown and Ollie Gordon II.

**How this was built**

- **Rosters:** all ten rosters from today's matchup screenshots (`examples/league_week06.json`).
- **Data:** nflverse data through Week 5 and FantasyPros Week 6 (scraped 10/14).
- **Research:** three research agents: your roster, waivers and the trade market.
- **News file:** `examples/news_week06.json`.
- **Engine runs:** `reports/week06_engine.md` and `reports/week06_trades_finder.md`, plus exact
  injury-scenario checks.
- **Reviewers:** three, covering news accuracy, roster and lock logic, and trade acceptance.

## Do first: fix the IR slot

Monangai is in IR with a **Q** tag. On ESPN, an IR player who loses his O/IR tag blocks every add
and every trade until he leaves the slot.

**Drop Monangai.** Turf toe is expected to keep him out until somewhere in Weeks 6-8. On his return
he is Swift's backup, and the engine rates his drop cost at 0.0.

## Waivers

None of the players below is on any of the ten rosters, so they should show as FA. If one shows WA,
claim Marks before Love: more teams need an RB than a QB.

| Move | Week 6 | Weeks 7-17 | Why |
|---|---|---|---|
| Add **Jordan Love**, drop **Colston Loveland** | +18.8 | -9.5 (recovered Tuesday) | You have no QB (Goff bye). Love is QB5 at 20.2 vs DAL on SNF. Fallbacks: Cousins or Shough, then Winston. |
| Add **Woody Marks**, drop **David Montgomery** | +8.1 | 0.0 | Montgomery: groin, week to week, likely out through Week 7, then HOU's Week 8 bye; a committee back on return. Marks: 85% of snaps and 19 touches in Week 5; FP RB20. |

**Dropping Gordon instead of Loveland** costs nothing in the engine. But Gordon has scored 14.5,
18.0 and 14.8 the last three weeks as Miami's lead back. He also gives you RB depth and a trade
piece (see the McBride offer below). The Week 11 TE value from Loveland comes back on Tuesday when
Love becomes a TE.

**Tuesday after Week 6**
- Drop Love.
- Add a TE for Kraft's Week 11 bye: Freiermuth (+10.4), Strange or Andrews.

**Not worth it:** Denzel Boston. Swapped for Hall, Smith, Loveland or Love, he costs points
because he would not start for you.

## Lineup

| Slot | Player | Proj | Kickoff (ET) |
|---|---|---|---|
| QB | Jordan Love | 19.6 | SNF 8:20 PM |
| RB | Chuba Hubbard | 13.7 | 1 PM |
| RB | Woody Marks | 9.9 | 9:30 AM London |
| WR | George Pickens | 15.5 | SNF |
| WR | **Jaylen Waddle** | 10.5 | **Thu 8:15 PM** |
| FLEX | CeeDee Lamb | 16.0 (18.8 if he plays, 85%) | SNF |
| TE | Tucker Kraft | 11.4 | SNF |
| D/ST | Steelers | 10.0 | 1 PM |
| K | Spencer Shrader | 10.7 | 1 PM |

The engine has this lineup at about 117 against the opponent's 75 as currently set. If they start
Walker, it is about 97.

**Rules**

- **Waddle in a WR slot, not FLEX, before Thursday.** He locks then. With Lamb at FLEX, an RB (Hall)
  or a WR (Smith) can still replace Lamb.
- **Lamb call.** Make it Sunday between 11:30 AM and 1 PM ET, after the 1 PM inactives are out.
  Every bench option plays at 1 PM, and nobody can replace him after SNF inactives.
  - Start Lamb unless reports lean toward him sitting.
  - Bench him if he is tagged D or O.
- **Friday option.** If Hall or Smith is ruled O, move him to the free IR slot and add a player:
  - Freiermuth if Lamb is healthy;
  - Rachaad White (WAS, Monday night) if Lamb is a true game-time decision. He is the only kind of
    player who could cover a late Lamb scratch.
  - On Tuesday, drop Love **before** activating anyone from IR.

## Trades

**Before sending anything**
1. Clear the IR slot (above).
2. Cancel last week's pending offers on ESPN's Trades tab: Walker/Olave, Smith + Hall for Nacua,
   and any old Kyren offer.

**1. Hakuna Mailata: Hubbard + Hall for Kyren Williams. Send now.**
- **Gain:** +50.8 for you, +7.2 for them; +8.8 for you in Week 6 if it clears before Sunday.
- **Acceptance:** about 55%. The charts make it fair: RSJ 1.38, CBS about 1.0.
- **Pitch:** "Hubbard's a bell cow (19.8 a game) with his bye already done. He covers your Week 7
  Bills bye, when Cook, Kincaid and Allen are all out, and Hall is a free stash."
- **Don't lead with Smith + Hall.** Hakuna is 3-2 and would get two injured players.

**2. Soaring Wings: Kraft + Smith + Gordon for Trey McBride. Send at the same time.**
- The two offers share no player.
- **Gain:** +56.7 for you, +11.6 for them. Together with #1: +78.8.
- **Acceptance:** about 45%. They are 1-4 and short at RB.
- **Pitch:** "Three weekly starters for one: Gordon (Miami's lead back), Smith (a WR2 when healthy)
  and Kraft (a top-8 TE) to replace McBride."
- **If Gordon is already gone:** Kraft + Smith for McBride is +46.3 for you, +5.0 for them, but
  harder to sell.
- **If it goes through:** McBride is your TE, and the two open spots go to a TE2 and depth (Higbee,
  Freiermuth, Odunze).

**Backup, only if Hakuna says no: Audubon Condors, Chase Brown + Hall for Derrick Henry.**
- **Gain:** +37.6 for you, +26.1 for them. Acceptance about 35%.
- They can accept after Sunday's games to keep Henry's Week 6 points.

**Skip**

| Offer | Why |
|---|---|
| Walker or Olave deals | That manager looks inactive (Walker on their bench, Henderson D starting); the realistic versions cost them 23-38 points. |
| Lamb + Hubbard for Nacua | About a 50% overpay, and it sells Lamb low. |
| Anything with Waddle | He locks Thursday. |
| Anything with Pickens | Hold until Lamb has played a full game. |
| Jefferson + Likely for Pickens + Hall | Fragile: negative if the incoming players hit 85% of projection. Look again after Week 6. |
