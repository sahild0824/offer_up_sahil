# Week 5 - Kai and his Guy

Built Monday 2026-10-05, after Week 4's Sunday games.
- **Data:** the engine runs on nflverse through Week 4 and Week 5 Vegas lines, with this week's
  news (`examples/news_week05.json`). FantasyPros has not published Week 5 rankings yet.
- **Research:** two agents (`research/week05_research.md`).
- **Trades:** `trades.py` on approximate league rosters (`examples/league_week05.json`).

## You are not screwed - this is a one-week dip

Week 5 is your worst week: two byes (Hubbard, Butker) and three injured starters (Ja'Marr
Chase, Smith, Hall) at once. Even so, the engine has your skill positions at:

| | Skill positions | With kicker and D/ST (about 15) |
|---|---|---|
| Chase plays | 103.6 | about 118 |
| Chase sits | 95.9 | about 111 |

That is close to your Week 4 projection, not a collapse. Hubbard returns in Week 6, Hall and Smith
by Week 6-7, and Chase in Week 7 after the bye. The fix this week is roster mechanics, plus two
trades that make the rest of the season much stronger.

## Do this before Thursday 8:15 PM ET (Pickens kicks off then)

**1. Move Pickens out of FLEX and into Chase's WR slot. Put Chase at FLEX.**
- Chase plays Sunday, but his concussion status may not be final until Friday or Saturday.
- With Chase at FLEX you can swap in any Sunday or Monday player if he is ruled out.
- Left as is, Pickens locks at FLEX on Thursday and only a WR could replace Chase. Your only
  bench WR is Smith, who is about 20% to play.

**2. Kicker: drop Justin Herbert, add Tyler Bass.**
- Bass: BUF @LAR, Monday night, under the SoFi roof, 53.5 total, 6 of 6 on field goals.
- Brandon Aubrey (Thursday) or Jake Bates (DET @ARI, dome) rank higher if either is free.
- An empty K slot scores zero, so this is worth about 8 points.
- Herbert's only remaining job was Goff's Week 6 bye. That game is @KC, the stingiest defence
  against QBs, and a streamer does better (step 5).

**3. Running back: claim Emanuel Wilson (SEA vs SF) and drop Tucker Kraft. Bid about 10% FAAB.**
- Wilson is Seattle's lead back while Jadarian Price (chest) is out: 21 carries and 2 TDs last
  week, and the consensus #1 add this week.
- Expect him to be worth 12-14 this week against Montgomery's 9 (Montgomery is losing goal-line
  work to Woody Marks). The engine has Wilson at only 8.8, because it cannot see Price's absence.
- His value fades when Charbonnet returns (Week 6-7). That is why the bid is modest and the drop
  is Kraft:
  - Kraft's only job is Warren's Week 13 bye, and a TE can be streamed then.
  - Montgomery stays because he is in the trade below.
- If you lose the claim, Montgomery starts at RB2.

**4. Keep the Steelers D/ST** vs IND, a mid-tier start. The Colts fly straight from London and
Daniel Jones threw for 143 yards there.

## Week 5 lineup

| Slot | Player | Note |
|---|---|---|
| QB | Goff | @ARI, DET implied 29 |
| RB | Chase Brown | @MIA (11 catches last week) |
| RB | Emanuel Wilson | If claimed; otherwise Montgomery |
| WR | Pickens | Thursday vs TB |
| WR | Waddle | @LAC |
| TE | Warren | @PIT |
| FLEX | Ja'Marr Chase | If he clears protocol. If not: Montgomery (or Wilson, if both RBs are on the roster) |
| D/ST | Steelers | |
| K | Bass | |

**Bench:** Hubbard (bye), Hall (about 35% to play - if he practises fully and is active, he
outranks Montgomery), Smith (about 20%), Montgomery.

## The trades - send both now

The finder reran on Week 4 data, with Waddle off Hakuna's roster and Andrews off Teemo's.

| To | You give | You get | You, Weeks 5-17 | Them | Market (they get / give) |
|---|---|---|---|---|---|
| **Hakuna Mailata** | Chuba Hubbard + David Montgomery | **Kyren Williams** | **+72** | +28 | 26 / 25 |
| **Soaring Wings** | George Pickens + Breece Hall | **Puka Nacua** | **+81** | +32 | 64 / 61 |

