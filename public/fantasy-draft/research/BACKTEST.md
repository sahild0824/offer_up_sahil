# Backtest of the draft model's signals, 2016-2025

Generated 2026-09-05. 1599 player-seasons with a preseason FantasyPros ADP inside the top 180 (QB 218, RB 552, WR 628, TE 201); 760 of them (2020-2025) also carry a preseason expert consensus with spread, best and worst. Outcomes are positional finishes by total PPR points from nflverse game logs. Definitions are in the script header.

## 1. How predictive are ADP and the expert consensus?

Spearman rank correlation between the preseason number and the actual positional finish (higher is better), drafted players only.

| position | ADP → finish (2016-25) | ADP → finish (2020-25) | ECR → finish (2020-25) | 50/50 blend (2020-25) | n (2020-25) |
|---|---|---|---|---|---|
| QB | 0.324 | 0.386 | 0.406 | 0.398 | 109 |
| RB | 0.531 | 0.598 | 0.602 | 0.601 | 255 |
| WR | 0.523 | 0.526 | 0.529 | 0.532 | 301 |
| TE | 0.399 | 0.353 | 0.305 | 0.333 | 95 |
| all | 0.391 | 0.423 | 0.398 | 0.414 | 760 |

By season (all positions, ECR years):

| season | ADP | ECR | blend | n |
|---|---|---|---|---|
| 2021 | 0.364 | 0.338 | 0.350 | 151 |
| 2022 | 0.483 | 0.426 | 0.460 | 151 |
| 2023 | 0.439 | 0.375 | 0.415 | 151 |
| 2024 | 0.415 | 0.416 | 0.420 | 151 |
| 2025 | 0.406 | 0.428 | 0.423 | 156 |

Does the gap between ADP and ECR carry information? Players the market takes later than the experts rank them (value) vs earlier (reach), 2020-25:

| group | n | hit rate | beat-ADP rate | bust rate |
|---|---|---|---|---|
| value ≥ 10 picks | 170 | 0.31 | 0.48 | 0.44 |
| within ±10 | 457 | 0.47 | 0.37 | 0.42 |
| reach ≥ 10 picks | 133 | 0.40 | 0.41 | 0.47 |

## 2. Hit, boom and bust rates by ADP round and position (12-team rounds, 2016-25)

