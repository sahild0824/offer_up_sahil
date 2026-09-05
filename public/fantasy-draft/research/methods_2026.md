# Quantifying 2026 situational factors for redraft fantasy football — methods & effect sizes

Compiled 2026-09-05. Network constraints: fantasy/sports sites, Medium, Substack and most academic hosts were not fetchable, so
industry sources are captured from search snippets; GitHub repositories were read in full via raw.githubusercontent.com.

Labels: **[source-code]** = read directly from a public repo; **[search-snippet]** = a number quoted in a search-result snippet of
the named article (the article itself was not fetched); **[secondary]** = a claim reported second-hand, or an analyst assertion
without published data.

A recurring theme worth stating up front: three independent hobbyist backtests (fantasy-forecast, nfl-player-value-analysis,
fantasy-dashboard) each found that **team-environment, schedule and vacated-opportunity multipliers are approximately neutral or
slightly negative for season-long rank accuracy**, while **player share/usage terms carry the signal**. The situation layer should
therefore be small, bounded, and mostly a *risk/variance* adjustment rather than a *mean* adjustment.

---

## 1. Coaching / coordinator changes

### 1.1 How sticky are the coach-controlled quantities?

| Quantity | Year-over-year r | Condition | Source |
|---|---|---|---|
| Plays per game | 0.43–0.47 | QB, HC, or offensive team held constant | PFF, "The factors that help determine teams' pace of play" [search-snippet] |
| Plays per game | 0.39 | team changes primary QB; also QB under a different HC | same [search-snippet] |
| Plays per game (defensive influence) | 0.28 | defense's own YoY | same [search-snippet] |
| Raw seconds per play | 0.47 | all teams | The Spade (Ray Carpenter), "Predicting the 2026 NFL Season's Fastest Offenses" [search-snippet] |
| Steady-State Pace (huddled pace, no-huddle regressed out) | **0.57** | same coach and QB | same [search-snippet] |
| Steady-State Pace | **0.45** | same play-caller, new QB | same [search-snippet] |
| Steady-State Pace | **0.23** | **only the play-caller changes** — "next offense is much more likely to be significantly slower" | same [search-snippet] |
| EPA / pass attempt (team) | ≈0.60 | stickiest team stat since 2021 | SumerSports, "Sticky Stats" [search-snippet] |
| Coach pace ranks when coach stays | — | Bengals never faster than 19th in neutral pace in 7 Zac Taylor seasons; Cowboys under Kellen Moore ranked 6,2,2,8,3,3,2 in OT-adjusted plays/game 2019–25 | ETR, Thorman "2026 Pace Preview" [search-snippet] |

Method note (The Spade): they removed no-huddle plays and regressed each team's huddled pace on no-huddle rate, keeping the residual;
this cut the no-huddle/pace correlation from ~25% to ~2%, and "steady state pace is entirely up to the play-caller."

**How to reuse:** pace/plays carry over at r≈0.45–0.57 when the play-caller stays and only r≈0.23 when he leaves. Treat a
returning play-caller's prior pace as ~50% signal / 50% league mean; treat a departed play-caller's pace as ~25% signal, and use
the *new* play-caller's own history (if any) for the rest.

### 1.2 PROE and coach tendencies (numbers used by analysts)

