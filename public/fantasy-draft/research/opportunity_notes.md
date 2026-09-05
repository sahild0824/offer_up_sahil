# 2026 Opportunity-Change Research Notes (redraft, as of Sept 5, 2026)

Companion to `opportunity.json` (165 players = every QB/RB/WR/TE inside the consensus top-165 of `rankings.json`, which covers all consensus top-120 picks). Built by `build_opportunity.py` in this directory.

## 1. What is in each field

| Field | Meaning |
|---|---|
| `team_2025`, `games_2025` | Team and regular-season games with a stat line in 2025 (nflverse). |
| `targets_2025`, `carries_2025` | 2025 regular-season totals from nflverse `stats_player_reg_2025.csv`. |
| `target_share_2025` | Player targets / team targets **in the games the player appeared in** (computed from `stats_player_week_2025.csv` + `stats_team_week_2025.csv`). This differs from nflverse's own `target_share` column, which divides by full-season team targets and therefore understates players who missed games (e.g., Rashee Rice 14.2% season-basis vs 28.7% games-played basis). |
| `rush_share_2025` | Player carries / team carries in games played (same method). Extra field, useful for RBs. |
| `snap_share_2025` | Mean of per-game offensive snap % over games played, from `snap_counts_2025.csv`. Null for a few players whose snap rows did not match by name (Chase Brown, Kenny Gainwell, Chig Okonkwo). |
| `proj_target_share_2026`, `proj_touches_2026` | Only filled where an outlet published a number (see section 3). `proj_touches_2026` is whatever unit the outlet used and is stated in the note (touches, targets, carries or receptions). |
| `opportunity_change` | Expected 2026 per-game role vs 2025 role: -2 big loss ... +2 big gain. Rookies and players with no 2025 role are scored relative to zero (+2 if expected to start / +1 if a defined but secondary role). |
| `competition_change` | Change in competition for the player's touches: +2 much less ... -2 much more. For QBs this field is job-security (negative = real battle or short leash); supporting-cast quality for QBs is in the extra `supporting_cast_change` field (-2..+2). |
| `qb_change` | Quality of 2026 QB vs the QB(s) the player actually played with in 2025 (0 for QBs themselves). |
| `coaching_change` | Effect of any new play-caller/scheme on this player (0 if staff unchanged). |
| `uncertain` | true when the situation is genuinely unresolved (injury/discipline/battle/new play-caller with no track record). |
| `drivers` | One-line facts behind the scores. `note` summarizes; `sources` lists the URLs the facts came from, always ending with the nflverse stats file and depth-chart release used for baselines. |

Scores are analyst-style judgments derived from the sourced facts, not published metrics.

## 2. Data actually obtained

**nflverse release assets (downloaded, computed locally):**
- https://github.com/nflverse/nflverse-data/releases/download/stats_player/stats_player_reg_2025.csv (season totals; note the tag is `stats_player`, not `player_stats`, for 2025 files)
- https://github.com/nflverse/nflverse-data/releases/download/stats_player/stats_player_week_2025.csv and `stats_team` weekly file (for games-played shares)
- https://github.com/nflverse/nflverse-data/releases/download/snap_counts/snap_counts_2025.csv
- https://github.com/nflverse/nflverse-data/releases/tag/depth_charts -> `depth_charts_2026.csv`, latest `dt = 2026-09-04T11:57Z` (used for every "listed RB1/WR2/TE3" statement) and `roster_2026.csv` status column (ACT/RES/EXE) used for IR/exempt confirmations: Conner, Pacheco, Charbonnet, Tyson, Dell, Higgins, Pearsall, Benson = RES; Josh Jacobs = EXE; Christian Watson, Alec Pierce, Nabers, Kittle, Rice = ACT.
- Red-zone share was NOT computed (play-by-play was downloaded but not processed within the time budget); the `play_by_play_2025.csv.gz` file is in the scratchpad if the coordinator wants to add it.

