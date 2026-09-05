# Additional GitHub data sources for the 2026 draft model — survey (2026-09-05)

Method: GitHub repo search (MCP) for discovery → blobless `git clone --filter=blob:none` to list trees and commit dates → every URL below was fetched with curl and returned **HTTP 200** unless marked otherwise. Sizes are bytes downloaded; row counts are `wc -l` (header included) unless noted. "No license" = no LICENSE file in repo root (all-rights-reserved by default; treat data as personal-use only).

Environment notes: `github.com` HTML pages return 403 from this sandbox (proxy scoping), but `raw.githubusercontent.com`, `github.com/<o>/<r>/releases/download/...`, and anonymous `git clone` all work. `api.github.com` is blocked, but the GitHub MCP `search_repositories` tool works and was the main discovery channel.

Rejected up front (fail the "2025-or-newer for rankings/ADP/projections" rule or hold no data):
- `tyleralgigi/FFRankExtension` `data/pff_ranks.csv` and `data/rotoballers.csv` — **2025 data** despite a 2026-09-01 commit ("new year new data"): bye weeks are 2025's (CIN bye 10; 2026 CIN bye is 6), Nabers WR2, none of the 2026 first-round rookies (Jeremiyah Love, Carnell Tate, Jordyn Tyson, Makai Lemon) present.
- `TheSirLancelot/the_combine` (PFF+ESPN blend) and `ethanmackey/fantasy-draft-board` — PFF CSVs are git-ignored/removed; code only.
- `nmiller0113/fantasy-copilot` (Draft Sharks) — requires DS subscription; no data, but `skills/fantasy-copilot/references/draft-sharks.md` (200, 5.7KB) documents DS's injury-discount / "Next Pick Odds" field semantics.
- `ball-and-chain-gfl/adp-board-2026` — single HTML page; Underdog column removed 2026-08-29.
- `cwecht15/Mock-Draft-Database` — NFL (not fantasy) mock drafts.
- `JaeBrian/fantasy-draft-2026`, `ryanfischman/nfl-projections`, `jmsone/ff-assistant`, `rohithm1/ff-draft-room`, `shaunak3000/fantasy-football` — data embedded in built HTML or not committed.
- `predictionmarketspicks/fantasy-draft-mcp` — hosted MCP server, no data files.

---

## Priority 1 — Weekly player stats 2024/2025 (nflverse + ffverse)

### 1.1 nflverse/nflverse-data — `stats_player` release (the current weekly stats asset; the old `player_stats` release stops at 2024)
Repo: https://github.com/nflverse/nflverse-data (README 200; license line not in README — nflverse publishes data as CC-BY-SA 4.0 per its site, UNVERIFIED here)

| File | URL | Status | Size | Notes |
|---|---|---|---|---|
| stats_player_week_2025.csv | https://github.com/nflverse/nflverse-data/releases/download/stats_player/stats_player_week_2025.csv | 200 | 8,656,387 B, 19,422 rows | season 2025 only; REG 18,540 rows (weeks 1–18) + POST 882 (weeks 19–22); 150 cols |
| stats_player_week_2024.csv | https://github.com/nflverse/nflverse-data/releases/download/stats_player/stats_player_week_2024.csv | 200 | 8,470,040 B | same schema |
| stats_player_week_2023 / 2022 / 2015 | …/stats_player/stats_player_week_2023.csv, _2022.csv, _2015.csv | 200 / 200 / 200 | 8.3 MB / 8.4 MB / 7.9 MB | series goes back to at least 2015 (all verified) |
| stats_player_reg_2025.csv | https://github.com/nflverse/nflverse-data/releases/download/stats_player/stats_player_reg_2025.csv | 200 | 882,104 B, 2,021 rows | season totals, REG only, `games` column |
| stats_player_reg_2024 / 2021 / 2018 / 2015 | …/stats_player/stats_player_reg_YYYY.csv | 200 each | ~0.8–0.9 MB | season-end finishes for backtests 2015–2025 |
| stats_player_week_2026.csv | …/stats_player/stats_player_week_2026.csv | **404** | — | not published until Week 1 (games start 2026-09-09) |
| player_stats_2025.csv (legacy) | …/player_stats/player_stats_2025.csv | **404** | — | legacy release ended with 2024 |
| player_stats.csv (legacy, all seasons) | https://github.com/nflverse/nflverse-data/releases/download/player_stats/player_stats.csv | 200 | 33,447,747 B | seasons 1999–2024 (~5,000–5,700 rows/season), legacy schema (`recent_team`, `dakota`, …) |

Columns (stats_player_week, 150): `player_id, player_name, player_display_name, position, position_group, headshot_url, season, week, season_type, game_id, team, opponent_team, completions, attempts, passing_yards, passing_tds, passing_interceptions, sacks_suffered, sack_yards_lost, sack_fumbles, sack_fumbles_lost, passing_air_yards, passing_yards_after_catch, passing_first_downs, passing_epa, passing_cpoe, passing_2pt_conversions, pacr, passing_10/16/20/40, carries, rushing_yards, rushing_tds, rushing_fumbles, rushing_fumbles_lost, rushing_first_downs, rushing_epa, rushing_2pt_conversions, rushing_10/12/20/40, receptions, targets, receiving_yards, receiving_tds, receiving_fumbles, receiving_fumbles_lost, receiving_air_yards, receiving_yards_after_catch, receiving_first_downs, receiving_epa, receiving_2pt_conversions, receiving_10/16/20/40, racr, target_share, air_yards_share, wopr, special_teams_tds, def_* (25 cols), misc_yards, fumble_recovery_*, penalties, penalty_yards, fumbles_*, punt_returns…, kickoff_returns…, fg_*/pat_* (kickers), pt_* (punters), fantasy_points, fantasy_points_ppr`.
Scoring: `fantasy_points` = standard, `fantasy_points_ppr` = full PPR (4-pt pass TD, -2 INT, -2 fumble lost). Row 2 example: A.Rodgers 2025 wk1 PIT vs NYJ, 22/30, 244 yds, 4 TD → 25.66 / 25.66.
What it adds: per-game 2024 + 2025 lines for every player → weekly boom/bust rates, PPG stdev, target/air-yards share and WOPR by week.

### 1.2 nflverse play-by-play & participation
| File | URL | Status | Size |
|---|---|---|---|
| play_by_play_2025.csv.gz | https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2025.csv.gz | 200 | 19,105,296 B |
| play_by_play_2024.csv.gz | https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2024.csv.gz | 200 | 19,362,351 B |
| pbp_participation_2025.csv | https://github.com/nflverse/nflverse-data/releases/download/pbp_participation/pbp_participation_2025.csv | 200 | 49,094,943 B, 45,185 rows |
| pbp_participation_2024.csv | …/pbp_participation/pbp_participation_2024.csv | 200 | 49,688,308 B |
Participation cols: `nflverse_game_id, old_game_id, play_id, possession_team, offense_formation, offense_personnel, defenders_in_box, defense_personnel, number_of_pass_rushers, players_on_play, offense_players, defense_players, n_offense, n_defense, ngs_air_yards, time_to_throw, was_pressure, route, defense_man_zone_type, defense_coverage_type, offense_names, defense_names, offense_positions, defense_positions, offense_numbers, defense_numbers`. Adds route participation (routes run) for 2024–2025.

### 1.3 ffverse/ffopportunity — expected fantasy points (the real "ff_opportunity"; the nflverse-data `ff_opportunity` release tag returns 404 for `ff_opportunity_2025_weekly.csv`)
Repo: https://github.com/ffverse/ffopportunity (README 200, 6.8 KB; R package, MIT per CRAN — not in README text). Release tag `latest-data` (also `v1.0.0-data`).

