# Open-source in-season fantasy tools: what they actually do

Surveyed 2026-09-16. Sixteen repositories were shallow-cloned and their scoring and feature
code read directly; star counts and push dates are from the GitHub API on that date. This
is the source for the design choices in `weekly.py`.

## Headline findings

1. **Star count is inversely correlated with methodological depth.** Every high-star repo
   (dtcarls 307, uberfastman 227, ffanalytics 190, krmisystems 93, derekrbreese 83, amarvin 56)
   is a reporting bot, a projection aggregator, or a thin weighted-projection optimizer. The
   genuinely interesting in-season modeling lives in 0-1 star personal projects created
   Jul-Sep 2026. Reference implementations, not dependencies.
2. **Almost nobody scrapes FantasyPros for start/sit.** One repo (InvaderFry) uses ECR as a
   live signal; two pull rest-of-season ECR for waiver drop-protection. Everyone else uses
   Sleeper/ESPN/Yahoo platform projections or builds from nflverse.
3. **nflverse via `nflreadpy` (Polars) has replaced `nfl_data_py` in 2026 repos.** Weekly
   features in the wild: shifted rolling 3/5/8-game means of targets/carries/receptions,
   `offense_pct` snap share, `target_share`, ffopportunity's `total_fantasy_points_exp`,
   implied team total from `spread_line`/`total_line`, `roof`, rest days, and
   defense points-allowed-to-position.
4. **Floor/ceiling is common but rarely calibrated.** From crude (`floor = 0.65 x proj`) to real
   (LightGBM quantile with coverage gating; hurdle-gamma Monte Carlo). Only ffpred, crollila,
   srsavas42 and spagnotta1 validate coverage.
5. **Waiver value is quantified three ways:** (a) lineup delta from re-running the optimizer,
   (b) rest-of-season VOR with a weeks-remaining scaler, (c) change in P(championship) from
   simulation. FAAB sizing is a heuristic everywhere except Schroedes (curve fitted from 423
   real claims).

## Tier A: full engines with distributional modeling

### blobspire/fantasy_quant
https://github.com/blobspire/fantasy_quant - 0 stars, created 2026-09-07. The most rigorous
in-season codebase found.
- **Signals:** ESPN + Sleeper + ETR + sportsbook props (component-level); nflverse closing
  lines (implied team/opp totals); opponent-adjusted DvP; opportunity metrics (carry/snap/
  target/air-yards share, WOPR, RZ touch share).
- **Combination:** component ensemble with **equal weights** and Hodges-Lehmann location
  ("over twelve seasons, equal weighting beat accuracy-weighting in 64% of head-to-heads").
  Per-position calibration: level `E[actual|proj] = a + b*proj` (b ~ 0.92-0.96); hurdle
  `logit P(zero) = alpha + beta*sqrt(mu)`; width `sigma(mu) = c + m*mu`
  (RB/WR/TE ~ 2.2-2.7 + 0.39-0.45*mu, QB 4.7 + 0.17*mu). Hurdle-gamma outcomes, correlated
  by NFL team via Gaussian copula. Calibrated on ~24,000 ESPN projection-vs-actual
  player-weeks 2022-2025.
- **Start/sit rule:** `d_mu - z*d_sd > 0`, z = standardized margin vs opponent (favorites
  refuse variance, underdogs buy it). "One projected point is worth ~1.16pp of weekly win
  probability at an even matchup and ~14% of that in a blowout." Variance-seeking gained
  +0.35pp in-sample, -0.24pp out-of-sample, so the shipped default is **start your studs**.
- **DvP:** two-way additive `y_ij = mu + offense_i + defense_j` with ridge shrinkage
  (QB k=15, RB 45, WR 90, TE 90; half-life 6-10 games). Verifies ESPN's positional ratings
  are the naive measure (rho = +1.000).
- **Waivers:** claim value = expected lineup-sum delta on the drawn tensor (bench depth has
  option value); priority leagues as optimal stopping; wire floor = second-best unrostered
  player per slot, week by week.
- **Streaming:** D/ST `proj_coef = 0.516, opp_total_coef = -0.443`; kickers declared not
  streamable (R^2 0.006 on implied total). "ESPN's D/ST projection is under-reactive to the
  matchup by about 2x."

### srsavas42/fantasy-football-research
https://github.com/srsavas42/fantasy-football-research - 1 star, 461 commits. Hierarchical
Bayesian (PyMC) on nflreadpy.
- **Model:** team plays and pass rate -> opportunity share (Dirichlet-Multinomial over active
  roster) -> per-touch efficiency -> scoring. Role tiers from EWMA trailing snap share.
  Removing an injured player renormalizes shares to teammates automatically.
- **Results:** beats 14 naive baselines by -11.6% CRPS; **best naive is EWMA half-life 2.**
  Trained waiver/lineup agent: +1.66 wins/season, 73% of oracle. Perfect start/sit = +2.58
  wins, perfect waivers = +0.77 more.
