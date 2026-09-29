# Week 4 - Kai and his Guy vs Teemo

Built Tuesday 2026-09-29, evening. Engine: nflverse through Week 3 and Week 4 Vegas lines, run
with this week's injury news (`examples/news_week04.json`). There is **no current FantasyPros
consensus**: the mirror still holds Week 3 rankings, so the engine now discards them. Research
ran in two rounds, 14 agents in all, followed by a completeness critic, four follow-ups, a
synthesis, and three independent skeptics per proposed move. Full record:
`research/week04_first_round.md`, `research/week04_rerun.md`, `research/week04_verification.md`.
Neither Reddit thread you sent could be read, because Reddit is blocked from this sandbox.

## The matchup

**You are the favourite: about 75-80% with Hall benched, and 62% if Hall stays in the lineup and
sits.** Moving Hall to the bench is worth more than any waiver move this week.

- **Hall:** right quad, week-to-week. Monday's MRI was better than feared, but every outlet
  expects him to miss @CHI and ESPN projects him at 0.0.
- **Teemo:** realistic median about 102 on the engine's scale (110-114 on ESPN's), against your
  roughly 123.
- **Jefferson:** about a coin flip to play. O'Connell said the ankle sprain "avoided anything
  long-term".
- **Teemo's late-swap problem:** his backups lock early (Diggs 9:30 AM, Harrison Jr. 1 PM). If
  Jefferson is a game-time call at 4:05, Teemo has nothing on his roster to swap in.
- **Teemo's D/ST:** the Panthers lost CB Jaycee Horn for 6-12 weeks, which also helps Goff on
  Sunday night.

## Start this

| Slot | Player | Engine | Why |
|---|---|---|---|
| QB | **Jared Goff** | 19.2 | @CAR, Sunday night. DET implied 27.0; CAR without both starting corners. |
| RB | **Chase Brown** | 14.6 | vs JAX. Best game environment on the roster (CIN implied 27.0). The Week 3 dip was team volume; his 70% snap share held. |
| RB | **Chuba Hubbard** | 12.8 | Move him from FLEX into Hall's slot. 84% snaps, 19 carries to Dillon's 4 in Week 3. Ranked about RB9-12 this week. |
| WR | **Ja'Marr Chase** | 20.4 | vs JAX. 12 targets (32%) last week. |
| WR | **DeVonta Smith** | 14.3 | vs LAR. 100% snaps, Goedert still out. |
| TE | **Tyler Warren** | 13.3 | @WAS, **9:30 AM ET Sunday**, so set it Saturday night. WAS allows the most TE points; 29% target share. |
| FLEX | **George Pickens** | 14.1 | From the bench. Targets 6, 8, 11; expected points 8.9, 14.2, 21.6. A lean over Montgomery, not a lock (see below). |
| D/ST | **Steelers** @CLE (Thursday) | | About DST5. CLE implied 18.0, a 38.5 total, CLE's center in concussion protocol. Swap only if the Minnesota claim below clears before Thursday 8:15 PM ET. |
| K | Butker | | @LV, dome, KC implied 26.0. |