**Web research:** 60 WebSearch calls this task (the session-wide cap of 200 was then reached, so two final verification searches did not run). All fantasy-site pages (ESPN incl. the g.espncdn.com Clay projection PDF, PFF, 4for4, FantasyPros, CBS, Yahoo, etc.) are egress-blocked for direct fetch, so every qualitative fact comes from search-result summaries of the linked articles, not full article text. The existing `context.md` in this directory (prior session) was used for coaching staff, injury and Week 1 QB tables and is cited by the same URLs.

## 3. Published 2026 usage projections found (numbers)

| Player | Number | Outlet |
|---|---|---|
| A.J. Brown (NE) | ~25% target share; 130 targets / 86 rec / 1,216 yds / 7 TD | ESPN (Clay) trade reaction; Sharp Football |
| Makai Lemon (PHI) | 19% of receiving offense, 39 yds/game, 4.7 TD | Establish The Run |
| Emeka Egbuka (TB) | 121 targets (tied 16th) | FantasyPros projections (via outlook) |
| Bhayshul Tuten / Chris Rodriguez (JAX) | 227 carries / 994 yds ; 100 carries / 432 yds | ESPN (Clay) |
| Stefon Diggs (WAS) | 74 rec / 864 yds / 5 TD (WR36) | CBS Sports |
| Jeremiyah Love (ARI) | ~275 touches, ~50 rec, 1,500 yds, 10 TD "realistic" | SI / RotoBaller |
| Jadarian Price (SEA) | 15-20 touches/game "if he secures" | SI |
| Kenneth Walker (KC) | 15-18 carries/game + goal line | Fantasy Points |
| Mark Andrews (BAL) | 80-85 targets | Fantasy Life |
| Malik Willis (MIA) | 661 rush yds projected | Footballguys |
| Javonte Williams (DAL) | RB13 projection; Jake Ferguson ~TE15 | ETR / Fantasy Life |

Team-level vacated targets (PFF/Yahoo/4for4 summaries): PHI most receiving volume lost (A.J. Brown); SF 139 targets (Jennings, Bourne); GB 131 (Doubs, Wicks); MIA 128 (Hill, Waddle); WAS leads "notable talent" vacated (Deebo, Ertz); NYG lost Wan'Dale Robinson's 140; IND lost Pittman's 111; CHI lost Moore's 85; LAC lost Keenan Allen's 122; PIT lost Gainwell's 85 targets/114 carries; DET traded Montgomery's 158 carries; SEA lost ~405 combined Walker/Charbonnet carries; NO lost none but added Etienne; JAX lost Etienne's 260 carries; CAR lost Dowdle's 236 carries.

## 4. Biggest movers (from the JSON)

**Largest gains (opportunity +2 or +1 with +1/+2 competition):** DeVonta Smith (AJB gone), Jahmyr Gibbs (Montgomery traded, Pacheco IR), Isaiah Likely (NYG TE1), Luther Burden III, Travis Etienne (NO lead), David Montgomery (HOU lead), Kenneth Walker (KC lead), Bhayshul Tuten (JAX lead), MarShawn Lloyd (Jacobs exempt), Nico Collins/Dalton Schultz (Higgins ACL, Dell IR), Ladd McConkey/Omarion Hampton (McDaniel, Allen gone), Jaylen Waddle (DEN WR1), DJ Moore (BUF WR1 with Allen), Rome Odunze/Colston Loveland, Zay Flowers, Garrett Wilson/Breece Hall (Geno + Reich), Chig Okonkwo, plus rookies Love, Price, Tate, Lemon, Concepcion, Stribling.

**Largest losses:** Alvin Kamara (-2/-2), Josh Jacobs (-2, exempt list), Zach Charbonnet (-2, IR), Isiah Pacheco (IR/backup), Woody Marks (Montgomery), Bucky Irving (Gainwell + zone scheme), Courtland Sutton (Waddle), Romeo Doubs/Hunter Henry (AJB), Khalil Shakir (Moore), Kyren Williams (Corum rotation), Rico Dowdle (lead to 50/50), Wan'Dale Robinson (140 targets to WR2), Brian Thomas Jr. (usage signals), Keenan Allen, Deebo Samuel, Travis Kelce, Aaron Jones, Jordan Addison/T.J. Hockenson (Jennings), Trey McBride (mild, MHJ featured), Christian McCaffrey (mild, off 413 touches), Tony Pollard, Dobbins.

