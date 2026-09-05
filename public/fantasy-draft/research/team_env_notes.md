# 2026 Offensive Environment Notes (compiled 2026-09-05, Week 1 in five days)

## How this was built / caveats
- Direct fetch of every fantasy, sports, sportsbook, Wikipedia and NFL.com page was blocked by the egress proxy; the only readable sources were **WebSearch result snippets** (search-engine summaries, sometimes contradictory) and **nflverse data files on GitHub** (rosters 2022-2026, 2026 depth charts dated 2026-09-04, play-by-play 2022-2025, draft picks). The WebSearch budget was exhausted after ~31 queries (shared session cap), so several per-team tendency articles could not be pulled.
- Anything backed only by a single snippet, or by my own inference, is marked **[UNVERIFIED]**. Numbers were never guessed: `null` in the JSON means not found.
- **Computed fields (from nflverse pbp, regular season only):** "neutral" = Q1-Q3 with score within 8; pass rate = pass plays / (pass+run) excluding kneels/spikes; pace = drive time of possession / plays on drives that began in neutral situations (rank 1 = fastest); top-RB carry share = leading RB's share of RB/FB carries; TE/RB target share = share of team targets. These were attributed to play-callers by mapping each coach to the teams/years he called plays.
- **Vacated targets/carries** = 2025 regular-season targets/carries by players who were on that team in 2025 and are NOT on that team's 2026 Week 1 roster (includes traded, released, retired, and unsigned players; excludes injured players still on the roster). Denominators are the team's 2025 totals.
- **Week 1 QB / starters** = pos_rank 1 on the nflverse 2026 depth chart (dated 2026-09-04) cross-checked against ESPN/SI/NFL.com snippets. Roster status codes from the 2026 Week 1 roster file: RES = reserve (IR/PUP), EXE = Reserve/Exempt, DEV = practice squad.
- **Win totals**: NFL_Stats X post (Fanatics/DraftKings lines) plus Yahoo/FOX/Fanatics snippets; ARI and MIA were 3.5 at one book earlier in the summer and 4.5 in the most recent snippets (4.5 used). ATL 6.5 came from a single snippet that conflicted with "Titans are the only 6.5 on the Fanatics board" [UNVERIFIED].
- **OL ranks**: PFF 2026 preseason confirmed only DEN 1, PHI 2, TB 3. Ranks for CHI 6, LAR 9, BAL 13, DET 14, NE 19, MIN 20, KC 21, CIN 25, HOU 30, CLE 32 came from an **unnamed ranking quoted in a search snippet** [UNVERIFIED - could be a non-PFF source]. The same snippet had ATL 7th, which contradicts FantasyPros ("one of the worst units"), so ATL was left null. 4for4 run-block tiers: top-5 LAR, SF, DEN, DAL, IND; bottom-5 NO, WAS, CIN, CLE, MIA; KC very good pass-block.
- **Implied PPG**: only DAL 25.75 (4th) was quoted (RotoWire). Ordering from snippets: LAR 1st, BUF 2nd, DAL 4th, with CIN and DET in the top 5. Full table lives behind Sharp/FirstDown tools that could not be fetched.
- **League-wide context (PFF)**: league neutral pass rate hit a multi-year low of 57.44% over the last two seasons; play volume trending down; pre-snap motion at an all-time high (63.9%); 10 new head coaches (ties record), 21 new OCs, 18 new play-callers (ESPN).

