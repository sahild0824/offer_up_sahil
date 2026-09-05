# Review of the data, process and methods (September 5, 2026)

A self-audit of what shipped on September 4. Every claim below was measured against the files in `data/`; the scripts that produced the numbers are in the session log and can be re-run from `build.py`.

## Verdict in three lines

- **Solid:** the player universe, teams, bye weeks and the top-60 composite are trustworthy; the strategy synthesis agrees across nine independent expert sources; the pipeline is reproducible and nothing is fabricated.
- **Weak:** the 19 ranking outlets are far less independent than they look, the article-derived boom/bust signals cover two thirds of the top 100 and come from search snippets rather than full articles, injury risk is a positional base rate for 97% of players, and none of the score weights are fitted to outcomes.
- **Fixed during this review:** a Draft Sharks ADP feed in round.pick format that dragged 86 of the top-150 ADPs 2 to 6 picks early, undrafted placeholders (701, 3054) leaking into ADP means, and a precedence bug that let an older "healthy" article note override a verified PUP designation (Christian Watson).

## 1. Data

### Freshness
| source group | date | players | note |
|---|---|---|---|
| FantasyPros ECR, ESPN (3 boards), Yahoo (Winks, Boone), Sleeper default | Sept 4 | 240-253 | current |
| RotoBaller, ETR auction, Flock, Subvertadown, FFToday, PrizePicks | Aug 29 - Sept 2 | 148-251 | current |
| RotoWire, Draft Sharks, LineupExperts | Aug 26 | 243-250 | before the Jacobs, Love and Jeanty news |
| NBC top 200, Bleacher Report top 100, BDGE top 50 | Aug 12-15 | 50-196 | three weeks old |
| CBS, Fantasy Life, 4for4 | Jul 27 - Aug 3 | 173-252 | stale, weight 0.5 |

Dropping the three stale lists moves exactly one top-100 player more than three composite spots, so their inclusion is harmless and their removal would be equally harmless.

**News lag is the real freshness problem.** ADP is a trailing average, so every feed still shows Josh Jacobs around pick 38 even though he went on the exempt list on August 30 and current drafts reportedly take him near 95. The same lag affects Jeremiyah Love (ankle), Ashton Jeanty (ankle), Christian Watson (PUP) and Isiah Pacheco (IR). The hand adjustments in `adjustments.json` patch 63 players for this, which is a manual, subjective layer on top of the model.

### Independence
Every outlet's ranking correlates between 0.84 and 0.99 with ADP over the top 150. Sleeper's default order is ADP (r = 0.989). ESPN, RotoWire, Draft Sharks, NBC, LineupExperts, PrizePicks, Bleacher Report, BDGE, Subvertadown and CBS each track the market more closely than they track the FantasyPros expert consensus. In practice the "19-outlet composite" is closer to three or four independent opinions plus the market, and it sits within two spots of ADP for most players. The model's information lives where the outlets disagree: Derrick Henry (composite 22 vs FantasyPros 38), Jeanty, Love, Skattebo, Kyren Williams, and the QBs (FantasyPros ranks Maye, Burrow and Lamar 12-17 spots higher than the other outlets).

### Truncated lists
A top-50 or top-100 list only contributes when it is bullish on a player near its cutoff; players it omits get no offsetting signal. Measured effect: players inside the last 20% of a truncated list carry a list rank 11 to 52 spots better than their composite. Applying an expert-only, truncation-guarded composite moves only 2 of the top 120 players more than two spots, so the bias is real but small. It should still be fixed because it is systematic.

### Coverage of the signals behind boom, bust and risk (top 100 by composite)
| signal | players covered |
|---|---|
| projection (ESPN, CBS) | 98 |
| ffanalytics floor, ceiling, uncertainty, age | 98 |
| any boom or bust article citation | 64 |
| any risk-research row | 73 |
| a numeric injury probability | 1 (McCaffrey, 78%) |

Injury risk is therefore the positional base rate (RB 40, WR 35, TE 35, QB 25 on the 0-100 input scale) for almost everyone, which means the risk meter mostly measures expert and platform disagreement. Citation counts also carry a popularity bias: a famous player collects more "bust" articles than an equally risky obscure one.

### Projections
Only two stat-line sources. The median ESPN-versus-CBS gap is 20 PPR points and 24 players differ by more than 40, so VBD has roughly a ±20-point error bar. The ffanalytics export is standard scoring and undated, so it is used only as ratios (ceiling/points, floor/points) and for age.

### Conflicts between research streams
The risk research and the context research disagreed on Christian Watson (healthy vs PUP; PUP is correct, verified September 5), Kenneth Walker's team (SEA vs KC; KC is correct) and two other teams. Article snippets predate moves. Rule adopted: the curated context file wins over article-derived status text.

### What is missing entirely
PFF, NFL.com, ESPN's individual analysts, current CBS, The Athletic, FTN, Fantasy Points, Footballguys; first-hand Reddit; Draft Sharks injury probabilities beyond one player; weekly game logs (so no true boom/bust rates); any ADP snapshot after the August 30 news.

## 2. Process

**What held up.** Every ranking and ADP file has a verified date and a named mirror. Names were matched with a normalizer and an alias table, and every player named in the strategy resolves to a data row. Bye weeks were derived from the schedule and cross-checked against three sources. `build.py` regenerates everything deterministically.