| round | pos | n | hit (starter line) | boom | bust | avg games |
|---|---|---|---|---|---|---|
| 1 | RB | 69 | 0.78 | 0.38 | 0.23 | 13.3 |
| 1 | WR | 50 | 0.80 | 0.42 | 0.22 | 14.5 |
| 2 | QB | 12 | 0.83 | 0.42 | 0.17 | 14.9 |
| 2 | RB | 48 | 0.77 | 0.19 | 0.25 | 13.9 |
| 2 | WR | 46 | 0.57 | 0.24 | 0.43 | 13.7 |
| 2 | TE | 9 | 0.78 | 0.44 | 0.22 | 13.3 |
| 3 | QB | 13 | 0.69 | 0.23 | 0.31 | 14.3 |
| 3 | RB | 41 | 0.68 | 0.22 | 0.32 | 13.4 |
| 3 | WR | 56 | 0.64 | 0.14 | 0.36 | 14.1 |
| 3 | TE | 12 | 0.83 | 0.42 | 0.17 | 14.2 |
| 4 | QB | 12 | 0.50 | 0.17 | 0.50 | 14.8 |
| 4 | RB | 40 | 0.57 | 0.23 | 0.42 | 13.2 |
| 4 | WR | 55 | 0.49 | 0.25 | 0.49 | 13.3 |
| 4 | TE | 11 | 0.64 | 0.27 | 0.36 | 13.4 |
| 5 | QB | 19 | 0.68 | 0.16 | 0.32 | 14.6 |
| 5 | RB | 33 | 0.39 | 0.24 | 0.48 | 13.5 |
| 5 | WR | 43 | 0.47 | 0.33 | 0.51 | 14.4 |
| 5 | TE | 17 | 0.53 | 0.24 | 0.47 | 13.1 |
| 6 | QB | 16 | 0.69 | 0.31 | 0.31 | 15.2 |
| 6 | RB | 39 | 0.38 | 0.28 | 0.44 | 12.9 |
| 6 | WR | 52 | 0.35 | 0.29 | 0.56 | 12.2 |
| 6 | TE | 13 | 0.46 | 0.15 | 0.54 | 14.3 |
| 7 | QB | 15 | 0.27 | 0.07 | 0.73 | 12.7 |
| 7 | RB | 31 | 0.29 | 0.26 | 0.52 | 12.4 |
| 7 | WR | 44 | 0.14 | 0.14 | 0.59 | 12.8 |
| 7 | TE | 20 | 0.45 | 0.15 | 0.55 | 13.8 |
| 8 | QB | 16 | 0.50 | 0.31 | 0.44 | 13.1 |
| 8 | RB | 34 | 0.26 | 0.26 | 0.47 | 12.8 |
| 8 | WR | 46 | 0.20 | 0.20 | 0.52 | 13.2 |
| 8 | TE | 12 | 0.25 | 0.17 | 0.67 | 11.8 |
| 9 | QB | 17 | 0.47 | 0.41 | 0.53 | 11.2 |
| 9 | RB | 37 | 0.19 | 0.19 | 0.62 | 11.6 |
| 9 | WR | 40 | 0.23 | 0.23 | 0.38 | 14.2 |
| 9 | TE | 8 | 0.50 | 0.25 | 0.50 | 13.4 |
| 10 | QB | 21 | 0.57 | 0.43 | 0.43 | 13.2 |
| 10 | RB | 33 | 0.36 | 0.36 | 0.33 | 13.2 |
| 10 | WR | 38 | 0.18 | 0.18 | 0.68 | 12.3 |
| 10 | TE | 14 | 0.50 | 0.07 | 0.43 | 12.6 |
| 11 | QB | 16 | 0.56 | 0.56 | 0.31 | 15.6 |
| 11 | RB | 26 | 0.19 | 0.19 | 0.54 | 12.9 |
| 11 | WR | 28 | 0.18 | 0.18 | 0.57 | 12.5 |
| 11 | TE | 14 | 0.43 | 0.36 | 0.50 | 14.8 |
| 12 | QB | 16 | 0.12 | 0.12 | 0.44 | 14.8 |
| 12 | RB | 32 | 0.09 | 0.09 | 0.56 | 11.8 |
| 12 | WR | 33 | 0.24 | 0.24 | 0.52 | 13.2 |
| 12 | TE | 17 | 0.53 | 0.53 | 0.35 | 13.8 |
| 13 | QB | 15 | 0.33 | 0.33 | 0.40 | 12.5 |
| 13 | RB | 31 | 0.06 | 0.06 | 0.42 | 12.7 |
| 13 | WR | 35 | 0.06 | 0.06 | 0.54 | 12.1 |
| 13 | TE | 16 | 0.19 | 0.19 | 0.50 | 12.9 |
| 14 | QB | 19 | 0.32 | 0.32 | 0.37 | 13.1 |
| 14 | RB | 23 | 0.13 | 0.13 | 0.61 | 12.4 |
| 14 | WR | 36 | 0.08 | 0.08 | 0.50 | 11.1 |
| 14 | TE | 19 | 0.26 | 0.26 | 0.47 | 13.1 |
| 15 | QB | 11 | 0.09 | 0.09 | 0.27 | 14.0 |
| 15 | RB | 35 | 0.06 | 0.06 | 0.51 | 11.6 |
| 15 | WR | 26 | 0.08 | 0.08 | 0.58 | 12.8 |
| 15 | TE | 16 | 0.19 | 0.19 | 0.62 | 11.8 |

## 3. Does each signal move the boom or bust rate? (within position, ADP top 120)

Each row compares a slice against the rest of its position after controlling for ADP band (rounds 1-3, 4-6, 7-10). Lift is the slice's rate minus the matched base rate, in percentage points.

