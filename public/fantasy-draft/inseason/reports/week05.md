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