| File | URL | Status | Size |
|---|---|---|---|
| ep_weekly_2025.csv | https://github.com/ffverse/ffopportunity/releases/download/latest-data/ep_weekly_2025.csv | 200 | 5,426,028 B, 6,055 rows (22 season-weeks incl. playoffs) |
| ep_weekly_2024.csv | https://github.com/ffverse/ffopportunity/releases/download/latest-data/ep_weekly_2024.csv | 200 | 5,380,748 B |
| ep_weekly_2015.csv / ep_weekly_2006.csv | …/latest-data/ep_weekly_2015.csv, ep_weekly_2006.csv | 200 / 200 | 4.9 MB / 4.6 MB (series 2006–2025) |
| ep_weekly_2025.parquet / .rds | …/latest-data/ep_weekly_2025.parquet, ep_weekly_2025.rds | 200 / 200 | 1.13 MB / 829 KB |
| ep_pbp_pass_2025.rds | …/latest-data/ep_pbp_pass_2025.rds | 200 | 1.64 MB |
Columns (159): `season, posteam, week, game_id, player_id, full_name, position, pass_attempt, rec_attempt, rush_attempt, pass_air_yards, rec_air_yards, pass_completions, receptions, pass_completions_exp, receptions_exp, pass_yards_gained, rec_yards_gained, rush_yards_gained, *_exp, pass_touchdown, rec_touchdown, rush_touchdown, *_touchdown_exp, *_two_point_conv(_exp), *_first_down(_exp), pass_interception(_exp), rec_fumble_lost, rush_fumble_lost, pass_fantasy_points_exp, rec_fantasy_points_exp, rush_fantasy_points_exp, pass_fantasy_points, rec_fantasy_points, rush_fantasy_points, total_yards_gained(_exp), total_touchdown(_exp), total_fantasy_points(_exp), *_diff …`. Scoring: default ffopportunity (PPR). Adds expected vs actual fantasy points by week → TD/efficiency regression signals.

### 1.4 Other nflverse assets verified (all 200)
| Asset | URL | Size / rows | Key columns |
|---|---|---|---|
| injuries_2025.csv | https://github.com/nflverse/nflverse-data/releases/download/injuries/injuries_2025.csv | 695,623 B, 6,069 rows | `season, season_type, game_type, team, week, gsis_id, position, full_name, first_name, last_name, report_primary_injury, report_secondary_injury, report_status (Out 1,396 / Questionable 1,280 / Doubtful 106 / blank 3,286), practice_primary_injury, practice_secondary_injury, practice_status` |
| injuries_2024 / 2023 / 2020 | …/injuries/injuries_2024.csv (816,989 B), _2023 (738,501), _2020 (737,474) | | same schema; 2026 → **404** (appears after Week 1) |
| depth_charts_2026.csv | https://github.com/nflverse/nflverse-data/releases/download/depth_charts/depth_charts_2026.csv | 47,443,930 B, 496,714 rows | snapshot log: `dt` (2026-08-31 … 2026-09-04T11:57Z, ~2,200 rows/day), `team, player_name, espn_id, gsis_id, pos_grp_id, pos_grp, pos_id, pos_name, pos_abb, pos_slot, pos_rank` |
| depth_charts_2025.csv / 2024.csv | …/depth_charts/depth_charts_2025.csv (52.9 MB), _2024.csv (3.4 MB, legacy schema) | | |
| roster_weekly_2026.csv (= roster_2026.csv) | https://github.com/nflverse/nflverse-data/releases/download/weekly_rosters/roster_weekly_2026.csv | 938,960 B, 2,947 rows (week 1) | 36 cols: `season, team, position, depth_chart_position, jersey_number, status, full_name, birth_date, height, weight, college, gsis_id, espn_id, sportradar_id, yahoo_id, rotowire_id, pff_id, pfr_id, fantasy_data_id, sleeper_id, years_exp, headshot_url, week, game_type, entry_year, rookie_year, draft_club, draft_number` |
| roster_weekly_2025.csv | …/weekly_rosters/roster_weekly_2025.csv | 15,385,661 B | |
| players.csv | https://github.com/nflverse/nflverse-data/releases/download/players/players.csv | 7,290,422 B, 24,833 rows | 39 cols incl. `gsis_id, esb_id, nfl_id, pfr_id, pff_id, otc_id, espn_id, birth_date, position, height, weight, college_name, rookie_season, last_season, latest_team, status, years_of_experience, draft_year, draft_round, draft_pick, draft_team` — the age/experience table |
| snap_counts_2025.csv / 2024 / 2015 | …/snap_counts/snap_counts_2025.csv (2,401,193 B, 26,613 rows), _2024 (2.4 MB), _2015 (2.2 MB) | | `game_id, pfr_game_id, season, game_type, week, player, pfr_player_id, position, team, opponent, offense_snaps, offense_pct, defense_snaps, defense_pct, st_snaps, st_pct` |
| ngs_receiving.csv.gz / ngs_rushing / ngs_passing | https://github.com/nflverse/nflverse-data/releases/download/nextgen_stats/ngs_receiving.csv.gz (981,431 B, 14,732 rows, 2016–2025), ngs_rushing.csv.gz (323,622 B), ngs_passing.csv.gz (584,224 B) | | receiving: `avg_cushion, avg_separation, avg_intended_air_yards, percent_share_of_intended_air_yards, catch_percentage, avg_yac, avg_expected_yac, avg_yac_above_expectation, player_gsis_id …` (per-season file names like `ngs_2025_receiving.csv.gz` → 404) |
| advstats_season_rec.csv / advstats_season_rush.csv | …/pfr_advstats/advstats_season_rec.csv (419,750 B, 4,131 rows, 2018+), advstats_season_rush.csv (226,049 B) | | rec: `tgt, rec, yds, td, x1d, ybc, ybc_r, yac, yac_r, adot, brk_tkl, rec_br, drop, drop_percent, int, rat` (weekly variants at `advstats_week_rec.csv` → 404) |
| ftn_charting_2025.csv | …/ftn_charting/ftn_charting_2025.csv | 8,128,926 B, 47,317 plays | `is_motion, is_play_action, is_screen_pass, is_rpo, is_contested_ball, is_drop, is_catchable_ball, n_blitzers, n_pass_rushers …` (FTN charting, free tier) |
| stats_team_week_2025.csv | …/stats_team/stats_team_week_2025.csv | 229,660 B, 571 rows, 138 cols | team pace/pass-rate context |
| qbr_season_level.csv | …/espn_data/qbr_season_level.csv | 285,760 B, 1,524 rows | ESPN QBR 2006+ |
| games.csv | https://github.com/nflverse/nflverse-data/releases/download/schedules/games.csv | 2,177,170 B, 7,549 rows; 272 rows for 2026 | includes `spread_line, total_line, away/home_moneyline, roof, surface, away/home_qb_name, coach` (same file as nflverse/nfldata already pulled) |
| draft_picks.csv / combine.csv | …/draft_picks/draft_picks.csv (1,657,534 B, 1980–2026), …/combine/combine.csv (893,875 B, 2000+) | | 2026 class: Mendoza QB 1.1, Jeremiyah Love RB 1.3, Carnell Tate WR 1.4, Jordyn Tyson WR 1.8 … |
| ff_playerids / ff_rankings | nflverse-data tags `players_components/ff_playerids.csv`, `ff_rankings/db_fpecr*.csv` → **404** | | canonical files are dynastyprocess/data `files/db_playerids.csv` (200, 2,631,648 B) and `db_fpecr_latest.csv` — already pulled |
| sc_lines / contracts | `misc/sc_lines.csv`, `contracts/historical_contracts.csv` → **404** at those names | | not pursued |