## Sources used
### Coaching staffs / play-callers
- NFL.com: Which new head coach will win most in 2026 (ranking of all 10) - https://www.nfl.com/news/which-new-nfl-head-coach-will-win-most-in-2026-jesse-minter-and-joe-brady-top-my-ranking-of-all-10
- Yahoo: Meet the NFL's new head coaches in 2026 - https://sports.yahoo.com/articles/meet-nfls-head-coaches-2026-080002508.html
- ESPN: Who calls plays for every NFL team in 2026 - https://www.espn.com/nfl/story/_/id/49711157/nfl-playcallers-32-teams-mike-mcdaniel-sean-mcvay-mike-mccarthy
- Acme Packing Co: play-callers set for 2026 - https://www.acmepackingcompany.com/green-bay-packers-coaching-staff/79405/the-nfls-play-callers-are-set-for-2026-only-4-new-names-get-a-chance
- FOX coaching tracker - https://www.foxsports.com/stories/nfl/2026-nfl-coaching-gm-tracker-interviews-rumors-personnel-changes
- CBS coordinator grades - https://www.cbssports.com/nfl/news/nfl-coaching-grades-2026-offensive-defensive-coordinator-hires/
- ESPN: 10 new coordinators with questions (Cowboys, Bills, Commanders) - https://www.espn.com/nfl/story/_/id/49166861/new-nfl-coordinators-offense-defense-questions-2026-season-cowboys-bills-commanders
- Browns play-calling (Monken) - https://www.si.com/nfl/browns/onsi/news/browns-head-coach-todd-monken-reveals-who-will-be-calling-plays-on-offense-01kgj9t3ezar ; https://www.clevelandbrowns.com/news/browns-name-coordinators-for-the-2026-coaching-staff
- Cardinals staff - https://www.espn.com/nfl/story/_/id/47800131/sources-cardinals-set-hire-rams-mike-lafleur-head-coach ; https://arizonasports.com/nfl/arizona-cardinals/coaching-staff-3/3611638/
- Raiders staff - https://www.raiders.com/news/klint-kubiak-named-head-coach-of-the-las-vegas-raiders ; https://www.espn.com/nfl/story/_/id/47882318/las-vegas-raiders-hired-klint-kubiak-meaning-offense-bowers-jeanty-draft-mendoza
- Rams OC (Scheelhaase) - https://www.si.com/nfl/rams/onsi/los-angeles-finally-make-decision-naming-their-offensive-coordinator-2026 ; https://www.therams.com/news/rams-2026-coaching-staff-set
### Fantasy coaching-change analysis
- Establish The Run - https://establishtherun.com/fantasy-impact-of-nfl-coaching-changes-3/ ; pace preview https://establishtherun.com/thorman-pace-preview/
- Fantasy Life - https://www.fantasylife.com/articles/fantasy/2026-nfl-coaching-changes-klint-kubiak-john-harbaugh-and-fantasy-football-impact-of-new-play-callers
- Dynasty Nerds OC hires - https://www.dynastynerds.com/dynasty/offensive-coordinator-hires-2026-fantasy-football-impact/ ; Raiders/Kubiak https://www.dynastynerds.com/dynasty/las-vegas-raiders-klint-kubiak-2026-fantasy-football-impact/
- CBS new play-caller rankings - https://www.cbssports.com/fantasy/football/news/new-play-caller-nfl-fantasy-football-rankings/
- PFF risers/fallers - https://www.pff.com/news/fantasy-football-top-5-risers-and-fallers-from-2026-nfl-coaching-changes
- PFF neutral pass rates - https://www.pff.com/news/projecting-2026-fantasy-volume-through-neutral-situation-pass-rates
- RotoWire division previews: AFC East https://www.rotowire.com/football/article/fantasy-impact-of-afc-east-coaching-personnel-changes-123894 ; AFC North https://www.rotowire.com/football/article/afc-north-preview-2026-fantasy-impact-of-coaching-and-personnel-changes-123705 ; AFC West https://www.rotowire.com/football/article/afc-west-preview-2026-fantasy-impact-of-coaching-personnel-changes-124758 ; NFC East https://www.rotowire.com/football/article/nfc-east-preview-2026-fantasy-impact-of-coaching-personnel-changes-125700 ; NFC North https://www.rotowire.com/football/article/nfc-north-preview-2026-fantasy-impact-of-coaching-personnel-changes-126064 ; NFC South https://www.rotowire.com/football/article/nfc-south-preview-2026-fantasy-impact-of-coaching-personnel-changes-126613
### QBs
- ESPN 32 starting QBs - https://www.espn.com/nfl/story/_/id/47977560/32-nfl-starting-quarterbacks-predictions-2026-season ; SI weekly list - https://www.si.com/nfl/every-starting-nfl-quarterback-2026-season-updated-weekly ; Watson named starter - https://www.nfl.com/news/browns-deshaun-watson-starting-qb-week-1-2026-season ; nflverse depth charts (2026-09-04)
### Vegas
- NFL_Stats win totals post - https://x.com/NFL_Stats/status/2093781229229236313 ; Yahoo schedule-release O/Us - https://sports.yahoo.com/nfl/betting/article/2026-nfl-schedule-release-odds-overunders-for-all-32-teams-ravens-rams-have-nfls-highest-season-win-total-013716986.html ; FOX - https://www.foxsports.com/stories/nfl/2026-nfl-win-totals-over-unders-all-32-squads ; Fanatics - https://betfanatics.com/blog/2026-nfl-win-totals
- Implied totals: RotoWire - https://www.rotowire.com/football/article/vegas-implied-totals-best-ball-2026-119601 ; Sharp tool - https://www.sharpfootballanalysis.com/fantasy/nfl-implied-team-totals-tool/ ; FirstDown - https://www.firstdown.studio/implied-totals/season
### Offensive line
- PFF - https://www.pff.com/news/nfl-offensive-line-rankings-2026 ; 4for4 - https://www.4for4.com/2026/preseason/2026-projected-offensive-line-rankings ; FantasyPros - https://www.fantasypros.com/2026/07/nfl-offensive-line-rankings-2026-fantasy-football/ ; Sharp - https://www.sharpfootballanalysis.com/analysis/best-nfl-offensive-line-rankings/
### Personnel moves / vacated targets
- PFF target vacuums - https://www.pff.com/news/fantasy-football-team-target-vacuums-going-into-2026 ; Yahoo vacated targets - https://sports.yahoo.com/fantasy/article/fantasy-football-using-vacated-targets-to-identify-wrs-and-tes-who-should-see-an-increase-or-decrease-in-value-for-2026-144632341.html
- A.J. Brown trade - https://www.espn.com/nfl/story/_/id/48937845/sources-eagles-agree-trade-aj-brown-patriots-2-picks ; Walker signing - https://www.nfl.com/news/chiefs-signing-ex-seahawks-rb-kenneth-walker-iii-mvp-of-super-bowl-lx ; Waddle trade - https://www.nfl.com/news/dolphins-trading-wr-jaylen-waddle-to-broncos-for-draft-picks-including-2026-first-rounder
- nflverse-data (rosters, depth charts, pbp, draft picks) - https://github.com/nflverse/nflverse-data/releases

## Computed play-caller reference table (neutral pass rate % / rank, neutral sec per play / rank, top-RB carry share %, TE target share %)


