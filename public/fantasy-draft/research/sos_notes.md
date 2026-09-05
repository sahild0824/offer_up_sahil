# 2026 Fantasy Strength of Schedule (SOS) by position — methods research, data, results, caveats

Prepared 2026-09-05. Companion data file: `sos.json` (same directory). All defense ratings in this file were **computed by this agent from nflverse weekly player stats (2025 and 2024 seasons)**; no points-allowed numbers were copied from fantasy sites (those were blocked for direct fetch, and search snippets were used only to cross-check).

## 1. How the major outlets compute fantasy SOS for 2026, and what they say it is worth

Only search-result snippets were readable (fantasy/sports sites are blocked for direct fetch in this environment), so method descriptions below are quoted/paraphrased from those snippets and attributed to the page they came from.

| Outlet | Method (as described by the outlet) | What they published for 2026 (from snippets) |
|---|---|---|
| **FantasyPros** — [SOS tool](https://www.fantasypros.com/nfl/strength-of-schedule.php) (per-position pages for [QB](https://www.fantasypros.com/nfl/strength-of-schedule.php?position=QB), [RB](https://www.fantasypros.com/nfl/strength-of-schedule.php?position=RB), [WR](https://www.fantasypros.com/nfl/strength-of-schedule.php?position=WR), TE, K, DST) | "SOS is based on each opponent's Fantasy Points Allowed to a position, adjusted for strength of schedule. Favorable matchups receive better matchup star ratings." Preseason it runs on 2025 fantasy points allowed (their [Points Allowed](https://www.fantasypros.com/nfl/points-allowed.php) page, weeks 1-17), then rolls in-season. | [15 Schedule Winners & Losers (2026)](https://www.fantasypros.com/2026/05/15-fantasy-football-schedule-winners-losers-2026/): Eagles a winner (WAS allowed 3rd-most FP to QBs in 2025, TEN 5th-most; PHI's first eight weeks include LAR, DAL, CHI, CAR, JAX); Browns a winner (schedule drops from 2nd-toughest to 15th). [Best & Worst Playoff Schedules (2026)](https://www.fantasypros.com/2026/05/2026-nfl-schedule-release-best-worst-fantasy-football-playoff-schedules/): Cowboys get three dome games (LAR, JAX, NYG) in weeks 15-17; RB notes on NE (wk 15), CAR (wk 16, most 100-yd rushers allowed), LAR (wk 17, 14th in PPR PPG to RBs). |
| **4for4** — [aFPA FAQ](https://www.4for4.com/faq/what-schedule-adjusted-fantasy-points-allowed) | Signature metric **aFPA = schedule-adjusted fantasy points allowed**: "compares fantasy points allowed data on a more accurate scale than raw fantasy points allowed, by adjusting for each team's individual strength of schedule … uses rolling 10-week data" in season. Their **Hot Spots** team-level SOS app colors every team's 2026 schedule using **2025 aFPA**. | [12 players with easy early-season schedules (2026)](https://www.4for4.com/2026/preseason/12-fantasy-football-players-easy-early-season-schedules-2026); [QB SOS beneficiaries & late-round pairings](https://www.4for4.com/2026/preseason/fantasy-football-quarterback-sos-beneficiaries-ideal-late-round-pairings); [Tiered D/ST rankings by early SOS](https://www.4for4.com/2026/preseason/tiered-dst-rankings-based-early-strength-schedule). Names behind the paywall/blocked. |
| **Sharp Football Analysis** (Warren Sharp / Rich Hribar) — [2026 Fantasy SOS](https://www.sharpfootballanalysis.com/fantasy/strength-of-schedule-fantasy-football/), [team SOS](https://www.sharpfootballanalysis.com/analysis/nfl-strength-of-schedule/) | Forward-looking: "a proprietary metric based on **Vegas win totals for opponents**" (2026 projected win totals measure opponent quality) rather than last year's points allowed. The fantasy article "breaks down which passing and rushing attacks have the easiest path to fantasy points this season, both for the full season and the fantasy playoffs." Sharp's own caveat: "even the best ones are not actionable for fantasy drafts … teams change dramatically every season, especially on defense; simple turnover luck can help the worst passing defense improve to middle-of-the-pack." | Team-level 2026 SOS: easiest DET (1), NO (2), CIN (3), CLE (4), NYJ (5); hardest LAR (28), DAL (29), CAR (30), MIA (31), ARI (32). Fantasy: "Gibbs has the easiest-ranked rushing schedule this season" (DET favored in 14 games; opens NO, BUF, NYJ, CAR, ARI); Carolina the most difficult RB schedule. |
| **Fantasy Points** — [Points Allowed – Schedule Adjusted](https://www.fantasypoints.com/nfl/stats/points-allowed/schedule-adjusted); annual position SOS articles (e.g. [2025 QB SOS](https://www.fantasypoints.com/nfl/articles/season/2025/fantasy-strength-of-schedule-qbs)) | Publishes schedule-adjusted fantasy points allowed by position (a data page) and preseason SOS articles by position built from it. Dynasty Nerds' [2026 SOS Standouts](https://www.dynastynerds.com/analytics/2026-schedule-standouts/) is built entirely on "the FantasyPoints data suite" and reports 2025 FP/G allowed: WR — DAL 39.3, IND 36.2, BAL 36.0, CHI 35.9, DET 35.8, LAR 33.0; TE — CIN 21.0, ARI 17.0, PIT 16.7. | Dynasty Nerds (Fantasy Points data): "Philadelphia has the easiest schedules at every position, including quarterback"; GB faces six top-11 WR-generous defenses (CHI x2, DET x2, DAL, LAR). Mark Andrews 2nd-friendliest TE slate; Kelce 5th. |
| **ESPN (Mike Clay)** — [Why the 2026 schedule benefits the Lions and Eagles](https://www.espn.com/fantasy/football/story/_/id/48755471/fantasy-football-2026-nfl-schedule-strength); [2026 Projection Guide PDF](https://g.espncdn.com/s/ffldraftkit/26/NFLDK2026_CS_ClayProjections2026.pdf) (blocked) | **Projection-based**: charts for QB/RB/WR/TE/DST/K show "where each position ranked in SOS last season, as well as a projection for 2026 based on each team's schedule (Weeks 1 to 17)". Uses his 2026 team/unit projections, not last year's FPA. "Lower/greener = easier." Week 18 excluded. Also publishes expected fantasy points against (xFPA) in season. | Eagles have "the easiest projected schedule at three of the four key fantasy positions" (five NFC East games + A-plus matchups vs TEN and ARI); Lions rival PHI for easiest fantasy-regular-season schedule. **Fantasy playoffs: hardest PHI, SEA, SF; easiest WAS, NO, ARI.** |
| **PFF** — [Fantasy SOS tool](https://www.pff.com/fantasy/strength-of-schedule); [WRs primed to exploit soft schedules](https://www.pff.com/news/fantasy-football-2026-wide-receivers-primed-to-exploit-soft-schedules); [RBs primed…](https://www.pff.com/news/fantasy-football-2026-running-backs-primed-to-exploit-soft-schedules) | "A league-wide, season-long view of opponent matchups for each fantasy position … the only one that factors in **PFF Player Grades** into its methodology" (i.e., roster/grade-based projection of each defense, not last year's FPA). | WR: Amon-Ra St. Brown softest WR schedule; Justin Jefferson 4th; Carnell Tate (rookie, 4th overall pick) 5th; George Pickens 6th; Steelers WRs 2nd-worst. RB: Blake Corum (LAR), Travis Etienne (NO), Jahmyr Gibbs (DET) the three softest; Etienne's boost strongest in the fantasy playoffs. TE: Andrews 2nd-friendliest, Kelce 5th. |
| **RotoBaller** — [Early-season SOS rankings (2026)](https://www.rotoballer.com/early-season-fantasy-football-strength-of-schedule-rankings-qb-rb-wr-te-matchups-2026/1915215); [Teams to target/fade](https://www.rotoballer.com/2026-fantasy-football-strength-of-schedule-teams-to-target-fade-2026/1861130) | Prior-season fantasy points allowed by position applied to **weeks 1-4** ("make-or-break first four weeks"); five easiest/toughest per position. | Patriots drew the 6th-toughest overall SOS (fade); target rookie RBs facing three bottom-tier run defenses out of the gate. Kyler Murray (MIN) early slate GB, CHI, TB, MIA, NO averaged 17.98 FP/G allowed to QBs in 2025. |
| **Draft Sharks** — [SOS article](https://www.draftsharks.com/article/fantasy-strength-of-schedule), per-position pages ([QB](https://www.draftsharks.com/strength-of-schedule/qb), [RB](https://www.draftsharks.com/strength-of-schedule/rb), [WR](https://www.draftsharks.com/strength-of-schedule/wr), [TE](https://www.draftsharks.com/strength-of-schedule/te)) | "Tabulated off total fantasy points allowed (PPR) to that position … values represent the **percentage difference in fantasy points allowed vs. what opponents usually score**" (i.e., opponent-adjusted). #1 = easiest, #32 = hardest. | Tables blocked. |
| **Footballguys** — [Ultimate SOS](https://www.footballguys.com/article/2026-ultimate-strength-of-schedule-sos) ([RB](https://www.footballguys.com/article/2026-strength-schedule-running-backs), [WR](https://www.footballguys.com/article/2026-strength-schedule-wide-receivers), [TE](https://www.footballguys.com/article/2026-strength-schedule-tight-ends)) | USOS "is based on fantasy points … scheduling bias has been removed … position-specific"; weekly color-coded opponent values. | Tables blocked. |
| **CBS Sports** (Dave Richard's projected SOS; [2025 methodology](https://www.cbssports.com/fantasy/football/news/2025-fantasy-football-strength-of-schedule-methodology-how-to-project-the-best-and-worst-schedules)) | Subjective/projected: studies "every defense, every projected starter, quality depth, scheme… playcaller tendencies", grades five categories (vs run, pass rush, vs pass, covering TEs/RBs, depth), applies grades to the schedule. Explicitly rejects using last season's numbers. | 2026 article not found in search. |
| **Yahoo** — [SOS matrix](https://sports.yahoo.com/fantasy/article/fantasy-football-strength-of-schedule-matrix-identifying-teams-with-best-and-worst-schedules-by-position-172441044.html), [easiest early-season schedules](https://sports.yahoo.com/fantasy/article/fantasy-football-players-at-each-position-who-have-the-easiest-early-season-schedules-for-2026-171040350.html) | Last season's FPA by position; "not a perfect picture, since offseason personnel moves, coaching changes, injuries, rookie additions and scheme adjustments will reshape how teams perform." Advice: "focus on the first few weeks." | Saquon Barkley 2nd-easiest RB schedule; Justin Jefferson 4th-easiest WR schedule. |
| **Fantasy Life** — [4 playoff schedules to target](https://www.fantasylife.com/articles/fantasy/4-fantasy-football-playoff-schedules-to-target) | Playoff (wk 15-17) power ranking using **weather (dome/warm), Vegas game totals, and "vibes"** rather than FPA. | DAL: @LAR (52.5), JAX (51.5), NYG (49.5) — three dome games; DET: @MIN (46.5), NYG (48.5), @CHI (49.5). |
| **Establish The Run** — [2026 playoff schedules](https://establishtherun.com/fantasy-football-playoff-schedules-3/) | Team-by-team wk 15-17 write-ups (venue, totals, opponent quality). | DAL best (three dome games, totals ~50); MIA plays six 2025 playoff teams in wk 13-18; PHI difficult finish. |
| **Fantasy Alarm** — [2026 playoff schedule rankings by position](https://www.fantasyalarm.com/articles/nfl/fantasy-football-draft-guide/2026-playoff-schedule-rankings/191969) | Index, 100 = league-average matchup, >100 softer. | Softest WR draws wk 15-17: CLE 114.4, TEN 111.5, MIN 110.2. |
| **Aggregator tables** ([FTA](https://fantasyteamadvice.com/nfl/strength-of-schedule), [StatChasers](https://statchasers.com/nfl/fantasy-football-strength-of-schedule/), [fftoolbox](https://fftoolbox.fulltimefantasy.com/football/strength_of_schedule.cfm)) | 2025 FPA per game by position credited to the defense, averaged over 2026 opponents; some index to 100. | The 2026 lists that recur across snippets (source page ambiguous among these): **QB** easiest PHI, TEN, CLE / toughest CHI, NYJ, LV; **RB** easiest LAR, SEA, WAS / toughest CIN, CAR, BUF; **WR** easiest PHI, MIN, TEN / toughest LAC, PIT, LV; **TE** easiest PHI, ATL, BAL / toughest GB, ARI, CHI. |

**Two families of method.** (a) *Backward-looking*: last season's fantasy points allowed per game by position, usually opponent-adjusted (FantasyPros, 4for4 aFPA, Draft Sharks, Footballguys USOS, Fantasy Points, Yahoo, RotoBaller, aggregators). (b) *Forward-looking*: projected defensive quality from Vegas win totals (Sharp), analyst projections (ESPN/Clay, CBS), or player grades (PFF). Nearly all outlets add a playoff-weeks (15-17) view and an early-weeks (1-4) view.

### Is SOS predictive? Published evidence
- **Footballguys, "The Strength of Schedule Myth" / "Can We Trust SOS?"** ([link](https://www.footballguys.com/article/15StengthofScheduleMyth)): teams giving up the fewest points to a position "are liable to fall out of the top 10 from year to year. In fact, no team has repeated as the stingiest against any position over the past five years"; personnel change is the main driver.
- **RotoWire, "According to the Data: Does SOS Matter?"** ([link](https://www.rotowire.com/football/article/according-to-the-data-does-strength-of-schedule-matter-18032)): year-to-year rank correlation for **run defense averaged 0.43** since 2010 (as low as 0.17 in 2011→12); **interceptions 0.14**; **pass defense negative (-0.295)** in one span ("the worst pass defenses one year often became the best the next").
- **SI, "2025/2026 schedule release will be mostly useless/irrelevant in fantasy drafts"** ([2025](https://www.si.com/fantasy/2025-nfl-schedule-release-will-be-mostly-useless-in-fantasy-football-drafts-01jv2f3v5frm), [2026](https://www.si.com/fantasy/nfl-2026-schedule-release-irrelevant-fantasy-football)): Cowboys allowed 14.2 FP/G to QBs (7th-fewest) in 2023, then the most (~21) in 2024; Eagles allowed 44.6 FP/G to WRs in 2023, 31 in 2024; "the gap between players with the best and the worst schedules … has been shrinking"; "schedule works best as a tiebreaker rather than a main argument."
- **Fantasy Index (Ian Allen), via Footballguys forum** ([link](https://forums.footballguys.com/threads/predictive-validity-of-preseason-sos-rankings.768063/)): preseason SOS is "virtually useless except at the extremes."
- **Sharp Football**: "no perfect way … even the best ones are not actionable for fantasy drafts."
- **Yahoo / RotoBaller / 4for4**: the actionable use is the **first few weeks** (roster you can pivot from) and **weeks 15-17** as a tiebreaker.

### Own stability test (nflverse 2024 → 2025, PPR points allowed per game by position)
Computed from the same files used for the ratings (see section 2):

| | QB | RB | WR | TE |
|---|---|---|---|---|
| Year-over-year r, raw FPA/g (2024 vs 2025) | 0.25 | 0.20 | -0.09 | 0.24 |
| Year-over-year r, schedule-adjusted FPA/g | 0.12 | 0.24 | -0.09 | 0.32 |
| r(2025 team SOS built from 2024 adj. ratings, 2025 team SOS built from actual 2025 adj. ratings), wk 1-17 | -0.25 | -0.15 | 0.16 | 0.79 |
| same, playoff weeks 15-17 only | 0.08 | 0.01 | -0.26 | 0.64 |
| Spread of *actual* 2025 SOS across 32 teams (pts/game, sd; max-min) | 0.57; 2.6 | 0.61; 3.0 | 0.87; 3.5 | 0.55; 2.0 |

Reading: a defense's points allowed to QB/RB/TE carries roughly r≈0.2-0.3 into the next season and WR essentially zero; preseason SOS built from last year's numbers had no predictive relationship with the realized 2025 SOS for QB/RB/WR (TE was the exception this year — treat as a one-season result, not a rule). Even the realized spread is modest: about 3 PPR points per game between the easiest and hardest WR *team* schedule (shared across 3-4 receivers), ~3 for RB rooms, ~2.5 for QBs. This matches the outlets' consensus: **use SOS as a tiebreaker only, weight early weeks and weeks 15-17, and prefer forward-looking defense projections where available.**

## 2. Defense-quality table for 2026 (computed here)

**Source and method (computed by this agent, not copied):**
- Files: `nflverse/stats_player_week_2025.csv` and `nflverse/stats_player_week_2024.csv` (nflverse-data release `stats_player`), regular season weeks 1-18 only, positions QB/RB/WR/TE as tagged by nflverse (`LA` mapped to `LAR`).
- Points: nflverse `fantasy_points_ppr` (0.04/yd pass, 4 pass TD, -2 INT, 0.1/yd rush & rec, 6 TD, 1/reception, -2 fumble lost, 2 for 2-pt). Every player's points in a game are credited to the `opponent_team` defense and summed by position; divided by 17 games per defense = **raw FPA/g** (2025 league averages: QB 16.3, RB 22.0, WR 30.8, TE 13.3).
- **Schedule adjustment** (the 4for4-aFPA / Footballguys-USOS idea): each team-game's positional points = league mean + offense effect + defense effect, solved by 10 alternating-least-squares iterations, so a defense that faced strong offenses is not penalized. `adj_2025` and `adj_2024` are those defense effects re-centered on the league mean.
- **Final rating = 0.75 × adj_2025 + 0.25 × adj_2024** (prior year at lower weight as mild shrinkage given the low year-over-year stability above). Higher = more points allowed = easier matchup.
- **Cross-check vs. published 2025 numbers** (search snippets, Fantasy Points data via Dynasty Nerds, and FantasyPros): WR raw — DAL 39.3 (ours 39.31), IND 36.2 (36.13), BAL 36.0 (35.96), CHI 35.9 (36.21), DET 35.8 (35.70), LAR 33.0 (ours 31.71 — the one material discrepancy, likely position tagging of a Rams opponent's receivers); TE raw — CIN 21.0 (20.86), ARI 17.0 (16.94), PIT 16.7 (16.61); QB — WAS 3rd-most (ours 3rd), TEN 5th-most (ours 5th). Small differences come from position tags and the position-assignment of gadget players.
- **No numeric 2026 overlay**: no complete 1-32 projected defensive table (Sharp/PFF/ESPN unit grades) could be retrieved through snippets, and blending a partial list would bias only the mentioned teams. Qualitative 2026 changes are listed in section 3 and in `sos.json → defense_ratings[team].notes_2026`; the consensus signals are LAR (big upgrade), SEA/HOU (elite), ARI/MIA (weak), CLE/KC (downgrades).

Ratings (PPR points allowed per game; higher = more generous):

| Team | QB | RB | WR | TE | QB raw25 | RB raw25 | WR raw25 | TE raw25 | QB adj24 | RB adj24 | WR adj24 | TE adj24 | rank QB/RB/WR/TE (1 = most generous) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ARI | 16.31 | 24.92 | 27.64 | 15.32 | 16.95 | 26.22 | 30.16 | 16.94 | 15.96 | 23.56 | 30.25 | 10.63 | 17/6/28/4 |
| ATL | 17.52 | 21.87 | 34.35 | 10.93 | 16.32 | 21.51 | 33.63 | 10.19 | 20.21 | 21.49 | 38.03 | 12.30 | 11/15/7/28 |
| BAL | 17.97 | 21.93 | 36.85 | 11.00 | 17.71 | 23.12 | 35.96 | 10.92 | 17.21 | 19.85 | 36.27 | 12.52 | 8/13/2/27 |
| BUF | 14.80 | 24.62 | 30.20 | 9.21 | 13.09 | 23.92 | 26.46 | 7.57 | 16.05 | 25.47 | 34.45 | 11.52 | 24/8/21/31 |
| CAR | 15.17 | 24.95 | 27.61 | 13.85 | 13.82 | 24.15 | 26.58 | 13.71 | 20.72 | 29.41 | 34.29 | 14.44 | 21/5/29/10 |
| CHI | 17.52 | 21.92 | 34.66 | 13.09 | 18.13 | 21.16 | 36.21 | 13.06 | 13.07 | 24.49 | 27.19 | 12.84 | 10/14/6/12 |
| CIN | 19.07 | 26.12 | 30.18 | 19.32 | 18.42 | 28.30 | 25.29 | 20.86 | 18.76 | 23.12 | 34.46 | 15.47 | 3/2/22/1 |
| CLE | 14.54 | 19.87 | 31.22 | 11.91 | 13.31 | 21.85 | 26.91 | 12.11 | 16.33 | 18.91 | 37.11 | 11.77 | 26/23/18/23 |
| DAL | 22.37 | 25.34 | 39.25 | 12.10 | 23.33 | 24.89 | 39.31 | 12.35 | 19.76 | 21.66 | 36.27 | 9.91 | 1/3/1/22 |
| DEN | 14.48 | 19.83 | 27.96 | 13.00 | 14.20 | 16.95 | 27.03 | 13.65 | 16.25 | 21.32 | 32.52 | 10.39 | 27/24/26/15 |
| DET | 18.07 | 19.92 | 35.52 | 12.74 | 18.23 | 19.37 | 35.70 | 13.67 | 17.58 | 19.02 | 35.08 | 10.14 | 7/22/4/18 |
| GB | 15.15 | 21.23 | 31.07 | 12.40 | 15.01 | 21.46 | 31.25 | 12.11 | 14.45 | 21.72 | 29.78 | 13.01 | 22/17/19/20 |
| HOU | 13.13 | 19.47 | 27.36 | 11.68 | 12.82 | 19.97 | 25.94 | 12.28 | 17.04 | 19.05 | 34.33 | 11.51 | 31/27/30/24 |
| IND | 17.30 | 21.16 | 35.66 | 15.13 | 16.90 | 19.94 | 36.13 | 15.24 | 18.11 | 24.30 | 34.07 | 16.35 | 12/18/3/6 |
| JAX | 17.25 | 21.13 | 31.91 | 14.43 | 15.86 | 18.32 | 31.24 | 14.78 | 20.93 | 26.91 | 37.30 | 14.53 | 13/19/14/8 |
| KC | 14.97 | 18.77 | 28.24 | 12.15 | 15.08 | 19.20 | 27.34 | 11.01 | 16.93 | 16.04 | 34.05 | 14.31 | 23/31/25/21 |
| LAC | 13.80 | 19.70 | 29.91 | 9.90 | 12.58 | 18.52 | 27.42 | 10.45 | 16.41 | 18.76 | 35.30 | 8.38 | 29/26/24/30 |
| LAR | 15.71 | 19.44 | 32.18 | 13.05 | 15.16 | 20.16 | 31.71 | 13.13 | 17.20 | 20.40 | 34.27 | 13.81 | 19/28/12/13 |
| LV | 15.66 | 23.99 | 31.72 | 11.53 | 16.09 | 22.95 | 33.51 | 10.06 | 17.79 | 22.09 | 31.75 | 14.84 | 20/10/15/26 |
| MIA | 17.16 | 23.97 | 31.57 | 15.91 | 18.16 | 24.86 | 29.87 | 16.28 | 14.32 | 22.51 | 31.60 | 13.20 | 15/11/16/3 |
| MIN | 12.10 | 18.38 | 26.68 | 11.66 | 11.12 | 19.58 | 23.72 | 10.65 | 15.32 | 18.63 | 38.39 | 13.19 | 32/32/31/25 |
| NE | 16.15 | 19.82 | 33.36 | 13.82 | 14.70 | 18.76 | 29.19 | 13.81 | 16.10 | 24.45 | 32.18 | 12.52 | 18/25/9/11 |
| NO | 14.68 | 20.42 | 30.05 | 12.80 | 14.00 | 20.72 | 27.78 | 12.48 | 16.54 | 24.21 | 34.33 | 12.73 | 25/21/23/17 |
| NYG | 17.20 | 26.46 | 31.96 | 10.72 | 18.25 | 25.70 | 33.78 | 11.36 | 15.95 | 24.28 | 32.82 | 9.12 | 14/1/13/29 |
| NYJ | 18.89 | 24.97 | 31.28 | 14.31 | 19.95 | 27.98 | 30.35 | 15.23 | 16.32 | 20.06 | 32.15 | 10.92 | 4/4/17/9 |
| PHI | 13.53 | 21.51 | 25.56 | 8.79 | 14.53 | 22.75 | 26.78 | 8.34 | 14.39 | 16.47 | 30.07 | 9.44 | 30/16/32/32 |
| PIT | 18.10 | 19.07 | 35.19 | 16.30 | 18.79 | 19.46 | 35.24 | 16.61 | 13.78 | 20.54 | 31.99 | 13.67 | 6/29/5/2 |
| SEA | 14.36 | 18.89 | 27.89 | 13.01 | 14.00 | 18.48 | 26.26 | 14.68 | 16.14 | 20.85 | 33.09 | 12.24 | 28/30/27/14 |
| SF | 16.70 | 23.99 | 30.53 | 12.95 | 17.11 | 23.58 | 32.16 | 14.82 | 15.81 | 24.62 | 29.43 | 10.16 | 16/9/20/16 |
| TB | 19.91 | 20.76 | 32.99 | 15.21 | 19.45 | 22.06 | 31.46 | 15.81 | 20.37 | 19.05 | 37.17 | 13.90 | 2/20/10/5 |
| TEN | 17.76 | 22.78 | 32.38 | 12.68 | 19.05 | 21.41 | 35.58 | 14.16 | 16.39 | 24.30 | 28.24 | 10.70 | 9/12/11/19 |
| WAS | 18.44 | 24.73 | 33.51 | 15.12 | 19.56 | 25.45 | 34.91 | 15.89 | 15.76 | 21.90 | 33.03 | 11.05 | 5/7/8/7 |

## 3. 2026 defensive changes worth overlaying by hand (from search snippets; not applied numerically)
- **ARI**: Ranked the worst projected defense for 2026 by Sportsnaut.
- **BAL**: New DC in 2026 (search snippets conflict: Anthony Weaver vs. Mike Rutenberg).
- **BUF**: New DC Jim Leonhard.
- **CAR**: Signed EDGE Jaelan Phillips.
- **CIN**: Reportedly acquired DL "Lawrence" from NYG for the No. 10 pick (per CBS/ESPN snippets).
- **CLE**: Lost Myles Garrett (to LAR); received Jared Verse. Pass rush likely worse than 2025 numbers imply.
- **DAL**: New DC in 2026 (snippets conflict: Christian Parker from PHI vs. Jonathan Gannon). 2025 unit was the most generous in the league to QB/WR/RB.
- **HOU**: Consensus top-3 projected defense for 2026 (NFL.com/Sportsnaut rank it No.1).
- **JAX**: Cited as a strong run defense / top-10 projected unit (NFL.com).
- **KC**: Traded CB Trent McDuffie (and Watson) to LAR; secondary likely weaker than 2025.
- **LAC**: New DC Chris O'Leary (replacing Jesse Minter).
- **LAR**: Major 2026 upgrade: traded for EDGE Myles Garrett (from CLE, for Jared Verse + picks) and CB Trent McDuffie (+ Watson) from KC; ratings based on 2025 likely understate this pass defense.
- **MIA**: Projected among the worst pass defenses in 2026 (Sportsnaut).
- **NYG**: New DC Dennard Wilson; reportedly traded DL "Lawrence" to CIN for the No. 10 pick.
- **PHI**: Traded for EDGE Jonathan Greenard (per CBS/ESPN offseason recaps).
- **PIT**: New DC Patrick Graham; added a starting DB (reported as "Dean", 3yr/$36.75M) opposite Joey Porter Jr.
- **SEA**: 2025 No.1 scoring defense; consensus top-3 projected unit for 2026 (NFL.com, Sportsnaut).
- **TB**: Cited as a top-10 projected defense (NFL.com).
- **TEN**: Traded for EDGE Jermaine Johnson II; signed John Franklin-Myers.
- **WAS**: Signed EDGE Odafe Oweh and K'Lavon Chaisson; new DC Sean Duggan (from GB).

Also: 14 teams have new defensive coordinators in 2026 (FOX Sports / CBS coordinator-grade pieces) — the largest turnover in years — which further weakens the carry-over of 2025 numbers. Other reported DC hires: PIT Patrick Graham, BUF Jim Leonhard, NYG Dennard Wilson, WAS Sean Duggan, LAC Chris O'Leary. Snippets conflicted on BAL (Weaver vs. Rutenberg) and DAL (Parker vs. Gannon) — verify before relying on them.

## 4. 2026 SOS results (rank 1 = easiest; value in parentheses = mean opponent rating, PPR pts/game allowed)

### Full season, weeks 1-17
- **QB** easiest: PHI (17.38), TEN (17.25), CLE (17.23), HOU (16.99), NYG (16.93); hardest: LV (15.54), NYJ (15.74), SF (15.85), BUF (15.88), DEN (15.98)
- **RB** easiest: PHI (22.77), SEA (22.77), LAR (22.73), WAS (22.47), NO (22.39); hardest: CAR (20.81), BUF (21.07), LV (21.35), CIN (21.37), ATL (21.45)
- **WR** easiest: TEN (32.80), HOU (32.65), CLE (32.60), CIN (32.56), PHI (32.53); hardest: LV (30.14), LAR (30.41), SF (30.53), DEN (30.58), LAC (30.61)
- **TE** easiest: ATL (13.66), CLE (13.58), BAL (13.54), PHI (13.54), CIN (13.53); hardest: ARI (12.39), SF (12.45), LAR (12.48), DAL (12.56), WAS (12.58)

### Early season, weeks 1-4
- **QB** easiest: HOU (18.39), NYG (18.04), BAL (18.03), CLE (17.61), MIN (17.43); hardest: MIA (14.85), CHI (14.92), LV (15.15), TB (15.21), LAC (15.28)
- **RB** easiest: HOU (24.31), DET (23.74), TEN (23.72), DAL (23.15), NYG (23.12); hardest: BUF (19.73), CIN (20.11), LV (20.72), DEN (20.83), CAR (20.89)
- **WR** easiest: NO (34.61), BAL (34.34), CAR (33.94), HOU (33.82), NYJ (33.41); hardest: CHI (27.78), LAR (29.00), MIA (29.29), LAC (29.36), TB (29.79)
- **TE** easiest: CLE (14.95), JAX (14.51), CIN (14.40), SF (14.32), MIN (14.15); hardest: TEN (11.21), LAR (11.36), NO (11.55), ARI (11.65), BUF (12.04)

### Fantasy playoffs, weeks 15-17
- **QB** easiest: LAR (18.88), MIN (18.46), NYG (18.33), JAX (17.98), NO (17.91); hardest: SF (14.10), MIA (14.58), PHI (14.73), SEA (14.80), NYJ (14.85)
- **RB** easiest: PIT (23.22), MIN (23.20), CLE (23.18), JAX (23.18), ARI (23.13); hardest: SF (19.99), WAS (20.46), TB (20.58), PHI (20.78), NYJ (21.04)
- **WR** easiest: NYG (35.33), CLE (34.82), TEN (34.19), MIN (33.44), LAR (33.38); hardest: SF (27.91), SEA (28.45), PHI (28.59), NE (29.16), NYJ (29.23)
- **TE** easiest: CAR (16.21), BAL (15.84), IND (14.64), ATL (14.37), TEN (14.32); hardest: SF (10.28), MIA (10.50), CHI (11.45), DEN (11.52), DET (11.82)

Comparison with the outlets: our full-season lists agree with the published consensus on most of the extremes — PHI/TEN/CLE easiest for QB and PHI/TEN among the easiest for WR; LV, SF, DEN, LAC hardest for WR/QB; CAR/BUF/CIN hardest for RB; PHI/ATL/BAL/CLE easiest for TE; ARI hardest for TE — and on the playoff extremes (SF, PHI, SEA hardest; ESPN's Clay independently has PHI/SEA/SF hardest in weeks 15-17). Where we differ (e.g., our RB list has PHI/SEA/LAR/WAS at the top versus the aggregators' LAR/SEA/WAS) it is because of the schedule adjustment and the 25% 2024 weight; `full_rank_2025only` in `sos.json` gives the unblended 2025-only rank.

### All 32 teams — full season
| Team | Bye | QB rank (QB avg) | RB rank (RB avg) | WR rank (WR avg) | TE rank (TE avg) | Opponents |
|---|---|---|---|---|---|---|
| ARI | 14 | 22 (16.18) | 22 (21.64) | 22 (30.98) | 32 (12.39) | @LAC, SEA, @SF, @NYG, DET, @LAR, DEN, @DAL, @SEA, LAR, @KC, WAS, PHI, BYE, NYJ, @NO, LV |
| ATL | 11 | 11 (16.68) | 28 (21.45) | 13 (31.71) | 1 (13.66) | @PIT, CAR, @GB, @NO, BAL, CHI, SF, @TB, CIN, KC, BYE, @MIN, DET, @CLE, @WAS, TB, NO |
| BAL | 13 | 8 (16.81) | 14 (22.08) | 10 (31.85) | 3 (13.54) | @IND, NO, @DAL, TEN, @ATL, @CLE, CIN, @BUF, JAX, LAC, @CAR, @HOU, BYE, TB, @PIT, CLE, @CIN |
| BUF | 7 | 29 (15.88) | 31 (21.07) | 14 (31.46) | 18 (12.87) | @HOU, DET, LAC, NE, @LAR, @LV, BYE, BAL, @MIN, @NYJ, MIA, KC, @NE, @GB, CHI, @DEN, @MIA |
| CAR | 5 | 16 (16.35) | 32 (20.81) | 15 (31.45) | 11 (13.14) | CHI, @ATL, @CLE, DET, BYE, @PHI, TB, @GB, DEN, @NO, BAL, @TB, @MIN, NO, CIN, @PIT, SEA |
| CHI | 10 | 24 (16.12) | 26 (21.47) | 21 (31.04) | 24 (12.76) | @CAR, MIN, PHI, NYJ, @GB, @ATL, NE, @SEA, TB, BYE, NO, @DET, JAX, @MIA, @BUF, GB, DET |
| CIN | 6 | 7 (16.87) | 29 (21.37) | 4 (32.56) | 5 (13.53) | TB, @HOU, @PIT, JAX, @MIA, BYE, @BAL, TEN, @ATL, PIT, @WAS, NO, @CLE, KC, @CAR, @IND, BAL |
| CLE | 11 | 3 (17.23) | 10 (22.25) | 3 (32.60) | 2 (13.58) | @JAX, @TB, CAR, PIT, @NYJ, BAL, @TEN, @PIT, @NO, HOU, BYE, LV, CIN, ATL, @NYG, @BAL, IND |
| DAL | 14 | 17 (16.34) | 9 (22.27) | 24 (30.94) | 29 (12.56) | @NYG, WAS, BAL, @HOU, TB, @GB, @PHI, ARI, @IND, SF, TEN, PHI, @SEA, BYE, @LAR, JAX, NYG |
| DEN | 10 | 28 (15.98) | 18 (21.94) | 29 (30.58) | 12 (13.09) | @KC, JAX, LAR, @SF, @LAC, SEA, @ARI, KC, @CAR, BYE, LV, @PIT, MIA, @NYJ, @LV, BUF, @NE |
| DET | 6 | 21 (16.25) | 8 (22.34) | 19 (31.07) | 17 (12.92) | NO, @BUF, NYJ, @CAR, @ARI, BYE, GB, MIN, @MIA, NE, TB, CHI, @ATL, TEN, @MIN, NYG, @CHI |
| GB | 11 | 14 (16.42) | 23 (21.63) | 12 (31.78) | 21 (12.82) | @MIN, @NYJ, ATL, @TB, CHI, DAL, @DET, CAR, @NE, MIN, BYE, @LAR, @NO, BUF, MIA, @CHI, HOU |
| HOU | 8 | 4 (16.99) | 7 (22.37) | 2 (32.65) | 15 (13.04) | BUF, CIN, @IND, DAL, @TEN, @JAX, NYG, BYE, @LAC, @CLE, IND, BAL, @PIT, @WAS, JAX, @PHI, @GB |
| IND | 13 | 12 (16.53) | 17 (21.99) | 16 (31.35) | 16 (13.01) | BAL, @KC, HOU, @WAS, @PIT, TEN, @MIN, @JAX, DAL, MIA, @HOU, NYG, BYE, @PHI, @TEN, CIN, @CLE |
| JAX | 7 | 9 (16.78) | 16 (22.02) | 8 (32.18) | 13 (13.06) | CLE, @DEN, NE, @CIN, PHI, HOU, BYE, IND, @BAL, @TEN, @NYG, TEN, @CHI, PIT, @HOU, @DAL, WAS |
| KC | 5 | 26 (16.01) | 15 (22.05) | 25 (30.77) | 10 (13.14) | DEN, IND, @MIA, @LV, BYE, LAC, @SEA, @DEN, NYJ, @ATL, ARI, @BUF, @LAR, @CIN, NE, SF, @LAC |
| LAC | 7 | 25 (16.05) | 19 (21.76) | 28 (30.61) | 20 (12.86) | ARI, LV, @BUF, @SEA, DEN, @KC, BYE, @LAR, HOU, @BAL, NYJ, NE, @TB, @LV, SF, @MIA, KC |
| LAR | 11 | 20 (16.29) | 3 (22.73) | 31 (30.41) | 30 (12.48) | SF, NYG, @DEN, @PHI, BUF, ARI, @LV, LAC, @WAS, @ARI, BYE, GB, KC, @SF, DAL, @SEA, @TB |
| LV | 13 | 32 (15.54) | 30 (21.35) | 32 (30.14) | 27 (12.68) | MIA, @LAC, @NO, KC, @NE, BUF, LAR, @NYJ, @SF, SEA, @DEN, @CLE, BYE, LAC, DEN, TEN, @ARI |
| MIA | 6 | 23 (16.15) | 12 (22.13) | 18 (31.15) | 23 (12.80) | @LV, @SF, KC, @MIN, CIN, BYE, @NYJ, NE, DET, @IND, @BUF, NYJ, @DEN, CHI, @GB, LAC, BUF |
| MIN | 6 | 6 (16.92) | 11 (22.22) | 6 (32.43) | 8 (13.29) | GB, @CHI, @TB, MIA, @NO, BYE, IND, @DET, BUF, @GB, @SF, ATL, CAR, @NE, DET, WAS, @NYJ |
| NE | 11 | 27 (16.00) | 25 (21.62) | 23 (30.96) | 26 (12.70) | @SEA, PIT, @JAX, @BUF, LV, NYJ, @CHI, @MIA, GB, @DET, BYE, @LAC, BUF, MIN, @KC, @NYJ, DEN |
| NO | 8 | 10 (16.68) | 5 (22.39) | 11 (31.85) | 9 (13.17) | @DET, @BAL, LV, ATL, MIN, @NYG, PIT, BYE, CLE, CAR, @CHI, @CIN, GB, @CAR, @TB, ARI, @ATL |
| NYG | 8 | 5 (16.93) | 13 (22.10) | 9 (32.09) | 14 (13.06) | DAL, @LAR, TEN, ARI, @WAS, NO, @HOU, BYE, @PHI, WAS, JAX, @IND, SF, @SEA, CLE, @DET, @DAL |
| NYJ | 13 | 31 (15.74) | 27 (21.47) | 20 (31.07) | 22 (12.81) | @TEN, GB, @DET, @CHI, CLE, @NE, MIA, LV, @KC, BUF, @LAC, @MIA, BYE, DEN, @ARI, NE, MIN |
| PHI | 10 | 1 (17.38) | 1 (22.77) | 5 (32.53) | 4 (13.54) | WAS, @TEN, @CHI, LAR, @JAX, CAR, DAL, @WAS, NYG, BYE, PIT, @DAL, @ARI, IND, SEA, HOU, @SF |
| PIT | 9 | 15 (16.38) | 20 (21.73) | 17 (31.18) | 6 (13.49) | ATL, @NE, CIN, @CLE, IND, @TB, @NO, CLE, BYE, @CIN, @PHI, DEN, HOU, @JAX, BAL, CAR, @TEN |
| SEA | 11 | 19 (16.31) | 2 (22.77) | 26 (30.77) | 25 (12.73) | NE, @ARI, @WAS, LAC, SF, @DEN, KC, CHI, ARI, @LV, BYE, @SF, DAL, NYG, @PHI, LAR, @CAR |
| SF | 8 | 30 (15.85) | 24 (21.63) | 30 (30.53) | 31 (12.45) | @LAR, MIA, ARI, DEN, @SEA, WAS, @ATL, BYE, LV, @DAL, MIN, SEA, @NYG, LAR, @LAC, @KC, PHI |
| TB | 10 | 13 (16.53) | 21 (21.69) | 7 (32.29) | 19 (12.87) | @CIN, CLE, MIN, GB, @DAL, PIT, @CAR, ATL, @CHI, BYE, @DET, CAR, LAC, @BAL, NO, @ATL, LAR |
| TEN | 9 | 2 (17.25) | 6 (22.37) | 1 (32.80) | 7 (13.41) | NYJ, PHI, @NYG, @BAL, HOU, @IND, CLE, @CIN, BYE, JAX, @DAL, @JAX, WAS, @DET, IND, @LV, PIT |
| WAS | 7 | 18 (16.31) | 4 (22.47) | 27 (30.69) | 28 (12.58) | @PHI, @DAL, SEA, IND, NYG, @SF, BYE, PHI, LAR, @NYG, CIN, @ARI, @TEN, HOU, ATL, @MIN, @JAX |

### All 32 teams — weeks 1-4
| Team | Bye | QB rank (QB avg) | RB rank (RB avg) | WR rank (WR avg) | TE rank (TE avg) | Opponents |
|---|---|---|---|---|---|---|
| ARI | 14 | 25 (15.52) | 11 (22.26) | 24 (30.07) | 29 (11.65) | @LAC, SEA, @SF, @NYG |
| ATL | 11 | 24 (15.77) | 22 (21.42) | 21 (30.98) | 9 (13.84) | @PIT, CAR, @GB, @NO |
| BAL | 13 | 3 (18.03) | 9 (22.43) | 2 (34.34) | 15 (13.18) | @IND, NO, @DAL, TEN |
| BUF | 7 | 27 (15.29) | 32 (19.73) | 15 (31.54) | 28 (12.04) | @HOU, DET, LAC, NE |
| CAR | 5 | 11 (16.91) | 28 (20.89) | 3 (33.94) | 24 (12.17) | CHI, @ATL, @CLE, DET |
| CHI | 10 | 31 (14.92) | 8 (22.45) | 32 (27.78) | 25 (12.15) | @CAR, MIN, PHI, NYJ |
| CIN | 6 | 10 (17.10) | 31 (20.11) | 13 (31.86) | 3 (14.40) | TB, @HOU, @PIT, JAX |
| CLE | 11 | 4 (17.61) | 20 (21.48) | 12 (31.93) | 1 (14.95) | @JAX, @TB, CAR, PIT |
| DAL | 14 | 15 (16.68) | 4 (23.15) | 9 (32.42) | 26 (12.13) | @NYG, WAS, BAL, @HOU |
| DEN | 10 | 17 (16.16) | 29 (20.83) | 22 (30.72) | 16 (13.15) | @KC, JAX, LAR, @SF |
| DET | 6 | 23 (15.88) | 2 (23.74) | 27 (29.79) | 20 (12.54) | NO, @BUF, NYJ, @CAR |
| GB | 11 | 9 (17.10) | 19 (21.49) | 18 (31.33) | 17 (13.03) | @MIN, @NYJ, ATL, @TB |
| HOU | 8 | 1 (18.39) | 1 (24.31) | 4 (33.82) | 7 (13.94) | BUF, CIN, @IND, DAL |
| IND | 13 | 20 (16.13) | 26 (21.23) | 16 (31.49) | 21 (12.49) | BAL, @KC, HOU, @WAS |
| JAX | 7 | 21 (16.06) | 23 (21.41) | 23 (30.68) | 2 (14.51) | CLE, @DEN, NE, @CIN |
| KC | 5 | 18 (16.15) | 12 (22.24) | 14 (31.73) | 8 (13.89) | DEN, IND, @MIA, @LV |
| LAC | 7 | 28 (15.28) | 6 (23.11) | 29 (29.36) | 22 (12.27) | ARI, LV, @BUF, @SEA |
| LAR | 11 | 26 (15.48) | 7 (22.95) | 31 (29.00) | 31 (11.36) | SF, NYG, @DEN, @PHI |
| LV | 13 | 30 (15.15) | 30 (20.72) | 25 (29.94) | 19 (12.69) | MIA, @LAC, @NO, KC |
| MIA | 6 | 32 (14.85) | 25 (21.28) | 30 (29.29) | 27 (12.07) | @LV, @SF, KC, @MIN |
| MIN | 6 | 5 (17.43) | 15 (21.97) | 8 (32.57) | 5 (14.15) | GB, @CHI, @TB, MIA |
| NE | 11 | 19 (16.13) | 27 (20.93) | 19 (31.30) | 14 (13.24) | @SEA, PIT, @JAX, @BUF |
| NO | 8 | 7 (17.30) | 16 (21.93) | 1 (34.61) | 30 (11.55) | @DET, @BAL, LV, ATL |
| NYG | 8 | 2 (18.04) | 5 (23.12) | 7 (32.87) | 13 (13.29) | DAL, @LAR, TEN, ARI |
| NYJ | 13 | 8 (17.12) | 21 (21.46) | 5 (33.41) | 18 (12.73) | @TEN, GB, @DET, @CHI |
| PHI | 10 | 6 (17.36) | 13 (22.22) | 6 (33.18) | 12 (13.49) | WAS, @TEN, @CHI, LAR |
| PIT | 9 | 14 (16.82) | 17 (21.92) | 10 (32.28) | 6 (13.99) | ATL, @NE, CIN, @CLE |
| SEA | 11 | 16 (16.18) | 10 (22.29) | 20 (31.11) | 11 (13.54) | NE, @ARI, @WAS, LAC |
| SF | 8 | 22 (15.92) | 14 (22.04) | 26 (29.84) | 4 (14.32) | @LAR, MIA, ARI, DEN |
| TB | 10 | 29 (15.21) | 24 (21.40) | 28 (29.79) | 10 (13.82) | @CIN, CLE, MIN, GB |
| TEN | 9 | 12 (16.90) | 3 (23.72) | 17 (31.41) | 32 (11.21) | NYJ, PHI, @NYG, @BAL |
| WAS | 7 | 13 (16.89) | 18 (21.73) | 11 (32.09) | 23 (12.26) | @PHI, @DAL, SEA, IND |

### All 32 teams — weeks 15-17
| Team | Bye | QB rank (QB avg) | RB rank (RB avg) | WR rank (WR avg) | TE rank (TE avg) | Opponents |
|---|---|---|---|---|---|---|
| ARI | 14 | 15 (16.41) | 5 (23.13) | 22 (31.02) | 17 (12.88) | NYJ, @NO, LV |
| ATL | 11 | 6 (17.68) | 14 (21.97) | 12 (32.18) | 4 (14.37) | @WAS, TB, NO |
| BAL | 13 | 8 (17.23) | 21 (21.68) | 10 (32.20) | 2 (15.84) | @PIT, CLE, @CIN |
| BUF | 7 | 16 (16.39) | 17 (21.91) | 16 (31.39) | 7 (14.00) | CHI, @DEN, @MIA |
| CAR | 5 | 9 (17.18) | 24 (21.36) | 21 (31.09) | 1 (16.21) | CIN, @PIT, SEA |
| CHI | 10 | 20 (16.01) | 16 (21.92) | 9 (32.26) | 30 (11.45) | @BUF, GB, DET |
| CIN | 6 | 13 (16.81) | 8 (22.68) | 6 (33.37) | 14 (13.33) | @CAR, @IND, BAL |
| CLE | 11 | 7 (17.49) | 3 (23.18) | 2 (34.82) | 22 (12.28) | @NYG, @BAL, IND |
| DAL | 14 | 14 (16.72) | 11 (22.34) | 13 (32.02) | 18 (12.73) | @LAR, JAX, NYG |
| DEN | 10 | 26 (15.54) | 7 (22.81) | 14 (31.76) | 29 (11.52) | @LV, BUF, @NE |
| DET | 6 | 24 (15.61) | 12 (22.25) | 20 (31.10) | 28 (11.82) | @MIN, NYG, @CHI |
| GB | 11 | 22 (15.94) | 19 (21.79) | 19 (31.20) | 12 (13.56) | MIA, @CHI, HOU |
| HOU | 8 | 27 (15.31) | 25 (21.29) | 26 (29.51) | 27 (11.87) | JAX, @PHI, @GB |
| IND | 13 | 10 (17.12) | 6 (22.92) | 18 (31.26) | 3 (14.64) | @TEN, CIN, @CLE |
| JAX | 7 | 4 (17.98) | 4 (23.18) | 7 (33.37) | 16 (12.97) | @HOU, @DAL, WAS |
| KC | 5 | 25 (15.55) | 27 (21.17) | 17 (31.27) | 25 (12.22) | NE, SF, @LAC |
| LAC | 7 | 17 (16.27) | 13 (22.24) | 25 (30.12) | 9 (13.67) | SF, @MIA, KC |
| LAR | 11 | 1 (18.88) | 22 (21.66) | 5 (33.38) | 13 (13.44) | DAL, @SEA, @TB |
| LV | 13 | 18 (16.19) | 10 (22.51) | 27 (29.33) | 10 (13.67) | DEN, TEN, @ARI |
| MIA | 6 | 31 (14.58) | 18 (21.85) | 24 (30.39) | 31 (10.50) | @GB, LAC, BUF |
| MIN | 6 | 2 (18.46) | 2 (23.20) | 4 (33.44) | 6 (14.05) | DET, WAS, @NYJ |
| NE | 11 | 19 (16.11) | 26 (21.19) | 29 (29.16) | 15 (13.15) | @KC, @NYJ, DEN |
| NO | 8 | 5 (17.91) | 9 (22.52) | 15 (31.66) | 8 (13.82) | @TB, ARI, @ATL |
| NYG | 8 | 3 (18.33) | 20 (21.71) | 1 (35.33) | 24 (12.25) | CLE, @DET, @DAL |
| NYJ | 13 | 28 (14.85) | 28 (21.04) | 28 (29.23) | 11 (13.60) | @ARI, NE, MIN |
| PHI | 10 | 30 (14.73) | 29 (20.78) | 30 (28.59) | 19 (12.55) | SEA, HOU, @SF |
| PIT | 9 | 12 (16.97) | 1 (23.22) | 8 (32.28) | 20 (12.51) | BAL, CAR, @TEN |
| SEA | 11 | 29 (14.80) | 15 (21.97) | 31 (28.45) | 26 (11.90) | @PHI, LAR, @CAR |
| SF | 8 | 32 (14.10) | 32 (19.99) | 32 (27.91) | 32 (10.28) | @LAC, @KC, PHI |
| TB | 10 | 21 (15.97) | 30 (20.58) | 11 (32.19) | 23 (12.26) | NO, @ATL, LAR |
| TEN | 9 | 11 (17.02) | 23 (21.41) | 3 (34.19) | 5 (14.32) | IND, @LV, PIT |
| WAS | 7 | 23 (15.62) | 31 (20.46) | 23 (30.98) | 21 (12.34) | ATL, @MIN, @JAX |

## 5. Caveats
1. Ratings are last-season results (plus 25% of 2024). Per section 1, year-over-year stability is weak (r≈0.2 for QB/RB/TE, ~0 for WR) and 14 defenses have new coordinators; treat differences of less than ~0.5 pts/game as noise and use ranks as tiebreakers only.
2. No projection overlay was applied. If you want one, the strongest documented 2026 signals are: LAR much better vs. pass (Garrett + McDuffie), CLE and KC worse, SEA/HOU elite, ARI/MIA poor.
3. Position tagging follows nflverse; WR/TE/RB assignment of hybrid players (e.g., Taysom-Hill types) can shift a point or two per game for a defense.
4. Week 18 is excluded from all windows (ESPN/FantasyPros convention); byes are skipped, so "full" averages 17 games, "early" 4 (3 for teams with a week 1-4 bye — none in 2026; the earliest byes are week 5), "playoffs" 3.
5. Snippet-sourced outlet tables above are exactly what the snippets said; several aggregator lists share wording, so the specific originating page is uncertain and is labeled as such.
6. Search budget: ~45 WebSearch calls used; direct fetches of fantasy/sports sites (including ESPN, PFF, FantasyPros, Sharp, Draft Sharks, The Ringer, NFL.com, Sportsnaut, footballdb, fftoday, fftoolbox, espncdn PDF) were blocked by the egress proxy.