---

## Priority 2 — 2026 projections from additional sources

### 2.1 najibismail95/Fantasy-Football-ADP-Comparison-Tool — daily ESPN + Sleeper season projections (and ADP, see 3.1)
Repo: https://github.com/najibismail95/Fantasy-Football-ADP-Comparison-Tool — last commit 2026-09-04 14:56Z "data: ADP snapshot 2026-09-04" (GitHub Action, daily). No license.
- https://raw.githubusercontent.com/najibismail95/Fantasy-Football-ADP-Comparison-Tool/main/data/silver/projections.parquet — 200, 194,868 B, **66,543 rows**; cols `player_id (Sleeper id), source {ESPN, SLEEPER}, scoring {PPR, HALF, STD}, proj_points, captured_at` — 39 daily snapshots 2026-07-27 → 2026-09-04. Example: 9221 (Gibbs) ESPN PPR 365.09 on 07-27.
- https://raw.githubusercontent.com/najibismail95/Fantasy-Football-ADP-Comparison-Tool/main/data/silver/player_xref.parquet — 200 (Sleeper↔ESPN↔Yahoo id crosswalk; CROSSWALK.md 200 documents tiers).
- README (200, 14.6 KB): all sources are unauthenticated APIs (ESPN, Sleeper, Yahoo, nflverse); FantasyPros feed broke → ECR frozen at 2026-08-16.
Adds: a projection *time series* (ESPN + Sleeper, three scoring formats) to measure projection drift through camp and preseason.

### 2.2 Danoodli/fantasy-drafter — full ESPN 2026 projection stat lines (kona) + Sleeper projections
Repo: https://github.com/Danoodli/fantasy-drafter — nightly GH Action; last commit 2026-09-04 19:01Z "chore: nightly board refresh". No license.
- https://raw.githubusercontent.com/Danoodli/fantasy-drafter/main/data/raw/espn-kona.json — 200, **14,518,270 B**, 500 players (ESPN `kona_player_info`, fetched 2026-09-04T19:01Z per `meta.json`). Per player: `player.stats[]` with `seasonId 2026, statSourceId 1, statSplitTypeId 0` = ESPN season projection (45 stat ids, `appliedTotal` e.g. Gibbs 365.67) plus 18 weekly projections (`statSplitTypeId 1`) and 2025 actuals (`statSourceId 0`); `ownership.averageDraftPosition` (1.32), `auctionValueAverage` (70.83), `percentOwned`, `percentStarted`; `draftRanksByRankType {STANDARD, PPR}.rank/auctionValue`; `injuryStatus`; `seasonOutlook` text.
- https://raw.githubusercontent.com/Danoodli/fantasy-drafter/main/data/raw/sleeper-projections.json — 200, 297,304 B, 3,115 Sleeper ids → `stats {passYds, passTD, passInt, rushYds, rushTD, receptions, recYds, recTD, fumblesLost, rushFd, recFd}` + `adp {standard, half-ppr, ppr, 2qb}` (Gibbs: 1251 rush yds/12 TD/63 rec/533/3; ADP ppr 1.0).
- https://raw.githubusercontent.com/Danoodli/fantasy-drafter/main/data/raw/meta.json — 200 (fetchedAt per file).
Adds: ESPN's full 2026 stat-line projections (not just points) and weekly ESPN projections keyed by ESPN id; Sleeper stat-line projections keyed by Sleeper id.

### 2.3 theoauyeung/TAY-Analytics-FF — ESPN + FantasyPros stat lines keyed by gsis_id
Repo: https://github.com/theoauyeung/TAY-Analytics-FF — last commit 2026-09-02. No license.
- https://raw.githubusercontent.com/theoauyeung/TAY-Analytics-FF/main/data/consensus_projections_2026.csv — 200, 104,375 B, 1,498 rows; cols `gsis_id, season, source (espn 1,457 rows / fantasypros 40 rows), pass_yards, pass_tds, interceptions, rush_yards, rush_tds, receptions, rec_yards, rec_tds, points`. Adds: ESPN 2026 projections already joined to nflverse gsis_id.

### 2.4 srsavas42/fantasy-football-research — hierarchical-Bayesian distributional 2026 PPR projections (p10/p50/p90)
Repo: https://github.com/srsavas42/fantasy-football-research — last commit 2026-09-04 18:07 (PR #28). No license. README (200, 21 KB): PyMC bottom-up model (team plays → opportunity share via Dirichlet-Multinomial → efficiency → scoring), walk-forward CRPS/log-score gates vs ECR baselines; `docs/*.md` (adp-ablation, injury-availability, vegas-win-totals, out-of-sample-2025) document each validation.
- https://raw.githubusercontent.com/srsavas42/fantasy-football-research/main/projections/2026_ppr.csv — 200, 236,926 B, 591 rows; cols `overall, player_name, team, position, adp_rank, adp_drafted, projection, p10, p50, p90, model_only, projected_games, suspended_games, snap_share, pass_attempt_share, target_share, carry_share, pass_attempts, targets, carries, completion_rate, yards_per_attempt, pass_td_rate, …, pass_cmp, pass_yds, pass_td, pass_int, rush_yds …`. Row 1: Bijan 313.5 (p10 160 / p90 449), 14.5 projected games.
- https://raw.githubusercontent.com/srsavas42/fantasy-football-research/main/projections/2026_ppr.meta.json — 200 (`blend_weight 0.316`, `market_adp_availability true`, 590 rows, ppr, season 2026).
Scoring: full PPR. Adds: the only source with per-player outcome *distributions* and projected games; also a methodology worth copying.

### 2.5 lhallee/fantasy-football-feature-discovery — leakage-controlled ML projections + injury probabilities
Repo: https://github.com/lhallee/fantasy-football-feature-discovery — last commit 2026-08-22; roster snapshot 2026-08-09. No license (NOTICE.md present). README: Extra Trees on 512 features from 2017+, audit Spearman 0.756 (2022–25) vs 0.647 prior-season baseline; injury classifier ROC-AUC 0.749, calibration slope 1.02.
- https://raw.githubusercontent.com/lhallee/fantasy-football-feature-discovery/main/artifacts/predictions_2026.parquet — 200, 343,556 B, 958 rows; `target_season, player_id (gsis), model_position, team, roster_status, available_for_draft, previous_points_baseline, is_rookie, predicted_points, feature_value__…` (scoring_profile `espn_full_ppr_2026`).
- https://raw.githubusercontent.com/lhallee/fantasy-football-feature-discovery/main/artifacts/players_2026.parquet — 200, 786,128 B, 2,930 rows (birth_date, draft round/number, depth_rank, espn/pfr/sleeper ids).
- https://raw.githubusercontent.com/lhallee/fantasy-football-feature-discovery/main/outputs/fantasy_football_final_rankings_2026.xlsx — 200, 591,884 B (ALL/QB/RB/WR/TE/K/INJURED sheets incl. injury probability).
Scoring: ESPN full PPR. Adds: an independent, audited ML projection and a calibrated missed-time probability per player.