| signal | pos | n | boom lift | bust lift | boom rate | bust rate |
|---|---|---|---|---|---|---|
| age ≥ 29 | QB | 56 | +0.8 | -1.2 | 0.29 | 0.43 |
| age ≥ 29 | RB | 44 | -8.2 | +7.8 | 0.18 | 0.50 |
| age ≥ 29 | WR | 101 | -2.7 | +5.3 | 0.22 | 0.52 |
| age ≥ 29 | TE | 37 | +0.5 | +4.1 | 0.24 | 0.49 |
| age 27-28 | RB | 61 | -1.9 | +4.3 | 0.25 | 0.43 |
| age 27-28 | WR | 86 | -0.0 | -6.6 | 0.24 | 0.40 |
| age 27-28 | TE | 29 | +0.9 | -0.2 | 0.28 | 0.41 |
| age ≤ 24 | QB | 32 | +0.8 | -6.6 | 0.28 | 0.34 |
| age ≤ 24 | RB | 188 | +3.7 | -3.1 | 0.30 | 0.36 |
| age ≤ 24 | WR | 165 | +1.7 | -0.5 | 0.25 | 0.47 |
| age ≤ 24 | TE | 27 | -3.2 | +1.3 | 0.19 | 0.48 |
| year 2 (second season) | RB | 65 | +10.2 | -4.8 | 0.37 | 0.34 |
| year 2 (second season) | WR | 60 | -1.6 | +3.6 | 0.22 | 0.53 |
| year 3 | RB | 74 | -2.4 | -2.0 | 0.24 | 0.35 |
| year 3 | WR | 63 | +3.6 | +2.9 | 0.29 | 0.48 |
| rookie | RB | 44 | -1.6 | -2.9 | 0.25 | 0.39 |
| rookie | WR | 25 | +16.4 | -17.4 | 0.36 | 0.36 |
| changed teams | RB | 59 | -4.3 | +8.1 | 0.22 | 0.53 |
| changed teams | WR | 68 | -5.6 | +6.9 | 0.18 | 0.57 |
| prior-year boom-week rate ≥ 35% | RB | 42 | +10.4 | +0.6 | 0.38 | 0.29 |
| prior-year boom-week rate ≤ 10% | QB | 44 | +2.6 | -1.7 | 0.32 | 0.45 |
| prior-year boom-week rate ≤ 10% | RB | 143 | +1.7 | -0.6 | 0.28 | 0.43 |
| prior-year boom-week rate ≤ 10% | WR | 196 | -2.6 | +0.3 | 0.20 | 0.51 |
| prior-year boom-week rate ≤ 10% | TE | 37 | -6.7 | +16.2 | 0.11 | 0.68 |
| prior-year bust-week rate ≥ 30% | QB | 42 | +9.4 | +0.7 | 0.38 | 0.48 |
| prior-year bust-week rate ≥ 30% | RB | 91 | +3.4 | -0.3 | 0.30 | 0.45 |
| prior-year bust-week rate ≥ 30% | WR | 119 | -4.8 | +4.8 | 0.18 | 0.56 |
| prior-year bust-week rate ≥ 30% | TE | 67 | +2.6 | +0.3 | 0.22 | 0.49 |
| missed ≥ 4 games prior year | RB | 119 | +3.7 | +0.9 | 0.30 | 0.40 |
| missed ≥ 4 games prior year | WR | 112 | -4.0 | +3.4 | 0.19 | 0.53 |
| missed ≥ 4 games prior year | TE | 29 | -14.1 | +21.4 | 0.07 | 0.69 |
| played all 17 prior year | QB | 25 | -4.7 | +10.7 | 0.24 | 0.48 |
| played all 17 prior year | RB | 46 | -0.8 | +7.0 | 0.26 | 0.43 |
| played all 17 prior year | WR | 62 | +4.0 | -5.6 | 0.29 | 0.39 |
| prior-year weekly CV ≥ 0.65 (volatile) | RB | 80 | +2.3 | -3.1 | 0.29 | 0.40 |
| prior-year weekly CV ≥ 0.65 (volatile) | WR | 94 | +1.7 | -4.2 | 0.24 | 0.46 |
| prior-year weekly CV ≥ 0.65 (volatile) | TE | 27 | -2.2 | -3.5 | 0.19 | 0.44 |
| prior-year top-6 finish | QB | 53 | -6.4 | +4.6 | 0.21 | 0.40 |
| prior-year top-6 finish | RB | 60 | -4.3 | +4.0 | 0.23 | 0.32 |
| prior-year top-6 finish | WR | 60 | +10.2 | +0.2 | 0.37 | 0.35 |
| prior-year top-6 finish | TE | 55 | +6.3 | -6.9 | 0.36 | 0.31 |
| Vegas win total ≥ 10 | QB | 61 | +2.4 | +0.8 | 0.31 | 0.38 |
| Vegas win total ≥ 10 | RB | 100 | +6.3 | +1.2 | 0.33 | 0.40 |
| Vegas win total ≥ 10 | WR | 127 | +1.4 | -3.7 | 0.26 | 0.43 |
| Vegas win total ≥ 10 | TE | 45 | -2.2 | -5.8 | 0.27 | 0.33 |
| Vegas win total ≤ 6.5 | RB | 75 | -7.9 | -2.0 | 0.19 | 0.39 |
| Vegas win total ≤ 6.5 | WR | 69 | +1.7 | -4.5 | 0.25 | 0.46 |
| incumbent on team that vacated ≥ 35% | RB | 66 | +3.8 | -1.8 | 0.30 | 0.38 |
| incumbent on team that vacated ≥ 35% | WR | 67 | +1.8 | +2.7 | 0.25 | 0.51 |
| arrival/rookie on team that vacated ≥ 35% | RB | 59 | +0.7 | -1.0 | 0.27 | 0.42 |
| arrival/rookie on team that vacated ≥ 35% | WR | 44 | -5.1 | +8.0 | 0.18 | 0.59 |
| expert spread in top quartile (2020+) | RB | 50 | -2.7 | +5.5 | 0.24 | 0.44 |
| expert spread in top quartile (2020+) | WR | 59 | -0.3 | +7.4 | 0.24 | 0.54 |
| expert spread in bottom quartile (2020+) | RB | 49 | +1.9 | -16.1 | 0.29 | 0.22 |
| expert spread in bottom quartile (2020+) | WR | 58 | +5.3 | -17.5 | 0.29 | 0.29 |
| most bullish expert ≥ 30% above consensus (2020+) | QB | 47 | +5.0 | +1.0 | 0.32 | 0.40 |
| most bullish expert ≥ 30% above consensus (2020+) | RB | 186 | +1.8 | -3.9 | 0.28 | 0.34 |
| most bullish expert ≥ 30% above consensus (2020+) | WR | 219 | +0.7 | -2.4 | 0.25 | 0.45 |
| most bullish expert ≥ 30% above consensus (2020+) | TE | 50 | -1.1 | +0.7 | 0.22 | 0.46 |
| most bearish expert ≥ 30% below consensus (2020+) | QB | 61 | +1.6 | +4.3 | 0.30 | 0.43 |
| most bearish expert ≥ 30% below consensus (2020+) | RB | 193 | +0.8 | -3.8 | 0.27 | 0.35 |
| most bearish expert ≥ 30% below consensus (2020+) | WR | 230 | +1.7 | -3.1 | 0.26 | 0.44 |
| most bearish expert ≥ 30% below consensus (2020+) | TE | 51 | -3.1 | +3.4 | 0.22 | 0.47 |
| ADP ≥ 8 picks later than ECR (2020+) | WR | 65 | +11.7 | -11.4 | 0.34 | 0.42 |
| ADP ≥ 8 picks earlier than ECR (2020+) | QB | 33 | +3.7 | +2.8 | 0.30 | 0.39 |
| ADP ≥ 8 picks earlier than ECR (2020+) | RB | 49 | +0.1 | +0.6 | 0.27 | 0.41 |
| ADP ≥ 8 picks earlier than ECR (2020+) | TE | 26 | +6.3 | -5.7 | 0.27 | 0.42 |

