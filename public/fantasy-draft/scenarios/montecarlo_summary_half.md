# Monte Carlo draft simulation (1000 drafts per strategy)

Generated 2026-09-05 17:04. 10 teams, slot 4, snake, 14 rounds (QB, 2 RB, 2 WR, TE, FLEX, D/ST, K, 5 bench); opponents draft from ESPN ADP with each player's measured spread and simple roster rules; your picks follow the strategy preset. Roster score = optimal lineup (QB, 2 RB, 2 WR, TE, FLEX) on projected points plus a quarter of the best five bench players (bench depth matters in head-to-head); floor and ceiling use the Bayesian p10 / p90. All 12 skill rounds are simulated and reported.

## 1. Strategy comparison

| strategy | profile | lineup proj (mean) | p10 of runs | p90 of runs | floor lineup | ceiling lineup | avg RB / WR / QB / TE drafted |
|---|---|---|---|---|---|---|---|
| hero-rb | balanced | 1775 | 1738 | 1819 | 680 | 2297 | 5.0 / 5.0 / 1.0 / 1.0 |
| robust-rb | balanced | 1781 | 1748 | 1822 | 676 | 2302 | 5.0 / 5.0 / 1.0 / 1.0 |
| balanced | balanced | 1769 | 1719 | 1819 | 684 | 2296 | 4.9 / 5.1 / 1.0 / 1.0 |
| zero-rb | balanced | 1678 | 1641 | 1721 | 656 | 2189 | 4.9 / 5.1 / 1.0 / 1.0 |
| wr-heavy | balanced | 1760 | 1714 | 1807 | 688 | 2283 | 4.9 / 5.1 / 1.0 / 1.0 |
| hero-rb | upside | 1782 | 1744 | 1829 | 661 | 2307 | 4.7 / 5.2 / 1.0 / 1.1 |
| hero-rb | safe | 1777 | 1741 | 1824 | 690 | 2307 | 5.0 / 5.0 / 1.0 / 1.0 |

Best mean lineup: **hero-rb / upside**. Differences under ~10 points are noise at this sample size.

## 2. Who to take at your first pick (when available)

Forcing each candidate at pick 4 whenever he is on the board, then drafting normally (hero-rb / balanced). Rows are only comparable on the runs where the candidate was available.

| forced pick | available in % of runs | lineup proj (mean) | floor lineup | ceiling lineup |
|---|---|---|---|---|
| Jahmyr Gibbs | 98% | 1772 | 680 | 2296 |
| Bijan Robinson | 99% | 1767 | 692 | 2290 |
| Ja'Marr Chase | 100% | 1712 | 674 | 2224 |
| Puka Nacua | 100% | 1725 | 665 | 2232 |
| Jaxon Smith-Njigba | 100% | 1711 | 658 | 2214 |
| Amon-Ra St. Brown | 100% | 1695 | 656 | 2202 |
| Jonathan Taylor | 100% | 1724 | 639 | 2217 |
| Christian McCaffrey | 100% | 1721 | 648 | 2234 |

## 3. Most frequent picks by round: hero-rb / balanced

| Rd | Pick | #1 | #2 | #3 | #4 |
|---|---|---|---|---|---|
| 1 | 4 | Jahmyr Gibbs (98%) | Bijan Robinson (2%) | Ja'Marr Chase (0%) |  |
| 2 | 17 | Chase Brown (40%) | James Cook III (27%) | Amon-Ra St. Brown (15%) | Jonathan Taylor (9%) |
| 3 | 24 | Nico Collins (63%) | Chase Brown (20%) | Justin Jefferson (12%) | CeeDee Lamb (4%) |
| 4 | 37 | DeVonta Smith (46%) | Brock Bowers (21%) | George Pickens (13%) | Tee Higgins (12%) |
| 5 | 44 | Tee Higgins (71%) | DeVonta Smith (13%) | Emeka Egbuka (8%) | Brock Bowers (3%) |
| 6 | 57 | Luther Burden III (53%) | Colston Loveland (23%) | Tee Higgins (9%) | Ladd McConkey (5%) |
| 7 | 64 | Luther Burden III (37%) | Tyler Warren (23%) | Bhayshul Tuten (18%) | Jameson Williams (8%) |
| 8 | 77 | Justin Herbert (58%) | Jadarian Price (20%) | Luther Burden III (4%) | Christian Watson (4%) |
| 9 | 84 | Christian Watson (30%) | Justin Herbert (21%) | Tucker Kraft (18%) | Trevor Lawrence (11%) |
| 10 | 97 | Kyle Monangai (32%) | Brian Thomas Jr. (30%) | Parker Washington (10%) | Jaylen Warren (8%) |
| 11 | 104 | Kyle Monangai (44%) | RJ Harvey (34%) | Brian Thomas Jr. (10%) | Jordan Addison (7%) |
| 12 | 117 | RJ Harvey (35%) | Blake Corum (34%) | Kyle Monangai (13%) | Jordan Mason (9%) |