### 2.6 peytonramsey/fantasy-football-draft-model-2026 — R component model (RB/WR/TE) with walk-forward metrics
Repo: https://github.com/peytonramsey/fantasy-football-draft-model-2026 — last commit 2026-08-29. No license. `building-model-deepdive.md` (200) documents the pipeline (R/01–14: nflverse pull → features → walk-forward → projections → VOR board → tier clustering → optimizer → mock sim).
- https://raw.githubusercontent.com/peytonramsey/fantasy-football-draft-model-2026/master/output/tables/projections_2026.csv — 200, 39,097 B, 190 rows; `gsis_id, player_display_name, position, season, adp, adp_rank_pos, is_rookie, games_played_hat, carries_hat, ypc_hat, rush_td_rate_hat, targets_hat, catch_rate_hat, receptions_hat, ypr_hat, rec_td_rate_hat, fantasy_points_ppr_hat, projected_rank_pos, projected_rank_overall`.
- …/output/tables/draft_board_2026.csv (200, 21,669 B; VOR, PAB) and …/output/tables/walkforward_metrics_pooled.csv (200; RB full model Spearman 0.739).
Scoring: PPR. Adds: component-level (games, carries, targets, catch rate) projections for RB/WR/TE; no QB.

### 2.7 keganvosteen/draft-assistant — consensus stat-line projections for 2,209 players (Sleeper + FFToday + ESPN)
Repo: https://github.com/keganvosteen/draft-assistant — release 0.5.0, 2026-08-29. **Proprietary license** ("All rights reserved") — check before redistributing.
- https://raw.githubusercontent.com/keganvosteen/draft-assistant/master/data/projections.json — 200, 1,789,275 B, 2,209 players; `id "sleeper:9221", name, position, team, bye_week, adp, projections {rush_yd, rush_td, rec, rec_yd, rec_td, fumbles, rush_2pt, rec_2pt …}, age, experience, historical_stats{2025…}`. `collectors/combined.py` (200) names the free-source consensus (Sleeper projections, FFC ADP, nflverse, FFToday, ESPN).

### 2.8 connerfrock-bit/fantasy-football-ai — multi-source consensus with stat lines + Sleeper/ESPN ADP
Repo: https://github.com/connerfrock-bit/fantasy-football-ai — auto-refresh 2026-09-04. No license.
- https://raw.githubusercontent.com/connerfrock-bit/fantasy-football-ai/main/pipeline/data/ff_players.csv — 200, 40,634 B, 385 rows; `board_rank, name, pos, team, bye, inj, proj_ppr, proj_half, proj_std, adp_ppr, adp_half, adp_std, adp_ppr_sleeper, adp_ppr_espn, adp_sources, gp, rec, rec_yd, rec_td, rush_att, rush_yd, rush_td, pass_yd, pass_td, pass_int, sleeper_id, espn_id`.

### 2.9 Camdenw1/sleeper-draft-guide — blended board with Monte-Carlo modelled points (half-PPR TE-premium)
Repo: https://github.com/Camdenw1/sleeper-draft-guide — refreshed 2026-09-04 16:52Z. No license.
- https://raw.githubusercontent.com/Camdenw1/sleeper-draft-guide/main/rankings.csv — 200, 53,610 B, 250 rows; `Rank, OverallTier, Pos, PosTier, Player, Team, Bye, Tag, MarketADP, ExpertRank, FantasyCalc, FFCHalfPPR, YahooADP, ESPNpprADP, NumSignals, DecisionAnchor, Spread, ModelRank, Gap, AwardOdds (e.g. "OPOY fav (+850)"), LeaguePts, YardBonusPts, Injury, InjuryBody, GreenFlag, RedFlag`. Scoring: 12-team half-PPR + TE premium + yardage bonuses (not our format) — use the market columns, not LeaguePts.

### 2.10 Others (2026, verified 200)
- StrubeTube/the-lab `docs/data/players.json` — 207,731 B, 282 players (see 3.6): `proj` = Sleeper 2026 projection rescored to a 10-team half-PPR league; `crs {joel, flock, fb, ffa}` consensus ranks; `data/predictions_2026.json` (200, 58.7 KB) frozen 2026-08-27 with preregistered bust/hit metrics.
- benirvin714/fantasy-2026 `data/raw/clay-team-projections.json` — https://raw.githubusercontent.com/benirvin714/fantasy-2026/main/data/raw/clay-team-projections.json — 200, 2,172 B; ESPN **Mike Clay 2026 team** PF/PA/proj_wins for all 32 teams (source ESPN draft-kit PDF, fetched 2026-08-17). Team-level only.
- charliecjr15/nfl-fantasy-football-advisor `results/public/latest_rankings.csv` — 200, 396,219 B, 809 rows; 2026 **Week 1** `projected_fantasy_points_ppr` from an nflverse ML model (model_accuracy.csv: Spearman 0.68 all / 0.51 QB on test). Weekly not seasonal.
- justinmck (see 5.2) has 2025 FantasyPros positional projections and ESPN 2025 preseason projections for the 2025 backtest.
- benitoooooooooooo/draft-engine `data/draft_pool_2026.json` — 200, 61,805 B; FantasyPros ECR (`ecr_rank, rank_min, rank_max, rank_std, owned_pct`) + `projected_pts` (unlabeled source) + sleeper_id, 2026-09-04.

---

## Priority 3 — Current rankings / ADP exports we lack

### 3.1 najibismail95 — daily ESPN / Sleeper / Yahoo / FantasyPros ADP + ESPN auction values since 2026-07-27
- https://raw.githubusercontent.com/najibismail95/Fantasy-Football-ADP-Comparison-Tool/main/data/silver/adp_snapshots.parquet — 200, 293,495 B, **61,156 rows**; `player_id (Sleeper), source {ESPN, FANTASYPROS, SLEEPER, YAHOO}, adp_format {PPR_1QB, YAHOO_DEFAULT}, adp, auction_value, captured_at` — 39 daily captures 2026-07-27 → 2026-09-04.
- …/data/silver/rank_snapshots.parquet — 200, 103,191 B, 52,327 rows; ESPN `rank_type {STANDARD, PPR}`, `rank`, `auction_value`, daily.
- …/data/silver/ecr_snapshots.parquet — 200, 261,044 B, 20,726 rows; FantasyPros ECR `{PPR, STD}` with `rank_ecr, rank_ave, rank_std, rank_min, rank_max`, 20 captures 2026-07-27 → 2026-08-16 (feed then broke; frozen).
- …/data/silver/sos_ratings.parquet — 200, 256 rows (2026 SOS by team/position from 2025 basis, computed 2026-08-20).
Adds: **Yahoo ADP** and **ESPN ADP + auction** as daily time series (we had neither as a series), keyed to Sleeper ids with an ESPN/Yahoo crosswalk.

### 3.2 Danoodli/fantasy-drafter — FantasyFootballCalculator ADP (4 formats, with stdev) + ESPN ADP/auction + Sleeper ADP history
- https://raw.githubusercontent.com/Danoodli/fantasy-drafter/main/data/raw/ffc-ppr.json — 200, 50,776 B; FFC API payload: `meta {type PPR, teams 12, rounds 15, total_drafts 7,681, start 2026-08-28, end 2026-09-04}`, players `{player_id, name, position, team, adp, adp_formatted, times_drafted, high, low, stdev, bye}`. Also `ffc-half-ppr.json`, `ffc-standard.json`, `ffc-2qb.json` (same dir; fetchedAt 2026-09-04T19:01Z in meta.json).
- https://raw.githubusercontent.com/Danoodli/fantasy-drafter/main/data/raw/adp-history-ppr.json — 200, 33,959 B; Sleeper PPR ADP by day, 2026-08-26 → 2026-09-04 (10 days × 267 players, keyed by Sleeper id); `adp-history-half-ppr/standard/2qb.json` alongside.
- `espn-kona.json` (2.2) — ESPN ADP, auction, ownership for 500 players as of 2026-09-04.
- https://raw.githubusercontent.com/Danoodli/fantasy-drafter/main/data/raw/sos.json — 200, 4.8 KB (season/playoff SOS index by team×position).
Adds: FFC ADP with per-player **stdev** (the pick-availability input) in PPR/half/std/2QB — FFC itself is blocked from here.