### 2025
| team | pass% | rk | s/play | rk | plays/g | topRB% | TE% | RB tgt% |
|---|---|---|---|---|---|---|---|---|
| ARI | 65.7 | 1 | 32.5 | 24 | 63.2 | 31.4 | 35.3 | 20.0 |
| KC | 65.7 | 1 | 29.9 | 3 | 61.6 | 48.5 | 27.0 | 16.1 |
| CIN | 62.7 | 3 | 31.4 | 11 | 61.7 | 69.6 | 21.3 | 18.3 |
| DEN | 62.6 | 4 | 31.0 | 9 | 63.5 | 43.1 | 19.5 | 19.9 |
| LAC | 62.0 | 5 | 32.9 | 29 | 63.5 | 43.2 | 18.2 | 13.6 |
| JAX | 61.7 | 6 | 31.4 | 11 | 63.2 | 69.5 | 19.1 | 14.2 |
| LA | 61.6 | 7 | 29.6 | 2 | 62.1 | 62.7 | 25.8 | 11.0 |
| IND | 61.3 | 8 | 31.7 | 15 | 59.5 | 86.6 | 26.3 | 14.6 |
| NE | 61.2 | 9 | 31.5 | 13 | 59.8 | 48.4 | 23.4 | 17.8 |
| NO | 60.2 | 10 | 30.3 | 5 | 62.6 | 43.7 | 22.3 | 13.6 |
| HOU | 60.0 | 11 | 31.9 | 16 | 63.4 | 49.1 | 23.5 | 13.8 |
| PIT | 59.3 | 12 | 31.4 | 11 | 57.4 | 59.8 | 30.0 | 25.2 |
| MIN | 59.2 | 13 | 32.7 | 28 | 55.5 | 45.7 | 20.1 | 16.9 |
| LV | 59.2 | 13 | 32.2 | 20 | 55.4 | 86.7 | 31.7 | 19.2 |
| PHI | 59.0 | 15 | 32.3 | 22 | 58.5 | 77.0 | 22.3 | 15.0 |
| DAL | 58.5 | 16 | 29.5 | 1 | 64.9 | 65.8 | 22.8 | 13.4 |
| SF | 58.5 | 16 | 30.4 | 6 | 62.6 | 76.8 | 23.5 | 30.5 |
| DET | 58.0 | 18 | 30.8 | 7 | 61.8 | 59.6 | 16.7 | 22.4 |
| WAS | 57.5 | 19 | 32.2 | 20 | 57.6 | 50.7 | 24.1 | 12.8 |
| CHI | 57.2 | 20 | 30.0 | 4 | 64.5 | 55.5 | 25.7 | 14.7 |
| ATL | 57.0 | 21 | 31.5 | 13 | 60.9 | 65.5 | 24.5 | 22.8 |
| TEN | 56.9 | 22 | 32.6 | 26 | 58.5 | 73.8 | 26.4 | 17.5 |
| NYG | 56.0 | 23 | 30.8 | 7 | 63.5 | 44.3 | 20.2 | 19.6 |
| CLE | 55.9 | 24 | 32.6 | 26 | 60.5 | 65.3 | 32.4 | 22.9 |
| GB | 55.5 | 25 | 32.0 | 17 | 58.4 | 60.6 | 21.2 | 17.1 |
| CAR | 55.5 | 25 | 33.0 | 30 | 58.6 | 60.3 | 20.5 | 19.1 |
| TB | 55.2 | 27 | 32.5 | 24 | 62.6 | 43.4 | 16.0 | 16.7 |
| MIA | 54.7 | 28 | 33.0 | 30 | 55.4 | 62.6 | 22.6 | 24.5 |
| BUF | 54.6 | 29 | 33.1 | 32 | 62.6 | 73.7 | 25.2 | 18.4 |
| SEA | 53.1 | 30 | 32.1 | 18 | 58.6 | 50.2 | 22.5 | 13.8 |
| BAL | 53.0 | 31 | 32.1 | 18 | 56.2 | 78.3 | 30.1 | 17.8 |
| NYJ | 50.8 | 32 | 32.3 | 22 | 59.4 | 72.5 | 22.4 | 19.7 |

### 2024
| team | pass% | rk | s/play | rk | plays/g | topRB% | TE% | RB tgt% |
|---|---|---|---|---|---|---|---|---|
| CIN | 70.1 | 1 | 30.9 | 18 | 62.9 | 69.3 | 24.8 | 16.0 |
| KC | 66.4 | 2 | 29.3 | 3 | 62.9 | 55.7 | 33.6 | 16.4 |
| HOU | 64.6 | 3 | 31.5 | 23 | 61.5 | 67.3 | 20.1 | 17.4 |
| MIN | 63.3 | 4 | 30.9 | 18 | 60.5 | 67.1 | 22.6 | 16.6 |
| SEA | 62.9 | 5 | 30.9 | 18 | 59.9 | 47.5 | 19.9 | 19.2 |
| DEN | 62.9 | 5 | 29.8 | 6 | 61.1 | 39.7 | 13.1 | 21.3 |
| ARI | 62.1 | 7 | 30.5 | 13 | 60.6 | 63.9 | 34.0 | 18.2 |
| NYJ | 61.3 | 8 | 31.5 | 23 | 59.6 | 63.5 | 18.4 | 19.4 |
| CLE | 60.9 | 9 | 30.6 | 14 | 65.9 | 33.8 | 26.2 | 13.6 |
| SF | 60.7 | 10 | 32.0 | 27 | 59.6 | 45.8 | 21.4 | 17.7 |
| TB | 60.6 | 11 | 32.7 | 29 | 63.8 | 51.6 | 18.9 | 21.6 |
| DAL | 60.2 | 12 | 29.0 | 1 | 64.4 | 67.9 | 21.8 | 13.9 |
| CHI | 59.5 | 13 | 30.1 | 9 | 62.3 | 77.4 | 13.6 | 14.9 |
| BUF | 59.4 | 14 | 30.1 | 9 | 59.1 | 56.9 | 23.8 | 16.5 |
| NE | 59.1 | 15 | 32.9 | 31 | 60.1 | 57.5 | 31.5 | 16.9 |
| LAC | 58.9 | 16 | 32.7 | 29 | 58.7 | 52.1 | 21.9 | 12.1 |
| LV | 58.7 | 17 | 31.5 | 23 | 62.0 | 42.9 | 33.3 | 18.9 |
| JAX | 58.6 | 18 | 30.3 | 12 | 58.3 | 48.0 | 26.5 | 15.7 |
| CAR | 58.5 | 19 | 31.8 | 26 | 58.1 | 73.0 | 16.6 | 17.3 |
| WAS | 58.4 | 20 | 29.9 | 7 | 64.2 | 52.7 | 21.9 | 15.6 |
| PIT | 57.9 | 21 | 30.7 | 16 | 62.7 | 61.7 | 26.4 | 23.8 |
| MIA | 57.4 | 22 | 31.7 | 25 | 63.3 | 53.1 | 25.8 | 23.0 |
| BAL | 57.2 | 23 | 31.1 | 20 | 61.1 | 81.9 | 30.1 | 17.7 |
| NO | 57.0 | 24 | 29.7 | 5 | 60.4 | 65.5 | 28.0 | 26.1 |
| NYG | 56.5 | 25 | 31.3 | 21 | 61.8 | 60.2 | 11.5 | 15.9 |
| ATL | 56.5 | 25 | 29.1 | 2 | 63.1 | 66.9 | 16.1 | 15.7 |
| DET | 56.0 | 27 | 30.6 | 14 | 64.6 | 52.2 | 19.1 | 21.0 |
| TEN | 55.0 | 28 | 34.4 | 32 | 60.6 | 70.9 | 25.7 | 18.6 |
| LA | 54.9 | 29 | 30.2 | 11 | 60.5 | 79.6 | 15.3 | 10.1 |
| PHI | 53.6 | 30 | 30.0 | 8 | 64.3 | 76.3 | 20.8 | 16.5 |
| IND | 52.5 | 31 | 29.4 | 4 | 60.8 | 77.6 | 15.4 | 13.2 |
| GB | 48.9 | 32 | 32.4 | 28 | 60.1 | 67.6 | 18.6 | 15.4 |