## 4. Specific claims the model leans on

- **Receivers who change teams.** PPG change vs prior year: moved -2.15 (n=62, 69% declined) vs stayed -0.90 (n=350, 62% declined).
- **RB age ≤ 25.** PPG change +0.05, hit rate 0.56, bust rate 0.35 (n=188).
- **RB age 26.** PPG change -1.62, hit rate 0.54, bust rate 0.35 (n=48).
- **RB age 27.** PPG change -1.67, hit rate 0.61, bust rate 0.32 (n=31).
- **RB age 28.** PPG change -3.28, hit rate 0.38, bust rate 0.54 (n=26).
- **RB age ≥ 29.** PPG change -3.47, hit rate 0.35, bust rate 0.46 (n=37).
- **Prior-year top-3 RBs** (n=30): repeated a top-3 finish 23% of the time, finished top-12 47%, PPG change -4.48.
- **Breakouts by experience (WR, boom as defined).** Year 2: 0.22 (n=60), year 3: 0.29 (n=63), 5th season or later: 0.25 (n=251).
- **Vacated targets vs incumbent growth (WR/TE).** Spearman between the team's vacated target share and the incumbent's PPG change: 0.033 (n=462).
- **Expert disagreement as a variance signal (2020-25, top 120).** Spearman between expert spread and |finish − ECR positional rank|: 0.239; between spread and bust: 0.183; between spread and boom: -0.059.
- **Vegas win total.** Spearman with total PPR points for drafted players: 0.130 (n=1123); with finish rank residual after ADP (finish − ADP positional rank): 0.009.
- **Prior-year boom-week rate.** Spearman with boom: 0.069; prior bust-week rate with bust: 0.108; prior games missed with bust: 0.076.