### 3.3 cal-chan-cloud/gridiron-edge — Sleeper ADP daily history (4 formats)
Repo: https://github.com/cal-chan-cloud/gridiron-edge — daily GH Action; last commit 2026-09-04 15:04Z "data: ADP snapshot 2026-09-04". No license.
- https://raw.githubusercontent.com/cal-chan-cloud/gridiron-edge/main/data/adp_history.csv — 200, 346,512 B, 9,666 rows; `fmt {2qb, half-ppr, ppr, standard}, search_name, date, adp`; 2026-08-26 → 2026-09-04, ~964 rows/day (Sleeper ADP incl. DSTs).

### 3.4 benirvin714/fantasy-2026 — Sleeper half-PPR ADP daily since 2026-08-09 (longest series found)
- https://raw.githubusercontent.com/benirvin714/fantasy-2026/main/data/adp-history.json — 200, 81,746 B; `snapshots[{date, adp{sleeper_id: adp}}]`, 26 daily snapshots 2026-08-09 → 2026-09-04, 248 players, half-PPR.

### 3.5 tykim516/fantasy-draft-agent — CBS Sports ADP (2026-08-12) + Sleeper ADP (2026-08-06)
- https://raw.githubusercontent.com/tykim516/fantasy-draft-agent/main/config/market/adp.csv — 200, 10,191 B, 220 rows; `Rank, Player ("Jahmyr Gibbs RB  DET"), Trend, Avg Pos, Hi/Lo, Pct` — README states "CBS Sports, pulled 2026-08-12, league size unknown". Same content at `config/market/history/adp-cbs-2026-08-12.csv`.
- …/config/market/history/adp-sleeper-2026-08-06.csv — 200, 300 rows (`Name, ADP, Position ADP`). No license. Adds: CBS ADP (missing from our set), albeit early-August.

### 3.6 StrubeTube/the-lab — FFC half-PPR ADP archive, analyst lists (Joel Smyth / Flock / Fantasy Footballers / FFA), Vegas props archive, DK win totals
Repo: https://github.com/StrubeTube/the-lab — daily GH Action; last commit 2026-09-04 14:26Z. No license. Sources per README/fetch_data.py: Sleeper API, FFC half-PPR ADP, Boris Chen tiers, BettingPros season props (removed from daily run 2026-09-01; archives kept).
- https://raw.githubusercontent.com/StrubeTube/the-lab/main/data/archive/2026-09-03_adp.json — 200, 144,117 B; Sleeper id → FFC half-PPR ADP (999 = undrafted); also `2026-08-27/08-30/08-31_adp.json`. meta.json: 10-team half-PPR, 3,064 drafts 2026-08-30 → 09-04.
- https://raw.githubusercontent.com/StrubeTube/the-lab/main/data/archive/2026-09-03_vegas.json — 200, 32,487 B; **179 players' season-long props** `{pass_yd/rush_yd/pass_td/rush_td/rec/rec_yd/rec_td: {over:[line, price], under:[line, price]}}` from BettingPros (also 08-27, 08-30, 08-31 archives).
- https://raw.githubusercontent.com/StrubeTube/the-lab/main/data/analyst_lists.json — 200, 51,483 B; positional rank lists: `joel` (Joel Smyth sheet 2026-09-01), `flock` (2026-09-02), `fb` (2026-09-03, QB/RB/WR/TE + D/ST), `ffa` (FFAnalytics CSV, 726 skill players).
- https://raw.githubusercontent.com/StrubeTube/the-lab/main/data/consensus_ranks.json — 200, 86,355 B (avg of the four by position).
- https://raw.githubusercontent.com/StrubeTube/the-lab/main/data/team_context.json — 200, 1.5 KB; DraftKings season win totals (July 2026) + PFF preseason O-line rank per team.
- https://raw.githubusercontent.com/StrubeTube/the-lab/main/docs/data/players.json — 200, 207,731 B, 282 players; per Sleeper id: `adp, fadp, asd (ADP sd), adp_pos, dyn (dynasty), proj, p25 (2025 pts), ppg25, gp25, fin25 (2025 positional finish), wk25 [18 weekly points], bc (Boris tier), cr/crs, lab{age, alvl, dcr, dcp, dcy (draft capital), vt, va …}`. Scoring: 10-team half-PPR.

### 3.7 Vegas season-long player props (three independent captures)
- lucasreydman/nfl-fantasy-draft-big-board — https://raw.githubusercontent.com/lucasreydman/nfl-fantasy-draft-big-board/main/src/data/vegas.json — 200, 47,680 B; `season 2026, generatedAt 2026-08-24, source "bettingpros.com season-long player props — median line across sportsbooks, shaded by juice"`, 9 books (DraftKings 295 lines, Caesars 276, BetMGM 206 …), converted to full-PPR points with replacement levels (QB12/RB28/WR32/TE12). No license.
- Abhinav811/NFLDraftModel — https://raw.githubusercontent.com/Abhinav811/NFLDraftModel/main/data/external/season_long_props_wide.csv — 200, 40,811 B, 633 rows; `Rank, Name, Pos, Attempts, Comps, Pass TDs, Pass Yards, Ints, Receptions, Rec Yards, Rec TDs, Rec FD, Rush Attempts, Rush Yards, Rush TDs, Rush FD, Fumbles, Projections, 7-Day Delta` (props-aggregator export; date not in file — repo last commit 2026-08-31); `season_props.csv` (200, 33 DraftKings lines via "fta"); `offensive_coordinators.csv` (200, 2018–2026 OC by team); `defense_epa.csv`. No license.
- StrubeTube archives (3.6) — raw lines with both sides' prices, 4 dates.
- srsavas42 — https://raw.githubusercontent.com/srsavas42/fantasy-football-research/main/Vegas%20Win%20Totals/NFL%20Win%20Totals-export-2026-08-23.csv — 200, 32 rows (team, coach, Vegas total, over/under odds, hold) + `2003_2022_win_totals.csv`, `2023/2024/2025_nfl_regular_season_win_total_odds.csv` in the same folder.

### 3.8 FantasyPros exports (2026, in repos)
- srsavas42 — https://raw.githubusercontent.com/srsavas42/fantasy-football-research/main/ADP/FantasyPros_2026_Overall_ADP_Rankings.csv — 200, 8,536 B, 265 rows; `Rank, Player (Bye), POS` only (per-site columns stripped).
- eholland33/2026-Fantasy-Draft-Edge-Calculator — https://raw.githubusercontent.com/eholland33/2026-Fantasy-Draft-Edge-Calculator/main/data/FantasyPros_2026_WR_ADP_Rankings.csv — 200, 8,719 B, 166 rows; `WR, Overall, Player (Bye), ESPN, Sleeper, CBS, NFL, RTSports, Fantrax, AVG, Real-Time` (WR only; commit 2026-08-18). No license.
- HeyItsJohnny/dynastydestroyer — https://raw.githubusercontent.com/HeyItsJohnny/dynastydestroyer/main/CSVFiles/2026/FantasyPros_2026_Draft_RB_Rankings.csv — 200, 17,143 B, 142 rows (`RK, TIERS, PLAYER NAME, TEAM, BYE WEEK, UPSIDE, BUST, SOS SEASON, ECR VS. ADP`); QB/WR/TE files in same folder; `PlayerAuctionValues.csv` (200, 338 rows; `Number, Player, Value` — Puka $67, JSN $63; source unlabeled). 2026 bye weeks confirm season; commit 2026-08-16. No license.
- MacSupportPlus/fantasy-football-draft-assistant — https://raw.githubusercontent.com/MacSupportPlus/fantasy-football-draft-assistant/main/data/processed/rankings-ppr.json — 200, 166,035 B; FantasyPros ECR PPR with `fantasyProsId, tier, rankEcr, rankAve, rankMin, rankMax, rankStd, ownedPct, byeWeek` (refresh 2026-09-04). Duplicates dynastyprocess ECR but adds FantasyPros ids + tiers.

