# Quantitative Fantasy Football Ranking, Boom/Bust and Risk Methodologies — Research Digest

Compiled 2026-09-04.

**Access note (read first).** In this session the network proxy blocked direct fetches of fantasypros.com, footballguys.com, draftsharks.com, borischen.co, fantasyfootballanalytics.net, rotowire.com, r-bloggers.com, arxiv.org, reddit.com and web.archive.org, and the web-search budget was exhausted after the first round of queries. What follows therefore comes from three kinds of evidence, labelled per item:

* **[search-snippet]** — content returned in search-result summaries of the primary page (URL given). Numbers are quoted as returned; treat as "reported" until re-verified against the live page.
* **[source-code]** — files read directly from GitHub via raw.githubusercontent.com (URL given). These are exact.
* **[secondary]** — a third-party document (usually a GitHub research note) that quotes or paraphrases a vendor's methodology. Weakest tier; flagged where used.

Where a vendor's method could not be documented at all, the entry says so explicitly rather than guessing.

---

## 1. Consensus / aggregation (ECR, ADP, ADP-vs-ECR value)

### 1.1 FantasyPros Expert Consensus Rankings (ECR) — how it is computed
* Source: https://support.fantasypros.com/hc/en-us/articles/115001219327-What-is-ECR-Expert-Consensus-Rankings-and-how-do-you-calculate-it **[search-snippet]**; also https://support.fantasypros.com/hc/en-us/articles/115001363408-What-is-Best-and-Worst-Rank **[search-snippet]**
* Method, in their terms:
  * ECR is **not** an average rank. "Each ranked position is worth a certain number of Rank Points – the better the rank, the higher the Rank Points. These Rank Points are added up for each player across all experts to determine the player's consensus rank."
  * Rationale for rank points rather than mean: an average "requires assigning an arbitrary rank to unranked players, which skews the results"; rank points avoid treating every unranked player as if every expert put him in the same artificial slot (unranked = 0 rank points from that expert).
  * The exact rank-points schedule (points for rank 1, 2, 3 …) is **not published**.
  * Expert pool weighting: the pool is filtered, not weighted continuously. Per a secondary note quoting FantasyPros' in-season page: "Weeks 1–2 combine recent contributors with prior-year proven performers, while Week 3 onward shifts to accuracy-based selection with recency as a secondary filter." (dillonmannion/quantasy.ai market analysis, **[secondary]**) and "a process that weighs past accuracy, current-season accuracy and submission recency" **[search-snippet]**.
  * Columns exposed with ECR: **Best** (most optimistic expert), **Worst** (most pessimistic expert), **Avg** (arithmetic mean rank of experts who ranked him), **Std Dev** (standard deviation of expert ranks — the "rank spread"). The FantasyPros API fields are `rank_ecr`, `rank_min`, `rank_max`, `rank_ave`, `rank_std` (read from Boris Chen's downloader `src/fp_api.py`, https://raw.githubusercontent.com/borisachen/fftiers/master/src/fp_api.py **[source-code]**). The cheat sheet also carries a `TIER` column and an `ECR VS ADP` column (column list captured in https://raw.githubusercontent.com/hrm619/fantasy_data_pipeline/main/docs/data-sources.md **[source-code]**).
* Reuse: use rank-points (Borda-style) aggregation across your rank sources so that unranked players are not imputed; carry `rank_std`, `rank_min`, `rank_max` forward as the primary "expert disagreement" inputs to the risk score.

### 1.2 FantasyPros expert accuracy scoring (how experts are graded, the basis for pool selection)
* Source: https://www.fantasypros.com/about/faq/football-draft-accuracy-methodology/ (blocked); the mechanism is restated by a benchmark that replicates it: https://raw.githubusercontent.com/colindiggs/nfl-fantasy-rankings-rankings/main/README.md **[source-code, secondary for FantasyPros]**
* Method: "each predicted rank implies the points that rank slot has historically produced … and the gap is the distance from what the player really scored." I.e. accuracy gap = |points_implied_by(predicted rank) − actual points|, summed over the ranked pool. "It weights automatically — a miss at RB2 costs far more than one at RB45."
* Same repo's own metrics (exact code, `scripts/compute.py`): Spearman(predicted rank, actual points); rank MAE = mean|pred_rank − actual_rank|; **top-12 hit rate** = #(pred ≤ 12 AND actual ≤ 12) / min(12, pool); pool depths QB/TE/K/DST 24, RB 36, WR 48; min pool 8; pre-draft overall window 150.
* Reuse: to weight sources by accuracy, back-test each source with the points-implied-by-rank gap (convert each source's rank to a positional rank→points curve from 3–5 prior seasons). This is also the cleanest way to convert a *rank* into a *points-like* quantity for blending with projections.

### 1.3 ADP aggregation
* FantasyPros consensus ADP page https://www.fantasypros.com/nfl/adp/overall.php **[search-snippet]**: "combines Average Draft Position rankings from major league commissioner sites to produce a consensus ADP"; the composite "consists of consensus draft values across the most popular league hosts" (ESPN, Yahoo, Sleeper, NFC/RTSports, Underdog etc. depending on format). The exact combination rule (simple vs. draft-count-weighted mean) is **not documented on the page**; a third-party explainer (scoutcast.ai, **[secondary]**) describes it as "filter out outliers, and compute a weighted average pick number," which should be treated as unverified.
* Fantasy Football Calculator publishes ADP **with a standard deviation per player** by league size/format; hobbyist tools use that dispersion directly (see JAAFFL survival model, §1.4 and zjserapin/ff-edge glossary: "ADP dispersion: Standard deviation of his draft slot, in picks. The underused column." https://raw.githubusercontent.com/zjserapin/ff-edge/main/src/glossary.py **[source-code]**).
* Reuse: if you aggregate ADP yourself, weight each platform by its draft count and keep the cross-platform SD (or FFC's within-platform SD) as `adp_sd`; it feeds both the risk score and the pick-survival model.

### 1.4 "ADP vs ECR" value definitions actually in use
| Definition | Formula (their terms) | Source |
|---|---|---|
| FantasyPros cheat-sheet column | `ECR VS ADP` = difference between ADP and ECR (positive = drafted later than experts rank him → value). Sign convention should be confirmed against the live sheet. | hrm619 data-sources.md **[source-code]** |
| adriantwill/adp-estimate | `Value Score = (Actual Half-PPR PPG Rank) − (ADP Rank)` (used as the *target* for a value model) | https://raw.githubusercontent.com/adriantwill/adp-estimate/main/.agents/PLAN.md **[source-code]** |
| zjserapin/ff-edge | `Value Gap = quality percentile − price percentile` ("Positive means cheap for the quality") | ff-edge glossary **[source-code]** |
| Prometheus-Frameworks/TIBER | `efficiency = 1 − |projRank − adpRank| / 36.0` | https://raw.githubusercontent.com/Prometheus-Frameworks/TIBER-Fantasy/main/PLAYER_COMPASS_METHODOLOGY.md **[source-code]** |
| jeisey/jeisey-tiers (ADR-034/040) | `rank_gap = market_adp − fair_rank`; `regional_value_gap = ln(market_adp / fair_rank)`; score = within-preset percentile of `regional_value_gap` | https://raw.githubusercontent.com/jeisey/jeisey-tiers/main/docs/DECISIONS.md **[source-code]** |
| hicklax13/Project_JAAFFL | Pick-survival: `S_j(N) = 1 − Φ((N − m_j)/s_j)` with `m_j` = ADP mean, `s_j` = ADP SD, N = your next pick | https://raw.githubusercontent.com/hicklax13/Project_JAAFFL/main/docs/draft-system-design.md **[source-code]** |
* Reuse: the log-ratio form `ln(ADP / rank)` is the best of these because a 5-pick gap at pick 5 is not the same as at pick 95; the survival formula converts ADP+SD into "probability he is still there at my next pick."

### 1.5 Aggregating *projections* (not ranks) across sources
* ffanalytics R package (Isaac Petersen / FantasyFootballAnalytics), `R/calc_projections.R`, https://raw.githubusercontent.com/FantasyFootballAnalytics/ffanalytics/master/R/calc_projections.R **[source-code]**:
  * `projections_table(avg_type = c("average","robust","weighted"))`.
  * `weighted`: `weighted.mean()` with default source weights `c(CBS = 0.145, ESPN = 0.157, NFL = 0.140, FFToday = 0.151, NumberFire = 0.142, FantasySharks = 0.142, WalterFootball = 0.130, RTSports = 0.123, FanDuel = 0.142)` (weights are near-equal, i.e. roughly 1/n with small accuracy tilts).
  * `robust`: Hodges–Lehmann / Wilcoxon location estimator — median of all pairwise averages: `pairAvg <- sort(c(vec, combn(vec, 2L, function(x) sum(x)/2))); median(pairAvg)`.
  * `sd_pts`: SD of point projections across sources (weighted SD `sqrt((sum.w/(sum.w^2 − sum.w2)) * sum(w*(x − mean.w)^2))` in weighted mode; MAD-based in robust mode).
* Older FFA site scripts (`R Scripts/Functions/League Settings.R`, https://raw.githubusercontent.com/FantasyFootballAnalytics/FantasyFootballAnalyticsR/master/R%20Scripts/Functions/League%20Settings.R **[source-code]**): all `sourceWeights` = 1 (equal), i.e. plain "wisdom of the crowd."
* Petersen textbook, decision-making chapter (https://raw.githubusercontent.com/isaactpetersen/Fantasy-Football-Analytics-Textbook/main/decision-making.qmd **[source-code]**): use "at least 5–10 sources of projections" (diminishing returns beyond), and either weight "each prediction according to the historical accuracy of the prediction source" or use a robust centre (median / Hodges–Lehmann). Caveat he reports: crowd projections explain only "~30%" of variance among high-projected/high-scoring players.
* Industrial-strength blending in a hobbyist repo (riskittogetthebrisket FORMULA_INVENTORY, https://raw.githubusercontent.com/jasonleetucker-code/riskittogetthebrisket/main/docs/master-site-audit/FORMULA_INVENTORY.md **[source-code]**): count-aware blend — 1 source pass-through; 2 → mean; 3–4 → untrimmed mean-median; ≥5 → trimmed mean-median; Hampel outlier reject `|x − median| > 2.75 × 1.4826 × MAD` (min n = 4); single-source rows get a 0.30 haircut; hierarchical shrinkage `shrunk = 0.9·group + 0.1·anchor`.
* Reuse: blend projections with a robust centre (median or Hodges–Lehmann) plus a Hampel reject; keep `sd_pts` as a risk input; weight sources by back-tested accuracy only if you have ≥3 seasons of history, otherwise equal weights.

---

## 2. Value Based Drafting (VBD / VORP / VOLS / VONA)

### 2.1 Joe Bryant's VBD (Footballguys)
* Source: https://www.footballguys.com/article/bryant_vbd?article=bryant_vbd **[search-snippet]** and https://www.footballguys.com/article/2026-value-based-drafting-one-strategy-behind-every-strategy **[search-snippet]**.
* Core statement: "The value of a player is determined not by the number of points he scores, but by how much he outscores his peers at a particular position." Requires (1) projections for every fantasy-relevant player and (2) a baseline per position under your league settings.
* Formula: `VBD(player) = ProjPts(player) − ProjPts(baseline player at his position)`.
* Baseline variants (names as used in the VBD literature; definitions quoted from famendola1/VBD-Package README, https://raw.githubusercontent.com/famendola1/VBD-Package/master/README.md **[source-code]**):
  * **VOLS** — Value Over Last Starter: "How much better is [RB] than the last starting running back?" (baseline = starter count × teams).
  * **VORP** — Value Over Replacement Player: "…than the best running back available on waivers?" (baseline = first undrafted player).
  * **VONA** — Value Over Next Available: "…than the best running back available at your next pick?" (dynamic, ADP-driven).
  * Bryant's classic operational baseline (used by FFA below): the number of players at each position taken within the first N picks (N = 100, or `teams × rounds` of the draftable pool), e.g. "12-team league with 180 total drafted players… counting drafted players at each position within the top 180 slots by ADP, then using the next available player."
  * Worked example in that README: RB projected 289.8 − baseline RB 67.1 = **222.7 VBD**.
* Footballguys' Draft Dominator adjusts baselines with a "replaceability factor": "quarterbacks and tight ends are considered more replaceable than running backs and wide receivers, with kickers and team defenses being even more replaceable, so the baselines at some positions have been modified" (https://sportsguys.zendesk.com/hc/en-us/articles/360007697334 **[search-snippet]**). Exact factors not published.
* Harstad's "Rethinking VBD" (https://www.footballguys.com/subscribers/apps/article.php?article=HarstadValueOverBaseline) is subscriber-only and could not be read; **undocumented here**.

### 2.2 Baselines actually used (collected)
| Implementation | League | Baseline ranks | Notes |
|---|---|---|---|
| FFA site scripts (2013–14) `League Settings.R` | 1QB/2RB/2WR/1TE, top-100 picks | **QB15 / RB37 / WR36 / TE11** | "position replacements within top 100 draft picks" **[source-code]** |
| ffanalytics package default `default_baseline` | generic 12-team | **QB13 / RB35 / WR36 / TE13 / K8 / DST3** (DL10/LB10/DB10) | `VOR = points − points[rank == baseline]` **[source-code]** |
| nick-holt/sfb15 `vorp_calculator.py` | 12-team 1/2/3/1 | QB12 / RB24 / WR36 / TE12 (`starters × teams + 1`) | plus scarcity multipliers QB 0.8, RB 1.3, WR 1.1, TE 1.2 **[source-code]** |
| kylelevesque12 `fantasy_vorp.py` | 12-team 1/2/2/1 + 1 FLEX | fills 12/24/24/12 fixed starters, then 12 flex greedily from RB/WR/TE; replacement = best player left | `vorp = proj − replacement_points` **[source-code]** |
| benitoooooooooooo/draft-engine | configurable | `starters_per_pos = {QB: qb_slots×teams, RB: (rb_slots+flex_slots)×teams, …}` — all flex assigned to RB | **[source-code]** |
| Project_JAAFFL (12-team, non-PPR, 1/1/3/1 + flex) | | **QB13 / RB22–24 / WR40–42 / TE13 / K13 / DST13**; flex split default 8 RB / 4 WR; "swing of ±2 ranks ≈ 2–4 points of VOR on the RB20 bubble" | VOLS blended with man-games adjustment **[source-code]** |
| jbondurant Model B (waiver replacement, 12-team 1/2/3/1/2FLEX) | | **QB21 / RB61 / WR81 / TE19** (positional ranks in historical full drafts) | true VORP (waiver) baseline **[source-code]** |
| Dayy346/fantasy-draft-assistant | 12-team | RB30 / WR36 / TE12 / QB12 (PPG) | `vorp = player_ppg − replacement_ppg` **[source-code]** |
| jj-song/fantasy_football | deep | QB24 / RB50 / WR60 / TE20 / K15 / DST12 | **[source-code]** |
| riskittogetthebrisket F-041 | | "mean per-game pace of the FIVE players ranked just below the league's starter cutoff; vorp = points − replacement × games" | smooths the cutoff **[source-code]** |
* For a **10-team** 1QB/2RB/2WR/1TE/1FLEX league the same logic gives VOLS baselines ≈ **QB10–11, RB20–24, WR24–30, TE10** (flex split decides RB/WR), and top-100-pick VORP-style baselines of roughly QB12, RB30, WR30–32, TE10. These are derived from the rules above, not quoted from a source.

### 2.3 Converting VBD into a draft/auction value
* Auction share (kylelevesque12): `discretionary = league_budget − teams × roster_spots`; `share = positive_vorp / Σ positive_vorp`; `auction_value = 1 + share × discretionary` **[source-code]**.
* Normalised draft value (nick-holt): 0–100 scale = **50% VORP + 30% scarcity-adjusted VORP + 20% raw projection**; tiers by absolute score ≥80 Elite, 60–79 High, 40–59 Good, 20–39 Average, 1–19 Low, 0 replacement **[source-code]**.
* Rank→cardinal value (riskittogetthebrisket F-010): Hill curve `v = 1 + 9998 / (1 + ((rank − 1)/65.4)^0.91)` on a 0–10,000 scale (KTC/FantasyCalc-style) **[source-code]**.
* dynasty-genius Phase 12 recommended pipeline: positional VORP → isotonic-regression calibration to realised positional percentile → exponential-decay scaling to 0–10,000 (https://raw.githubusercontent.com/davidtleess/dynasty-genius/main/docs/strategies/Phase%2012%20Research%20Brief%20-%20Merged.md **[source-code]**).
* Subvertadown BEER+ (quoted in makoncline/fantasy-tiers research note, **[secondary]**): only published weight is `VOLS weight = VOLS relevant-player count / (BEER count + VOLS count)`, example "≈40% VOLS / 60% BEER."
* Reuse: VBD (points over VOLS baseline with flex-aware allocation) is the right *cross-position* currency; convert to 0–100 with a percentile or a saturating curve, not a linear min-max, because the value curve is convex at the top.

---

## 3. Boom / bust, ceiling / floor, consistency

### 3.1 FantasyPros "Boom or Bust" report — exact thresholds
* Source: https://support.fantasypros.com/hc/en-us/articles/360055737733-How-is-a-boom-or-bust-performance-determined-on-the-Boom-or-Bust-Report **[search-snippet]**; report pages e.g. https://www.fantasypros.com/nfl/reports/ppr-boom-bust-rb.php.
* Thresholds are **points-based, derived from that season's weekly positional averages** (not a fixed rank finish):
  * QB and TE: **boom** week = at or above the average weekly **QB3 / TE3** points total; **bust** week = at or below the average weekly **QB18 / TE18** points total.
  * RB and WR: **boom** = at or above the average weekly **RB6 / WR6** total; **bust** = at or below the average weekly **RB40 / WR56** total.
  * The report also computes "the average points total for an RB1, WR1, etc." and reports how often a player hits those thresholds (a "startable" rate) alongside Boom% and Bust%.
* Reuse: compute per-season positional weekly point thresholds (mean of the weekly k-th ranked score) and count boom/bust weeks for each player; this is cheap and matches an industry-standard definition.

### 3.2 4for4 consistency / boom-bust
* Source: 4for4 (John Paulsen) consistency articles — paraphrased in search results only **[search-snippet]**: "looking at each player's numbers in every week throughout a full season, then calculating a player's standard deviation to determine how much variation there was in their fantasy scoring on a week-to-week basis." The site's exact "consistency rating" scaling and any boom/bust cut-offs are **not documented in what I could access**.

### 3.3 Fantasy Points ("Fantasy Consistency Review"), Establish The Run ("range of outcomes"), RotoViz ("range of outcomes"), Underdog / PFF ceiling projections
* Fantasy Points publishes an annual "Fantasy Consistency Review: Production" (https://www.fantasypoints.com/nfl/articles/2025/2024-fantasy-consistency-review-production) — page blocked; method not captured. Their draft export columns are `RK, PLAYER NAME, POS, TEAM, BYE, TIER, EXODIA` (hrm619 data-sources **[source-code]**), so "EXODIA" is their composite; formula unpublished.
* Establish The Run, RotoViz, Underdog and PFF ceiling/floor methodologies: **undocumented** — no accessible methodology write-up was found (only marketing mentions in secondary docs). Do not cite specific percentiles for them.

### 3.4 Draft Sharks "3D Value" and ceiling/floor
* Draft Sharks export columns: `Rank, Team, Player, Fantasy Position, Games, ADP, Bye, SOS, InjuryRisk, Floor Proj, Consensus Proj, DS Proj, CeilingProj, 3D Value` (https://raw.githubusercontent.com/hrm619/fantasy_data_pipeline/main/.claude/agent-memory/playwright-automation-engineer/draftsharks-export.md **[source-code]**).
* Their description of 3D Value, quoted by rollingrock/ff-house-rules APP-FEATURE-SURVEY **[secondary]**: "a single composite number that already contains projections + filled roster slots + dropoff-to-your-next-pick + tiers" and "17 in-draft value indicators tracked in real time." Scale observed in a league export: 0–10,000 ("offense max 10,000"), with an empirical projection→value slope ≈ 0.096 (riskittogetthebrisket ceiling audit **[source-code]**).
* How Floor/Ceiling projections are generated is **not published**.

### 3.5 Hobbyist / open definitions you can actually implement
| Metric | Definition | Source |
|---|---|---|
| Ceiling / floor from a spread | `floor = μ − 1.28·σ`, `ceiling = μ + 1.28·σ` (10th/90th pct), with `σ = blend(cross-source SD, historical same-tier weekly SD)` | Project_JAAFFL design doc **[source-code]** |
| Boom / bust probability by simulation | `boom_prob = mean(sim > 0.9 × ceiling)`; `bust_prob = mean(sim < 1.1 × floor)`; 10,000 Monte-Carlo draws; report p5/p10/p25/p50/p75/p90/p95 | derekrbreese/fantasy-football-mcp-public `src/utils/scoring.py` **[source-code]** |
| Consistency (0–1) | `1 − (SD_weekly / mean_weekly)` = 1 − CV | Dayy346 metrics.md **[source-code]** |
| Consistency composite | startable rate 45% + floor-as-share-of-average 25% + inverted variance 15% + availability 15% | zacharytran26/Fantasy-Football-Draft-MCP methodology.md **[source-code]** |
| Percentile projections | Position × scoring LightGBM quantile regression at P10/P25/P50/P75/P90, monotone via L2 projection; season value = hurdle model `availability (games / horizon) × PPG-when-active` with Gaussian copula | jeisey/jeisey-tiers DECISIONS.md **[source-code]** |
| Risk-adjusted objective | `mean − λ·(mean − p10)` (λ tunable) | jbondurant/fantasyFootball MODEL.md **[source-code]** |
| Weekly noise model | lognormal weekly scores with `σ_log = sqrt(log(1 + WEEKLY_CV²))`; playoff weeks 15–17 weighted 1.90 | montoash/draft_commander **[source-code]** |
| Positional rank bands | RB1 = ranks 1–12, RB2 = 13–24, same width for WR/TE/QB | kaedonj16/fantasy-dashboard historical_analytics.md **[source-code]** |
| Petersen textbook | uncertainty = SD or **CV = s/x̄** of projections across sources; "players with greater uncertainty are risky and tend to have a higher upside (or ceiling) and a lower downside (or floor)"; variance of a sum `s_(x+y) = sqrt(s_x² + s_y²)` | player-evaluation.qmd, modern-portfolio-theory.qmd **[source-code]** |
| Petersen week-to-week variability | compute week-to-week SD per stat category per player-season, take a robust average across players/seasons, propagate with `var(aX+bY) = a²var(X) + b²var(Y)` — TDs are far more variable than yards | https://fantasyfootballanalytics.net/2014/07/weekly-variability-simulation.html **[search-snippet]** |

---

## 4. Injury risk models and age/durability tables

### 4.1 Draft Sharks Injury Predictor
* Sources: https://www.draftsharks.com/injury-predictor/about and https://www.draftsharks.com/kb/injury-predictor **[search-snippet]**.
* Method (their words): "a comprehensive database of NFL injuries" (30 years), "advanced machine learning" evaluating "nearly 300 variables for almost 3,500 player seasons" (marketing copy elsewhere says "more than 1,000 variables"), including "individual injury histories, total accumulated injuries by type and category, days elapsed between injuries, durability and susceptibility scores, injuries and games missed per 100 opportunities, and player usage and athletic profiles." Trained on "player seasons prior to 2016 for players with vetted injury histories… while hiding some data from the model until training is complete."
* Outputs (exact field names scraped by matttoppi/ffsim `archive/scripts/injury_risk_scraper.py`, https://raw.githubusercontent.com/matttoppi/ffsim/main/archive/scripts/injury_risk_scraper.py **[source-code]**): `career_injuries`, `injury_risk` (categorical, e.g. "High Risk"), `probability_of_injury_in_the_season`, `projected_games_missed`, `probability_of_injury_per_game`, `durability`. "Projected Games Missed" is stated with an **80% confidence interval**.
* The mapping from probability to risk category, and the model form, are **not published**.
* Reuse: if you licence/scrape it, use `probability_of_injury_per_game` and `projected_games_missed` directly; otherwise emulate with position × age base rates (§4.3–4.4) and history flags (§4.5).

### 4.2 Sports Injury Predictor
* No methodology page was reachable; only a 2017 GitHub post about its premium paywall surfaced. **Undocumented.**

### 4.3 Published injury-rate tables by position
* WalterPicks 2026 Advanced Fantasy Guide (15-year history; https://raw.githubusercontent.com/anthonydellapia1117/yeahthatfantasyleague/main/data/Walter%20Ai-2026_Advanced_Fantasy_Guide.md **[source-code copy of vendor PDF]**):
  * RB: **5.2% injury rate per game; 62% miss ≥1 game per season; 3.9 games missed per injury**
  * WR: 4.5%; 50%; 3.2
  * TE: 4.9%; 49%; 2.6
  * QB: 2.5%; 31%; 3.1
* Mean games played, starters, 17-game era 2021–24 (mearls0501/gridiron-gm nfl-reference.md, nflverse-derived **[source-code]**): QB 14.23 of 17 (2.77 missed; 32% play all 17; 34% under 14), RB 15.31, WR 15.20, TE 15.51.
* Zinkelburger/Fantasy-Football-Tool `research/injury_predictor/position_age_injury.py` **[source-code]** builds empirical tables 2018–2025: % of games missed = `total_missed_inj / total_team_games × 100`; weekly hazard = `new_absences / at_risk_players`; age buckets RB ≤22, 23–24, 25–26, 27–28, 29+ (others ≤23, 24–25, 26–27, 28–29, 30+); continuous slope via `missed_inj = β0 + β1·age + β2·log_adp`. (Code, not results.)
* Reuse: convert per-game injury rate `p` and mean games-per-injury `g` to expected games missed `E[miss] ≈ 17·p·g` (RB ≈ 17×0.052×3.9 ≈ 3.4; WR ≈ 2.4; TE ≈ 2.2; QB ≈ 1.3) as a position prior, then scale by age multiplier (§4.5).

### 4.4 Age curves / "age cliff" evidence
* tevans-barton/PositionalDropoffs (paired t-tests on consecutive ages, points normalised to career high, PFR data 2017/2022 cohorts, n = 126 QB / 129 RB / 173 WR / 100 TE; https://raw.githubusercontent.com/tevans-barton/PositionalDropoffs/main/README.md **[source-code]**): significant drops at **RB age 27→28 and 28→29**; **WR career years 6→7 and 7→8 (ages 27–29), annual declines from 30+**; **QB 34→35 and 38→39**; **TE career year 7→8** (holds value longer than RB/WR).
* Adam Harstad mortality tables (Footballguys), as reproduced in dynasty-genius Phase 8 brief **[secondary]**: WR "death rate" (DR%) / expected years remaining — age 24: 4.3% / 6.26 yrs; 26: 6.8% / 4.86; **28: 10.8% / 3.62**; **30: 17.2% / 2.54**; 32: 27.3% / 1.64. RB: "Following the age 26 threshold, breakaway run percentage declines and soft-tissue injury exposure spikes." TE: "steep cliff at age 30." QB: flag over 33 (mobile QBs lose rushing floor mid-30s).
* dynasty-genius Phase 12 (citing Apex Fantasy Leagues, ESPN, Footballguys **[secondary]**): RB modal peak **25.46**; "76.5% of 15+ PPR seasons occur in the 22–26 window"; "**25.2% PPG decline from age-28 to age-29**"; WR modal peak **26.95**, decline from ~29; TE cliff ~30, "85% of TE breakouts occur by Year 3"; TE Y1→Y2 +98.5%.
* zacharytran26 methodology.md: RBs "decline from 27", receivers "decline from 30" **[source-code]**.
* Reuse: age flags — RB ≥27 (+1 tier of risk), RB ≥29 (+2); WR ≥29/30; TE ≥30; QB ≥34 (mobile QB ≥33).

### 4.5 Open durability / injury-risk scoring rules
| Rule | Detail | Source |
|---|---|---|
| Age multiplier on injury risk | <26: 1.0×; 26–28: 1.1×; 29–30: 1.25×; 31+: 1.5× | sdubois777/Rook `backend/agents/injury_risk.py` **[source-code]** |
| Pattern flags | RECURRING_SOFT_TISSUE; CONCUSSION_HISTORY (≥2); HIGH_MILEAGE (RB career carries ≥600); POST_ACL (within ~2 seasons); CHRONIC_CONDITION; WORKLOAD_CLIFF (RB last-season carries ≥300) | Rook **[source-code]** |
| Value modifier tiers | low 0 to −0.05; moderate −0.10 to −0.20; high −0.20 to −0.35; volatile −0.35 to −0.40 (needs multiple severe flags AND 8+ games missed in 2 of last 3 seasons; single-season injuries cap at "high"); final = base × age multiplier | Rook **[source-code]** |
| Position injury multipliers | RB 1.5×, WR 1.2×, TE 1.1×, QB 1.0×, K/DEF 0.5×; age-risk thresholds QB 35, RB 30, WR/TE 32 | derekrbreese `src/models/draft.py` **[source-code]** |
| Status → expected games multiplier | Out 0.82, IR 0.30, PUP 0.45, Suspended 0.60 | montoash/draft_commander **[source-code]** |
| Availability-adjusted value | `vorp_per_game = vorp / expected_games_played` (default 17) | nick-holt **[source-code]** |
| Draft-model split | Rounds 1–7 "projections exact, no injuries"; rounds 8+ add measured projection error ("fog"), per-player injury risk (Draft Sharks), waiver replacement | jbondurant MODEL.md **[source-code]** |
| Durability normalisation | `(durability − 50)/50` (Draft Sharks durability treated as a 0–100 percentile) | worthybrae/fantasy-football `scoring/draft_model.py` **[source-code]** |

---

## 5. ADP hit-rate / historical bust-rate studies and projection accuracy

### 5.1 Hit / bust rates by ADP round and position (fantasy ADP unless noted)
| Finding | Numbers | Source |
|---|---|---|
| First-round bust rate, 11 seasons | **36% of first-round picks bust** — highest of any round except that "it is simply easier for a first-round pick to not deliver ROI"; the **#1 overall pick finished #1 at his position once in 11 years, and every miss was an injury** | RotoWire, https://www.rotowire.com/football/article/first-round-busts-what-11-years-of-fantasy-football-drafts-say-about-first-round-bust-rates-130067 **[search-snippet]** |
| First-round RBs since 2016 | **64% of RBs with R1 ADP finished top-12; 25% top-3**; top-half-of-R1 RBs: **71.7% top-12, 40% top-3** | PlayerProfiler, https://www.playerprofiler.com/article/draft-top-rbs-in-auction-formats/ **[search-snippet]** |
| Top-12 ADP RBs, 5 seasons | 28 of 60 missed top-12 (**53% hit / 47% miss**); "in round one, receivers hit more and bust less" | The IDP Center, https://www.theidpcenter.com/whats-new/rb1-bust-rate-vs-wr1-bust-rate-do-wr-actually-have-the-higher-floor **[search-snippet]** |
| Top-12 ADP → top-12 finish, 2016–2025 (n = 84 each) | **RB 58.3%, WR 44.0%** (difference not significant by z-test); preseason consensus RB1 → actual RB1 **2/10 = 20%**; prior-year RB1 declined in 6 of last 7 seasons, avg −35 to −45% PPG; 13 of last 21 first-time WR1s came from WR18–WR50 ADP; 96% of WRs with 140+ targets finished top-24, 74% top-12 | yeahthatfantasyleague 2026 research director report **[source-code]** |
| Hit rate by ADP round, 2018–2025 PPR | **RB R1 57% top-12 vs 1% for rounds 11+; WR R1 58% vs 1%**; base rate P(top-12) per player-season: QB 16%, RB 10%, WR 6%, TE 10%; bust defined as "drafted inside positional ADP top-12 and finished outside"; rates shrunk with empirical-Bayes prior n = 30, Wilson 95% CIs | kaedonj16/fantasy-dashboard historical_analytics.md **[source-code]** |
| Bust/hit rates by round 2015–2025 | article exists (https://fantasysquawk.com/blog/adp-vs-reality-2015-2025) but was blocked — numbers **not captured** | **[undocumented]** |
| Breakout / fall-off base rates 2001–2024 | breakout (Starter→Star tier) rate per candidate-season **QB 7.4%, RB 7.9%, WR 6.1%, TE 10.8%**; bounce-back after a fall-off ≈ **30.2%**; logistic model: each year of age −15% odds, each PPG of drop −24%, each PPG above Star cutoff +43%, each consecutive Star year +22% (LOOCV AUC 0.747 but walk-forward 2023–24 AUC 0.50–0.61) | Ian-Heslin breakout-falloff-methodology.md **[source-code]** |
| Bust detectability in-season | preseason busts become statistically detectable at **week 4** (accuracy ≈58–62% by position), flat after week 6; RB weekly σ grows ~10.4× from RB1 to RB60, no such structure for WR/QB | jbondurant RESEARCH-PLAN.md **[source-code]** |
| NFL draft-capital (not ADP) rates, for priors on rookies | R1 RBs: 25.5% RB1 / 55.3% RB2 seasons; R2: 10% / 20%; R4: 1.4% / 4.1%; R1 WRs: 40.5% ever deliver a WR1 season; TE: 53.6% of top-6 seasons are one-year wonders | EyalPasha blueprint (aggregating PFF/FantasyPoints/RotoWire) **[secondary]** |
* Reuse: a round-based prior — P(top-12 | R1 ADP) ≈ 0.55–0.65 for RB, ≈ 0.45–0.60 for WR; bust ≈ 0.35–0.45 in R1 rising steeply after R3; add +0.1 bust for RB age ≥28 and for prior-year RB1s.

### 5.2 Projection accuracy findings (for source weighting)
* FFA "Subscription Accuracy" study (2015 season, 10 free + 6 paid sources; https://raw.githubusercontent.com/FantasyFootballAnalytics/FantasyFootballAnalyticsR/master/R%20Markdown/SubcriptionAccuracy/subscriptionAccuracy.md **[source-code]**): overall R² free 0.63 vs paid 0.62; MASE 0.56 vs 0.57. By position (free R² / MASE): QB 0.72 / 0.41; RB 0.49 / 0.67; WR 0.62 / 0.60; TE 0.58 / 0.56. "Subscription sources are not more accurate than the free sources."
* FFA `Evaluate Projections.R` **[source-code]**: metrics = R², MASE, correlation, ICC, Harrell's c-index / Somers' Dxy; ensembles = simple mean and median of ~19 sources; no accuracy weighting applied in the ensemble.
* Petersen textbook, evaluating-prediction-accuracy.qmd **[source-code]**: yardage far more predictable than TDs (e.g. passing yards R² = .51 vs passing TDs R² = .16) — low-base-rate events drive most projection error.
* dynasty-genius Phase 12 **[secondary]**: RB "Weighted Opportunity" y/y correlation 0.95–0.97; RYOE ≈ 0 (rejected); recommends Kendall τ-b over Spearman for small heavy-tailed pools and NDCG@12/@24 as the accuracy metric that matches draft decisions.

### 5.3 Fantasy Football Analytics "risk" measure (Isaac Petersen)
* Original site script `R Scripts/Calculations/Risk.R` (https://raw.githubusercontent.com/FantasyFootballAnalytics/FantasyFootballAnalyticsR/master/R%20Scripts/Calculations/Risk.R **[source-code]**):
  * `sdPts` = `mad(points)` across projection sources per player.
  * `sdPick` = SD of expert ranks (FantasyPros ECR `rank_std`) and SD of crowd ADP (`sdPick_experts`, `sdPick_crowd`).
  * z-score **within position**: `sdPickZ := scale(sdPick), by = pos`; `sdPtsZ := scale(sdPts), by = pos`.
  * `risk := rowMeans(cbind(sdPickZ, sdPtsZ), na.rm = TRUE)`.
  * rescale to **mean 5, SD 2**: `risk := (risk × 2/sd(risk)) + (5 − mean(risk))`.
  * Use: `risk ≤ 5 & vor ≥ 0` = "starters" (safe); `risk ≥ 5 & vor ≥ 0` = "sleepers" (high-variance value).
* Package successor `add_uncertainty()` (ffanalytics `calc_projections.R` **[source-code]**): `mean_risk <- scale(rowMeans(scale(cbind(sd_pts, sd_ecr))))`, then `percent_rank(mean_risk)` reported on a 1–99 scale; uncertainty is *relative within position*.
* Reuse: this is the canonical open-source "risk = disagreement" definition; adopt it, add ADP SD and prior-season weekly CV as extra columns.

---

## 6. Hobbyist / Reddit / GitHub models

### 6.1 Boris Chen tiers (the reference implementation)
* Sources: http://www.borischen.co/ **[search-snippet]** and his code https://github.com/borisachen/fftiers — `src/main.R`, `src/ff-functions.R`, `src/fp_api.py` **[source-code]**.
* Input: FantasyPros ECR for a *selected* expert pool ("chosen based on individual experts' accuracy… consistent accuracy above the rest over several seasons"); the field clustered is **`Avg.Rank` only** (Best/Worst/Std.Dev are plotted, not clustered).
* Algorithm: `mclust <- Mclust(df, G = k)` on the 1-D `Avg.Rank` vector (modelNames left to Mclust's default selection); cluster label = tier; tiers renumbered sequentially if Mclust returns fewer than k.
* k is **hand-set per position and format** (`main.R`):
  * Pre-draft: top-200 split first into 3 high-level groups, then re-clustered with k = 10 / 8 / 8 in those groups; formats std, PPR, half-PPR.
  * Weekly: QB k=8 (top 26); RB k=9 std / 10 PPR / 9 half (top 40); WR k=12 / 12 / 10 (top 60); TE k=8 / 8 / 7 (top 24–25); K k=5 (20); DEF k=6 (20); FLEX k=14 / 14 / 15 (95 players starting rank 20).
* Chart: `geom_errorbar(ymin = Avg.Rank − Std.Dev/2, ymax = Avg.Rank + Std.Dev/2)` — i.e. the whiskers are ±½ SD of expert ranks; x-axis = ECR, y-axis = Avg.Rank.
* Replications: aptmac/fftiers-python uses **KMeans on avg rank** with k QB8 / RB9 / WR12 / TE8 / K5 / DST6 **[source-code]**; Robert-F-Mulligan/fantasy-football uses `GaussianMixture(n_components=k, covariance_type='diag')` on `[best, worst, avg]` with k QB6 / RB8 / WR5 / TE5 / DST6 / K7 / FLEX10 **[source-code]**; cbratkovics/fantasy-football-ai uses a 16-component full-covariance GMM (one per round) on PCA-10 features, BIC search over 10–20, reports alternative-tier probability if >0.05 **[source-code]**.
* Reuse: 1-D GMM on the blended rank/value per position; if you dislike hand-set k, choose k by BIC in a bounded range (§6.3).

### 6.2 Other tier-detection rules
| Rule | Detail | Source |
|---|---|---|
| Cumulative drop-off vs. projection SD | `pts_sd = median(sd_pts)`; `tier = 1 + trunc((cumsum(dropoff) − dropoff[1]) / (pts_sd × tier_thresh))`, `tier_thresh` = 1 for QB/RB/WR/TE/K, 0.1 for DST — a new tier starts whenever cumulative points lost since the tier began exceeds one median cross-source SD | ffanalytics `calc_projections.R` **[source-code]** |
| mclust with BIC/ICL | `Mclust(fantasyPoints, G = 1:9)`; choose G by BIC ("closer to zero is better"), ICL, or bootstrapped LRT; result: 3–4 tiers per position on season points; "criteria should only be used as a guide" | Petersen textbook cluster-analysis.qmd **[source-code]** |
| Rolling-median gap detection | tiers = "rolling-median gap detection over the sorted value series"; confidence bucket thresholds: percentile spread ≤0.08 high / ≤0.20 medium; raw spread ≤30 / ≤80 | riskittogetthebrisket F-180/F-182 **[source-code]** |
| DP quantile segmentation | `dp_quantile_wasserstein_v1`, penalty 1.0; stability gate bootstrap ARI ≥0.60, singleton rate ≤0.20, no tier >25% of board, boundary agreement ≥0.50 (their tiers failed the last gate at 0.24 — evidence that tier edges are genuinely fuzzy) | jeisey/jeisey-tiers ADR-035 **[source-code]** |
| SD bands | "Tier 1 = top 1.0 SD above mean", then successive 1-SD bands | Sports Gaming Bible §1.5 **[source-code]** |
| Score thresholds | Elite ≥85, Stud ≥70, Solid ≥55, Flex ≥40, Bench <40 on a 0–100 composite | derekrbreese draft_evaluator **[source-code]** |

### 6.3 Normalising ranks/values across sources
* **Rank points (Borda)** — FantasyPros ECR (§1.1); robust to unranked players.
* **Z-score within position** — `Z = (X − μ)/σ` (Dayy346; Sports Gaming Bible; FFA Risk.R). Dayy346's draft score is a "weighted sum of z-scores, renormalized if metrics are missing" with position-specific weights, e.g. RB: PPG 40%, PPT 20%, OPPG 15%, YPC 10%, Injury −10%, Consistency 5%; WR: PPG 40%, TPG 20%, YPRR/YPT 15%, PPT 10%, aDOT 5%, Consistency 5%, Injury −5%; QB: PPG 45%, pass-TD rate 15%, YPA 10%, rushing PPG index 15%, INT rate −10%, Consistency 5%; three-year blend `0.6·y1 + 0.3·y2 + 0.1·y3` **[source-code]**.
* **Percentile within position** — dynasty-genius argues z-scores "fail on the heavy right-skew inherent in elite athlete performance" and recommends positional percentile as the intermediate, then isotonic calibration **[source-code]**.
* **Points-implied-by-rank** — FantasyPros accuracy method (§1.2): map each source's rank to the historical points of that positional rank slot, then blend in points space. Also used by TIBER (`efficiency = 1 − |projRank − adpRank|/36`) and by the makoncline note's warning: never interpolate *ranks*, only *points* ("rank interpolation can create a number with no FantasyPros-defined meaning").
* **Saturating rank→value curve** — Hill curve (§2.3) or `rank → percentile p = (rank−1)/(500−1)` with tail clamp (riskittogetthebrisket F-015).
* **Min-max** — `(X − min)/(max − min)` (Sports Gaming Bible) — simplest, least robust.

### 6.4 Source weighting in practice
* Equal weights: FFA site scripts; JAAFFL (`μ_p = Σ w_s·proj_s`, `w_s = 1/n`, "empirically ≥ weighted; wisdom of crowd").
* Near-equal accuracy-tilted: ffanalytics defaults (0.123–0.157).
* Accuracy-weighted recommendation without published weights: Petersen textbook.
* Market vs. expert split: jbondurant found "the market feeds cluster tightly (.34–.50) — one consensus, mediocre at outcomes, excellent at behavior," i.e. ADP predicts *drafting behaviour* better than *outcomes*; JAAFFL treats ECR as "a market prior (distinct from projections — it tells you what the room will do)."
* Anti-pattern warning: montoash/draft_commander v35+ abandoned weighted sums entirely — "v34 scored picks with a weighted sum of quantities that lived on four different scales… v35 has exactly one objective: expected points scored by your starting lineup over the season" (`EV = MV + E[best follow-on at next pick]`, `E[max] = Σ_j MV_j·S_j·Π_{i<j}(1 − S_i)`). If you keep a weighted composite, put every component on the same scale (percentile or points) first.

### 6.5 Risk quantification in hobbyist models (summary)
* SD of ranks across experts (`rank_std`) — FantasyPros, Boris Chen whiskers, FFA.
* SD / MAD / CV of projections across sources — FFA, ffanalytics, Petersen.
* ADP SD in picks — FFC, ff-edge, JAAFFL survival model.
* Prior-season weekly CV / consistency = 1 − CV — Dayy346, zacharytran26.
* Simulation percentiles (p10/p90) — derekrbreese, jeisey, jbondurant.
* Games-missed / availability — Draft Sharks fields, nick-holt `vorp_per_game`, Rook flags.

---

## 7. Published weighting recommendations for a single composite score

| Model | Components and weights | Scale | Source |
|---|---|---|---|
| derekrbreese draft evaluator (STRATEGY_WEIGHTS) | **Balanced:** VORP 0.30, scarcity 0.25, need 0.20, bye 0.10, risk 0.10, upside 0.05. **Conservative:** 0.35 / 0.25 / 0.25 / 0.10 / 0.05 / 0.00. **Aggressive:** 0.25 / 0.20 / 0.15 / 0.05 / −0.05 / 0.40. Each component 0–100; VORP score = min(100, max(0, proj − replacement)/100·100); risk score starts at 50 and subtracts age-excess, injury-history and position penalties; upside = +20 if age <25, +15 if volatility >0.7, +15 if ≤2 yrs experience | 0–100 clamp | `src/models/draft.py`, `src/agents/draft_evaluator.py` **[source-code]** |
| nick-holt sfb15 | VORP 50% + scarcity-adjusted VORP 30% + raw projection 20% | 0–100 | **[source-code]** |
| Project_JAAFFL | `Score(p) = MLV_p + κ·max(0, VONA_p) − λ(phase,slot)·σ̂_p + α·CliffBonus_p`, κ ≈ 0.5–0.8, λ = +0.2…+0.4 for starter slots (floor tilt) and −0.3…−0.5 for bench (ceiling tilt), α ≈ 0.3–0.5 for last player in a tier | points | **[source-code]** |
| TIBER Player Compass | 0.25·North(usage) + 0.25·East(team context) + 0.25·South(age/injury) + 0.25·West(market); market efficiency `1 − |projRank − adpRank|/36`; tiers Elite ≥90, High-End ≥80, Solid ≥70, Upside ≥60 | 1–10 / 0–100 | **[source-code]** |
| zacharytran26 consistency sub-score | startable 45%, floor share 25%, inverted variance 15%, availability 15%; baseline regression 40% last year decaying to 5%; RB age ≥27 / WR age ≥30 penalties | 0–1 | **[source-code]** |
| Dayy346 | position-specific z-score weights (§6.3), injury −5% to −10%, consistency +5% | z | **[source-code]** |
| Sports Gaming Bible | `Total = Σ scaled_stat × weight`; `Context Score = Base × (1 + modifier)` with modifiers −9%…+12% for injuries/lineup; scarcity index `SI = league avg − position avg` | arbitrary | **[source-code]** |
| jbondurant | single objective `V(K)` (optimal lineup points) with `mean − λ(mean − p10)` risk knob; market data used only in the opponent-behaviour model | points | **[source-code]** |
| jeisey / dynasty-genius | **ADP/ECR forbidden as inputs to the intrinsic model**; market used only as a post-hoc overlay (`ln(ADP/fair_rank)`) | — | **[source-code]** |
* Consensus across these: (1) projection-derived value (VBD/VORP) is always the largest weight (30–50%); (2) market/consensus is a *prior* or an *overlay*, not a training feature; (3) risk enters as a subtraction proportional to spread (λ·σ), signed by roster context; (4) injury/age enter as multiplicative availability or a bounded negative modifier (≈ −5% to −40%); (5) all components must be percentile- or points-scaled before summing.

---

## Recommended composite model

Everything below is built only from the mechanisms documented above; parameter values are my proposal and the sources for each choice are cited. All per-position calculations use the draftable pool `N_pos` (10-team default: QB 20, RB 50, WR 60, TE 20).

### (a) Composite rank from multiple sources
1. **Put every source in points space.** For each rank source `s` (ECR, ADP, any expert list) map `rank_{s,i}` → `P_pos(rank)` = average season points earned by that positional rank slot over the last 5 seasons (FantasyPros accuracy method, §1.2; makoncline: interpolate points, never ranks). Projection sources are already in points. Handle unranked players by omitting that source and renormalising weights (FantasyPros rank-points logic, §1.1; Dayy346 "renormalized if metrics are missing").
2. **Robust weighted blend.**
   `pts_i = HL_w({ w_s · P_pos(rank_{s,i}) })` — Hodges–Lehmann / trimmed mean-median of the available sources after a Hampel reject at 2.75·MAD (ffanalytics `robust`, riskittogetthebrisket F-020/F-022).
   Default weights (renormalised over available sources): **projection consensus 0.45, ECR 0.35, ADP 0.20**. Rationale: projections carry the outcome signal (FFA R² 0.5–0.7 by position, §5.2); ECR is an accuracy-filtered expert pool (§1.1); ADP is "excellent at behaviour, mediocre at outcomes" (jbondurant) so it gets the smallest weight in the *value* blend and is used fully in (f). Replace with back-tested accuracy weights once ≥3 seasons of history exist (Petersen).
3. **VBD.** `VBD_i = pts_i − P_pos(B_pos)` with VOLS+flex baselines for 10 teams: **QB10, RB22, WR28, TE10** (2RB/2WR/1FLEX split 6 RB / 4 WR, per JAAFFL flex-split logic; cf. ffanalytics QB13/RB35/WR36/TE13 for 12 teams).
4. **Availability and risk adjustment.** `VBD_adj,i = VBD_i × (E[games_i]/17) − λ·σ_i`, with `E[games]` from Draft Sharks `projected_games_missed` if available, else the position prior 17·p·g × age multiplier (§4.3, §4.5), and `σ_i` = cross-source SD of points (`sd_pts`), λ = 0.25 for projected starters, 0 for bench (JAAFFL λ schedule; jbondurant `mean − λ(mean − p10)`).
5. **Composite rank** = descending order of `VBD_adj` across all positions.

### (b) Tier detection
Per position, on `VBD_adj` (or blended avg rank for pure consensus tiers):
* Fit 1-D Gaussian mixtures with `k ∈ [3, k_max]` and pick k by BIC (Petersen `G = 1:9`), with `k_max` = Boris Chen's draft/weekly k for that position (QB 8, RB 9–10, WR 10–12, TE 7–8) and a minimum tier size of 2.
* Guard rail (deterministic fallback when the GMM is unstable or bootstrap ARI < 0.60, jeisey gate): ffanalytics rule — start a new tier when cumulative drop-off since the tier began exceeds `1.0 × median(sd_pts)` for the position.
* Publish a tier-confidence flag = the GMM posterior of the assigned component (cbratkovics reports alternatives with p > 0.05).

### (c) Boom score (0–100)
`Boom_i = 100 × pct_pos( 0.40·boom_rate_i + 0.35·ceiling_gap_i + 0.25·upside_disagreement_i )`, each term first converted to a within-position percentile (dynasty-genius: percentiles over z-scores for skewed data):
* `boom_rate` = share of games in the last two seasons (weighted 0.65 / 0.35) with points ≥ that season's mean weekly **RB6 / WR6 / QB3 / TE3** score (FantasyPros Boom/Bust thresholds, §3.1); rookies/no-history → position median.
* `ceiling_gap` = `(ceiling − pts) / pts` using source ceilings if licensed (Draft Sharks `CeilingProj`), else `ceiling = pts + 1.28·σ_total` where `σ_total = sqrt(sd_pts² + σ_weekly²·17)` (JAAFFL z = 1.28; Petersen variance propagation).
* `upside_disagreement` = `(ECR_avg − rank_min) / ECR_avg` — how far the most optimistic expert sits above consensus (`rank_min` field, §1.1).

### (d) Bust score (0–100)
`Bust_i = 100 × pct_pos( 0.30·bust_rate_i + 0.30·availability_risk_i + 0.15·round_prior_i + 0.15·age_flag_i + 0.10·downside_disagreement_i )`:
* `bust_rate` = share of games (same 2-season weighting) with points ≤ mean weekly **RB40 / WR56 / QB18 / TE18** score (FantasyPros).
* `availability_risk` = `projected_games_missed / 17` (Draft Sharks) or position prior × age multiplier (RB 5.2%/game·3.9 g; WR 4.5%·3.2; TE 4.9%·2.6; QB 2.5%·3.1; ×1.0 <26, 1.1 26–28, 1.25 29–30, 1.5 31+) plus flag bumps (+0.05 each: POST_ACL, RECURRING_SOFT_TISSUE, RB carries ≥300 last season, career carries ≥600; Rook rules).
* `round_prior` = historical P(miss top-12 | ADP round, position): R1 RB ≈ 0.42, R1 WR ≈ 0.42–0.56, rising to ≈ 0.99 by R11+ (kaedonj16; yeahthatfantasyleague; RotoWire 36% R1 overall); add +0.10 for a prior-year RB1 (6 of 7 declined) and for 400+ touch RBs.
* `age_flag` = 0 / 0.5 / 1.0 for {below, at, past} the cliff: RB 27 / 29; WR 29 / 31; TE 30 / 32; QB 34 / 36 (PositionalDropoffs, Harstad, dynasty-genius).
* `downside_disagreement` = `(rank_max − ECR_avg) / ECR_avg` (most pessimistic expert).

### (e) Risk / volatility score (0–100)
FFA definition extended:
`Risk_i = 100 × percent_rank_pos( mean( z_pos(sd_pts_i), z_pos(rank_std_i), z_pos(adp_sd_i), z_pos(CV_weekly_i) ) )`
* `sd_pts` = SD (or MAD) of points across projection sources (FFA `sdPts`); `rank_std` = FantasyPros `rank_std` (FFA `sdPick_experts`); `adp_sd` = ADP SD in picks (FFA `sdPick_crowd`, FFC); `CV_weekly` = prior-season weekly SD / mean (Dayy346 consistency = 1 − CV; 4for4 weekly-SD approach).
* Missing components are dropped from the mean (`na.rm`, as in Risk.R). `percent_rank` follows ffanalytics `add_uncertainty()` (1–99); if you prefer FFA's original scale, rescale to mean 5 / SD 2 instead and treat ≥5 as "sleeper", ≤5 as "starter".
* Interpretation: Risk is symmetric spread; Boom and Bust above are the signed halves. A player with high Risk, high Boom, low Bust is a target; high Risk with high Bust is a fade.

### (f) ADP value score (0–100)
* Core gap in log space (jeisey ADR-034): `gap_i = ln(ADP_i / CompositeRank_i)` (positive = market drafts him later than your board → value; log form equalises early- and late-round gaps).
* Score: `ADPValue_i = 50 + 50·tanh(gap_i / ln 2)` — so being available a full "doubling" later than his rank (e.g. rank 20, ADP 40) ≈ 88; a one-doubling reach ≈ 12. Alternative: within-pool percentile of `gap` (jeisey) or the linear picks form `ADP − rank` shown as the familiar FantasyPros "ECR vs ADP" number.
* Pick timing companion (not part of the score): `P(available at my next pick N) = 1 − Φ((N − ADP_i)/adp_sd_i)` (JAAFFL); recommend a player when `P(available) < 0.5` and he is the last member of his tier (JAAFFL cliff bonus, montoash follow-on EV).

### Sanity constraints
* Never feed ADP or ECR into a model that is later *evaluated* against them (jeisey/dynasty-genius leakage rule).
* Report tier boundaries as fuzzy (jeisey measured boundary agreement 0.24); show the GMM posterior.
* Re-derive `P_pos(rank)` and the boom/bust point thresholds every season — they are season-relative by construction (FantasyPros).