## 5. Fitted boom and bust models, walk-forward

Logistic regression (L2, standardized inputs) trained on 2016-2023 and scored on 2024-2025 held out. Baseline = ADP positional rank alone. AUC 0.5 is coin-flip.

| target | position | features | train n | test n | AUC ADP-only | AUC model | top-decile rate | base rate |
|---|---|---|---|---|---|---|---|---|
| boom | RB | ADP + history | 328 | 77 | 0.646 | 0.561 | 0.88 | 0.27 |
| boom | RB | + expert spread (2020+) | 161 | 77 | 0.646 | 0.479 | 0.25 | 0.27 |
| boom | WR | ADP + history | 373 | 96 | 0.471 | 0.520 | 0.40 | 0.29 |
| boom | WR | + expert spread (2020+) | 187 | 96 | 0.471 | 0.522 | 0.30 | 0.29 |
| boom | ALL | ADP + history | 901 | 226 | 0.536 | 0.541 | 0.35 | 0.28 |
| boom | ALL | + expert spread (2020+) | 446 | 226 | 0.536 | 0.503 | 0.39 | 0.28 |
| bust | RB | ADP + history | 328 | 77 | 0.698 | 0.641 | 0.88 | 0.34 |
| bust | RB | + expert spread (2020+) | 161 | 77 | 0.698 | 0.656 | 0.88 | 0.34 |
| bust | WR | ADP + history | 373 | 96 | 0.539 | 0.563 | 0.60 | 0.44 |
| bust | WR | + expert spread (2020+) | 187 | 96 | 0.539 | 0.549 | 0.50 | 0.44 |
| bust | ALL | ADP + history | 901 | 226 | 0.585 | 0.589 | 0.52 | 0.41 |
| bust | ALL | + expert spread (2020+) | 446 | 226 | 0.585 | 0.594 | 0.48 | 0.41 |

Standardized coefficients (sign and size tell you what the fit actually uses), ALL positions, 2016-2023 training:

- **boom, ADP + history:** prior_boom +0.20, vegas +0.18, prior_missed -0.17, age -0.15, prior_ppg -0.15, moved -0.12, years_exp +0.09, adp_pos -0.08, rookie +0.08, prior_bust -0.04, vac_share +0.01, prior_cv +0.01
- **boom, + expert spread (2020+):** value -0.34, ecr_gap -0.34, moved +0.14, vegas +0.14, rookie +0.14, age -0.12, prior_missed -0.12, adp_pos +0.12, prior_cv +0.11, prior_ppg +0.09, years_exp -0.08, prior_bust +0.07, prior_boom +0.07, vac_share -0.01, ecr_sd -0.01
- **bust, ADP + history:** age +0.58, years_exp -0.50, adp_pos +0.33, prior_cv -0.19, prior_bust +0.19, prior_missed +0.18, rookie -0.14, moved +0.12, vegas -0.08, prior_ppg +0.05, prior_boom -0.05, vac_share -0.02
- **bust, + expert spread (2020+):** ecr_gap +0.46, prior_cv -0.42, rookie -0.33, adp_pos +0.32, age +0.31, ecr_sd -0.26, years_exp -0.19, prior_missed +0.16, prior_ppg -0.15, vegas -0.13, prior_bust +0.10, vac_share +0.07, value -0.06, moved -0.04, prior_boom +0.01

