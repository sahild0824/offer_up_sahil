# Fourth Pick War Room

A single-file, phone-first draft app for a 10-team, full-PPR snake draft from the 4th slot, plus the research and scoring model behind it.

Open `index.html` on your phone, or the published copy at https://claude.ai/code/artifact/9231f494-587f-450a-9a8c-b52b6a9c9d0d, and you get four tabs:

- **Plan** – the pick-4 strategy synthesized from PFF, Draft Sharks, ESPN, CBS, Fantasy Life, 4for4, Yahoo, FantasyPros, RotoBaller and the secondhand r/fantasyfootball consensus: who to take at 4, a round-by-round target list for picks 4 / 17 / 24 / 37 / 44 / 57 / 64 / 77 / 84 / 97 / 104 / 117 / 124 / 137 / 144 / 157, QB and TE timing, sleepers, avoids, ten rules.
- **Board** – 253 players with a composite rank built from 19 outlets, ADP from 22 feeds, value vs ADP, projection and VBD, tier, and boom / bust / risk meters. Filter by position, search, sort.
- **Draft** – live tracker. Mark players taken or drafted to your team; it shows the current pick, your next pick, best available overall and by position, who is falling to you, and the chance each player is still there at your next pick. State is saved in the browser.
- **Model** – how every number is computed, the source list with coverage counts, and what could not be reached.

Tap any player for the full sheet: source-by-source ranks on a strip chart, ADP by platform, floor / ceiling, the reasons behind his boom, bust and risk scores, and availability at each of your picks.

## 2026 situation layer

The fourth meter, **2026**, scores each player's situation relative to his position: team offensive environment (confirmed play-caller and his computed 2022-25 tendencies, quarterback tier, Vegas win total, PFF offensive-line rank), the player's 2026 change (opportunity, competition, quarterback and coaching change, with an unresolved flag), vacated volume for arrivals and drafted rookies, and 2026 strength of schedule by position with fantasy-playoff weeks 15-17 weighted most. Evidence-based priors from `research/methods_2026.md` are applied (year-2 and year-3 receivers, first-round rookies, receivers who changed teams). The player sheet shows the team card, the change drivers, the schedule and the reasons.

## Rebuilding the data

```
python3 nflverse_features.py --fetch   # 2024-25 game logs, 2026 rosters, birthdates -> data/nflverse_features.json
python3 market_features.py --fetch     # fresh ADP (FFC, ESPN, Sleeper, FantasyPros, Yahoo), projections, injury model, Vegas, O-line, play-callers
python3 build.py                       # scores everything and injects the data into index.html
python3 scenario.py --strategy hero-rb # top-4 targets per round (also --sit-weight, --sos-weight)
python3 montecarlo.py --sims 1500        # simulated opponents; feeds per-pick availability into the app
```

## Rebuilding the data (details)

```
python3 build.py          # merges data/*.json + data/raw/*.csv, scores players, injects into index.html
```

Inputs live in `data/`:

| file | what |
|---|---|
| `rankings.json` | 26 ranking lists and 22 ADP feeds per player, mirrored from public GitHub exports of FantasyPros, ESPN, Yahoo, RotoWire, RotoBaller, Draft Sharks, Flock, NBC, FFToday, PrizePicks, Bleacher Report, ETR, Sleeper, Underdog, FFPC and more (dates and caveats in `research/rankings_sources.md`) |
| `risk.json` | boom / bust / sleeper citations, injury labels, risk and boom factors for 122 players from ~70 articles (`research/risk_sources.md`) |
| `adjustments.json` | hand-curated 2026 context nudges: trades, coaching changes, IR / PUP / exempt list, depth-chart battles (`research/context.md`) |
| `raw/*.csv` | ESPN and CBS stat-line projections (converted to PPR points) and the ffanalytics export (floor, ceiling, uncertainty, age) |
| `strategy.json` | the Plan tab content, including the per-round forum / expert debate blocks (`research/strategy.md` is the long form with links; `research/round_debates.md` summarises the Sept 5 round-by-round sweep and `research/rounds_*.md` are the raw reports) |
| `model.json` | Model tab text, source list, unreachable-sources list |
| `byes.json` | 2026 bye weeks |
| `nflverse_features.json` | per-player 2024-25 boom/bust-week rates, usage shares, consistency, games missed, ages, Week 1 roster status; per-team vacated targets and carries; 2025 points allowed by defense (built by `nflverse_features.py`) |
| `market_features.json` | Sept 4 ADP feeds with per-player stdev and 7/30-day trend, live ESPN and Sleeper projections, Bayesian p10/p50/p90 and projected games, calibrated injury probability, injury log, expected-points regression, Vegas and O-line by team, play-caller census (built by `market_features.py`) |
| `team_env.json` | 2026 team environments: coaches, play-callers and their computed tendencies, QB tiers, Vegas, arrivals and departures (`research/team_env_notes.md`) |
| `sos.json` | 2026 strength of schedule by position, full / early / playoffs (`research/sos_notes.md`) |
| `opportunity.json` | per-player 2026 change drivers for the top 165 (`research/opportunity_notes.md`) |

Weights and baselines sit at the top of `build.py`. The scoring method is documented in the app's Model tab and in `research/methodology.md`.

## Running scenarios

```
python3 scenario.py                                    # 10 teams, slot 4, balanced strategy and risk profile
python3 scenario.py --strategy hero-rb --profile upside
python3 scenario.py --strategy zero-rb --profile safe
python3 scenario.py --taken "Ja'Marr Chase,Bijan Robinson" --mine "Puka Nacua"   # mid-draft: plan from round 2
python3 scenario.py --teams 12 --slot 7
```

Each run prints and saves `scenarios/<name>.md` and `.csv`: the top 4 targets for every one of your picks (name, position rank, composite, chance still on the board), assuming you take the #1 target each round, plus the resulting roster. Strategies: `balanced`, `hero-rb`, `zero-rb`, `robust-rb`, `wr-heavy`. Profiles: `safe`, `balanced`, `upside`. Use `--min-avail` to tighten or loosen how likely a player must be to reach your pick.

## Monte Carlo draft simulator

```
python3 montecarlo.py --sims 1500                                   # GDL Fantasy: 10 teams, slot 4, ESPN room, full PPR
python3 montecarlo.py --sims 1000 --players data/players_half.json --tag _half
python3 montecarlo.py --teams 12 --slot 7 --room blend
```

`montecarlo.py` replays the whole 14-round draft (QB, 2 RB, 2 WR, TE, FLEX, D/ST, K and 5 bench; the IR slot is not drafted) a few thousand times. The nine opponents draw each player's draft position from a normal around his ESPN ADP with his measured spread and follow simple roster rules (one QB and one TE until the late rounds, position caps, K and D/ST mostly in rounds 13-14). Your picks follow a strategy preset. It writes `scenarios/montecarlo_summary<tag>.md` (strategy and first-pick comparison, per-round pick frequencies, availability at every one of your picks) and `scenarios/montecarlo_avail<tag>.json`, which `build.py` attaches to every player as `mcAvail` so the app's availability chips use simulated rather than logistic odds when the league settings match.

## Scoring formats

The header toggle switches the app between full PPR (GDL Fantasy's setting: 1 point per reception), half PPR and standard. `build.py` builds all three: stat-line projections are re-scored, the Bayesian floor / ceiling shift by projected receptions, boom / bust week rates are recomputed from the game logs at the format's thresholds, format-specific ADP feeds are used (FFC, Sleeper, ESPN, Yahoo, Underdog, Draft Sharks) and the composite is shifted by half the change in value over the positional baseline. Overlays are embedded in `index.html` as `alt.half` and `alt.std`.

## Caveats

This environment could not open fantasy sites, Reddit or the Sleeper API directly; rankings and ADP come from dated GitHub mirrors and article findings from search-result summaries. See the Model tab and `research/*.md` for what is stale or missing. Verify ADP on your own platform before draft night.