**QB upgrades for skill players:** Jefferson/Addison/Hockenson/Mason/Jones (Kyler), Waddle (Nix vs Miami), DJ Moore (Allen), A.J. Brown (Maye), G. Wilson/Hall (Geno), Chase/Higgins/Chase Brown (Burrow healthy), McLaurin/JCM (Daniels healthy), CMC/Kittle (Purdy healthy), Okonkwo (Daniels). **Downgrades:** Achane (Willis), Montgomery (Stroud vs Goff), Likely (Dart vs Lamar), Keenan Allen (Jones vs Herbert).

**Coaching flags:** 10 new HCs / 21 new OCs. Positive for: Judkins (Monken run-heavy), Fannin/Pitts (TE-friendly HCs), Chargers skill players (McDaniel), Bijan (Stefanski run-lean), Jeanty/Bowers (Kubiak), Hall (Reich), Cook/Kincaid (Carmichael), MHJ (LaFleur "Adams role"), Goff/ARSB/Jamo/LaPorta (Petzing pass-heavy), Okonkwo/Dowdle/Wan'Dale (reunions). Negative/uncertain: Irving (Zac Robinson zone), London (run-lean), Nabers/Skattebo (Harbaugh/Nagy), Henry/Flowers (Doyle has never called plays), Darnold/JSN/Price (Fleury replaces Kubiak).

## 5. Unresolved items flagged `uncertain: true` (as of Sept 5)
- Puka Nacua: NFL conduct review ongoing; not suspended yet; discipline possible even after Week 1.
- Christian Watson: this project's earlier `context.md` listed him on PUP (ACL, Jan 2026); the Sept 4 roster file shows ACT and WR1 and an Aug 30 CBS piece treats him as draftable. Not resolved - verify before trusting either.
- Alec Pierce: second ankle injection, may miss the start; listed WR1 anyway.
- Jeremiyah Love (ankle), Ashton Jeanty (low ankle), Jadarian Price (held out of preseason), Kyle Monangai (knee), TreVeyon Henderson (ankle), Breece Hall (groin - expected to play), George Kittle (Achilles), Patrick Mahomes (ACL, no preseason), Jonathon Brooks (2 ACLs).
- QB battles / leashes: ATL (Tua vs Penix), LV (Cousins vs Mendoza), CLE (Watson), MIN (Kyler over McCarthy), ARI (Brissett/Beck).
- Backfield splits: PIT (Warren/Dowdle 50/50), NE (Stevenson/Henderson), NYG (Skattebo/Tracy co-starters), WAS (JCM/White), MIN (Mason/Jones), DEN (Dobbins/Harvey/Coleman), TEN (Pollard/Spears/Singleton), CAR (Hubbard/Brooks), LAR (Williams/Corum drives), JAX (Tuten/Rodriguez), SEA (Price/Holani/Wilson), GB (Lloyd/K. Johnson/Brooks).
- Keenan Allen: an SI headline referenced a "potential suspension"; no detail captured.
- Josh Jacobs: exempt list, 0-17 game range, ~6 most likely.

## 6. What could NOT be obtained
- Mike Clay's per-player 2026 target/carry share table (ESPN game projections and the g.espncdn.com PDF are blocked; only the A.J. Brown and Tuten/Rodriguez numbers surfaced in article summaries).
- PFF / 4for4 / Fantasy Points / ETR published projected target-share leaderboards (pages blocked; search snippets did not carry the tables). `proj_target_share_2026` is therefore null for all but A.J. Brown (25%) and Lemon (19%).
- Team-by-team vacated-target percentages beyond the totals listed in section 3.
- 2025 red-zone target/carry shares (pbp downloaded, not processed).
- Verification of the Watson PUP contradiction and of Clay's rookie projections (search cap reached).