**Kyren Williams (LAR):**
- 36.7 points in Week 4 on 83% of snaps.
- A 25.6 points-a-game form line.
- Goal-line back.

Hakuna gets two starting-calibre backs for one. Hubbard just ran for 122 and 2 TDs, and
Montgomery covers depth. Hubbard's bye this week means he costs you nothing now.

**Puka Nacua (LAR):** back from his hip injury with 27.7 points on 90% of snaps.

Soaring Wings lost Etienne and needs a running back. Hall, when healthy, is an RB1, and Pickens
replaces Nacua's receiver output for them. They come out ahead on market value (64 for 61).

**Both Rams play Monday night**, so if a trade lands before Sunday you still have a late-swap
option.

- **If the Pickens trade lands before Thursday:** Nacua takes Pickens' WR slot and the FLEX
  logic is unchanged.
- **If you still have the Week 4 offers out** (Amon-Ra for Brown and Pickens; Kyren for
  Montgomery and Kraft), withdraw them first. These two replace them, and the Amon-Ra deal no
  longer helps Oh Saquon (+4.5 for them).

## Week 6 (Goff, Chase Brown and Ja'Marr Chase on bye)

**5. Swap the kicker for a QB:**
1. **Jordan Love** vs DAL (Sunday night).
2. **Kirk Cousins** vs BUF (20+ points three straight weeks).
3. Tyler Shough @NYG, if he is free.

Stroud and Brissett are the fallbacks. Butker is back in Week 6, so the streaming kicker is the
drop.

**If both trades land, Week 6 looks like:**

| Slot | Player |
|---|---|
| QB | Love or Cousins |
| RB | Kyren Williams, plus Wilson or Hall |
| WR | Nacua, Waddle (Smith if back) |
| TE | Warren |
| FLEX | Best of the rest |

That is a stronger Week 6 than the one you have now.

## What to check during the week

- **Ja'Marr Chase's protocol progress, Wednesday to Friday.** Cleared means he starts at FLEX.
- **Breece Hall's practice reports.** A full practice Friday makes him the RB2 or FLEX play.
- **Kyle Monangai's thumb.** He is a better back than Wilson if healthy, but not for Week 5.
- **Your Week 5 opponent's lineup.** Send the matchup screen and I will run the head-to-head.

## Update: Liza George (Hurts so Good) turned down Hubbard + Warren for Jonathan Taylor

Her reason: "I can't accept two bench players."

- **On lineups, the offer helped her.** The model has her +22 (and you +43). Her TE Kyle Pitts has
  4.0 points in four games, while Warren has 48.5. Hubbard has 79.0 points to Taylor's 86.2.
- **On trade charts it read as a lowball:** 17 offered for 69. Taylor ranks 6th overall rest of
  season; Hubbard about 95th and Warren about 71st. She is reading names, not production.
- Jayden Daniels is practising and aiming for Week 5, so she does not need a QB.

**Counter with Chase Brown + Tyler Warren for Jonathan Taylor.**
- +33 for you and +33 for her, and fair on charts (63 for 69).
- She gets a top-15 RB to replace Taylor plus a starting TE for her empty slot.
- Suggested message: "Fair - how about Chase Brown + Warren for Taylor? You get a top-15 RB to
  replace him, and Warren starts at TE for you (Pitts has 4 points all season; Warren has 48)."

**It stacks with the other two offers.** Taylor (Brown + Warren), Kyren (Hubbard + Montgomery) and
Nacua (Pickens + Hall) use six different players.

| If these land | Gain over Weeks 6-17 |
|---|---|
| Kyren + Nacua | +102 |
| All three | +136 |

**Revised Week 5 waiver move:** while the Warren counter is out, **keep Kraft.** He becomes your TE
if Warren goes, so skip the Wilson claim this week.
- Each accepted 2-for-1 opens a roster spot, and you can add a back then.
- Montgomery starts at RB2 until a trade lands.
- The kicker swap (Bass for Herbert) still happens.

## Tuesday re-run (2026-10-06): who to pick up

This run uses the new FantasyPros Week 5 rankings, Tuesday's waiver screenshot and Monday's
news:
- **Chase:** "day to day" in protocol; more on Wednesday.
- **Monangai:** his thumb is "not serious".
- **Price:** on IR (at least 4 games), and Charbonnet will not debut in Week 5.
- **Barkley:** hamstring.
- **Bigsby, Adonai Mitchell and Keenan Allen:** tagged OUT.