### 3.9 Other current rankings
- Paytience420-dev/2026-fantasy-draft-kit — https://raw.githubusercontent.com/Paytience420-dev/2026-fantasy-draft-kit/main/data/rotowire-ppr-top250.json — 200, 35,999 B; RotoWire PPR consensus top-250 (`rank, name, team, pos, bye`), refreshed 2026-09-04 (newer than our River-City-FFL RotoWire pull); `flock-wr-top50.json`, `pitcherlist-top25.json`, `sources.json` (200, weights per source), `boris-live.json` (empty). No license.
- gadife/nfl-draft-copilot — Yahoo mock-draft rooms with **Yahoo ADP** per player: https://raw.githubusercontent.com/gadife/nfl-draft-copilot/master/data/harvest/room9375193.json (200, 18,723 B; 12 teams, 180 picks, harvested 2026-08-21; `pickNo, id (Yahoo), name, pos, adp`), `room9377055.json` (14 teams, 189 picks), `room9383742.json` (14 teams, 182 picks). MIT.
- aidannconnorsdad/fantasy-draft-gm-advisor — https://raw.githubusercontent.com/aidannconnorsdad/fantasy-draft-gm-advisor/main/data/players.json — 200, 149,602 B, 119 players; `adp {fantasypros, yahoo, espn, draftkings, consensus}` + LLM-written "gm_insights"; `last_updated: "Preseason 2026"` (no exact date) — **DraftKings ADP provenance unverified**; low trust.
- golderr/fantasy-draft-war-room — https://raw.githubusercontent.com/golderr/fantasy-draft-war-room/main/outputs/late_round_rank_changes_september4.csv — 200, 3,727 B, 110 rows; Late-Round Draft Guide (paid) Top-250 rank/tier *changes* Sep 1 → Sep 4 only.
- stolte21/draft-driver — https://raw.githubusercontent.com/stolte21/draft-driver/main/public/tiers/weekly-ALL-PPR.csv — 200, 201 rows; Boris Chen tiers via fftiers, synced 2026-09-04 (`metadata.json` 200). Duplicates borisachen/fftiers.
- ajmartineau25/fantasy-football-guide — `data/adp_2026_live.json` (200, 2026-08-24, name→ADP, "expert consensus") — weak provenance.

Not found on GitHub with 2026 data: Underdog full ADP JSON (only our existing GraveGhost1 pull; `mistakia/league` has an `import-underdog-bestball-adp.mjs` scraper but no data), NFC daily ADP, DraftKings best-ball ADP files, PFF 2026 rankings/projections, FTN/numberfire, Footballguys, Fantasy Points, ESPN Clay/Karabell/Yates player-level, CBS Eisenberg, The Athletic.

---

## Priority 4 — Injury / risk data

- **nflverse injuries** 2020–2025 (1.4): weekly report/practice status per player. 2026 file not yet published (**404**).
- **ethankwyap-stack/fantasy-edge — per-player 2025 boom/bust rates** (computed from nflverse, PPR): https://raw.githubusercontent.com/ethankwyap-stack/fantasy-edge/main/boom-rates.json — 200, 116,571 B; generated 2026-09-01; `boomRule "top 5 at position within each week (PPR)"`, `bustPoints {QB 12, RB 8, WR 8, TE 8}`; 621 players → `{pos, g, boom, boomWeeks, bust, median, mean, best, sd}` (Gibbs: g 17, boom 0.35, bust 0.18, median 19.4, sd 13.5). `scripts/boom-rates.js` (in tree) is the generator. Also https://raw.githubusercontent.com/ethankwyap-stack/fantasy-edge/main/stat-stickiness.json — 200, 2.1 KB; Pearson r of year-Y stats vs year-Y+1 PPR PPG pooled 2018–2024 (QB own PPG 0.642, passing EPA/g 0.461 …). `playoff-sos.json` (200; weeks 15–17 opponent def ranks by position). No license. Note: files prefixed `draft-guide-smyth-*` are transcriptions of a paid draft guide — do not redistribute.
- **StrubeTube/the-lab — injury cohorts and per-player injury history**: https://raw.githubusercontent.com/StrubeTube/the-lab/main/data/injury_cohorts.json — 200, 5,841 B; by body part (Knee n=590: avgMissed 0.95, retPct 99, recurPct 23.9; tiers short/played-through/long …). https://raw.githubusercontent.com/StrubeTube/the-lab/main/data/injury_recent.json — 200, 33,456 B; Sleeper id → list of 2024–2025 injuries `{y, p (part), n (weeks listed), o (games out), t (tier)}`. `docs/data/players.json` has `gp25` and `wk25` (games played 2025).
- **lhallee** — calibrated missed-time injury probability per 2026 player (2.5; ROC-AUC 0.749).
- **curtisdearing/tailstail** — https://raw.githubusercontent.com/curtisdearing/tailstail/main/data/absence_matrix.json — 200, 1,593 B; pooled 2019–2025 volume/efficiency multipliers when a team's WR1/RB1/TE1 is out (e.g. WR1_out→WR2 vol ×0.844, →TE1 ×1.135; n≈1,150). https://raw.githubusercontent.com/curtisdearing/tailstail/main/data/draft_board_2026.csv — 200, 289,524 B, 870 rows; `mu_pergame, sigma_pergame, age, draft_number, availability_rate, age_multiplier, team_changed, season_mean/median/p10/p90, expected_games, vor_mean, vor_p90, adp, adp_sd`. Repo last commit 2026-08-31. No license.
- **dunlapjack/fantasy-football-rankings** — https://raw.githubusercontent.com/dunlapjack/fantasy-football-rankings/main/injury_overrides.csv — 200, 5,352 B, 128 rows; `player_name, status (OUT_SEASON …), note, games_missed` (2026-08-27); `playcaller_history.csv` in tree. No license.
- **Paytience420-dev** — https://raw.githubusercontent.com/Paytience420-dev/2026-fantasy-draft-kit/main/data/injuries.json — 200, 178,336 B; Sleeper-sourced injury statuses, generated 2026-09-04T14:23Z, daily.
- **Age / experience**: nflverse `players.csv` (birth_date, draft_year/round/pick, years_of_experience) and `roster_weekly_2026.csv` (birth_date, years_exp, entry_year) — 1.4; dynastyprocess `db_playerids.csv` (already pulled) also carries birthdates.
- **Games missed 2022–2025**: bernick4 workbook `GP` column (5.3); StrubeTube `gp25`; nflverse `stats_player_reg_*` `games`.
- **Coaching context**: Abhinav811 `offensive_coordinators.csv` (2018–2026); demansou/fantasy-football-26 `data/research/2026/playcaller_census.json`, `player_status_evidence.json`, and `data/research/backtests/2022–2025_opening_caller_changes.json` (tree verified; last commit 2026-09-04) — backtests of play-caller changes; srsavas42 `data/coaching/wikipedia/coach_history.csv`, `scheme_lineage.csv` (tree verified).
- Draft Sharks injury predictor / Sports Injury Predictor: no public scrapes found; only the field documentation in nmiller0113 (above).

---