### 2023
| team | pass% | rk | s/play | rk | plays/g | topRB% | TE% | RB tgt% |
|---|---|---|---|---|---|---|---|---|
| WAS | 70.0 | 1 | 30.5 | 19 | 62.4 | 59.9 | 20.3 | 17.9 |
| KC | 69.0 | 2 | 29.6 | 9 | 62.1 | 64.6 | 28.5 | 18.0 |
| CIN | 66.5 | 3 | 31.5 | 26 | 60.7 | 80.8 | 19.4 | 15.2 |
| LAC | 63.9 | 4 | 28.5 | 2 | 64.5 | 54.7 | 21.6 | 15.3 |
| MIA | 63.8 | 5 | 29.9 | 14 | 60.9 | 52.5 | 9.6 | 22.7 |
| DAL | 63.5 | 6 | 28.2 | 1 | 64.9 | 68.2 | 20.7 | 16.4 |
| MIN | 63.3 | 7 | 30.1 | 16 | 62.5 | 55.2 | 29.5 | 14.8 |
| BAL | 62.8 | 8 | 29.8 | 11 | 62.6 | 54.5 | 23.1 | 16.6 |
| SEA | 62.5 | 9 | 29.9 | 14 | 57.9 | 65.0 | 18.0 | 15.7 |
| BUF | 62.4 | 10 | 29.2 | 6 | 64.4 | 62.2 | 23.7 | 15.7 |
| TB | 61.7 | 11 | 30.2 | 17 | 60.5 | 75.6 | 14.6 | 17.0 |
| JAX | 61.2 | 12 | 29.7 | 10 | 64.8 | 74.7 | 27.5 | 14.9 |
| LA | 60.5 | 13 | 30.7 | 21 | 64.2 | 55.2 | 15.7 | 12.3 |
| NYG | 60.4 | 14 | 30.8 | 23 | 61.7 | 74.9 | 22.0 | 20.3 |
| PHI | 60.4 | 14 | 29.9 | 14 | 64.9 | 66.4 | 18.3 | 17.7 |
| CLE | 60.1 | 16 | 29.0 | 5 | 69.5 | 47.6 | 27.7 | 16.0 |
| NO | 59.9 | 17 | 29.8 | 11 | 64.8 | 51.7 | 15.7 | 22.2 |
| IND | 59.7 | 18 | 28.7 | 3 | 63.9 | 44.0 | 21.8 | 15.4 |
| HOU | 59.4 | 19 | 29.4 | 7 | 63.4 | 57.0 | 20.4 | 14.8 |
| LV | 59.1 | 20 | 30.7 | 21 | 58.6 | 65.3 | 14.1 | 18.6 |
| NYJ | 58.8 | 21 | 31.0 | 24 | 61.7 | 69.3 | 22.2 | 26.4 |
| CAR | 58.2 | 22 | 31.4 | 25 | 64.4 | 62.3 | 18.3 | 17.2 |
| NE | 58.1 | 23 | 30.4 | 18 | 59.8 | 51.7 | 22.5 | 22.0 |
| DEN | 57.8 | 24 | 32.0 | 29 | 58.9 | 61.5 | 12.9 | 32.1 |
| GB | 57.3 | 25 | 31.6 | 28 | 61.2 | 48.4 | 17.8 | 16.7 |
| CHI | 57.1 | 26 | 32.3 | 30 | 64.1 | 36.8 | 23.3 | 22.3 |
| ATL | 56.7 | 27 | 28.7 | 3 | 63.7 | 47.5 | 34.1 | 24.5 |
| SF | 56.6 | 28 | 32.4 | 31 | 58.6 | 68.3 | 20.2 | 23.8 |
| DET | 56.3 | 29 | 29.5 | 8 | 65.7 | 48.8 | 24.0 | 17.8 |
| TEN | 55.5 | 30 | 32.6 | 32 | 57.9 | 73.1 | 20.5 | 22.1 |
| ARI | 53.6 | 31 | 30.5 | 19 | 63.0 | 61.6 | 32.8 | 15.8 |
| PIT | 53.2 | 32 | 31.5 | 26 | 59.3 | 63.2 | 19.3 | 23.5 |

### 2022
| team | pass% | rk | s/play | rk | plays/g | topRB% | TE% | RB tgt% |
|---|---|---|---|---|---|---|---|---|
| KC | 70.6 | 1 | 28.3 | 4 | 63.8 | 50.7 | 32.7 | 18.3 |
| CIN | 68.7 | 2 | 29.7 | 10 | 64.6 | 67.3 | 15.4 | 22.2 |
| BUF | 66.8 | 3 | 28.3 | 4 | 63.6 | 60.8 | 13.9 | 20.1 |
| LAC | 66.7 | 4 | 28.0 | 2 | 66.9 | 59.3 | 18.4 | 25.8 |
| MIN | 64.0 | 5 | 29.2 | 8 | 65.5 | 73.9 | 22.8 | 13.6 |
| SEA | 63.7 | 6 | 30.2 | 14 | 60.8 | 65.1 | 24.5 | 15.1 |
| PHI | 62.6 | 7 | 27.8 | 1 | 65.0 | 70.5 | 18.4 | 12.1 |
| ARI | 62.2 | 8 | 29.1 | 7 | 67.2 | 57.7 | 18.7 | 17.5 |
| MIA | 61.6 | 9 | 31.6 | 22 | 58.5 | 54.0 | 12.9 | 20.0 |
| TB | 61.0 | 10 | 29.6 | 9 | 67.4 | 54.9 | 16.2 | 20.1 |
| NYJ | 60.8 | 11 | 30.6 | 15 | 62.5 | 33.7 | 19.9 | 21.4 |
| NE | 60.5 | 12 | 31.2 | 17 | 58.0 | 59.3 | 18.6 | 23.2 |
| DEN | 59.7 | 13 | 30.1 | 13 | 62.9 | 43.8 | 22.3 | 22.7 |
| LA | 59.0 | 14 | 32.5 | 28 | 58.1 | 58.8 | 23.4 | 12.2 |
| IND | 58.3 | 15 | 29.8 | 11 | 64.7 | 50.1 | 18.5 | 21.4 |
| GB | 58.2 | 16 | 32.3 | 26 | 60.9 | 52.0 | 17.9 | 21.5 |
| NYG | 58.0 | 17 | 30.7 | 16 | 63.4 | 77.6 | 17.2 | 22.3 |
| LV | 57.9 | 18 | 32.6 | 29 | 61.6 | 90.0 | 18.2 | 19.8 |
| DET | 57.5 | 19 | 29.0 | 6 | 63.6 | 61.2 | 16.7 | 21.1 |
| JAX | 57.0 | 20 | 30.0 | 12 | 62.7 | 61.4 | 21.7 | 14.1 |
| CLE | 55.6 | 21 | 31.3 | 18 | 64.6 | 69.0 | 26.4 | 17.3 |
| BAL | 55.5 | 22 | 31.8 | 24 | 60.6 | 31.0 | 44.0 | 13.5 |
| SF | 55.5 | 22 | 31.6 | 22 | 60.6 | 40.6 | 19.4 | 21.8 |
| PIT | 54.6 | 24 | 31.3 | 18 | 64.8 | 70.8 | 25.0 | 17.2 |
| HOU | 54.1 | 25 | 31.5 | 20 | 59.5 | 66.1 | 23.7 | 23.5 |
| TEN | 52.8 | 26 | 32.6 | 29 | 57.6 | 85.1 | 28.1 | 19.5 |
| DAL | 52.1 | 27 | 28.3 | 4 | 64.8 | 50.0 | 23.8 | 15.6 |
| NO | 51.8 | 28 | 32.4 | 27 | 59.1 | 67.2 | 20.6 | 21.6 |
| CAR | 51.5 | 29 | 31.5 | 20 | 57.1 | 48.8 | 18.0 | 19.9 |
| CHI | 51.0 | 30 | 31.9 | 25 | 57.9 | 54.6 | 23.1 | 17.1 |
| ATL | 50.2 | 31 | 32.9 | 31 | 58.8 | 46.3 | 26.4 | 16.4 |
| WAS | 47.3 | 32 | 32.9 | 31 | 66.8 | 47.3 | 18.3 | 22.9 |