**1. Kicker: drop Herbert.** Add Tyler Bass (BUF @LAR, Monday, dome), or Aubrey or Bates if
either is free. Swap the kicker for Kirk Cousins (vs BUF) or Jordan Love (vs DAL) in Week 6.

**2. Running back: claim Kyle Monangai and drop David Montgomery** (bid about 10%).

| | FantasyPros Week 5 | Engine |
|---|---|---|
| Kyle Monangai | RB17, 13.8 | 13.7 |
| David Montgomery | RB25, 10.8 | 10.1 |

Worth +2.9 this week and +5.1 over the season.
- If the Kyren offer (Hubbard + Montgomery) is still pending, drop Kraft instead and keep
  Montgomery.
- Emanuel Wilson (RB19, 12.5) is the backup claim.
- Every other add on this wire is worth less than a point.

## Trades, re-run Tuesday (after the Monangai pickup)

1. **Puka Nacua for George Pickens + Breece Hall (Soaring Wings).**
   - +67 for you and +32 for them; fair on value (65 for 61).
   - They have no RB with Etienne out; Hall is an RB1 once healthy.
2. **Kyren Williams for Chuba Hubbard + Tucker Kraft (Hakuna Mailata).**
   - +50 for you and +34 for them. Goedert is out, so Kraft starts at TE for them.
   - It reads light on the September trade chart, which predates Hubbard's season: 79 points
     in 4 games, against Kyren's 90.
   - Pitch it on production.
   - Do not offer Montgomery: he is being dropped for Monangai.
3. **Both together: +116.** Fill the two open spots from the wire with Carnell Tate and a TE
   (Loveland or Andrews).

The Taylor counter (Chase Brown + Warren) is now worth only +25 to you, because Chase Brown is
FantasyPros' RB6 this week. Keep it only if Liza comes back to you.

## Trades on the real rosters (screenshots, 2026-10-07)

You won Week 4, 115.28 to 108.68, so you are 3-1. The Week 4 recap screens show eight of the ten
rosters. They change the picture:
- Soaring Wings added Kamara and Braelon Allen.
- Hakuna added Dalton Kincaid at TE and has Corum and Lloyd behind Kyren.
- Hurts so Good still starts Kyle Pitts at TE.

**1. CeeDee Lamb for Ja'Marr Chase + Tyler Warren (Hurts so Good). +34 for you.**
- Lamb has been the better receiver this year: 41.3 points last week and a 30.7 form average.
- Chase is in concussion protocol with a Week 6 bye.
- Liza gets the bigger name plus a starting TE, and comes out ahead on value (78 for 64), so
  she is likely to say yes.
- Kraft becomes your TE.

**2. Puka Nacua for DeVonta Smith + Breece Hall (Soaring Wings). +50 for you.**
- Both of the players you send are hurt now but are starters when healthy.
- About even on value (58 for 61).

**Both together: +86.** Fill the open spots with Carnell Tate and Colston Loveland or Mark
Andrews.

**Backup:** Kyren Williams for Hubbard + Hall (Hakuna), +40. It uses Hall, so offer it only if
Soaring Wings says no.

**Unverified:** Derrick Henry for Hubbard + Pickens (Audubon) scores +40, and +125 alongside the
other two. Audubon's roster was not in the screenshots, so check it before offering. The Taylor
counter is now the weakest use of Warren (+25).

## Trade accepted (2026-10-07): CeeDee Lamb for Ja'Marr Chase + Tyler Warren

The trade processes Thursday 10/8 at about 7:35 AM.

**Lamb plays Thursday night** (DAL vs TB, 8:15 PM ET), so set him at WR as soon as the trade
processes.

**Week 5 lineup** - skill positions 110.7, about 125 with K and D/ST:

| Slot | Player |
|---|---|
| QB | Goff |
| RB | Chase Brown, Monangai (or Montgomery if the claim missed) |
| WR | Lamb, Pickens |
| TE | Kraft |
| FLEX | Waddle |
| D/ST | Steelers |
| K | Bass |