## Priority 5 — Historical outcomes for backtesting (2015–2025)

### 5.1 srsavas42/fantasy-football-research — FantasyPros Overall ADP 2015 → 2026 (12 files) + Vegas win totals 2003 → 2026
Base: `https://raw.githubusercontent.com/srsavas42/fantasy-football-research/main/ADP/FantasyPros_YYYY_Overall_ADP_Rankings.csv` for YYYY = 2015 … 2026 (tree verified; 2015, 2019, 2025, 2026 fetched → 200).
- 2015: 18,800 B, 461 rows; `Rank, Player (Bye), POS, ESPN, Sleeper, CBS, NFL, RTSports, Fantrax, AVG` (Le'Veon Bell 1.5). 2019: 44,595 B, 1,044 rows. 2025: adds `Real-Time`. Scoring: FantasyPros default (PPR "Overall").
- Pair with nflverse `stats_player_reg_YYYY.csv` (verified 2015/2018/2021/2024/2025) or legacy `player_stats.csv` (1999–2024) for season-end PPR finishes → 11 seasons of ADP-vs-finish.
No license.

### 5.2 justinmck/fantasy-football-draft-toolkit (MIT) — FantasyPros ADP 2020–2025 + ESPN preseason projections vs actuals 2020–2025
Repo: https://github.com/justinmck/fantasy-football-draft-toolkit — last commit 2026-08-22; README (200, 66 KB) documents the pipeline (NB05-projection-accuracy notebook).
- `https://raw.githubusercontent.com/justinmck/fantasy-football-draft-toolkit/main/data/raw/YYYY/adp/FantasyPros_YYYY_Overall_ADP_Rankings.csv` YYYY=2020–2025 (2020: 200, 40,427 B, 585 rows with Fantrax; 2025: 200, 62,004 B, 897 rows with FFC).
- `…/data/raw/YYYY/league_stats/player_stats_YYYY.csv` (2025: 200, 727,469 B, 522 rows) — ESPN API season rows: `points, avg_points, projected_points, projected_avg_points, actual_* stat lines (incl. targets, YAC), proj_*`, with player name/team/position/espn id at the end of the row → ESPN preseason projection vs actual, 2020–2025.
- `…/data/raw/2025/projections/espn_proj/2025_proj_stats.csv` (200, 164,473 B, 501 rows; `player_name, player_id, pro_team, projected_points, year, proj_*`) and `…/data/raw/2025/projections/Fantasy_Pros_Proj/{qb,rb,wr,te,k,dst}_projections.csv` (rb: 200, 184 rows; `Player, Team, ATT, YDS, TDS, REC, YDS, TDS, FL, FPTS`).

### 5.3 bernick4-cyber/draftkings-best-ball-optimizer — weekly points by ADP, 2022–2025 (xlsx)
- https://raw.githubusercontent.com/bernick4-cyber/draftkings-best-ball-optimizer/main/22-25%20Draft%20Data.xlsx — 200, 451,208 B. Sheets: `22-25` (1,212 rows: `Year, Position, Rookie?, RK, Player, Team, ADP, GP, wk1…wk17` weekly points, BYE marked), `2026 ADP` (479 rows: Rank, Player, POS, Team, Bye), `22/23/24/25 Draft ADP`, `Finish Points` (avg PPG by finish bucket), `Rookies 22-25`, `Positions By round`. Scoring: DraftKings best-ball (full PPR + bonuses) — verify before mixing. Also `NFL Project 2025.xlsx` (200, 86,371 B: `2025 Week by Week` 300 rows, DK points-allowed by position). Commit 2026-08-29. No license.

### 5.4 eholland33/2026-Fantasy-Draft-Edge-Calculator — pooled WR year-over-year dataset 2018→2025
- https://raw.githubusercontent.com/eholland33/2026-Fantasy-Draft-Edge-Calculator/main/data/pooled_wr_dataset.csv — 200, 92,795 B, 659 rows; `player_display_name, targets_per_game, receptions_per_game, receiving_yards_per_game, receiving_td_per_game, yards_per_target, air_yards_per_game, yards_after_catch_per_game, team_pass_attempts, games_played, baseline_fp, feature_year, target_year, target_fp` (PPR). Plus `FantasyPros_2021_WR_ADP_Rankings.csv` (200) and `top_100_wr_dataset*.csv` (tree).

### 5.5 StrubeTube/the-lab — career-best finish table and 2025 finishes
- https://raw.githubusercontent.com/StrubeTube/the-lab/main/data/career_finish_hist.json — 200, 8,885 B; 764 Sleeper ids → career-best positional finish (used as `CAREER_BEST` in compute.py). `docs/data/players.json` → `fin25`, `p25`, `ppg25`, `wk25`.

### 5.6 Other historical
- jbattohokson/Fantasy_Football_Draft_Analysis — https://raw.githubusercontent.com/jbattohokson/Fantasy_Football_Draft_Analysis/main/Datasets_V2.zip — 200, 128,269 B; FantasyPros advanced-stats season CSVs RB/WR/TE 2021–2025 (`Rank, Player, G, ATT, YDS, YBCON, YACON, BRKTKL, TGT, RZ_TGT …`); README claims 2021–2025 ADP-vs-PPR mispricing findings (mid-round WRs +10–20, early RBs −15–20) but ADP columns are not in the zip. LICENSE present (MIT).
- lhallee `data/processed/player_seasons.parquet`, `player_games.parquet`, `artifacts/audit_predictions.parquet` (tree verified; 2017–2025 modeling tables and 2022–2025 out-of-sample predictions).
- benirvin714 `data/pick-expectation.json` (200, 165,807 B) and `data/positional-ladder.json` (200, 5,991 B): Sleeper weekly stats 2020–2025 re-scored to a 10-team league; league-specific pick EV and positional value ladder (methodology reference).
- blahovec-labs/ffl-bigquery — tree verified; pipeline for FFC ADP history (2015+) and MFL ADP into BigQuery; only fixtures in repo (`tests/fixtures/ffc_ppr_2015.json`) — useful for FFC endpoint shape if FFC is reachable from the user's machine.
- nflverse coverage for outcomes: `stats_player_week/reg` 2015+, `player_stats.csv` 1999–2024, `ep_weekly` 2006–2025, `snap_counts` 2015+, `injuries` 2020+ (older years not tested).

---

## Priority 6 — Models / methodology worth studying (not yet in our set)

| Repo | License | What to study | Verified files |
|---|---|---|---|
| gadife/nfl-draft-copilot — https://github.com/gadife/nfl-draft-copilot | MIT | VORP/VONA valuation (`lib/vorp.mjs`), opponent simulator whose ADP-deviation and run-chasing parameters are **fit from harvested Yahoo rooms** (`simulate.mjs`, `lib/sim.mjs`, `lib/strategies.mjs`), 10 strategies × 1,800 paired drafts; `research/scoring-calibration.md` (200) | README 200; 3 harvest JSONs 200 |
| btarno/fantasy-draft-sim — https://github.com/btarno/fantasy-draft-sim | MIT | `ffsim.py`: Monte-Carlo snake draft, opponents = ADP + gaussian noise + positional-need + QB-run cascade; paired-seed strategy comparison with t-stats; opponent archetype sweeps (`calibrate.py`) | README 200 |
| Danoodli/fantasy-drafter | none | `lib/engine/montecarlo.ts`, survival = normal CDF on FFC mean/stdev shifted by observed room drift, VONA, strategy config (`config/strategies.json`, λ risk), best-ball mode, `scripts/backtest.ts` | README 200 |
| srsavas42/fantasy-football-research | none | Hierarchical Bayesian volume→efficiency→scoring with walk-forward CRPS; `docs/adp-ablation-2026-08.md`, `docs/injury-availability-2026-08.md`, `docs/vegas-win-totals-2026-08.md`, `docs/out-of-sample-2025.md` (tree) | README 200, projections 200 |
| Brandon-Kimberly/2026-fantasy-football-simulation — https://github.com/Brandon-Kimberly/2026-fantasy-football-simulation | MIT | Season Monte-Carlo with copula-correlated player variance (`fantasy_sim/player_variance.py`, `simulation.py`), byte-exact golden master + real-data backtest gates, 8-phase audit (`AUDIT_SUMMARY.md`); `data/logs/points_backtest.jsonl`, `predictions_2026.jsonl` (IDP league) | README 200 |
| lhallee/fantasy-football-feature-discovery | none | Leakage controls, chronological validation, injury classifier; `docs/report/report.pdf`, `experiments/LEDGER.md` (tree) | README 200 |
| peytonramsey/fantasy-football-draft-model-2026 | none | R walk-forward component model, `R/11_tier_clustering.R`, `R/12_draft_optimizer.R`, `R/13_mock_draft_simulation.R`; `building-model-deepdive.md` (200) | outputs 200 |
| Abhinav811/NFLDraftModel — https://github.com/Abhinav811/NFLDraftModel | none | Backtest figures: Spearman vs ADP, flag hit rates, TD-luck regression, age curves, workload cliff, sophomore leap (`docs/figures/*.png`); Vegas-props-as-volume-prior overlay | README 200, props CSVs 200 |
| sachin7421/fantasy-command-center | proprietary | `src/draft/survival.py`, `src/analytics/shrinkage.py`, `priors.py`, `regression.py`, `mockdraft.py`; golden tests (`tests/golden/survival.json`, `wait_cost.json`) | tree verified |
| curtisdearing/tailstail | none | Distributional draft board (p10/p90, availability, absence matrix), `data/backtest.json` | board 200 |
| ethankwyap-stack/fantasy-edge | none | Consensus-blend rules (omitted player = no vote; one analyst one file), `scripts/boom-rates.js`, `scripts/stat-stickiness.js`, `scripts/seed-odds.js` | JSONs 200 |
| mistakia/league — https://github.com/mistakia/league (23★) | none | Scraper library only: `scripts/import-{4for4,cbs,espn,fantasysharks,fbg,ffn,fftoday,sleeper-adp-and-projections,underdog-bestball-adp,yahoo-adp,rts-adp,mfl-adp,draftkings-odds,nflverse-injuries}.mjs` — endpoint reference for sources we can't reach from here | tree verified |
| jlchatha/ffanalytics-py — https://github.com/jlchatha/ffanalytics-py | GPL | Python port of ffanalytics scrapers (CBS, ESPN, FantasyPros, FFToday, NFL) — run on the user's machine to refresh projections | tree verified (2026-06-05) |
| demansou/fantasy-football-26, adam-zhu1/fantasy-football-draft (`BACKTEST.md`, floor-adjusted VBD), rafa0823/FantasyOptimizer (`docs/research_2026.md`), tsmith4014/fantasy-war-room-2026 (`docs/MODEL.md`, `docs/SOURCE_AUDIT.md`) | none | Methodology docs only | trees verified |

---

## Top 10 pulls ranked by impact

| # | Repo | URL(s) | What it adds | Effort |
|---|---|---|---|---|
| 1 | nflverse/nflverse-data `stats_player` + ffverse/ffopportunity | …/stats_player/stats_player_week_2024.csv, _2025.csv; …/latest-data/ep_weekly_2024.csv, _2025.csv; …/snap_counts/snap_counts_2025.csv | Per-game 2024–25 PPR points, targets/share/WOPR, expected points, snaps → boom/bust rates, PPG stdev, TD regression | Low (CSV, gsis_id join) |
| 2 | najibismail95/Fantasy-Football-ADP-Comparison-Tool | data/silver/adp_snapshots.parquet, projections.parquet, rank_snapshots.parquet, player_xref.parquet | Daily ESPN/Sleeper/Yahoo/FP ADP + ESPN auction + ESPN/Sleeper projections since 07-27 (39 snapshots), with id crosswalk | Low (pyarrow; Sleeper id key) |
| 3 | Danoodli/fantasy-drafter | data/raw/espn-kona.json, ffc-{ppr,half-ppr,standard,2qb}.json, sleeper-projections.json, adp-history-ppr.json | Full ESPN 2026 stat-line + weekly projections, ESPN ADP/auction/ownership; FFC ADP with stdev (pick-availability input); Sleeper stat lines + ADP | Low–Med (parse kona stats by statSourceId/splitType) |
| 4 | srsavas42/fantasy-football-research | ADP/FantasyPros_2015…2026_Overall_ADP_Rankings.csv; projections/2026_ppr.csv; Vegas Win Totals/* | 12 seasons of FantasyPros ADP for backtests; Bayesian p10/p50/p90 2026 projections with projected games; win totals 2003–2026 | Low (ADP) / Med (projections) |
| 5 | ethankwyap-stack/fantasy-edge | boom-rates.json, stat-stickiness.json, playoff-sos.json | Ready-made 2025 boom/bust/median/sd per player (cross-check vs #1) and YoY stat-stickiness correlations | Trivial |
| 6 | StrubeTube/the-lab | data/archive/2026-09-03_vegas.json (+08-27/08-30/08-31), injury_cohorts.json, injury_recent.json, analyst_lists.json, team_context.json, docs/data/players.json | Season-long prop lines with prices (4 dates), injury cohort priors + per-player 2024–25 injury log, Smyth/Flock/FFB/FFA rank lists, DK win totals + PFF O-line, 2025 weekly points + finishes | Low–Med (Sleeper id key; half-PPR proj) |
| 7 | justinmck/fantasy-football-draft-toolkit (MIT) | data/raw/{2020–2025}/adp/*.csv, league_stats/player_stats_YYYY.csv, 2025/projections/* | ESPN preseason projections vs actuals 2020–2025 + FP ADP 2020–2025 + 2025 FP/ESPN projections → projection-accuracy backtest | Med (ESPN stat-id columns) |
| 8 | lhallee/fantasy-football-feature-discovery | artifacts/predictions_2026.parquet, players_2026.parquet, outputs/…xlsx | Audited ML 2026 projection + calibrated missed-time injury probability per player; leakage-controlled methodology | Low |
| 9 | gadife/nfl-draft-copilot (MIT) + btarno/fantasy-draft-sim (MIT) | data/harvest/room*.json; simulate.mjs, lib/sim.mjs; ffsim.py, calibrate.py | Opponent-behaviour calibration from real Yahoo rooms (Yahoo ADP included) and paired-seed Monte-Carlo strategy testing | Med (study/port) |
| 10 | bernick4-cyber/draftkings-best-ball-optimizer | 22-25 Draft Data.xlsx | 2022–2025 weekly points + GP + ADP per player-season (1,211 rows) and 2026 ADP; finish-bucket PPG table | Low–Med (openpyxl; DK scoring) |

Runners-up: theoauyeung `consensus_projections_2026.csv` (ESPN stat lines on gsis_id — trivial join); tykim516 CBS ADP 2026-08-12; benirvin714 Sleeper half-PPR ADP since 08-09 and Clay team projections; lucasreydman + Abhinav811 Vegas props; Paytience420 RotoWire top-250 (09-04); HeyItsJohnny FP positional rankings with tiers/upside/bust + auction values; curtisdearing absence matrix; peytonramsey component projections; keganvosteen 2,209-player stat lines (proprietary license).
