# 2026 Redraft PPR Rankings — Sources & Caveats

Compiled 2026-09-04. Companion file: `rankings.json` (one object per player: `name`, `team`, `pos`, `bye`, `ranks{}`, `adp{}`, `adp_ranks{}`, `auction_values{}`, `meta{}`).

## Environment note (important for interpreting sources)
The network egress proxy in this session blocked direct fetches of every fantasy/sports site (fantasypros.com, espn.com, sports.yahoo.com, cbssports.com, nfl.com, pff.com, fantasyfootballcalculator.com, nbcsports.com, si.com, 4for4, fftoday, rotoballer, fantasylife, draftsharks, underdogfantasy.com, sleeper.com/api.sleeper.app, footballguys, etc.), and the WebSearch budget was exhausted early. All ranking/ADP data below was therefore obtained from **public GitHub repositories that mirror/export those sources** (raw.githubusercontent.com was reachable), and dates were verified from each file's commit history. Each entry lists the ultimate publisher, the mirror used, the date of the mirror, and format caveats. Nothing was fabricated; where a source could not be obtained it is listed under "Not obtained".

## 2026 NFL bye weeks (team → bye week)
Derived from the official 2026 regular-season schedule in the nflverse `games.csv` (https://raw.githubusercontent.com/nflverse/nfldata/master/data/games.csv, 272 REG games for season 2026; each team's missing week = bye). Cross-checked against search snippets from NFL.com / FOX Sports / Yahoo "2026 NFL bye weeks" articles (Wk5 CAR, KC; Wk6 CIN, DET, MIA, MIN; Wk7 BUF, JAX, LAC, WAS; Wk11 ATL, CLE, GB, LAR, NE, SEA; Wk14 ARI, DAL — all agree) and against the BYE column of the FantasyPros ECR export (0 mismatches).

| Team | Bye | Team | Bye | Team | Bye | Team | Bye |
|---|---|---|---|---|---|---|---|
| ARI | 14 | DAL | 14 | LAC | 7 | NYJ | 13 |
| ATL | 11 | DEN | 10 | LAR | 11 | PHI | 10 |
| BAL | 13 | DET | 6 | LV | 13 | PIT | 9 |
| BUF | 7 | GB | 11 | MIA | 6 | SEA | 11 |
| CAR | 5 | HOU | 8 | MIN | 6 | SF | 8 |
| CHI | 10 | IND | 13 | NE | 11 | TB | 10 |
| CIN | 6 | JAX | 7 | NO | 8 | TEN | 9 |
| CLE | 11 | KC | 5 | NYG | 8 | WAS | 7 |

By week: **5** CAR, KC · **6** CIN, DET, MIA, MIN · **7** BUF, JAX, LAC, WAS · **8** HOU, NO, NYG, SF · **9** PIT, TEN · **10** CHI, DEN, PHI, TB · **11** ATL, CLE, GB, LAR, NE, SEA · **12** none · **13** BAL, IND, LV, NYJ · **14** ARI, DAL.

## Player universe
The player list is the FantasyPros PPR Expert Consensus (overall) as of 2026-09-04, filtered to QB/RB/WR/TE and to ECR overall rank ≤ 300 (K and DST removed; `fantasypros_ecr` is the overall rank *including* K/DST so it matches the FantasyPros page numbering). Names are the FantasyPros spellings (e.g. "Ja'Marr Chase", "CeeDee Lamb", "Bijan Robinson", "James Cook III", "Kenneth Walker III"). Other sources were matched by normalized name (suffixes/punctuation stripped, plus an alias table) with a position check.

## `ranks{}` keys — overall PPR rank sources (unless noted)
| key | publisher / analyst | mirror used (GitHub) | data date | scope & caveats |
|---|---|---|---|---|
| `fantasypros_ecr` | FantasyPros Expert Consensus Rankings, Draft PPR overall (https://www.fantasypros.com/nfl/rankings/ppr-cheatsheets.php) | DynastyProcess `db_fpecr_latest.csv` (https://raw.githubusercontent.com/dynastyprocess/data/master/files/db_fpecr_latest.csv), rows with `fp_page=/nfl/rankings/ppr-cheatsheets.php` | scrape_date 2026-09-04 | Full 525-row overall list incl. K/DST; rank = order by consensus ECR average. `meta.fantasypros_ecr_avg/best/worst` also provided. |
| `espn_ppr300` | ESPN official 2026 PPR-300 cheat sheet PDF (ESPN staff PPR ranks + salary-cap $) | dsegundo2/RankingsDiff `frontend/public/data/2026/espn/rankings.json` (`sourceRank`) | refreshed 2026-09-04 (daily GitHub Action) | Top ~270 incl. K/DST. Full PPR. `auction_values.espn_auction_value` = ESPN $ from same sheet. |
| `espn_draft_rank` | ESPN fantasy default draft rank (leaguedefaults / kona player feed, PPR default) | Zinkelburger/Fantasy-Football-Tool `data/ranks/ppr_with_depth.csv` (`ESPN_Rank`) | refreshed 2026-09-04 (twice-weekly GitHub Action) | ESPN's in-app draft ranking, not an individual analyst. ~283 players. |
| `espn_rank_aug24` | ESPN PPR draft rank (older snapshot) | ebsoren/fantasy-analysis `draft_analysis/espn_rankings.csv` | 2026-08-24 | Secondary/older ESPN snapshot (260 players). |
| `sleeper_rank` | Sleeper app default PPR rank | Zinkelburger `data/ranks/ppr_with_depth.csv` (`Sleeper_Rank`) | 2026-09-04 | Sleeper's own ordering (ADP-driven). |
| `yahoo_winks` | Yahoo Fantasy — Hayden Winks' full-PPR rankings (Yahoo "adjusted rankings" widget) | dsegundo2/RankingsDiff `frontend/public/data/2026/yahoo-full/rankings.csv` | refreshed 2026-09-04 | Top ~380 incl. K/DST. Full PPR. |
| `yahoo_boone` | Yahoo Fantasy — Justin Boone's rankings | shreyasprasad14/FantasyHelper `boone.csv` | committed 2026-09-04 | 303 players incl. K/DST; scoring not labeled in the file (Boone publishes PPR/half; ordering matches his PPR board with Gibbs 1, Chase 2). |
| `yahoo_smyth_posrank` | Yahoo — Joel Smyth Draft Guide PPR **positional** ranks | ethankwyap-stack/fantasy-edge `draft-guide-smyth-2026-guide.json` | refreshed 2026-08-14 | Positional rank only (suffix `_posrank`). |
| `rotoballer` | RotoBaller 2026 PPR draft rankings (RK column of RotoBaller rankings table) | GraveGhost1/fantasydraftsheet `rotoballer-rankings.csv` | 2026-09-02 | ~400 players incl. K/DST. |
| `rotowire_consensus` / `rotowire_rank` | RotoWire 2026 draft kit — expert consensus (Theo/Ian/Jagger/Jeff/Jim) and RotoWire overall value rank | 1raybeez/River-City-FFL `data/auction/source-imports/exports/rotowire-2026.csv` | 2026-08-26 | Scoring per RotoWire default (PPR draft kit); `rotowire_rank` covers ~720 rows. |
| `draftsharks` | Draft Sharks 2026 rankings (Rank column, PPR consensus proj) | 1raybeez/River-City-FFL `.../exports/draftsharks-2026.csv` | 2026-08-26 | 523 players incl. K/DST. |
| `lineupexperts` | LineupExperts 2026 rankings (Rk) | 1raybeez/River-City-FFL `data/auction/adp/source-imports/exports/lineupexperts-adp-2026.csv` | 2026-08-26 | 510 rows incl. K/DST. |
| `fantasyfootballers_udk_posrank` | The Fantasy Footballers UDK 2026 — **positional** rank (+ `auction_values.fantasyfootballers_udk_auction` = UDK $) | 1raybeez/River-City-FFL `.../exports/fantasyfootballers-2026.csv` | 2026-08-26 | UDK export lists rank within position only; overall order can be approximated by the $ value. |
| `fftoday_krueger` | FFToday — Mike Krueger PPR rankings | zkelfer/draft-board-2026 `pipeline/sources.py` (raw pasted `FFTODAY_PPR` list) | 8/30/2026 | Top ~224 incl. K/DST; parsed from the raw list so players the repo owner "scratched" (e.g. Josh Jacobs) are retained. |
| `prizepicks_hardy` | PrizePicks — Christian Hardy PPR top 200 | zkelfer/draft-board-2026 `pipeline/sources2.py` (raw pasted `PP` list) | 8/29/2026 | Top 200 incl. K/DST; parsed from the raw list. |
| `subvertadown` | Subvertadown "TapThatDraft" value board (1.0 PPR, 12-team) | zkelfer/draft-board-2026 `pipeline/data.json` (`r.sd`) | 8/31/2026 | Value-model ordering, top ~200. |
| `nbc_rotoworld` | NBC Sports / Rotoworld 2026 Fantasy Football Top 200 overall (https://www.nbcsports.com/fantasy/football/news/2026-fantasy-football-top-200-overall-rankings) | andycon-007/katy-draft-assistant `data/sources/rotoworld_top200.json` | retrieved 2026-08-15 | 1-QB overall; not explicitly labelled PPR by NBC (treated as PPR-leaning). |
| `bleacher_report` | Bleacher Report Top 100 PPR (https://bleacherreport.com/articles/25458550-...) | andycon-007/katy-draft-assistant `data/sources/br_standard_top100.json` (`ppr_rank`) | retrieved 2026-08-14 | Top 100 only. |
| `bdge_top50` | BDGE (Big Dog Gaming Enterprise) top-50 full-PPR expert board | gadelrosario/Sharingan `data/rankings/bdge_top_50_2026-08-12.json` | 2026-08-12 | Top 50 only. |
| `flock_consensus` | Flock Fantasy redraft PPR expert consensus ("Expert" column of Flock ADP tool) | griffonrubin/elite-rookie-scouter `dynasty-scout/data/flock/ppr_overall_3d_08312026.csv` | 2026-08-31 | Same file supplies `adp_ranks.flock_*_rank`. |
| `fantasylife_consensus_jul28` / `fantasylife_berry_jul28` | Fantasy Life rankings (Consensus; Matthew Berry column) — PPR | sansbacon/nfl `files/fantasy_life_fantasy_football_rankings.csv` | 2026-07-28 (**stale**) | Only Fantasy Life copy found; ~5 weeks old. Also has Valenzuela/Freedman/McFarland columns (not exported). |
| `fourfor4_jul27` | 4for4 PPR rankings table | mborysiak/Fantasy_Football `Data/OtherData/4for4/20264for4-fantasy-football-rankings-ppr-2026-table.csv` | 2026-07-27 (**stale**) | Only 4for4 copy found; ~5.5 weeks old. |
| `cbs_aug3` | CBS Sports PPR rank (CBS column of the JuiceBoxOne comparison sheet) | Zinkelburger `data/juicebox/2026/juicebox_rankings_CBS_PPR.csv` | 2026-08-03 (**stale**) | Only CBS ranking copy found; ~1 month old, 177 players. |
| `etr_auction_rank` | Establish The Run — derived ordering of ETR full-PPR auction values (ties broken by file order); `auction_values.etr_auction_value` = ETR $ | khoff3/inflaction_calculator `backend/2026/NFL_ETR_Auction_Values.csv` | ETR pull 2026-09-01 | Derived from $ values, not ETR's published rank list; ~150 skill players with value > 0. |

## `adp{}` keys — average draft position (overall pick number unless noted)
| key | source | mirror used | date | caveats |
|---|---|---|---|---|
| `sleeper_ppr` | Sleeper ADP, PPR | Zinkelburger `engine/league-sim/data/market/adp_2026.csv` (`sleeper_ppr`) | 2026-09-04 | |
| `sleeper_aug29` | Sleeper ADP | RealDiceflame/ProjectFootMoneyball `data/ADP/combined_adp_2026.csv` | 2026-08-29 | scoring not labeled |
| `nfc_ppr` | FantasyFootballCalculator (NFC) ADP, PPR | Zinkelburger market file (`ffc_ppr`) | 2026-09-04 | FFC default (12-team) |
| `nfc_ppr_aug28` | FantasyFootballCalculator ADP, PPR | gesmith0606/nfl_data_engineering `data/adp/adp_ffc_ppr_20260828.csv` | 2026-08-28 | includes times_drafted in mirror |
| `espn` | ESPN ADP (official ESPN fantasy game, format-agnostic) | RealDiceflame `combined_adp_2026.csv` (`NFL` column, labelled "ESPN (official fantasy game of NFL)") | 2026-08-29 | |
| `yahoo` | Yahoo ADP (all drafts) | RealDiceflame `combined_adp_2026.csv` | 2026-08-29 | format-agnostic |
| `yahoo_aug25` | Yahoo ADP (`adpAll`) | kjeffreys/ffbPlayerDraftingApp `draft_prep/yahoo_exports/yahoo_adp_clean.csv` | 2026-08-25 | |
| `underdog` | Underdog Fantasy best-ball ADP (half-PPR) | GraveGhost1 `rotoballer-rankings.csv` (`ADP (Underdog)`) | 2026-09-02 | Underdog is half-PPR best ball |
| `rotowire_underdog` | Underdog ADP | 1raybeez `.../rotowire-adp-2026.csv` | 2026-08-26 | |
| `ffpc` | FFPC ADP | GraveGhost1 `ffpc-rankings.csv` (`ADP (FFPC)`) | 2026-08-29 | FFPC is TE-premium |
| `udk_sleeper_pick` / `udk_espn_pick` / `udk_yahoo_pick` / `udk_underdog_pick` / `udk_avg_pick` | Fantasy Footballers UDK "ADP Comparison" (Sleeper, ESPN, Yahoo, Underdog, Avg) | capncrockett/grundle-ball `frontend/src/data/adp/UDK - ADP Comparison - ... 2026-08-31_12-05-31_PDT.csv` | 2026-08-31 | Source gives round.pick (12-team); converted to overall pick = (round-1)*12+pick |
| `fantasypros_avg` (+ `fantasypros_espn`, `fantasypros_cbs`, `fantasypros_sleeper`, `fantasypros_rtsports`, `fantasypros_fantrax`) | FantasyPros PPR ADP consensus page (https://www.fantasypros.com/nfl/adp/ppr-overall.php) | chasecotton27/fantasy-football-draft-assistant `adp-data/adp_full_ppr.csv` | 2026-08-28 | Yahoo/NFL columns were empty in the export |
| `draftsharks_half_consensus` | Draft Sharks consensus redraft ADP (0.5 PPR) | 1raybeez `.../draftsharks-adp-2026.csv` | 2026-08-26 | half-PPR |

## `adp_ranks{}` — platform ADP expressed as an ordinal rank
| key | source | mirror | date |
|---|---|---|---|
| `flock_sleeper_rank`, `flock_espn_rank`, `flock_yahoo_rank`, `flock_underdog_rank`, `flock_cbs_rank`, `flock_ffpc_rank` | Flock Fantasy ADP tool (3-day window, PPR) per-platform ADP rank | griffonrubin/elite-rookie-scouter `.../flock/ppr_overall_3d_08312026.csv` | 2026-08-31 |
| `underdog_rank_aug24`, `yahoo_rank_aug24` | Underdog / Yahoo ADP rank (half-PPR) as republished by FFToday | zkelfer/draft-board-2026 `pipeline/data.json` | 2026-08-24 |

## Not obtained (blocked and no public mirror found)
- **PFF** fantasy rankings (pff.com blocked; no 2026 PFF redraft export found on GitHub).
- **NFL.com** (Fabiano/Grant) rankings — nfl.com blocked; only a June-2026 NFL.com projections export existed (too stale, not used).
- **ESPN individual analysts** (Mike Clay / Karabell / Field Yates) full lists — only search-snippet fragments (Yates top-19 and 135-160) were visible; not included to avoid partial/fabricated data. ESPN staff PPR-300 sheet is included instead (`espn_ppr300`).
- **CBS (Eisenberg/Richard)** current ranks — only the Aug-3 mirror (`cbs_aug3`).
- **The Athletic (Ciely)**, **FTN/NumberFire**, **Fantasy Points**, **FantasyLife current** (only Jul-28), **4for4 current** (only Jul-27), **Footballguys**, **Sleeper "expert" rankings** (Sleeper's own rank included).
- **Yahoo analyst consensus top-300 article** (Boone/Harmon/Norris/Pianowski/Smyth/Winks) — page blocked; Winks (full list), Boone (full list) and Smyth (positional) are included individually.

## Coverage by key (number of players in `rankings.json` carrying each key; ECR top-150 skill-player coverage)
| key | section | players covered (of 253) | covered in ECR top-150 |
|---|---|---|---|
| fantasypros_avg | adp | 252 | 165/165 |
| underdog | adp | 251 | 165/165 |
| fantasypros_fantrax | adp | 251 | 165/165 |
| ffpc | adp | 250 | 165/165 |
| udk_avg_pick | adp | 250 | 165/165 |
| udk_underdog_pick | adp | 249 | 164/165 |
| sleeper_ppr | adp | 246 | 165/165 |
| fantasypros_sleeper | adp | 232 | 165/165 |
| draftsharks_half_consensus | adp | 223 | 165/165 |
| udk_sleeper_pick | adp | 222 | 163/165 |
| espn | adp | 214 | 165/165 |
| sleeper_aug29 | adp | 214 | 165/165 |
| nfc_ppr_aug28 | adp | 213 | 165/165 |
| nfc_ppr | adp | 210 | 165/165 |
| rotowire_underdog | adp | 209 | 153/165 |
| fantasypros_rtsports | adp | 200 | 164/165 |
| yahoo | adp | 181 | 159/165 |
| udk_espn_pick | adp | 181 | 159/165 |
| fantasypros_espn | adp | 181 | 159/165 |
| udk_yahoo_pick | adp | 180 | 160/165 |
| yahoo_aug25 | adp | 179 | 159/165 |
| fantasypros_cbs | adp | 176 | 160/165 |
| flock_espn_rank | adp_ranks | 252 | 165/165 |
| flock_yahoo_rank | adp_ranks | 252 | 165/165 |
| flock_underdog_rank | adp_ranks | 252 | 165/165 |
| flock_ffpc_rank | adp_ranks | 252 | 165/165 |
| flock_sleeper_rank | adp_ranks | 232 | 165/165 |
| underdog_rank_aug24 | adp_ranks | 213 | 164/165 |
| yahoo_rank_aug24 | adp_ranks | 213 | 164/165 |
| flock_cbs_rank | adp_ranks | 177 | 160/165 |
| fantasyfootballers_udk_auction | auction_values | 248 | 165/165 |
| espn_auction_value | auction_values | 239 | 165/165 |
| etr_auction_value | auction_values | 148 | 147/165 |
| fantasypros_ecr | ranks | 253 | 165/165 |
| yahoo_winks | ranks | 252 | 165/165 |
| rotowire_rank | ranks | 252 | 165/165 |
| flock_consensus | ranks | 252 | 165/165 |
| fantasylife_consensus_jul28 | ranks | 252 | 165/165 |
| rotoballer | ranks | 251 | 165/165 |
| draftsharks | ranks | 250 | 165/165 |
| fantasyfootballers_udk_posrank | ranks | 248 | 165/165 |
| lineupexperts | ranks | 247 | 163/165 |
| sleeper_rank | ranks | 246 | 165/165 |
| fourfor4_jul27 | ranks | 246 | 163/165 |
| rotowire_consensus | ranks | 243 | 165/165 |
| yahoo_boone | ranks | 241 | 165/165 |
| espn_rank_aug24 | ranks | 241 | 165/165 |
| espn_ppr300 | ranks | 239 | 165/165 |
| espn_draft_rank | ranks | 213 | 165/165 |
| subvertadown | ranks | 200 | 161/165 |
| fftoday_krueger | ranks | 199 | 163/165 |
| nbc_rotoworld | ranks | 196 | 163/165 |
| fantasylife_berry_jul28 | ranks | 192 | 162/165 |
| yahoo_smyth_posrank | ranks | 180 | 159/165 |
| prizepicks_hardy | ranks | 175 | 156/165 |
| cbs_aug3 | ranks | 173 | 158/165 |
| etr_auction_rank | ranks | 148 | 147/165 |
| bleacher_report | ranks | 100 | 100/165 |
| bdge_top50 | ranks | 50 | 50/165 |