## Per-team evidence

### ARI - Mike LaFleur (NEW) / OC Nathaniel Hackett (NEW) / QB Jacoby Brissett (tier 4)
- Evidence: HC LaFleur/OC Hackett/LaFleur calls plays: confirmed by ESPN, azcardinals.com and Arizona Sports snippets. LaFleur tendencies: ETR ('distributes targets evenly, personnel versatility'); NYJ 2022 numbers computed. Benson/Conner IR from Week 1 roster file (RES). Brissett QB1 from depth chart + ESPN. Win total 4.5 (3.5 at one book earlier). OL null (no rank found). QB tier 4 reasoning: bridge veteran, weak supporting cast, Kyler traded.
- Vacated: 119/620 targets, 183/364 carries (computed).
- Verdict: Bottom-tier environment: bridge QB, 4.5-win total, first-year McVay-tree play-caller; McBride/Harrison target volume is the only safe piece; rookie Love is the de facto lead back with both vets on IR - fade WR2/WR3.

### ATL - Kevin Stefanski (NEW) / OC Tommy Rees (NEW) / QB Tua Tagovailoa (tier 3)
- Evidence: Stefanski HC confirmed (NFL.com/Yahoo). Rees as OC and play-caller from one search snippet only [UNVERIFIED who calls plays]. Tua QB1 from depth chart + ESPN. Tendencies computed from CLE 2025 (Rees) and CLE 2023 (Stefanski). Win total 6.5 [UNVERIFIED - conflicts with 'Titans only 6.5 on Fanatics']. OL: FantasyPros 'one of the worst units, RT concern' (rank null). Bellcow: Bijan 288 car/103 tgt (computed).
- Vacated: 124/522 targets, 143/465 carries (computed).
- Verdict: Run/TE-leaning Stefanski scheme with a weak OL (FantasyPros: one of worst units) and 6.5-win total: Bijan mega-bellcow (288 car/103 tgt in 2025), London and Pitts concentrate targets; Tua caps ceiling; fade ATL WR2/WR3.