**Open roster spot (2-for-1):** add the Week 6 QB now, Kirk Cousins vs BUF (+18) or Jordan Love vs
DAL (+16). Goff is on bye in Week 6.

**Next week:** in Week 6, drop the streaming kicker (Butker is back) for a backup TE, Loveland or
Andrews (+10). That covers Kraft's Week 11 bye.

**Still worth sending:** Nacua for Smith + Hall.

## Final plan (Thursday 10/8, after the final news sweep)

This plan comes from the last web sweep (`research/week05_final_sweep.md`), the engine re-run
with that news (`reports/week05_engine.md`, news file `examples/news_week05.json`), and three
reviewer passes:
- **News accuracy:** checked the facts against sources.
- **Lineup math:** an exact re-run over 96 injury scenarios.
- **Move timing:** an exact re-run over 48 scenarios.

The core lineup passed all three reviews. Their corrections to the moves are built into the plan
below.

**Lineup - 106.8 projected, already the best lineup.** The experts agree on every slot.

| Slot | Player | Proj | Note |
|---|---|---|---|
| QB | Goff | 20.8 | DET @ARI, implied 30 points |
| RB | Chase Brown | 17.2 | @MIA, a soft run defense |
| RB | Monangai | 10.6 | 13.3 if he plays (about 80%) |
| WR | Lamb | 21.5 | Tonight vs TB, full practices all week |
| WR | Pickens | 13.8 | Tonight vs TB |
| TE | Kraft | 10.5 | FantasyPros TE8 |
| FLEX | Waddle | 12.5 | Beats Montgomery 61% of the time |
| D/ST | Steelers | 8.1 | Daniel Jones has 7 turnovers; PIT @TB in Week 6 |
| K | Mevis | 7.5 | Monday night, highest total on the slate |

**Moves:**

1. **Today, after the trade processes (about 7:35 AM PT).**
   - Lamb into WR and Kraft into TE.
   - Add **Kirk Cousins** into the open spot, with no drop. He is the Week 6 QB while Goff is on
     bye: +18 over Weeks 6-17.
   - He is on the ESPN free-agent list, 32% rostered. If he is gone, take Love, then Rodgers.
2. **Friday's injury reports.**
   - **Monangai:** if he is active at the inactive list (about 8:30 AM PT Sunday), he starts.
     If he is inactive, Montgomery starts.
   - **Monangai inactive and Hall active:** Hall versus Montgomery is a coin flip.
   - **Waddle:** watch for a foot designation (he wore a walking boot after Week 3). If he gets
     one, settle FLEX before the 10 AM PT lock. Montgomery is the hedge while Monangai plays.
3. **Smith or Hall active.** Bench them anyway.
   - **Smith:** a coin flip with Waddle on the numbers. Benching him is a judgment call for his
     first game back from the hamstring.
   - **Hall:** stays on the bench unless the Monangai branch in move 2 applies.
4. **Montgomery.** Keep him for now.
   - He is the Monangai insurance this week.
   - He is the RB2 if the Nacua fallback below happens.
   - **Colston Loveland's** value is almost all cover for Kraft's Week 11 bye, so there is no
     rush. Add the best TE available after Week 6 by dropping Cousins.
   - If the league has an IR slot and Friday lists Smith or Hall OUT, move him to IR and add
     Loveland now.
5. **Nacua offer (Smith + Hall).**
   - **Keep it open.** The engine has it near +70 for you. On 9/25 FantasyPros values with the
     injury discount it is about even. On today's news it may look lopsided to them.
   - Reconsider only if Nacua has a Friday or Saturday DNP, or a Questionable-or-worse
     designation for Monday. A limited Thursday is his normal load management.
   - An accepted trade cannot be pulled back.
   - **If they decline,** offer Hubbard + Pickens for Nacua after tonight's game (+79 with
     Montgomery kept).
6. **No streams.**
   - Keep the Steelers and Mevis; no wire D/ST or kicker beats them by more than noise.
   - Shipley, Odunze, Brissett and the rest of the wire do not improve the lineup in any week.

**Week 6 preview.** Cousins starts at QB and Hubbard is back.
- If Smith returns, he starts and Waddle sits.
- Expect about 105 points, or about 103 if Smith and Hall both stay out.
- Caleb Williams (hamstring) is a long shot, so expect Bagent at QB for Chicago again.