**What did not.** Fantasy sites, Reddit and the Sleeper API are blocked here, so article findings came from search-result summaries, which garble names and drop context. The five research agents ran once each with no cross-checking between them, which is how the Watson conflict survived until this review. There is no automated freshness check, so stale ADP for news-affected players is invisible unless someone looks. The 73 hand adjustments are documented but are judgment calls with hand-picked magnitudes.

## 3. Methods

- **Composite.** A weighted mean of ranks with FantasyPros counted double and market-driven boards counted half. FantasyPros itself uses rank points to avoid imputing unranked players; omitting a source that does not rank a player is the equivalent here, but only if truncated lists are excluded near their cutoffs. The weights are reasoned, not fitted.
- **Boom and bust.** Within-position percentiles of hand-weighted signals. Read them as "relative to his price": the consensus No. 1 at a position cannot have upside disagreement, so Gibbs shows boom 53 and Josh Allen 25 even though both are elite. Nothing has been calibrated against a past season.
- **Risk.** Follows Isaac Petersen's ffanalytics construction (spread of ranks, spread of ADP, projection uncertainty) plus injury, camp and situation. Sound in form, but the injury input is a base rate for 97% of players.
- **Tiers.** The ffanalytics drop-off rule applied to ranks with a local spread. The top tiers match what the strategy sources describe (Gibbs and Bijan; Chase, Nacua, Smith-Njigba; Bowers and McBride; Allen alone, then Lamar). Deeper tiers are heuristic.
- **Availability.** A logistic around ADP with a width from platform spread. Plausible, uncalibrated. Fantasy Football Calculator publishes min, max and standard deviation per player, which could calibrate it directly.
- **VBD.** Two projection sources against the research's 10-team baselines (QB10, RB22, WR28, TE10). Directionally right, noisy.
- **Scenario runner.** Log-rank scoring with strategy presets that encode the research. It does not simulate other drafters, so "chance he is there" and the round-by-round table assume the market drafts exactly at ADP.
- **No backtest.** This is the largest gap. Every weight above is a judgment call because there was no historical data to fit or validate against.

## 4. What would actually move the needle, in order

1. **Backtest and calibrate.** Pull 2023-2025 preseason ECR and ADP history (DynastyProcess stores dated FantasyPros scrapes) and 2023-2025 season results (nflverse weekly player stats, reachable as GitHub release assets). Fit the boom, bust and risk weights to what actually happened, replace the hand-set age and round priors with measured hit rates, and validate the availability curve.
2. **Weekly game logs for 2024-2025.** Compute the FantasyPros-style boom rate (weeks at or above the weekly RB6/WR6/QB3/TE3 score) and bust rate (weeks at or below RB40/WR56/QB18/TE18) plus weekly consistency per player. These replace article citations as the main boom/bust inputs for veterans.
3. **A fresh ADP snapshot after August 30** from any daily Sleeper or Fantasy Football Calculator mirror, plus a freshness check that flags players whose ADP feeds disagree by more than 20 picks.
4. **More projection sources**, ideally an ffanalytics run in full PPR with its own floor, ceiling and standard deviation, and FantasyPros' aggregate projections.
5. **Expert-only composite with a truncation guard** (small effect, but it removes a systematic bias and lets the app report how many independent opinions stand behind each rank).
6. **Injury inputs from nflverse injury reports and games-missed tables** for 2023-2025, so durability is per player rather than per position.
7. **Monte Carlo opponents in the scenario runner**, drafting from ADP with noise, so availability and the top-4 tables reflect a distribution of drafts rather than a single ADP order.

Items 1, 2 and 6 depend on the GitHub repository survey (`repos_survey.md`, in progress at the time of writing).

## 5. Draft-day checks that no model replaces

Puka Nacua's NFL review, Jeanty's and Love's Week 1 status, Kittle's Achilles timeline, and the Falcons QB decision were all unresolved on September 4. Check each the morning of the draft; the app's flags reflect the September 4 state.


## Addendum, September 5: what changed after this review

- **Real game logs.** nflverse 2024-25 weekly stats now supply per-player boom-week and bust-week rates at the FantasyPros thresholds, weekly consistency, games missed, exact ages, and Week 1 roster status codes (item 2 above, done; item 6 partly done).
- **Fresh market data.** Five September 4 ADP feeds (Fantasy Football Calculator with per-player stdev over 7,681 drafts, ESPN live, Sleeper live, FantasyPros and Yahoo daily snapshots) replace the stale feeds when present, and a 7/30-day ADP trend flags news-driven moves (item 3, done). Availability now uses the within-draft stdev (item 7 partly done).
- **More projections and a calibrated injury model.** ESPN live, CBS, Sleeper and a hierarchical-Bayesian model (with p10/p90 and projected games) feed projections; a calibrated missed-time injury probability (AUC 0.75) replaces the positional base rate for 247 of 253 players (items 4 and 6, done).
- **2026 situation layer.** Team environment (confirmed play-callers with computed tendencies, QB tiers, Vegas, O-line), per-player opportunity change, vacated volume and schedule strength, with priors and weights taken from the methods research rather than guessed. Its mean effect is capped and the larger half of any change goes into variance.
- **Still open.** No backtest (item 1). The expert-only composite with a truncation guard (item 5) is measured but not switched on. Opponent simulation in the scenario runner (item 7) is not built. Team-environment inputs still lean on search snippets for some coordinators and win totals; see `research/team_env_notes.md` for the [UNVERIFIED] flags.