## 3. Most frequent picks by round: robust-rb / balanced

| Rd | Pick | #1 | #2 | #3 | #4 |
|---|---|---|---|---|---|
| 1 | 4 | Jahmyr Gibbs (98%) | Bijan Robinson (2%) | Ja'Marr Chase (0%) |  |
| 2 | 17 | Chase Brown (40%) | James Cook III (27%) | Amon-Ra St. Brown (15%) | Jonathan Taylor (9%) |
| 3 | 24 | Chase Brown (27%) | Ashton Jeanty (25%) | Omarion Hampton (23%) | Kenneth Walker III (11%) |
| 4 | 37 | DeVonta Smith (57%) | Tee Higgins (13%) | Brock Bowers (13%) | George Pickens (12%) |
| 5 | 44 | Tee Higgins (70%) | DeVonta Smith (10%) | Emeka Egbuka (10%) | Brock Bowers (5%) |
| 6 | 57 | Luther Burden III (55%) | Colston Loveland (21%) | Tee Higgins (8%) | Ladd McConkey (6%) |
| 7 | 64 | Luther Burden III (33%) | Tyler Warren (27%) | Jameson Williams (15%) | Drake Maye (7%) |
| 8 | 77 | Justin Herbert (70%) | Christian Watson (8%) | Tucker Kraft (8%) | Luther Burden III (6%) |
| 9 | 84 | Christian Watson (40%) | Tucker Kraft (19%) | Parker Washington (12%) | Trevor Lawrence (8%) |
| 10 | 97 | Brian Thomas Jr. (44%) | Kyle Monangai (19%) | Parker Washington (11%) | Jaylen Warren (7%) |
| 11 | 104 | Kyle Monangai (60%) | RJ Harvey (22%) | Brian Thomas Jr. (8%) | Jordan Addison (7%) |
| 12 | 117 | RJ Harvey (48%) | Blake Corum (29%) | Kyle Monangai (11%) | Jordan Mason (8%) |

## 3. Most frequent picks by round: balanced / balanced

| Rd | Pick | #1 | #2 | #3 | #4 |
|---|---|---|---|---|---|
| 1 | 4 | Jahmyr Gibbs (98%) | Bijan Robinson (2%) | Ja'Marr Chase (0%) |  |
| 2 | 17 | Justin Jefferson (30%) | James Cook III (27%) | Amon-Ra St. Brown (18%) | Chase Brown (9%) |
| 3 | 24 | Nico Collins (60%) | Chase Brown (24%) | Justin Jefferson (11%) | CeeDee Lamb (4%) |
| 4 | 37 | DeVonta Smith (41%) | Brock Bowers (24%) | George Pickens (11%) | Kenneth Walker III (6%) |
| 5 | 44 | Tee Higgins (63%) | DeVonta Smith (14%) | Colston Loveland (5%) | Kyren Williams (5%) |
| 6 | 57 | Luther Burden III (59%) | Colston Loveland (18%) | Tee Higgins (13%) | Ladd McConkey (5%) |
| 7 | 64 | Luther Burden III (32%) | Tyler Warren (20%) | Jameson Williams (15%) | Drake Maye (10%) |
| 8 | 77 | Justin Herbert (68%) | Christian Watson (10%) | Tucker Kraft (7%) | Luther Burden III (4%) |
| 9 | 84 | Christian Watson (39%) | Tucker Kraft (15%) | Parker Washington (12%) | Trevor Lawrence (7%) |
| 10 | 97 | Kyle Monangai (63%) | Brian Thomas Jr. (12%) | Jaylen Warren (8%) | Christian Watson (5%) |
| 11 | 104 | RJ Harvey (62%) | Kyle Monangai (26%) | Blake Corum (4%) | Brian Thomas Jr. (4%) |
| 12 | 117 | Blake Corum (48%) | RJ Harvey (21%) | Jordan Mason (15%) | J.K. Dobbins (8%) |

