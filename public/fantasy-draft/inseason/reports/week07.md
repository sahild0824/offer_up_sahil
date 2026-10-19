# Week 7 plan (Monday 10/19)

**How this was built**
- **Data:** nflverse through Week 6 and FantasyPros ROS ranks from 10/16. The FantasyPros Week 7
  weekly consensus was not out yet, so projections come from usage and matchup only.
- **Research:** three agents, on your roster, waivers and the trade market.
- **Engine runs:** `reports/week07_engine.md` and `reports/week07_trades_finder.md`, plus exact
  injury-scenario checks. The news file is `examples/news_week07.json`.
- **Reviewers:** three, covering news accuracy, roster logic and trade acceptance.

**The roster is assumed, not confirmed.** The plan assumes you made last week's moves (dropped
Monangai, Montgomery and Loveland; added Love and Marks) and that no trade has gone through.
- **League file:** `examples/league_week07.json`. Other teams are as of the Week 6 screenshots.
- **Byes:** BUF, JAX, LAC and WAS.

## News that matters

- **Jalen Hurts is out for the season** (blood clots in his leg and lungs). Tanner McKee starts for
  PHI.
  - DeVonta Smith still saw 14 targets for 20.5 with McKee in Week 6.
  - His rest-of-season ceiling drops, which makes him the right piece to sell.
- **Breece Hall** has missed Weeks 4-6 and has not practiced since the quad injury.
  - He is not on IR: nflverse's "INA" only means he was inactive in Week 6.
  - About 25% to play in Week 7.
- **Montgomery** has had no news since 10/16, and HOU's bye is Week 8. Marks stays the 75-80% lead
  back until Week 9. Do not re-add Montgomery.
- **Lamb** is healthy: 16.0 on 88% of snaps in Week 6.
- **Waddle** is a part-timer in Denver: 65% of snaps, 6.4 / 4.8 / 6.4 in three of his last four.

## Waivers

1. **If ESPN tags Hall O:** move him to the IR slot, which opens a spot with no drop. Then:
   - Claim **Colston Loveland** with no drop. He is your TE2 for Kraft's Week 11 bye (CHI's bye is
     Week 10): +15.7 over Weeks 8-17.
   - He scored 18.5 in Week 6 but averages 7.1, so he is not a Week 7 starter.
   - You dropped him last week, so he is on waivers: claim by Tuesday night.
   - Stack a second claim for **Brenton Strange** (+10.1), also with no drop. It fails automatically
     if Loveland's claim succeeds.
2. **If Hall is not tagged O:** drop **Woody Marks** for Loveland.
   - Marks goes back to a committee (about 7.7 a game) once Montgomery returns in Week 9.
   - The engine puts his drop cost at 0.
3. **Watch Hall's tag after the Wednesday and Thursday practices.** If ESPN changes him to Q while
   he is in IR, adds and trades are blocked until he is moved back to the bench. To make room,
   drop Love or Marks; either costs 0.
4. **Keep Jordan Love** for now. He is about 1 point of Goff insurance, and dropping him before
   Sunday gifts a QB to teams whose QB is on bye. He has no trade value, because free streamers
   exist.
5. **Skip:**
   - Germie Bernard and Omar Cooper. They are the consensus #1 and #2 adds, but are WR5 here.
   - The wire RBs: Kendre Miller, Mike Washington Jr. and Pierce. None of them would start for you.
6. **TE fallback rule:** Pitts and Higbee cannot cover Kraft, because ATL and LAR are also on bye
   in Week 11. They become valid only if McBride arrives (his ARI bye is Week 14).
7. **D/ST and K:** keep the Steelers (@NO in Paris; top tier) and Shrader.

## Lineup

| Slot | Player | Proj | Kickoff (ET) |
|---|---|---|---|
| QB | Goff | 22.3 | vs GB, Sun 1:00 |
| RB | Hubbard | 15.5 | vs TB, Sun 1:00 |
| RB | Chase Brown | 14.4 | @BAL, Sun 1:00 |
| WR | Lamb | 20.0 | @PHI, **Mon** |
| WR | Pickens | 16.4 | @PHI, **Mon** |
| TE | **Kraft** | 11.6 | @DET, Sun 4:25 |
| FLEX | DeVonta Smith | 16.2 | vs DAL, **Mon** |
| D/ST | Steelers | | @NO, Sun 9:30 AM (Paris) |
| K | Shrader | | |

**Rules**
- **Start Kraft, not Loveland.** Loveland plays Thursday, and keeping the TE slot open lets McBride
  start if that trade clears.
- **Decide Smith vs Waddle by Sun 4:05 PM ET**, when Waddle's game starts. After that, no bench
  player can cover a Monday-night scratch.
- **Goff vs Love** is a 60/40 lean to Goff.

## Trades

**Step 0: open ESPN, Team, Pending Moves.** Both offers below are yours from last Wednesday. They
share no player, so keep both open. Resend unchanged if either expired, then message both managers.

| Offer | Engine for you (raw / adjusted) | Them | Acceptance |
|---|---|---|---|
| **Hubbard + Hall for Kyren Williams** (Hakuna Mailata) | +5 / +28 | +38 | about 60-65% |
| **Kraft + Smith + Gordon for Trey McBride** (Soaring Wings) | +16 / +27 | +35 | about 45% |
| Both | +23 / +52 | | |

The adjusted numbers make three corrections:
- Hubbard loses about 15% once Jonathon Brooks returns (Weeks 9-11).
- Gordon is valued at his real lead-back rate.
- Smith is discounted for the McKee offense.

**Kyren deal**
- Kyren's role is stable: 72% of snaps in Weeks 5-6, with Corum at 27-28%. His 9.7 in Week 6 was
  one quiet game.
- **Pitch:** "Allen, Cook, Kincaid and McLaurin are all on bye this week. Hubbard just had 28 carries
  on 94% of snaps and starts for you vs TB. Hall is a free stash who comes back as the Jets' lead
  back."

**McBride deal**
- **Pitch:** "You're 1-4 and short at RB. Three starters for one: Gordon is Miami's lead back with
  Achane out (15.8 a game over Weeks 3-5), Smith just saw 14 targets with McKee, and Kraft
  replaces McBride at TE."
- They must drop one player (Wicks) to accept.
- **Do not switch Smith for Waddle.** Waddle is worth less to them on every chart but one, and that
  version would cancel the offer already in their inbox.

**Fallback, only if Soaring says no:** Chase Brown for Isaiah Likely (Teemo).
- About +22 for you and about 45-50% to be accepted. Teemo needs an RB, and Likely averages 18.2.
- It sells Brown below his chart value, so re-check it on whatever roster you have then.

**Skip**

| Offer | Why |
|---|---|
| Derrick Henry, any version | +6 at best |
| Waddle for LaPorta | NW BIRDIES lose 65 |
| Lamb + Waddle for Nacua | Their manager is your McBride partner; it sells Lamb |
| Anything built on Love | Free QBs on the wire make him worth nothing in a trade |
| Walker or Olave | Inactive manager |
| Both-new combo (Brown + Waddle for Kyren, Kraft + Hall + Gordon for McBride) | About 7% joint acceptance |

## If a trade already went through

- **Kyren done:** you have 1 open spot.
  - Claim Loveland with it; no IR move is needed.
  - If ESPN tags Monangai O, he can go in the empty IR slot.
  - McBride is still the best second deal.
- **McBride done:** you have 2 open spots. Add Loveland (TE2 for ARI's Week 14 bye; Pitts is now
  valid too) and Jalen Coker.