## 6. The app's hand-set weights vs the fitted model (2020-25, top 120)

- Hand-weight proxy (only the inputs that exist historically: disagreement, prior boom/bust rates, age, value, games missed): boom AUC 0.533, bust AUC 0.594 on 2020-25.
- Same proxy on the 2024-25 holdout: boom AUC 0.603, bust AUC 0.599, vs ADP-only 0.534 / 0.581.

## 7. What this means for the model

**The honest headline.** Nothing available before the season predicts *boom* much better than ADP does. The fitted boom model matches ADP alone on the 2024-25 holdout (AUC 0.54 vs 0.54) and the app's own hand weights score 0.60 on a 226-row holdout, which is a small edge on a small sample. *Bust* is more predictable (AUC 0.59-0.65): age, expert disagreement, games missed and team changes carry real signal. The expert consensus and ADP are interchangeable as a central rank (Spearman 0.40 vs 0.42), so the composite's job is transparency, not beating the market.

**Findings that hold up (consistent in the univariate tables and the fits, with usable sample sizes):**
- **RB age cliff is 28, not 27.** Age-27 backs hit 61% and bust 32%; age-28 backs hit 38%, bust 54%, and lose 3.3 PPG. Age is the single strongest bust coefficient (+0.58 standardized).
- **Expert spread predicts variance and bust.** Bottom-quartile spread (everyone agrees) busts 16-18 points less; top-quartile spread busts 6-7 points more; Spearman 0.24 with distance from the consensus finish. Spread does not predict boom.
- **Team changes hurt.** Backs who moved bust +8, receivers +7, boom −4 to −6; moved receivers lose 2.2 PPG vs 0.9 for stayers.
- **Vacated volume is noise** for incumbents (Spearman 0.03 with PPG change) and for arrivals (receivers arriving into rooms that vacated 35%-plus bust +8). It is now displayed but not scored.
- **Rookie receivers with draft capital boom** (+16, bust −17, n=25) and **year-2 backs boom** (+10, n=65). Year-2 and year-3 receivers show no lift, so that prior was dropped.
- **Vegas matters for backs**: win total ≥ 10 → RB boom +6; ≤ 6.5 → RB boom −8. Roughly nothing for receivers.
- **Prior-year top-3 backs regress**: 23% repeat top-3, 47% finish top-12, −4.5 PPG. Prior-year top-6 receivers, by contrast, boom +10 (stars repeat).
- **Value picks work for receivers**: ADP 8-plus picks later than the consensus → boom +12, bust −11 (n=65).
- **Weekly volatility does not predict busts** (volatile prior year → bust −3 to −4). Cut from 0.15 to 0.05 in the risk score.
- **Round priors**: R1 RB/WR hit ~80% with ~23% bust; R2 RB 77% vs WR 57%; R3 RB 68% vs WR 64%; from R5 on receivers hold up better than backs; QBs in rounds 5-6 hit ~68%, which supports late QB.

**Changes applied to the model** (build.py, situation.py): RB age cliff to 28; moved penalty extended to backs; vacated weight set to zero; rookie-WR and year-2-RB priors replace the year-2/3 WR prior; risk weight moved from volatility to expert spread; bust weight moved from reach to age and downside disagreement; boom weight moved from disagreement and history to ADP-versus-consensus value; a regression note added for backs coming off an elite season.

**Limits.** Samples are small (25-70 per slice), the outcome definitions are choices, seasons since 2020 have 17 games, and 2020-25 is the only span with expert spread. Nothing here is a reason to trust any single score; the value of the backtest is that the weights now point the way the data points and the dead signals are out.