## 4. Chance key players are still there at your picks (simulated, ESPN room)

| player | pos | ADP used | #4 | #17 | #24 | #37 | #44 | #57 | #64 | #77 | #84 | #97 | #104 | #117 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Jahmyr Gibbs | RB | 1.3 | 98% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Bijan Robinson | RB | 2.4 | 99% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Ja'Marr Chase | WR | 4.3 | 100% | 1% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Puka Nacua | WR | 5.3 | 100% | 2% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Jaxon Smith-Njigba | WR | 6.3 | 100% | 5% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Amon-Ra St. Brown | WR | 8.4 | 100% | 20% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Christian McCaffrey | RB | 7.7 | 100% | 21% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Jonathan Taylor | RB | 6.2 | 100% | 10% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| De'Von Achane | RB | 12.4 | 100% | 72% | 5% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Chase Brown | RB | 17.1 | 100% | 96% | 28% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| James Cook III | RB | 10.1 | 100% | 47% | 1% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Kenneth Walker III | RB | 24.8 | 100% | 100% | 90% | 9% | 1% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Omarion Hampton | RB | 18.1 | 100% | 94% | 44% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Derrick Henry | RB | 16.5 | 100% | 98% | 27% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Ashton Jeanty | RB | 21.8 | 100% | 100% | 75% | 2% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Saquon Barkley | RB | 14.0 | 100% | 81% | 13% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Brock Bowers | TE | 23.9 | 100% | 96% | 84% | 29% | 3% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Trey McBride | TE | 23.0 | 100% | 95% | 80% | 22% | 8% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Colston Loveland | TE | 42.4 | 100% | 100% | 100% | 93% | 79% | 33% | 3% | 0% | 0% | 0% | 0% | 0% |
| Tyler Warren | TE | 52.1 | 100% | 100% | 100% | 100% | 98% | 72% | 42% | 1% | 0% | 0% | 0% | 0% |
| Josh Allen | QB | 19.1 | 100% | 89% | 65% | 11% | 3% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Lamar Jackson | QB | 34.5 | 100% | 100% | 99% | 76% | 47% | 6% | 1% | 0% | 0% | 0% | 0% | 0% |
| Jayden Daniels | QB | 53.1 | 100% | 100% | 100% | 98% | 94% | 66% | 45% | 7% | 2% | 0% | 0% | 0% |
| Drake Maye | QB | 47.2 | 100% | 100% | 100% | 98% | 91% | 46% | 24% | 1% | 0% | 0% | 0% | 0% |
| Joe Burrow | QB | 53.5 | 100% | 100% | 100% | 100% | 99% | 73% | 44% | 3% | 0% | 0% | 0% | 0% |
| Jalen Hurts | QB | 54.7 | 100% | 100% | 100% | 98% | 94% | 69% | 51% | 17% | 7% | 0% | 0% | 0% |
| Malik Nabers | WR | 35.0 | 100% | 100% | 100% | 71% | 13% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| A.J. Brown | WR | 21.0 | 100% | 100% | 86% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Drake London | WR | 20.4 | 100% | 100% | 84% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Nico Collins | WR | 25.7 | 100% | 100% | 99% | 2% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| DeVonta Smith | WR | 36.6 | 100% | 100% | 100% | 80% | 14% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Zay Flowers | WR | 44.1 | 100% | 100% | 100% | 99% | 81% | 6% | 0% | 0% | 0% | 0% | 0% | 0% |
| Garrett Wilson | WR | 37.1 | 100% | 100% | 100% | 84% | 30% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Breece Hall | RB | 35.9 | 100% | 100% | 100% | 83% | 37% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Jeremiyah Love | RB | 26.0 | 100% | 100% | 96% | 12% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| MarShawn Lloyd | RB | 115.4 | 100% | 100% | 100% | 100% | 100% | 100% | 99% | 94% | 90% | 75% | 69% | 50% |