- **Non-obvious:** "a defense's own box-score history adds nothing over its own recent
  fantasy points; the opponent plus the closing line is worth -4.6% CRPS, forty-six times as
  much." Weather is a pooled null but real above 15 mph wind (over-projects QBs by +1.84).
  "Averaging only the weeks a player played is 3-5% worse at every window, because absence
  risk is part of next week's expectation."

### Brandon-Kimberly/2026-fantasy-football-simulation
https://github.com/Brandon-Kimberly/2026-fantasy-football-simulation - 0 stars, 648 tests.
- Sleeper + ESPN projections; The Odds API implied totals (required); defensive ratings with
  empirical-Bayes shrinkage (n0 = 12); injury onset hazard + duration mixture.
- Lognormal per player-week with aleatoric (weekly) and epistemic (per-season) variance:
  `VOLATILITY_CONSTANTS = {QB 1.65, RB 1.98, WR 1.8, TE 2.0, K 1.45}`.
- Start/sit: P(A > B) from joint draws; lineup shows p10/p50/p90 and margin over best bench.
- Waivers: blocks hole -> upgrade -> depth, sorted within block by season VORP, then
  re-ordered by week mean: "Season VORP selects; the WEEK decides the order."

### crollila/fantasy-manager
https://github.com/crollila/fantasy-manager - 0 stars. ESPN sync, nflverse cache.
- Season baseline (3 yrs recency-weighted) -> current-season usage update `w = n/(n+4)` on
  targets/carries -> matchup multiplier -> 65/35 blend with ESPN. LightGBM ratio model
  clipped [0.6, 1.6]; walk-forward MAE 4.59 -> 4.42 on 17,110 player-weeks.
- Matchup: ridge on log1p(points); defense multiplier `clip(exp(coef), 0.7, 1.3)`.
- Weekly `boom = P(> 1.5 x center)`, `bust = P(< 0.6 x center)`, graded by Brier afterwards.
- Waivers: `ros = vorp x remaining/17`; `utility = immediate_lineup_gain + 0.12 x ros +
  2 x breakout`; FAAB "a bounded budget heuristic, not a validated model."

### spagnotta1/fantasy-matchup
https://github.com/spagnotta1/fantasy-matchup - 0 stars. nflverse -> DuckDB warehouse.
- Stores p10/p25/p50/p75/p90 + boom/bust tails per player-week from empirical residual
  quantiles over a Gaussian; upper tail factor 2.0 (calibrated: 82.2% vs 80% coverage).
- ESPN scoreboard for pregame spread/total (nflverse lines are closing lines); Open-Meteo.

## Tier B: weighted-signal blenders (transparent formulas)

### InvaderFry/FF-Weekly-Rankings
https://github.com/InvaderFry/FF-Weekly-Rankings - 1 star. The FantasyPros ECR start/sit tool.
- **Default weights:** `ECR 0.60 / Vegas 0.18 / Injury 0.12 / Weather 0.10`, each min-max
  normalized 0-100 within the candidate set; missing signals drop out and weights renormalize.
- **Injury:** QUESTIONABLE 75, DOUBTFUL 35, OUT/IR 0, healthy 100.
- **Weather:** `100 - 3 x max(0, wind - 8) (cap 70) - 30 x precip_prob`; roofed = 100.
- **Close call:** top two within 5 points, or a materially weighted signal disagrees on order.
- **Self-calibration:** grid-searches weights against Sleeper's free weekly actuals.
- **FantasyPros:** `api.fantasypros.com/v2/json/nfl/{season}/consensus-rankings` (key) with
  fallback scrape of `fantasypros.com/nfl/rankings/{slug}.php`; keyless scrape has no week
  selector. ROS pages used for waiver drop-protection.
- **FAAB:** `share = 0.02 + 0.38 x (0.75 x conviction + 0.25 x demand)`, streamers capped 2%.

### MMcGough8/fantasy-football-guide
https://github.com/MMcGough8/fantasy-football-guide - 0 stars, Streamlit, Sleeper.
- Per-stat **median** blend of Sleeper + FantasyPros + ESPN, rescored with league rules.
- **Matchup factor:** `adjusted = points x clamp(implied x dvp x site, 0.88, 1.12)` with
  `implied = clamp(1 + 0.35 x (implied/avg - 1), 0.9, 1.1)`, `dvp = 1 + 0.25 x (factor - 1)`.
  **DvP from nflverse `stats_player_week_{season}.csv`: PPR allowed per (defense, position)
  relative to league mean, prior season blended at `n/(n+4)`, clamped 0.8-1.2.**
- **Confidence:** `swap_confidence = Phi(gap / hypot(sd_a, sd_b))`; < 55% coin flip, <= 65% lean.
- **Waivers:** three buckets by lineup delta - `season` (improves best season lineup),
  `week` (improves this week only = bye/injury filler), `depth` (beats least-valuable drop).

### kingoffrisco/FantasAI
Deterministic 0-100: Projection 30, Matchup 20 `(def_rank - 1)/31`, Opportunity 20
(WR/TE `0.65 x min(tgts/8, 1) + 0.35 x snap%`; RB `0.55 x min(carries/18, 1) +
0.25 x min(tgts/5, 1) + 0.20 x snap%`), Recent trend 10, Injury/Weather 15, Team env 5.