### BAL - Jesse Minter (NEW) / OC Declan Doyle (NEW) / QB Lamar Jackson (tier 1)
- Evidence: Minter HC + Declan Doyle OC/play-caller: ETR, Dynasty Nerds ('boldest hire, 29-year-old first-time caller'), NFL.com. Note one snippet mis-named him 'Jarrett Doyle'. Tendencies computed from CHI 2025 (Doyle's 2025 team, Johnson calling) and BAL 2024-25. Win total 11.5 (NFL_Stats, Yahoo). OL 13 [UNVERIFIED unnamed source].
- Vacated: 102/409 targets, 59/490 carries (computed).
- Verdict: Elite QB + highest AFC win total; run-first identity with Henry (307 car) as bellcow, but a Johnson-tree play-caller should raise pace/plays; Flowers and Andrews consolidate targets with Likely/Hopkins gone.

### BUF - Joe Brady (NEW) / OC Pete Carmichael (NEW) / QB Josh Allen (tier 1)
- Evidence: Brady promoted to HC, keeps play-calling (ESPN 'called plays since mid-Nov 2023', RotoWire). Carmichael OC from one FOX/tracker snippet [single-sourced]. DJ Moore from CHI confirmed via 2026 roster file and depth chart WR1. Tendencies computed (2025 pass rate #29, pace slowest). Win total 10.5. PFF: returns 4 OL starters (rank null).
- Vacated: 35/488 targets, 6/522 carries (computed).
- Verdict: Stable elite-QB offense, run-leaning and slow-paced under Brady; Cook bellcow; DJ Moore adds a true X (Bills 2nd in implied PPG per RotoWire) - Shakir/Coleman/Kincaid targets become more contested; OL returns 4 starters.

### CAR - Dave Canales / OC Brad Idzik / QB Bryce Young (tier 3)
- Evidence: Continuity (no snippet reported changes; Canales year 3 per NFC South snippet). Dowdle to PIT confirmed by roster file and RotoWire AFC North. Tendencies computed. Win total 7.5. Young tier 3 is my assessment [UNVERIFIED].
- Vacated: 76/482 targets, 237/445 carries (computed).
- Verdict: Slow, run-leaning Canales offense with modest QB; Hubbard regains lead role (Dowdle gone, 237 vacated carries) but Brooks looms; McMillan is the target hog; fade CAR WR2/TE.

### CHI - Ben Johnson / OC Press Taylor (NEW) / QB Caleb Williams (tier 2)
- Evidence: Press Taylor OC from Wikipedia-list snippet [single-sourced]; Doyle's departure to BAL confirmed. Johnson calls plays (ESPN framing; Johnson called plays in 2025). DJ Moore/Zaccheaus departures from roster diff. Tendencies computed. OL 6 [UNVERIFIED unnamed source]. Win total 9.5.
- Vacated: 151/536 targets, 19/496 carries (computed).
- Verdict: Fast, high-volume Johnson offense; 151 vacated targets flow to Odunze/Burden/Loveland (pass-catcher upgrade); Swift/Monangai committee caps either RB.

### CIN - Zac Taylor / OC Dan Pitcher / QB Joe Burrow (tier 1)
- Evidence: RotoWire: 'kept 2025 offensive core together'. Flacco QB2 from roster/depth chart. Tendencies computed. Win total 10.5. OL 25 [UNVERIFIED]; Big Lead: all 5 starters return for first time in Burrow era.
- Vacated: 65/611 targets, 0/372 carries (computed).
- Verdict: Pass-heaviest healthy environment in the league: Burrow + Chase/Higgins fully intact, Chase Brown bellcow, only 65 vacated targets; OL (all 5 starters return) remains the weak link.

### CLE - Todd Monken (NEW) / OC Travis Switzer (NEW) / QB Deshaun Watson (tier 4)
- Evidence: Monken HC calls plays (SI/Browns.com snippets); Switzer OC (RotoWire AFC North). Watson named Week 1 starter over Sanders (NFL.com, Browns.com). Gabriel IR from roster file. Rookies Concepcion #24 / Boston #39 from draft_picks. Tendencies: Monken BAL 2023-25 computed. Win total 5.5. OL 32 [UNVERIFIED unnamed source] + FantasyPros bottom-5.
- Vacated: 127/524 targets, 31/419 carries (computed).
- Verdict: Unsettled QB (Watson) behind a bottom-ranked OL with a 5.5-win total; Judkins bellcow and Fannin (TE1) are the only safe volume; Jeudy WR1 but two drafted rookies compete - fade.

### DAL - Brian Schottenheimer / OC Klayton Adams / QB Dak Prescott (tier 2)
- Evidence: Schottenheimer calls plays with Adams as OC year 2 (ESPN/CBS snippets). Implied 25.75 PPG 4th (RotoWire). Tendencies computed (fastest pace, most plays). PFF: all five OL starters return; Yahoo tiered look lists DAL among top lines (rank null). Win total 9.5.
- Vacated: 44/610 targets, 58/449 carries (computed).
- Verdict: Elite volume environment: fastest pace, most plays, 25.75 implied PPG, all five OL starters back, Lamb/Pickens/Ferguson intact; Javonte lead back - start everything.

### DEN - Sean Payton / OC Davis Webb (NEW) / QB Bo Nix (tier 2)
- Evidence: Webb promoted, Payton handed play-calling (ESPN, RotoWire AFC West). Waddle trade details (NFL.com/CBS). PFF OL #1. Tendencies computed (Payton 2024-25). Win total 9.5.
- Vacated: 6/589 targets, 37/439 carries (computed).
- Verdict: Pass-leaning offense behind the PFF No. 1 OL that added Waddle: Sutton/Franklin/Engram target competition rises; Dobbins/Harvey committee; first-time play-caller is the only caveat.

### DET - Dan Campbell / OC Drew Petzing (NEW) / QB Jared Goff (tier 2)
- Evidence: Petzing hired as DET OC per two snippets (NFC North search + Commanders/Lions search). Whether Petzing or Campbell calls plays [UNVERIFIED]. Petzing tendencies computed from ARI 2023-25 (TE share 33-35%). Montgomery to HOU and Pacheco IR from roster files. OL 14 [UNVERIFIED]. Win total 9.5.
- Vacated: 59/550 targets, 161/432 carries (computed).
- Verdict: Gibbs becomes a true bellcow with Montgomery gone (161 vacated carries) and Pacheco on IR; Petzing's TE-heavy history boosts LaPorta; St. Brown/Williams stable; mild pass-rate upgrade.

### GB - Matt LaFleur / OC Adam Stenavich / QB Jordan Love (tier 2)
- Evidence: Stenavich remains OC (two snippets). Jacobs on Reserve/Exempt (E02) in the Week 1 roster file - reason unknown [UNVERIFIED cause]; depth chart RB1 is MarShawn Lloyd. Doubs/Wicks/E. Wilson departures from roster diff. Tendencies computed. Win total 9.5.
- Vacated: 165/462 targets, 144/474 carries (computed).
- Verdict: Run-leaning LaFleur scheme with the RB room in flux (Jacobs exempt, Lloyd/Brooks/K. Johnson); 165 vacated targets go to Reed/Watson/Golden/Kraft; Kraft+Jonnu = TE-heavy; low pass rate caps WRs.

### HOU - DeMeco Ryans / OC Nick Caley / QB C.J. Stroud (tier 2)
- Evidence: Returns HC/OC/DC (AFC South snippet). Montgomery signing, Kirk/Chubb departures, Higgins IR from roster files. Tendencies computed. OL 30 [UNVERIFIED]; FantasyPros 'arguably worst OL last year'. Win total 9.5.
- Vacated: 86/557 targets, 133/463 carries (computed).
- Verdict: Middling pass rate, poor OL; Nico Collins target monopoly grows with Higgins on IR and Kirk gone; Schultz TE1; Montgomery/Marks committee limits both.

### IND - Shane Steichen / OC Jim Bob Cooter / QB Daniel Jones (tier 3)
- Evidence: Continuity (AFC South snippet). Pittman to PIT, Keenan Allen from LAC per roster diff (also PFF/Yahoo vacated-target notes). JT 86.6% carry share computed. Win total 7.5. Jones tier 3 my assessment.
- Vacated: 147/536 targets, 14/431 carries (computed).
- Verdict: JT bellcow + Warren TE1 anchor a mid-high pass-rate offense; Pittman's 114 targets replaced 1-for-1 by Keenan Allen (Pierce/Downs unchanged); ceiling capped by Jones and 7.5 wins.

### JAX - Liam Coen / OC Grant Udinski / QB Trevor Lawrence (tier 3)
- Evidence: Continuity (AFC South snippet). Etienne to NO, Rodriguez from WAS per roster diff; Tuten RB1 on depth chart. Tendencies computed. Win total 8.5.
- Vacated: 149/549 targets, 266/471 carries (computed).
- Verdict: Pass-leaning Coen offense; 266 vacated carries make Tuten a breakout candidate (Rodriguez early-down risk); Thomas/Hunter/Washington/Meyers WR corps unchanged.

### KC - Andy Reid / OC Eric Bieniemy (NEW) / QB Patrick Mahomes (tier 1)
- Evidence: Bieniemy OC (RotoWire AFC West: 'back as OC after Nagy left to call plays for the Giants'); Reid calls plays (ESPN). Walker 3y/$43M (Spotrac/NFL.com); Mahomes ACL (ESPN) but ACT + QB1 on Week 1 roster/depth chart. Tendencies computed; Bieniemy WAS 2023 computed. OL 21 [UNVERIFIED]; 4for4 strong pass-block. Win total 10.5.
- Vacated: 170/552 targets, 281/417 carries (computed).
- Verdict: Pass-heaviest, fast offense; Walker inherits 281 vacated carries as a clear lead back (RB upgrade); Rice/Worthy/Kelce absorb 119 vacated WR targets; Mahomes ACL return is the key risk.

### LV - Klint Kubiak (NEW) / OC Andrew Janocko (NEW) / QB Kirk Cousins (tier 4)
- Evidence: Kubiak HC calls plays, Janocko OC (Raiders.com/ESPN/RotoWire). ETR: heavy personnel, 2-TE rates (SEA 2nd, NO 3rd at 39%). Cousins listed ahead of Mendoza (ESPN + depth chart). Tendencies computed from SEA 2025 / NO 2024. Win total 5.5.
- Vacated: 102/496 targets, 69/364 carries (computed).
- Verdict: Run-heavy, heavy-personnel Kubiak scheme: Jeanty bellcow and Bowers/Mayer 2-TE usage up (ETR: bodes well for Jeanty); WRs (Tucker/Nailor) fade; QB bridge to Mendoza and 5.5 wins.

### LAC - Jim Harbaugh / OC Mike McDaniel (NEW) / QB Justin Herbert (tier 1)
- Evidence: McDaniel OC (Dynasty Nerds, RotoWire AFC West, ESPN). Keenan Allen to IND (roster diff + PFF vacated targets). Tendencies computed from MIA 2022-25. Win total 9.5. OL null.
- Vacated: 149/544 targets, 73/455 carries (computed).
- Verdict: McDaniel scheme upgrade for Hampton (Achane-style featured role) and McConkey (Allen's 122 slot targets vacated); Njoku/Kolar signal 2-TE looks; Herbert elite - pass-catcher volume concentrated.

### LAR - Sean McVay / OC Nathan Scheelhaase (NEW) / QB Matthew Stafford (tier 1)
- Evidence: Scheelhaase promoted to OC, McVay still calls (SI/therams.com snippets). Highest implied PPG and SB favorite (RotoWire/Yahoo). OL 9 [UNVERIFIED]; 4for4 top-5 run block. Zero vacated targets computed. Win total 11.5.
- Vacated: 0/581 targets, 0/439 carries (computed).
- Verdict: Best environment in the NFL: highest implied total, 11.5 wins, zero vacated targets, Nacua/Adams/Kyren/McVay all intact - start everything.

### MIA - Jeff Hafley (NEW) / OC Bobby Slowik (NEW) / QB Malik Willis (tier 4)
- Evidence: Hafley HC (NFL.com/Yahoo); Slowik OC internal promotion (Acme Packing snippet) [single-sourced]. Willis 3y/$67.5M starter (RotoWire/Yahoo). Waddle/Hill/Waller/Tua departures from roster diff. Tendencies computed from HOU 2023-24. Win total 4.5 (3.5 earlier). 4for4 bottom-5 run block (rank null).
- Vacated: 220/465 targets, 19/424 carries (computed).
- Verdict: Largest target vacuum by share (220, 47%) but weak QB/OL (4for4 bottom-5 run block) and a 4.5-win total; Achane is the only sure thing; Malik Washington has pure-volume upside; fade the rest.

### MIN - Kevin O'Connell / OC Wes Phillips / QB Kyler Murray (tier 3)
- Evidence: Kyler Murray QB1 (ESPN + depth chart; NFC North preview). Jennings from SF per roster diff. Tendencies computed. OL 20 [UNVERIFIED]. Win total 8.5. Kyler tier 3 my assessment.
- Vacated: 74/472 targets, 51/396 carries (computed).
- Verdict: Kyler + O'Connell lifts Jefferson/Addison/Hockenson floors and adds QB rushing; Jennings crowds WR3 targets; Jones/Mason split and slow pace limit RBs.

### NE - Mike Vrabel / OC Josh McDaniels / QB Drake Maye (tier 1)
- Evidence: McDaniels calls plays (ESPN). A.J. Brown trade (ESPN/NFL.com: 2028 1st + 2027 5th). Diggs to WAS, Doubs from GB per roster diff. OL 19 [UNVERIFIED]. Win total 10.5 (up after SB LX appearance). Tendencies computed.
- Vacated: 178/483 targets, 48/466 carries (computed).
- Verdict: Pass-leaning with Maye ascending; A.J. Brown is a WR1 upgrade over Diggs, Doubs WR2, Henry TE1; Stevenson/Henderson committee suppresses both backs.

### NO - Kellen Moore / OC Doug Nussmeier / QB Tyler Shough (tier 4)
- Evidence: Moore year 2 (NFC South snippet). Shough QB1 from depth chart [not confirmed by an article snippet]. Etienne signing, Tyson #8 pick on reserve, Neal IR from roster/draft files. Tendencies computed. 4for4 bottom-5 run block. Win total 7.5.
- Vacated: 108/566 targets, 73/429 carries (computed).
- Verdict: Fast-paced Moore offense but weak QB and bottom-5 run-blocking OL (4for4); Olave and Juwan Johnson volume is safe; Etienne/Kamara split; Tyson out to start.

### NYG - John Harbaugh (NEW) / OC Matt Nagy (NEW) / QB Jaxson Dart (tier 3)
- Evidence: Harbaugh HC (NFL.com/Yahoo); Nagy OC and play-caller (Commanders/Lions search snippet + RotoWire AFC West). Dart QB1 from depth chart. Wan'Dale to TEN, Mooney/Likely/Austin arrivals from roster diff. Tendencies computed (NYG 2025, BAL 2025). Win total 7.5.
- Vacated: 186/506 targets, 21/503 carries (computed).
- Verdict: Nabers absorbs Wan'Dale's 141 vacated targets in a likely run-leaning Harbaugh offense; Skattebo/Tracy split; Dart year 2 - Nabers only.

### NYJ - Aaron Glenn / OC Frank Reich (NEW) / QB Geno Smith (tier 3)
- Evidence: Reich play-caller + Geno QB (RotoWire AFC East, Yahoo). Sadiq #16 / Cooper #30 from draft_picks. Tendencies computed (IND 2022 partial, CAR 2023 partial - Reich was fired mid-season both years, so these are blended). Win total 5.5.
- Vacated: 107/477 targets, 113/453 carries (computed).
- Verdict: Reich + Geno should lift a 32nd-ranked pass rate; Breece Hall bellcow and Garrett Wilson are the plays; rookie TE/WR upside is speculative on a 5.5-win team.

### PHI - Nick Sirianni / OC Sean Mannion (NEW) / QB Jalen Hurts (tier 2)
- Evidence: Mannion OC (Dynasty Nerds, NFC East RotoWire 'new OC with play-calling'). A.J. Brown trade confirmed. Lemon #20 / Stowers #54 from draft_picks. PFF OL #2. Tendencies computed (Patullo 2025, Moore 2024). Win total 10.5.
- Vacated: 160/466 targets, 12/463 carries (computed).
- Verdict: DeVonta Smith becomes the clear WR1 (Brown's 121 targets vacated) with Goedert TE1; Saquon bellcow behind PFF No. 2 OL; first-time play-caller Mannion is an unknown - assume mid pass rate.

### PIT - Mike McCarthy (NEW) / OC Brian Angelichio (NEW) / QB Aaron Rodgers (tier 3)
- Evidence: McCarthy HC calls plays, Angelichio OC, Pittman/Dowdle/Tonyan acquired (RotoWire AFC North). Rodgers QB1 (roster + ESPN). Tendencies computed from DAL 2023-24. Win total 8.5. Vacated 239 targets computed (highest raw total).
- Vacated: 239/524 targets, 166/395 carries (computed).
- Verdict: McCarthy = faster pace and more passing than Arthur Smith; Metcalf/Pittman/Freiermuth split 239 vacated targets; Warren/Dowdle committee (Dowdle was McCarthy's bellcow in DAL); Rodgers age risk.

### SF - Kyle Shanahan / OC Klay Kubiak / QB Brock Purdy (tier 2)
- Evidence: Shanahan/Klay Kubiak continuity (NFC West snippet). Evans/Deebo/Kirk arrivals and Jennings/Bourne departures from roster diff (PFF: 139 vacated from Jennings+Bourne; my computed 158 includes B. Robinson's 12 targets). Pearsall IR, Kirk reserve, Guerendo PUP from roster file. Win total 9.5.
- Vacated: 158/554 targets, 92/462 carries (computed).
- Verdict: CMC mega-bellcow (30% of targets) unchanged in a fast, efficient offense; Evans/Deebo/Kittle share WR targets with Pearsall out; top-5 run-blocking OL (4for4).

### SEA - Mike Macdonald / OC Brian Fleury (NEW) / QB Sam Darnold (tier 2)
- Evidence: Fleury OC/play-caller (NFC West snippet, ESPN). Walker to KC (NFL.com). Charbonnet R04 reserve and Price #32 RB1 from roster/depth chart. Tendencies computed (Kubiak 2025). Win total 10.5.
- Vacated: 36/457 targets, 221/491 carries (computed).
- Verdict: Run-first defending champs with a first-time play-caller; JSN target monopoly intact (only 36 vacated targets); RB room wide open (rookie Price) after Walker exit + Charbonnet PUP - 221 vacated carries.

### TB - Todd Bowles / OC Zac Robinson (NEW) / QB Baker Mayfield (tier 2)
- Evidence: Zac Robinson OC after Grizzard fired (NFC South snippet). PFF OL #3. Evans to SF, White to WAS, Gainwell from PIT per roster diff. Tendencies computed from ATL 2024-25. Win total 8.5.
- Vacated: 161/545 targets, 137/464 carries (computed).
- Verdict: Robinson's outside-zone + PFF No. 3 OL = Bucky Irving bellcow upside (Gainwell pass-down); Egbuka WR1 with Evans gone, Godwin WR2, Otton TE1; mid pass rate.

### TEN - Robert Saleh (NEW) / OC Brian Daboll (NEW) / QB Cam Ward (tier 3)
- Evidence: Saleh HC (NFL.com/Yahoo); Daboll OC from one snippet [single-sourced]; play-caller assumed Daboll [UNVERIFIED]. Tate #4 from draft_picks; Wan'Dale from roster diff. Tendencies computed (NYG 2024-25). Win total 6.5.
- Vacated: 152/530 targets, 0/372 carries (computed).
- Verdict: Rebuilt WR room (Tate, Wan'Dale, Ayomanor, Dike) under Daboll for Ward's year 2; Pollard lead back with Spears on passing downs; 6.5-win total caps ceilings - volume plays only.

### WAS - Dan Quinn / OC David Blough (NEW) / QB Jayden Daniels (tier 2)
- Evidence: Blough promoted to OC, never called plays (Commanders/Lions search snippet; ESPN new-coordinators piece). PFF: 171 vacated from Deebo+Ertz, NFL-high 13 vacated RZ targets. Diggs/Okonkwo/White arrivals from roster diff. Kingsbury no-huddle rates computed. 4for4 bottom-5 run block. Win total 7.5.
- Vacated: 207/436 targets, 144/475 carries (computed).
- Verdict: Huge target churn (207 vacated, 47%) with a first-time play-caller; McLaurin/Diggs/Okonkwo inherit volume (Diggs profiles as Deebo replacement); JCM/White committee; Daniels health is the swing.