**Bench:** Breece Hall (out - bench him, don't drop him), David Montgomery, Tucker Kraft, and
whoever survives the claims below.

**Changes from your current lineup:** Hall to the bench, Hubbard from FLEX to RB, Pickens into
FLEX.

## The one real decision: Pickens or Montgomery at FLEX

**Pickens, about 58/42.** Earlier today I told you the engine had Montgomery at 14.9 and
starting. That came from a bug, now fixed. The engine's recent-form average gave each player's
first game half the weight, so Montgomery's 28.9-point Week 1 counted for more than the two
games since (4.4, 6.8). With the weighting corrected:

| | Engine (corrected) | Week 4 rank (published lists) | Trend |
|---|---|---|---|
| Pickens | 14.1 | about WR13-20 | Targets and expected points rising every week |
| Hubbard | 12.8 | RB9-12 | Lead back since Brooks went on IR |
| Montgomery | 12.0 | RB18-22 | Expected points 23.0, 5.8, 8.0 |

Montgomery's case is the matchup: DAL allows 24.9 RB points a game and HOU is implied for 25.
His case against is a 63/37 split with Woody Marks, who scored the 1-yard touchdown last week.
Pickens and Montgomery both kick off at 1 PM, so there is no late-swap angle.

**Pivot to Montgomery** if Stingley is confirmed shadowing Pickens, or Pickens shows up on the
injury report.

## Waivers - what to claim tonight

Each move below was checked by three independent skeptics. Three of the six moves in the first
plan did not survive; what follows is what did, with the changes they forced.

| # | Add | Drop | Bid | Why |
|---|---|---|---|---|
| **1** | **Braelon Allen** (RB, NYJ) | **Justin Herbert** | about **10% FAAB** | Hall insurance and Week 5-6 bye cover. He is not a Week 4 starter: he ranks 4th for your FLEX behind Hubbard, Pickens and Montgomery. |
| **2** | **Minnesota D/ST**, only if it is on your wire | **Rome Odunze** | 1-2% | vs MIA: implied 13.5, the lowest of the week. MIA is without Achane; MIN has 14 sacks in three games. Worth about +2.5 points of win probability over the Steelers. |

**On Allen.** He is the clear lead back while Hall is out, per Rich Cimini (via CBS). CBS
projects him for 19 touches and 12.3 points. Isaiah Davis has not played an offensive snap.

- **Hall's return, my estimate from the reporting:** Week 5 about 30%, Week 6 about 35%, Week 7
  about 20%, later about 15%.
- **Why the bid is modest:** your Week 5-6 byes are already mostly covered by Montgomery and
  Pickens. The engine values Allen at +1.8 lineup points for the season on your roster, more if
  Hall's absence runs long.
- **What to bid:** the consensus 15-35% FAAB is for teams that need him to start. Bid about
  10%. If your league uses rolling priority and you are near the top, do not spend that slot
  on him.
- **If you miss him:** do not chase Gordon or Kamara.

**On Herbert.** His only job on your roster is Goff's Week 6 bye, and that game is @KC, the
defence allowing the fewest QB points in the league (8.9 a game). Any Week 6 streamer beats him.
He is on this week's FantasyPros, PFF and Yahoo drop lists.

**This drop only works if you stream a QB in Week 6** (see the bye plan). Without one, you lose
about 12 points that week.

**On Minnesota.** If the claim clears, start MIN over PIT, but keep PIT. Pittsburgh's next four
are good (vs IND, @TB, @NO, vs CLE).

- **Cut in verification:**
  - **Baltimore:** a coin flip with the Steelers.
  - **Seattle:** 97% rostered, and no better.
- **Why Odunze is the drop:** 7.2, 7.3 and 7.4 points; fourth on CHI in targets; a backup QB
  until Caleb Williams returns (Week 5-6). He never makes your best lineup, so losing him costs
  about 0.5 points all season.

**Optional, Friday.** If the Minnesota claim fails and Jefferson is officially ruled **Out**,
pick up Jordan Addison as a free agent and drop Odunze. It is mostly about keeping him from
Teemo, who would otherwise have a 4:05 PM replacement. Worth about +2 points of win
probability. Otherwise skip it.

### Considered and not claimed

- **Juwan Johnson for Kraft** (all three skeptics refuted it). His snap share is sliding into a
  platoon with Noah Fant: 84%, then 53%, then 62%, with Fant at 57% in Week 3. A backup TE only
  plays for you in Warren's Week 13 bye.
  - **Check after his Monday night game:** if he gets at least 60% of snaps and 6 targets,
    claim him for Kraft in Week 5 at a minimum bid.
  - The engine likes him (+4.1), but on the Week 1-2 role the platoon may already be eroding.
- **Isaiah Likely.** Jaxson Dart is out for the regular season, and Likely scored 8.3 and 3.3
  with Winston. The Giants also traded for J.J. McCarthy.
- **Ollie Gordon II.** The most-added player on Sleeper (5 million adds).
  - A Gordon/Wright committee is likely: Wright is about 55-60% to play and listed ahead of him
    on the depth chart.
  - MIA is implied for 13.5 @MIN.
  - His Week 6 bye lands in your worst week.
  - On your roster he would never start. Fine for teams short on running backs; not for you.
- **Kenyon Sadiq** (check whether he is on your wire). His Week 13 bye is the same as Warren's,
  and his breakout came with Mason Taylor and Adonai Mitchell both out.
- **Keenan Allen.** The best short-term WR on the wire, but a fourth receiver does not start for
  you. A minimum three-game suspension is coming, earliest Week 8.
- **Kalif Raymond.** A 90% catch rate that will regress. Without the fix above, the engine had
  him above DeVonta Smith.
- **Carnell Tate.** The best long-term WR on the wire, if you ever want a fourth receiver.
- **Tyreek Hill.** Unsigned and coming off an ACL. His agent expects a signing around October.
  Watch only.
- **Alvin Kamara.** A lead role only while Etienne is out, split with Kendre Miller, and his
  Week 8 bye is the same as Montgomery's.
- **Every quarterback.** Stream one in Week 6 instead of carrying one through Young's Week 5
  bye.

## Weeks 5-8

**Week 5 - Hubbard and Butker on bye; Hall probably still out**

| Slot | Plan |
|---|---|
| QB | Goff |
| RB | Brown, plus Montgomery - or Allen, if the Jets confirm him as the lead and Hall is out |
| WR | Chase, Smith |
| TE | Warren |
| FLEX | Pickens |
| D/ST | PIT vs IND |
| K | Streamer. After Week 5 waivers, drop the MIN rental (or Odunze) for one. |

Kickers to check first: McPherson (CIN @MIA), Loop (BAL @ATL, dome), Bates (DET @ARI), Aubrey
(DAL vs TB, Thursday), Mevis (LAR vs BUF, Monday). Most likely free: **Tyler Bass** (BUF @LAR,
dome, 52.5 total), then Borregales (NE vs LV), Ryland, Shrader.

**Week 6 - Goff, Chase Brown and Ja'Marr Chase on bye**

| Slot | Plan |
|---|---|
| QB | Streamer, replacing the kicker (see below) |
| RB | Hubbard, Montgomery |
| WR | Smith, Pickens |
| TE | Warren |
| FLEX | Hall if he's back (about 65%), otherwise Allen |
| D/ST | PIT @TB |
| K | Butker |

QB streamers, in order:
1. **Tyler Shough** (NO @NYG) - check first, in case he is free.
2. **Bryce Young** @PHI - PHI allows 20.7 QB points a game.
3. **Jordan Love** vs DAL - DAL allows 23.5.
4. Cousins (vs BUF, dome).
5. Watson.
6. Brissett.
7. Darnold (Thursday).

**Week 7:** Full lineup. Drop the streamer and leave the spot open. Only add a receiver if an
injury opens a hole; Carnell Tate first if you want one anyway.

**Week 8:** Montgomery's bye. No hole.

**Looking ahead:**
- **Week 9:** PIT D/ST bye; stream a defence.
- **Week 13:** Warren and Hall bye; Kraft (or Juwan, if he earns the Week 5 claim) covers TE.

## Only you can check these

- **Waiver type:** FAAB or rolling priority, and where your priority sits.
- **Availability:** is Minnesota D/ST on the wire? Are Kenyon Sadiq, Chris Bell and Jaylen Wright?
- **IR slot:** does the league have one? If ESPN moves Hall to Out or IR, put him there. That
  frees a spot to keep Odunze or add Juwan later.
- **Wednesday:** the Jets' Hall update. IR or a multi-week timeline makes Allen a Week 5-7
  starter (over Montgomery).
- **Thursday:** the Steelers secondary (Jalen Ramsey's wrist, Brandin Echols' concussion).
- **Friday:** Jefferson's designation (the Addison trigger), any Stingley-on-Pickens plan, and
  Nico Collins' status.

## What changed in the engine this week

Five fixes, each found while building this report:

1. **Stale expert rankings.** FantasyPros rows for another week's game are now dropped. The 9/28
   scrape was still Week 3's; the old run had blended those projections in.
2. **Injury news.** `--news` marks players out, spreads their role across named heirs, and takes
   a spread of return dates. Braelon Allen went from 4.5 to 11-12 with Hall out, matching CBS
   and ESPN.
3. **Rest of season, one week at a time.** The engine now simulates Weeks 5-17 with byes and
   absences, so a backup quarterback is worth exactly his starter's bye week. The bench table
   shows what each player's loss costs the season lineup.
4. **Recent form.** The average was seeded with the first game, which ended up with half the
   weight after three weeks. It is now properly weighted: Montgomery 14.9 to 12.0, Pickens
   13.0 to 14.1.
5. **Players with no preseason projection** now start from a replacement-level baseline instead
   of taking their form at face value. Raymond went from 14.3 to 10.4 (ESPN: 10.1).