### derekrbreese/fantasy-football-mcp-public
83 stars, 40 forks - a Yahoo MCP server. `score = 0.10 matchup + 0.40 yahoo + 0.40 sleeper +
0.05 trending + momentum`. **Caveat: its defensive rankings are a hard-coded mock dict.**
Popular because it is an MCP server, not because of the model.

### vCxmp/FantasyOS
Sleeper projections, recent 3 weeks, snap %, target/carry share, DvP over a **last-4-game
window**, Sleeper trending adds (24h). FAAB doctrine: "league-winning starter 20-50%,
meaningful stash 5-15%, streamer 0-5%" of remaining budget.

## Tier C: waiver / FAAB specific

### Schroedes/fantasy-football-draft-optimizer PR #34
Rest-of-season VOR gain vs the drop candidate (`min_vor_gain = 5.0`). **FAAB curve fitted
from 423 real historical claims across three leagues:** `bid_pct = bid / remaining_budget`,
bucketed by `floor(vor_gain/10) x 10`, mean per bucket, never extrapolated upward. The only
empirically-fitted FAAB model found.

### DrR0mer0/FAAB-Bot
XGBoost breakout-week classifier. Label: >= 1.5x trailing 3-game average and >= 10 pts.
Features: trailing touches avg/trend, team touch share, opponent matchup, experience,
is_home, is_bye_return, starter_absent_proxy. **Dominant feature: touch share.**
Precision@10 ~ 28% vs 4.3% base rate.

### ramireztirso-rgb/fantasy-football-optimizer
ESPN base x `1 - INJURY_SEVERITY[status]`; recent form `(recent3 - seasonAvg) x 0.25`.
`DEFAULT_CV = {QB .32, RB .52, WR .58, TE .62, K .45, DST .68}`; floor/ceiling at +/- 0.84 sd.
Waivers: optimizer delta with byes neutralized ("a $17 bid that buys nothing after Sunday").

### Others
- **amarvin/fantasy-football-bot** (56 stars): Yahoo projections, MILP maximizing discounted
  ROS points, enumerates 1-3 player add/drops. No external signals.
- **bemky/opfor**: uses an LLM to predict opponents' FAAB bids from league bid history.
- **leofofeo/ml-faab-advisor**, **prashsamosa/swc-fantasy-football**: claim "ML FAAB" with
  no documented model. Trivial.

## Tier D: projection backbones on nflverse

### liaodzns/ffpred
https://github.com/liaodzns/ffpred - best-documented nflreadpy weekly feature pipeline.
- Shifted rolling means over windows [3, 5, 8] per position; game context
  `implied_team_total = total/2 +/- spread/2`, `home_away`, `rest_days`, `roof`; opponent =
  expanding shifted mean of points allowed to position. **Injury-report features exist but
  are OFF: "no effect for QB, RB, or WR."**
- LightGBM per position; baseline = last-3-game average; quantile models ship only if
  coverage passes. `start_sit.py` flags two players "within one MAE" as indistinguishable.

### ffverse/ffopportunity (23 stars, R)
Expected-points models on nflverse pbp; `nflreadpy.load_ff_opportunity()`. The de-facto
"expected fantasy points" signal.

### FantasyFootballAnalytics/ffanalytics (190 stars, R)
Scrapes weekly projections from CBS, ESPN, FantasyPros, FantasySharks, FFToday, NumberFire,
NFL; `add_ecr()` then `add_uncertainty()`. Mature, R-only, no lineup/waiver logic.

### Gin-G/nfl-data-py
NN on nflreadpy: `target_share, air_yards_share, wopr, racr`, snap counts, rolling windows,
`snap_trend = roll3 - roll5`, snap-role bins (0-25 / 25-60 / 60-100%).

## Abandoned / off-target
dtcarls (307 stars) - transaction log only. uberfastman (227) - league metrics, no start/sit.
krmisystems (93) - "legal lineup from current projections." rjh336/ffb_metis - dead since 2017.
jcdavis131/vector-gridiron - README admits results are non-reproducible.

## Patterns worth stealing (and what weekly.py takes)

1. **Implied team total from `total_line` / `spread_line` is the single most-used external
   signal** (ffpred, MMcGough8, InvaderFry, fantasy_quant, Brandon-Kimberly, srsavas42).
   "The betting market has already priced in injuries, weather, pace, and matchup."
2. **Shift-then-roll discipline** with explicit leakage tests.
3. **DvP needs shrinkage and opponent adjustment; raw points-allowed is schedule.** At
   minimum blend prior season at `n/(n+4)` and clamp 0.8-1.2.
4. **Waiver value = lineup delta from re-running the optimizer, never raw projection.**
   Neutralize byes before pricing a bid.
5. **Report noise:** close-call thresholds (5 pts; one MAE; `Phi(gap/sigma)` < 0.65).
6. **Kickers are not streamable; D/ST is mostly opponent + closing line** - two independent
   codebases reached the same conclusion.
7. **Absence counts as zero in recent form**, not dropped - absence risk is part of next
   week's expectation.
8. **Default to "start your studs."** Variance-seeking did not hold out of sample.