- PROE = actual pass rate − expected pass rate given down, distance, score, time, etc. (4for4, "How Play-Calling Tendencies
  Affect Fantasy Football," 2025/2026 editions) [search-snippet]. Passing EPA is slightly >0 per play, rushing ≈ −0.10 per play,
  so efficient offenses tend to run positive PROE [search-snippet].
- Volume of change in 2026: 10 new head coaches (tied most ever), 17–19 new offensive play-callers depending on how counted
  (ESPN: 19 new play-callers; RotoWire: 17 offenses with discontinuity; Fantasy Life: 18) [search-snippet].
- Coach-history examples analysts actually project from:
  - Ravens: departed OC averaged **−5.5% PROE over four seasons**; Todd Monken **+1.8% PROE across four seasons as an OC**
    (coaching-change article set; RotoWire/PlayerProfiler) [search-snippet].
  - Broncos: 5th/6th in PROE, 13th/7th in seconds per play in consecutive seasons; 64.2 plays/game (5th) [search-snippet].
  - Mike McCarthy: "past 12 NFL offenses totaled a **15% target share for tailbacks, all 12 in the 11–18% range**," vs league
    average 19% (Mike Clay, ESPN) [search-snippet]. This is the cleanest published example of the coordinator-history method:
    use the *entire* coach history as a range, and note whether the league mean sits inside it.
  - Mike McDaniel: RBs took **≥21.1% of early-down pass attempts in each of the last five seasons** (Fantasy Life) [search-snippet].
  - Zac Taylor/Burrow under a new OC: shotgun rate **88% → 57%** (Sharp Football podcast with JJ Zachariason) [search-snippet].
  - Dolphins 2019→2020 OC change: plays/game rank 11 → 22, pass rate fell ~8 points [search-snippet, anecdote].
- Dallas ran the NFL's highest pace at 65.9 plays/game (2025) [search-snippet].

**No published before/after regression of "coaching change → fantasy points" with averages was found.** Every industry piece
found is a per-team narrative using the coordinator's own history. Claims such as "coaching changes improve performance by 23%"
(NFL EdgeLine, 2026) appear without a defined sample and should be treated as **[secondary]/unverified**.

### 1.3 How open-source code encodes it

- **bsr-0/nfl-player-projections** `src/features/advanced_analytics.py` [source-code]
  (https://github.com/bsr-0/nfl-player-projections/blob/HEAD/src/features/advanced_analytics.py):
  ```
  _HC_CHANGE_IMPACT = {QB: -1.2, RB: +0.3, WR: -0.8, TE: -0.2}   # "avg PPG delta in first 6 weeks under new staff"
  _OC_CHANGE_IMPACT = {QB: -1.8, RB: -0.5, WR: -1.5, TE: -0.6}
  coaching_adaptation_score = exp(-0.693 * weeks_since_change / half_life);  ADAPTATION_WEEKS = 6
  coaching_change_impact = HC_impact*hc_adaptation + OC_impact*oc_adaptation   (OC compounds with HC)
  scheme classes by pass rate: heavy_pass >=0.62, pass_balanced >=0.55, balanced >=0.48, run_balanced >=0.42, else heavy_run
  proxy for an unknown coaching change: |Δ team pass rate vs 17 weeks earlier| > 0.10
  coaching_stability = clip(log1p(tenure_weeks)/log1p(52), 0, 1)
  ```
  The comment says the deltas are "derived from 2010–2024 coaching change analysis" but no data or notebook backs it; treat the
  values as **[secondary]**, the *structure* (position-specific, decaying, OC ≥ HC) as reusable.
- **kaedonj16/fantasy-dashboard** `data_building/breakout_engine/{components,config}.py` [source-code]
  (https://github.com/kaedonj16/fantasy-dashboard): on a 0–100 team-environment score,
  `OC_PASS_HEAVY_THRESHOLD = 0.58`, `OC_RUN_HEAVY_THRESHOLD = 0.44`, `OC_PASS_HEAVY_WR_BONUS = +8`, `OC_RUN_HEAVY_WR_PENALTY = -6`,
  `OC_RUN_HEAVY_RB_BONUS = +8`, `OC_PASS_HEAVY_RB_PENALTY = -4`, `HC_CHANGE_UNCERTAINTY_PENALTY = -3` (also applied when a new OC's
  prior pass rate is unknown). **Backtest result in the same file: the team-environment component had Pearson r ≈ −0.05 vs
  next-season PPG (2022+2023) and its weight was set to 0.00.**
- **curtisdearing/tailstail** `nflvalue/fantasy/features.py` [source-code] (https://github.com/curtisdearing/tailstail): builds
  *coach priors that follow the coach across teams*: per coach-week `coach_pass_rate = pass_att/(pass_att+rush_att)`,
  `coach_pace = plays`, `coach_{rb,wr,te}_target_share`, `coach_qb_rush_share`, each as a strictly-prior EWM with span 8 weeks
  (`pre_coach_*_ewm8`), plus a `coach_history_missing` flag for coaches with no NFL play-calling history.
- **jj-song/fantasy_draft_engine** [source-code]: `new_coaching_staff → −0.1` on a −3…+3 situational grade that carries 15% of a
  30% max weekly adjustment (net ≈ −0.15% of projection — effectively a placeholder).
- **nick-holt/sfb15_projections** [source-code]: hand multipliers of 1.12–1.15 for "coaching_change" on a QB — ad hoc.

**How to reuse:** (i) build coordinator priors as tailstail does (pass rate, pace, RB/WR/TE target shares by coach across his
history); (ii) regress them by the stickiness table above; (iii) use position-specific deltas with an uncertainty term, not a
constant.

---

## 2. Quarterback changes and pass-catcher value

### 2.1 Effect-size evidence

- **Catchable target rate is mostly a QB property and is unstable:** WR catchable-target-rate year-over-year correlation averages
  **0.2894 since 2023** (PFF, "Examining expected fantasy points for wide receivers through catchable target rate," 2026)
  [search-snippet]. ff-edge's glossary calls catchable rate "a property of his quarterback, not of him" [source-code].
- Tee Higgins 2025: catchable target rate **58% without Burrow vs 78% with Burrow**; season rate 64% (25th percentile), finished WR22
  (PFF) [search-snippet].
- Justin Jefferson 2025: catchable rate dropped **~10 points**, end-zone catchable rate fell **50% → 25%** with Wentz/McCarthy;
  finished 30th in PPG after four straight top-5 seasons (PFF) [search-snippet].
- An unnamed receiver: **4.8 catchable targets/game with one QB → 8.0/game with better QBs**, producing like a WR1 [search-snippet].
- **New-QB base rate for WR1 seasons:** of 41 non-rookie WR1 finishes since 2010 by receivers drafted below WR1 range,
  **27 (66%) came with a new full-time quarterback** (Sharp Football, "2026 WR Fantasy Football ADP: Analyzing Historical Trends")
  [search-snippet].
- Game-script channel (see §5): QBs average 18.5 FPG on winning teams vs 14.2 losing; WR/TE splits are "nearly identical to QBs"
  (PFF) [search-snippet].

**Gap:** no study of the form "WR1s with a top-10 QB average X more PPG" was found in accessible sources; nor a multi-season
before/after study of receivers who changed QBs. The Sharp 27/41 base rate and the PFF catchable-rate figures are the only
quantified anchors.

### 2.2 How code encodes it

- **kaedonj16** [source-code]: `QB_UPGRADE_WR_BONUS = +10`, `QB_DOWNGRADE_WR_PENALTY = -14`, `QB_LATERAL_CHANGE = 0` on the 0–100
  environment score; when direction unknown, tier by prior passer rating: ≥100 elite (+10), ≥92 good (+5), ≥84 average (0),
  <84 poor (−8). Note the asymmetry (downgrade hurts more than upgrade helps).
- **bhargavap21/fantasy-forecast** `ffb/projections/qb_fit.py` + `config/weights.yaml` [source-code]
  (https://github.com/bhargavap21/fantasy-forecast):
  `qb_fit_mult = clip(1 + 0.06 · z(team QB deep-ball rate, ≥20 air yds) · z(player aDOT), 0.90, 1.10)` for WR/TE only.
  Ablation: QB-fit "~neutral for season-long rank."
- **tailstail** [source-code]: `qb_changed` flag from week-to-week team QB id; conditional priors shrunk with
  `shrunk = (n·prior_mean + 8·baseline)/(n + 8)` (8 games of pseudo-observations).

**How to reuse:** model the QB effect through *target quality*, not through a flat PPG bonus: project the new QB's catchable
rate / expected points per target (regress ~70% to league mean given r≈0.29), and multiply the receiver's per-target efficiency
by new/old ratio, bounded ±10%.

---

## 3. Player movement: vacated volume, opportunity share, top-down allocation

### 3.1 Definitions used in 2026 articles

- Vacated targets = Σ targets of players no longer on the roster; vacated target share = that sum ÷ team targets
  [search-snippet, footballnationusa 2026 guide].
- **Adjusted vacated targets** (The Snap, "2026 Adjusted Vacated Targets"): subtract, for every incoming player, "the median number
  of targets each incoming player had last year, extrapolated over a full season" [search-snippet].
- FTN "Vacated Opportunities" and PFF "Team target vacuums" publish the same quantity for targets, carries and air yards
  [search-snippet].

### 3.2 Does vacated volume predict anything?

- **Dynasty Football Factory, "The Myth of Vacated Targets":** correlation between vacated targets and next-season PPG growth
  **R² < 0.01, p = 0.24** over four seasons; "vacated targets tell us more about an offense's churn than about opportunity for a
  given player." Among teams that lost a 70+ target player, the most common outcome was a rookie/FA absorbing them, **about half
  of teams simply saw the team target total fall** (less efficient offense), and single-player "unicorn" breakouts were rare
  [search-snippet].
- **zjserapin/ff-edge** README [source-code] (https://github.com/zjserapin/ff-edge): for veterans, "nothing predicts the promotion
  itself (vacated opportunity ~0)"; players *already identified* as promoted hit a top-quartile finish 4.1% / 10.2% / 18.4% by
  quality tercile. For **rookies** the vacated signal *does* matter: rookie model out-of-sample r = 0.592, 24% less error than the
  mean; "the RB model keys on vacated carries, the WR model on vacated targets — draft capital dominates everywhere; combine
  numbers are close to noise."
- **kaedonj16** config [source-code]: backtest Pearson r vs next-year PPG — `opportunity_opened ≈ −0.02`, `competition_removed ≈ −0.07`,
  `competition_added ≈ +0.04`, vs `role_trajectory +0.51`, `confidence +0.55`, `readiness +0.32`. Offseason weights:
  opportunity_opened 0.10, competition_added_penalty 0.07, competition_removed 0.00, team_environment 0.00.

**How to reuse:** vacated volume is a *gating* variable (who is eligible for a role change) and a rookie prior, not a mean shift for
incumbents. Analysts (Yahoo, PFF, ESPN 2026) say the same: "require role evidence before moving a player aggressively"
[search-snippet].

### 3.3 Top-down team projection method

- **Mike Clay (ESPN)** [search-snippet]: goes team by team, analyzes "historical league, team, coach and player trends," and
  "generates projected dropback, carry and target shares for each player"; team pages include coaches & play-callers, unit grades,
  SOS. The McCarthy RB-share example above shows the coach-history input.
- Industry description (Forbes, 2025) [search-snippet]: models "produce team-level totals for points, passing/rushing volume and
  touchdowns, which are then fed into player-level projections."
- **fantasy-forecast `SPEC_opportunity_model.md`** [source-code] — the cleanest written spec and the most honest backtest:
  ```
  proj_targets_pg = proj_target_share × proj_team_pass_att_pg
  proj_carries_pg = proj_carry_share  × proj_team_rush_att_pg
  proj_fp_pg      = targets×pts_per_target + carries×pts_per_carry   (split efficiency, regressed hard)
  team volume: regress hard to league mean (team_volume_shrink_games = 15); shares: EB-regress to role baseline
  (share_shrink_games = 3); efficiency_shrink_opps = 10; volume_shrink_games = 2
  ```
  Results (Spearman, veterans, 3 seasons): projected share predicts next-year share better than raw share (**0.724 vs 0.697**),
  but the reassembled model only ties the multi-season baseline (0.713 vs 0.716). **Vacated-share redistribution hurt by −0.04**
  because per-game shares measured in active games summed to **~1.55 per team (range 1.11–2.05)**; the fix is to normalize team
  shares to 1.0 *before* redistributing.
- **kylelevesque12/nfl-player-value-analysis** `report/two_stage_weekly.md` [source-code]
  (https://github.com/kylelevesque12/nfl-player-value-analysis): weekly WR/TE `team_pass_att × target_share × PPR_per_target`
  with shares renormalized to 1 per team-week: target-share stage **+34.3% RMSE skill vs mean**; team pass attempts stage
  **−3.2% (no skill: "Vegas implied team total + recent pass rate carry less per-game information than expected")**; PPR-per-target
  stage −0.2%; pooled gradient boosting beat the two-stage product by 7–10% RMSE in every year 2020–2025.
- **tailstail** [source-code]: reconciled shares — per team-week, shares of *active* players are divided by their sum when the sum
  exceeds 1 (`pre_reconciled_*_share`), an `overflow` feature records how far the raw shares exceeded 1, and
  `topdown_targets = team_pass_attempts_ewm4 × reconciled_target_share`.

### 3.4 Allocating vacated work among competitors (code formulas)

- **kaedonj16** [source-code]: split vacated work by usage-weighted claims raised to a power:
  `share_i = claim_i^1.6 / Σ claim_j^1.6` (`OPPORTUNITY_SHARE_CONCENTRATION = 1.6`), where claim = prior per-game usage
  (RB: carries + 1.5×targets). Rookies with no usage get a draft-round claim: WR/TE `{R1: 5.0, R2: 3.5, R3: 2.5, R4: 1.5, R5–7: 1.0}`
  targets/game; RB `{R1: 14, R2: 9, R3: 6, R4: 4, R5–7: 2}` weighted touches/game. Cross-position spillover weights let a WR
  departure feed a TE. Role-size normalizers: 110 targets, 220 carries, 0.80/0.70 snap share ≈ "full role." Arrival threat for a
  drafted rookie = `0.15·usage + 0.85·draft_signal`, draft_signal `{R1 1.00, R2 0.82, R3 0.62, R4 0.42, R5 0.28, R6–7 0.16}`;
  FA/trade threat = `max(usage, contract, role_opening × credibility) + 0.10·min(contract, role_opening)`; penalty caps QB 35 /
  RB 28 / WR-TE 24 points, stacked threats weighted 1.00 / 0.75 / 0.55 / 0.35.
- **sidhulyalkar/nfl-player-state-engine** `opportunity.py` [source-code] (https://github.com/sidhulyalkar/nfl-player-state-engine):
  ```
  available_opportunity = 0.35·vacated_target_share + 0.35·vacated_carry_share + 0.20·teammate_absence_prob + 0.10·depth_promotion
  role_capture = 0.18·snap + 0.18·routes + 0.20·target_share + 0.20·carry_share + 0.10·red_zone + 0.08·scheme_fit + 0.04·prospect + 0.02/depth_rank
  high_chance = active_prob × workload × (0.50·role_capture + 0.30·available_opportunity + 0.20·(role_growth+1)/2) × (1 − 0.25·uncertainty)
  flags: vacated_target_share > 0.08, vacated_carry_share > 0.12, carry_share > 0.35 = lead back, routes > 0.70 = every-down
  ```
- **bsr-0** [source-code]: same-position mid-season departure → `teammate_traded_boost = 0.05 × departures, cap 0.30` (multiplier).

### 3.5 Rookie draft-capital expectations

- First-round WRs, last five drafts (25 players, excl. Jameson Williams): **avg 62.1 rec on 100.5 targets, 799 yds, 5 TD**
  [search-snippet, Footballguys "Draft Capital Matters: Rookie WRs" 2026]. Over 2015–2022 the first-round WR average was closer
  to **65 targets** [search-snippet]. 2011–21 top-10-overall WRs who played ≥12 games: 9 of 10 had **90+ targets and ≥19% target
  share** [search-snippet, ESPN]. Only **15% (49/323)** of drafted WRs 2016–2025 finished top-48 as rookies [search-snippet].
  Draft-capital-to-volume examples: McMillan 122 targets, Egbuka 127 (52%/59% above the first-round average) but neither top-24 PPG
  [search-snippet].
- First-round RBs: **≈240 touches** in the rookie season (would rank ~20th–22nd at RB in each of 2022–25); "60% or more of the
  team's early-season carries" [search-snippet]; 14 first-round RBs in ten drafts, **71.4% top-24 as rookies vs 1.3% for 160 Day-3
  backs**; first-round RBs average 13.06 PPR PPG over first three seasons vs 8.59 for Day 2 (+34%) [search-snippet].
- **fantasy-forecast `rookies.py`** [source-code]: `rookie_ppg(pick) = max(floor, a + b·ln(pick))` fit per position on 2014+ classes
  with busts included as zeros; range ±45%.

### 3.6 Veterans changing teams

- WRs who changed teams: first-year drop **≈40 points per season (~2 PPG)**, >50 points after three seasons (Fantasy Footballers,
  "How do players perform after changing teams?") [search-snippet]. A 184-receiver sample of Keenan-Allen-level producers: **77%
  declined vs their prior three-year average, mean −3.89 PPG** [search-snippet, SI].
- Post-hype base rates (Yahoo 2026): hit rate "about a coin flip" for three of four positions; RBs over 26 with post-hype appeal
  beat cost only **9.1%** of the time; their opportunity stats dropped **2.6 percentage points** [search-snippet].

---

## 4. Schedule / strength of schedule

### 4.1 Year-over-year stability of fantasy points allowed (FPA)

| Study | Sample | Highest positional r | Other | Source |
|---|---|---|---|---|
| 4for4, "Do Defenses Repeat Fantasy Football Performances?" | 2014–2024 | **QB 0.26** | top-5 vs QB repeat **30%**, avg next-year finish DEF13 | [search-snippet] |
| Yahoo, "Do defenses repeat performances year-over-year?" | 2015–2025 | **0.27** | — | [search-snippet] |
| earlier study | 2010–2020 | QB **0.35** | top-5 vs QB repeat 33%; top-5 vs **TE repeat 20%**; TE lowest, **negative for bottom-five** | [search-snippet] |
| RotoWire, "Does Strength of Schedule Matter?" | 2010–2012 | — | interception rank YoY **r = 0.139** | [search-snippet] |

Spread is also small: 2025 QB "best schedule" = 19.6 FPA/g vs 18.8 at 16th (0.8 gap) vs 17.8 worst (1.8 total spread); RB
best-to-worst gap 2.7 FPA/g; "the gap ... was shrinking" (SI, "2025 NFL Schedule Release Will Be Mostly Useless") [search-snippet].
Example of noise: Eagles allowed 44.6 FP/g to WRs in 2023 and 31.0 in 2024 [search-snippet].

**Interpretation:** with r≈0.26 the expected next-year deviation is ~26% of last year's deviation; with a total positional spread of
~2 FP/g, the *expected* schedule effect between extreme teams is ≈0.5 FP/g before regression to the mean of the opponent set.

### 4.2 Methods analysts actually use

- **Sharp Football SOS:** opponent quality from **2026 Vegas win totals**, not last year's record [search-snippet].
- **4for4 aFPA:** rolling **10-week** FPA, adjusted for the quality of the offensive players faced (e.g., Dallas 11.6 raw FPA vs a QB
  set averaging 14.4; KC 14.3 raw vs QBs averaging 19.1 → KC ranked better) [search-snippet]. Weekly matchups use aFPA; a Playoff aFPA
  planner exists.
- **Playoff weeks 15–17:** ETR/Fantasy Life recommend it only as a **tiebreaker** between similarly ranked players, especially late
  picks and handcuffs; ETR's counterexample: the Patriots projected hardest 15–17 slate and scored 28/42/38 [search-snippet].
- **Early season:** PFF and Footballguys publish first-4/5-week RB tables to find "hot starts"; used as a tiebreaker for
  committee backs, no effect size published [search-snippet, secondary].
- **CBS "projected SOS"** projects defenses forward instead of using raw last-year FPA [search-snippet].

### 4.3 Code

- **fantasy-forecast** [source-code]: `factor(def, pos) = clip(FPA_factor, 0.90, 1.10)`; `matchup_season_mult = mean over the 17-week
  schedule`; `playoff_matchup_mult = mean over weeks 15–17`; `playoff_bye` flag; `DraftValue = VOR + 0.15·(playoff_score − pos avg)`
  (`playoff_tilt_lambda = 0.15`). Ablation: schedule ~neutral for season rank. DESIGN.md: "treat PlayoffScore as a tiebreaker/tilt."
- **jj-song/fantasy_draft_engine** [source-code]: `schedule_adjusted_vor = vor × (1 + 0.1·sos_rating)` (≤ ±10%); weekly matchup
  adjustment max 30% split 60% defense / 25% environment / 15% situational.
- **tailstail** [source-code]: opponent prior = EWM(8 weeks) of FP allowed to the position.
- **bsr-0** [source-code]: `sos_remaining_proxy = opponent win%`; `late_season_difficulty = sos × playoff_proximity` (uncertainty, not mean).

---

## 5. Offensive environment: Vegas totals, game script, offensive line

### 5.1 Implied totals and win totals

- Implied team total = `total/2 − spread/2` (favorite: `(total + |spread|)/2`) [search-snippet; identical formula in tailstail
  `_schedule_long` and fantasy-forecast `vegas.py` [source-code]].
- **ff-edge** `env_swing` [source-code]: **measured slope 45.3 season fantasy points per 1 point of implied team total**, applied as
  `45.3 × (team_implied − 22.0) × (player_expected_points / 947)`; the author labels it "an upper bound, not a correction to
  subtract" because ADP already prices part of it. FanDuel season-long markets exist for ~92 players (`vegas_gap`).
- **fantasy-forecast** [source-code]: `offense_mult = clip(implied_ppg / league_mean, 0.85, 1.15)`; when only win totals exist,
  `ppg ≈ 22.5 + 0.6 × (win_total − mean)` (`win_total_to_ppg_slope = 0.6`). Ablation: Vegas offense multiplier "~neutral for
  season-long rank"; kept "for precision and situation-changers."
- **nfl-player-value-analysis** [source-code]: at the *weekly* level, implied total + recent pass rate gave ~0 skill for team pass
  attempts.
- Win-total splits (PFF "Metrics that Matter: Vegas win totals"; Fantasy Points "Vegas and 2022 Gamescript Dependency")
  [search-snippet]: **RB 26.2 FPG on winning teams vs 20.6 on losing teams** (Fantasy Points five-year version: 26.7 vs 20.8);
  **QB 18.5 vs 14.2**; WR/TE splits "nearly identical to QBs"; RBs score a higher share of points when leading, QB/WR/TE when trailing.
- Game script (Fantasy Points "How Game Script Affects Fantasy"; PFF) [search-snippet]: league pass rate **≈50% leading / 56% tied /
  66% trailing** (other cuts: 49–51% leading, 66% trailing); teams trailed on 44% of plays but produced 51% of QB scoring; led on 33%
  of plays but 30% of QB scoring. Extreme: Rams 78% pass rate trailing by a FG, 83% by a TD+; Ravens +13.7 points more pass-heavy when
  trailing. Caveat: WRs on 7+ point underdogs get 66.5% of team yardage vs 66.0% on favorites — "the size of the pie is small enough
  to offset these gains" [search-snippet].
- Year-to-year r² of player fantasy PPG = **0.59** (all flex players since 2011; Fantasy Footballers "Players Who POP") [search-snippet]
  — the baseline any situation layer must not degrade.
- Draft Sharks "Fantasy Environment Score" combines Vegas-based metrics into one rating; components/weights not retrievable
  [secondary].

### 5.2 Offensive line → RB

- Adjusted Line Yards explain **28.9% of RB half-PPR production** (r ≈ 0.54); pass-block grade vs QB fantasy r = 0.15 (Draft Sharks,
  "The Impact of Offensive Line Play on Fantasy Production") [search-snippet].
- PFF: team run-blocking grade r = **0.50** with yards per attempt; team rushing grade r = 0.77 [search-snippet].
- Contrary findings: O-line effectiveness vs RB fantasy success r = **0.25** (Fantasy Footballers); team stuff rate vs RB PPR PPG
  **r = −0.08, p = 0.25, n = 205 RB-seasons 2023–25** [search-snippet]; "0.314 correlation between adjusted line yards and RB rushing
  production ... the strongest of any pair" (PFF) [search-snippet].
- Consensus wording: "Volume is king, then RB talent, then run blocking" [search-snippet].

### 5.3 Code for an environment score

- **kaedonj16** `calculate_team_environment_score` [source-code] (0–100): `volume = norm(plays_pg, 55–70)×20`;
  `scoring = norm(pts_pg, 16–30)×12 + norm(TD_pg, 1.6–3.8)×8`; `efficiency = norm(yds/play, 4.7–6.4)×10 + (1−norm(sacks_pg, 1–4))×5`;
  `red_zone = norm(RZ_trips_pg, 2.0–4.5)×15`; position fit (WR/TE: pass rate 0.48–0.67 ×10, pass yds 180–310 ×6, pass TD 1.1–2.4 ×4;
  RB: run rate 0.33–0.52 ×8, rush att 20–33 ×7, rush TD 0.5–1.8 ×5); league defaults 33.5 pass att, 25.5 rush att, 22.5 pts, 3.2 RZ
  trips, 2.4 sacks/g. **Backtest r ≈ −0.05 → weight zeroed.** Useful as a normalization recipe, not as evidence it helps.

---

## 6. Teammate availability, target competition, breakout base rates

- **Target share stability:** year-over-year r ≈ **0.70**; target share, WOPR and air-yards share each exceed 0.70 both for
  self-correlation and for next-year fantasy points (Sharp Football "WR stats that matter"; Fantasy Classroom; SumerSports)
  [search-snippet].
- **Alpha definition (2026 articles):** ≥25% target share, ≥15 PPR PPG, ≥12 games. Count of alphas **10 (2023) → 8 (2024) → 6 (2025)**;
  WRs with ≥20% target share **38 (2024) → 28 (2025)**; every league target leader had ≥32% share; JSN 36% share / 49% air-yards
  share in 2025 [search-snippet].
- **Same-team WR–WR season correlation ≈ −0.02** (RotoWire stacking study, four years) — offense boost cancelled by target
  competition [search-snippet].
- **Breakout base rates:** RotoViz (breakout = first 200-PPR-point season): **Year 2 ≈15%, Year 1 ≈12%, Year 3 ≈10%, all other
  years <5%**; since 2010, 26 Year-2 breakouts, more than any other class; thresholds ≥100 FP as a rookie and rookie age 21
  [search-snippet]. FF Dataroma 2026 (breakout = beat positional ADP by 60%, non-rookie, <28): **median target-share gain +4.8 points,
  median +2 TD, ~half +3 TD** [search-snippet]. NFL EdgeLine: "73% of second-year breakouts coincide with increased opportunity"
  [secondary; sample undefined].
- **Injury base rates for a risk term:** top-24 ADP RBs miss **2.4 games**, WRs **2.2** on average; a top-30 RB misses 0.86 more games
  than a top-30 WR over a three-year study; only **46%** of RBs finish "healthy" (0–1 games missed) [search-snippet].
- **WR1-out redistribution:** no systematic study found in accessible sources; only anecdotes (e.g., Michael Wilson 18 targets / 32%
  share with MHJ out) [secondary]. Code handles it structurally: tailstail's `wr1_out`/`rb1_out`/`te1_out` flags and vacated share
  = Σ EWM4 share of inactive teammates, with conditional priors shrunk by 8 pseudo-games; sidhulyalkar weights
  `teammate_absence_probability` at 0.20 of available opportunity [source-code].
- **kaedonj16** readiness prior [source-code]: Year 2 = 30, Year 3 = 25, Years 3–4 = 20, rookie = 15, veteran (5+ yrs) = 5, veteran
  age threshold 27 — consistent with the RotoViz base rates.
- **ff-edge** [source-code]: a per-position breakout model "does not beat draft price alone" out of sample — a warning that
  hand-built breakout scores rarely add to ADP.

---

## 7. Open-source implementations (URLs + exact formulas)

| Repo | What it implements | Exact formula / parameters |
|---|---|---|
| https://github.com/bhargavap21/fantasy-forecast | Top-down pillars, Vegas offense mult, QB fit, schedule + playoff tilt, rookie curve, share/volume shrinkage | `weekly_base = fp_pg_base × offense_mult × qb_fit_mult × age_mult × pos_calib`; `season = weekly_base × matchup_season_mult × availability × 17`; `offense_mult = clip(implied_ppg/league_mean, .85, 1.15)`; `qb_fit = clip(1 + .06·z(deep_rate)·z(aDOT), .9, 1.1)`; matchup band .9–1.1; `DraftValue = VOR + .15·(playoff − posavg)`; `team_volume_shrink_games 15`, `share_shrink_games 3`, `efficiency_shrink_opps 10`; `rookie_ppg = a + b·ln(pick)`; age curve 23:1.08, 25:1.04, 27:1.00, 28:.98, 30:.96 |
| https://github.com/kylelevesque12/nfl-player-value-analysis | Structured two-stage weekly (attempts × share × PPR/target), renormalized shares | Stage skills vs mean: share +34%, attempts −3%, PPR/target −0.2%; pooled HGB beats two-stage 7–10% |
| https://github.com/kaedonj16/fantasy-dashboard | Breakout engine: vacated split, competition added/removed, team environment, OC/QB change | `share_i = claim_i^1.6/Σclaim^1.6`; rookie claims WR {5,3.5,2.5,1.5}, RB {14,9,6,4}; OC thresholds .58/.44, WR ±8/−6, RB +8/−4; QB upgrade +10 / downgrade −14; HC uncertainty −3; component weights (offseason) trajectory .30, confidence .33, readiness .20, opp_opened .10, comp_added .07, env 0, comp_removed 0 |
| https://github.com/sidhulyalkar/nfl-player-state-engine | Opportunity ranking incl. vacated shares, teammate absence, uncertainty discount | `avail = .35·vac_tgt + .35·vac_carry + .20·teammate_absence + .10·promotion`; `score = active×workload×(.5·capture + .3·avail + .2·growth)×(1 − .25·uncertainty)` |
| https://github.com/zjserapin/ff-edge | Stability gates, env swing from implied total, neutral-script shares, rookie model | `env_swing = 45.3 × (implied − 22.0) × (xPts/947)`; neutral share restricted to WP 0.2–0.8; rookie model OOS r .592 |
| https://github.com/curtisdearing/tailstail | Coach priors that follow the coach, reconciled shares, implied points, WR1-out flags | `pre_coach_{pass_rate,pace,rb/wr/te_target_share,qb_rush_share}_ewm8`; `implied = total/2 − spread/2`; reconciled share = share/max(Σshare,1); condition prior shrink 8 games |
| https://github.com/bsr-0/nfl-player-projections | Coaching-change detector with position deltas and decay | HC {QB −1.2, RB +.3, WR −.8, TE −.2}; OC {QB −1.8, RB −.5, WR −1.5, TE −.6} PPG × `exp(−.693·weeks/half_life)`, 6-week window; departure boost .05/departure cap .30 |
| https://github.com/jj-song/fantasy_draft_engine | SOS-adjusted VOR, weekly matchup grade | `sched_vor = vor × (1 + .1·sos_rating)`; weekly max 30% split 60/25/15; new staff −0.1 grade |
| https://github.com/nick-holt/sfb15_projections | Manual in-season multipliers | coaching_change ×1.12–1.15 (ad hoc) |

Not useful: Grizzly27/fantasy-football-ml draws SOS uniformly in 0.7–1.3 (synthetic).

---

## Recommended situation layer (formulas)

Notation: `L` = league mean; `z(·)` = standardized within season; all multipliers clipped; `base` = consensus-rank-implied PPG.
Every term below returns a mean multiplier `m`, an uncertainty increment `u` (in PPG-variance units), or both. Weights are set so
the *sum of mean effects rarely exceeds ±10%* — consistent with the ablations above showing environment terms are near-neutral.

### (a) Team offensive-environment score `E_t`
```
implied_ppg_t   = mean over posted games of (total/2 − spread/2)      # fallback: 22.5 + 0.6·(win_total − L_win)
pace_t          = 0.5·prior_pace_t + 0.5·L_pace           if play-caller returns   (r≈.45–.57)
                = 0.25·prior_pace_t + 0.75·[coach_hist_pace or L_pace]  if new play-caller  (r≈.23)
proe_t          = 0.5·coach_hist_proe (regressed to 0 by seasons of history: n/(n+2)) + 0.5·prior_team_proe·[same caller ? 1 : 0.4]
pass_att_t      = pace_t × (L_pass_rate + proe_t) ; rush_att_t = pace_t − pass_att_t
E_t             = clip(implied_ppg_t / L_ppg, 0.85, 1.15)             # scoring environment (fantasy-forecast band)
volume_mult_pos = clip(pass_att_t / L_pass_att, .9, 1.1) for WR/TE/QB ; clip(rush_att_t / L_rush_att, .9, 1.1) for RB
```
Use `E_t` for TD-rate/efficiency and `volume_mult_pos` for attempts; do not apply both to the same quantity (double count).
Interpretation anchor: 1 point of implied total ≈ 45 season points spread across the offense (ff-edge), i.e. ≈ +2.7 PPG per point
for a player who is 100% of the offense, so a 25% share player gains ≈ +0.7 PPG per implied point.

### (b) Per-player opportunity-change score `O_p`
```
vac_share_pos   = Σ (share of departed players at the position group) / Σ team shares      # adjusted for arrivals:
adj_vac         = vac_share_pos − Σ_arrivals expected_share(arrival)
expected_share(arrival) = median last-year share (vets) or draft prior (rookies):
    WR/TE targets/g {R1 5.0, R2 3.5, R3 2.5, R4 1.5, R5–7 1.0}; RB touches/g {R1 14, R2 9, R3 6, R4 4, R5–7 2}
    (equivalently: first-round WR ≈ 100 targets ≈ 18–19% share; first-round RB ≈ 240 touches ≈ 60% early carries)
claim_p         = prior per-game usage (RB: carries + 1.5·targets), or draft prior if none
share_of_vac_p  = claim_p^1.6 / Σ_room claim^1.6
Δshare_p        = adj_vac × share_of_vac_p  − Σ_new_arrivals threat_j × stack_j × share_p     (stack weights 1, .75, .55, .35)
normalize: after all Δ, rescale the room so Σ shares = 1.0 (this step is what made redistribution fail in fantasy-forecast)
O_p (mean)      = clip(1 + 0.5·Δshare_p / share_p, 0.85, 1.15)    # only 50% credited: R²<.01 for vacated volume vs PPG growth
O_p (risk)      = u_opp = |Δshare_p| / share_p × σ_base            # the other 50% goes to variance, not mean
role_change     = +1 flag if Δshare_p/share_p > +0.15 or a documented depth-chart promotion; use as a gate for boom score
```

### (c) QB-change adjustment for pass catchers `Q_p`
```
tq_new  = 0.3·(new QB prior catchable rate or xFP/target) + 0.7·L      # r≈.29 → shrink 70%
tq_old  = 0.3·(old QB prior) + 0.7·L
Q_p     = clip( (tq_new/tq_old)^1.0 , 0.90, 1.10 )   for WR/TE ; 0.5 exponent for RB receiving; 1.0 for QB-dependent TDs
asymmetry: if downgrade, multiply the shortfall by 1.4 (kaedonj16 −14 vs +10); if unknown starter, Q_p = 1 and add u_qb = 0.5 PPG
boom flag: new full-time QB present → +1 (27 of 41 late-ADP WR1 seasons had one)
```

### (d) Coaching-change adjustment with uncertainty `C_p`
```
if same play-caller:            C_p = 1 ; u_coach = 0
if new OC, HC retained:         C_p = 1 + δ_pos_OC·adapt ; u_coach = 0.6 PPG
if new HC + new play-caller:    C_p = 1 + (δ_pos_HC + δ_pos_OC)·adapt ; u_coach = 0.9 PPG
δ_pos (early-season mean, in PPG/base): QB −0.08, WR −0.06, TE −0.03, RB −0.02 for the first ~6 weeks, decaying
      exp(−0.693·week/6) — these are the bsr-0 shape scaled to base ≈ 15–20 PPG; treat the magnitude as a prior, not data
position-usage tilt (the part that IS backed by coach history):
      RB_target_share_p ← 0.5·coach_hist_rb_share + 0.5·team_prior  (range, not point: e.g. McCarthy 11–18%, mean 15% vs L 19%)
      TE_target_share_p ← same with coach_hist_te_share
      apply as a share multiplier before (b) so normalization to 1.0 handles the offsets
pace/pass-rate part flows through (a); do not add it again here
```

### (e) Schedule adjustment `S_p` (small weight by design)
```
def_factor(d, pos)  = clip( 1 + 0.26·(FPA_{d,pos,last} − L)/L , 0.94, 1.06 )   # 0.26 = YoY r; shrink 74% to mean
                      (optionally blend 50/50 with an opponent-quality proxy from 2026 Vegas win totals, per Sharp)
S_full   = mean_{weeks 1–17} def_factor ; S_early = mean_{1–4} ; S_playoff = mean_{15–17}
mean use:  multiply projection by S_full^0.5  (i.e. half of an already tiny effect; expected best-vs-worst ≈ ±2–3%)
tiebreak:  rank-order ties by S_playoff (weight 0.15 of playoff-week score, per fantasy-forecast) and, for RB committees, S_early
never:     let S move a player more than one rank tier; bye in weeks 15–17 → flag, not points
```

### (f) Folding (a)–(e) into projection, boom, bust and risk
```
proj_p   = base_p × E_t^{w_E,pos} × volume_mult_pos × O_p × Q_p × C_p × S_full^0.5
           with w_E = {RB 0.5, WR 0.4, TE 0.4, QB 0.6} (RBs score more when winning; WR/TE partially offset by trailing pass rate)
           and the product hard-clipped to [0.85, 1.15] × base_p          # ablations: environment terms ≈ neutral for rank

σ_p²     = σ_base² (from the r²≈0.59 YoY baseline: σ_base ≈ 0.64·SD of positional PPG)
           + u_opp² + u_qb² + u_coach² + u_avail²
u_avail  = games-missed prior: RB 2.4 / WR 2.2 games for top-24 ADP; per-game σ from availability × PPG

boom_p   = P(proj > tier-up threshold) = 1 − Φ((thr_up − proj_p)/σ_p), plus additive base-rate priors:
           +0.15 if Year-2 WR, +0.10 if Year-3, +0.12 if rookie R1 (breakout rates: Y2 ≈15%, Y1 ≈12%, Y3 ≈10%, else <5%)
           +0.10 if role_change flag, +0.08 if new full-time QB (WR/TE), −0.05 if ≥2 new same-room competitors
bust_p   = Φ((thr_down − proj_p)/σ_p) with extra +0.10 if WR changed teams (77% decline, −3.9 PPG among producers; ~−2 PPG avg),
           +0.10 if RB > 26 in a post-hype slot (9.1% hit rate), +0.05 if new play-caller and player relied on screens/scheme yards
risk_p   = σ_p / proj_p (coefficient of variation), reported alongside the share of σ_p² that comes from u_coach + u_opp + u_qb
           so the user can see "situational" vs "baseline" risk
```
Sanity rules drawn from the evidence: (1) never let (a)–(e) together move a mean by more than ±15%; (2) put the larger half of every
situational effect into σ, not the mean; (3) shares must be renormalized to 1.0 per team before any player-level multiplier; (4) if a
term does not improve a held-out rank correlation over the consensus baseline, set its mean weight to 0 and keep only its variance
contribution (this is what kaedonj16 and fantasy-forecast ended up doing).

---

## Gaps / claims that are assertion-only
- No published regression of coaching change → fantasy points; all coordinator effects are per-coach histories.
- No "WR with top-10 QB averages X PPG more" study located; QB effect quantified only via catchable-rate instability (r≈0.29), the
  Higgins 58%→78% split, and the 27/41 new-QB base rate.
- No systematic WR1-out target-redistribution study located.
- "Coaching changes improve performance by 23%" (NFL EdgeLine) and Draft Sharks' Fantasy Environment Score weights are unverified.
- bsr-0's position PPG deltas cite a "2010–2024 analysis" that is not in the repo.
