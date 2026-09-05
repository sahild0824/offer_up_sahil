# Monte Carlo draft simulation (1000 drafts per strategy)

Generated 2026-09-05 02:25. 10 teams, slot 4, snake, 14 rounds (QB, 2 RB, 2 WR, TE, FLEX, D/ST, K, 5 bench); opponents draft from ESPN ADP with each player's measured spread and simple roster rules; your picks follow the strategy preset. Roster score = optimal lineup (QB, 2 RB, 2 WR, TE, FLEX) on projected points plus a quarter of the best five bench players (bench depth matters in head-to-head); floor and ceiling use the Bayesian p10 / p90. All 12 skill rounds are simulated and reported.

## 1. Strategy comparison

| strategy | profile | lineup proj (mean) | p10 of runs | p90 of runs | floor lineup | ceiling lineup | avg RB / WR / QB / TE drafted |
|---|---|---|---|---|---|---|---|
| hero-rb | balanced | 1770 | 1735 | 1816 | 679 | 2294 | 5.0 / 5.0 / 1.0 / 1.0 |
| robust-rb | balanced | 1777 | 1744 | 1817 | 674 | 2298 | 5.0 / 5.0 / 1.0 / 1.0 |
| balanced | balanced | 1765 | 1718 | 1812 | 682 | 2289 | 4.9 / 5.1 / 1.0 / 1.0 |
| zero-rb | balanced | 1674 | 1636 | 1715 | 652 | 2184 | 4.8 / 5.2 / 1.0 / 1.0 |
| wr-heavy | balanced | 1750 | 1708 | 1798 | 681 | 2270 | 4.9 / 5.1 / 1.0 / 1.0 |
| hero-rb | upside | 1781 | 1745 | 1827 | 660 | 2307 | 4.7 / 5.1 / 1.0 / 1.2 |
| hero-rb | safe | 1771 | 1735 | 1815 | 688 | 2301 | 5.0 / 5.0 / 1.0 / 1.0 |

Best mean lineup: **hero-rb / upside**. Differences under ~10 points are noise at this sample size.

## 2. Who to take at your first pick (when available)

Forcing each candidate at pick 4 whenever he is on the board, then drafting normally (hero-rb / balanced). Rows are only comparable on the runs where the candidate was available.

| forced pick | available in % of runs | lineup proj (mean) | floor lineup | ceiling lineup |
|---|---|---|---|---|
| Jahmyr Gibbs | 97% | 1768 | 679 | 2292 |
| Bijan Robinson | 98% | 1762 | 690 | 2287 |
| Ja'Marr Chase | 100% | 1707 | 668 | 2220 |
| Puka Nacua | 100% | 1721 | 660 | 2229 |
| Jaxon Smith-Njigba | 100% | 1707 | 652 | 2211 |
| Amon-Ra St. Brown | 100% | 1692 | 652 | 2201 |
| Jonathan Taylor | 100% | 1721 | 638 | 2213 |
| Christian McCaffrey | 100% | 1716 | 647 | 2229 |

## 3. Most frequent picks by round: hero-rb / balanced

| Rd | Pick | #1 | #2 | #3 | #4 |
|---|---|---|---|---|---|
| 1 | 4 | Jahmyr Gibbs (97%) | Bijan Robinson (2%) | Ja'Marr Chase (1%) |  |
| 2 | 17 | Chase Brown (40%) | James Cook III (27%) | Amon-Ra St. Brown (16%) | Jonathan Taylor (6%) |
| 3 | 24 | Nico Collins (63%) | Chase Brown (26%) | Justin Jefferson (7%) | CeeDee Lamb (2%) |
| 4 | 37 | DeVonta Smith (57%) | George Pickens (15%) | Brock Bowers (13%) | Tee Higgins (7%) |
| 5 | 44 | Tee Higgins (72%) | DeVonta Smith (15%) | Emeka Egbuka (7%) | Trey McBride (2%) |
| 6 | 57 | Luther Burden III (52%) | Colston Loveland (18%) | Tee Higgins (11%) | Ladd McConkey (7%) |
| 7 | 64 | Luther Burden III (39%) | Bhayshul Tuten (22%) | Tyler Warren (17%) | Jameson Williams (9%) |
| 8 | 77 | Justin Herbert (63%) | Jadarian Price (16%) | Tucker Kraft (6%) | Luther Burden III (5%) |
| 9 | 84 | Tucker Kraft (29%) | Christian Watson (28%) | Justin Herbert (17%) | Trevor Lawrence (12%) |
| 10 | 97 | Kyle Monangai (40%) | Brian Thomas Jr. (28%) | Parker Washington (8%) | Tucker Kraft (6%) |
| 11 | 104 | Kyle Monangai (44%) | RJ Harvey (41%) | Brian Thomas Jr. (7%) | Jordan Addison (5%) |
| 12 | 117 | RJ Harvey (39%) | Blake Corum (39%) | Kyle Monangai (10%) | J.K. Dobbins (6%) |

## 3. Most frequent picks by round: robust-rb / balanced

| Rd | Pick | #1 | #2 | #3 | #4 |
|---|---|---|---|---|---|
| 1 | 4 | Jahmyr Gibbs (97%) | Bijan Robinson (2%) | Ja'Marr Chase (1%) |  |
| 2 | 17 | Chase Brown (40%) | James Cook III (27%) | Amon-Ra St. Brown (16%) | Jonathan Taylor (6%) |
| 3 | 24 | Chase Brown (32%) | Omarion Hampton (29%) | Ashton Jeanty (25%) | Kenneth Walker III (7%) |
| 4 | 37 | DeVonta Smith (66%) | George Pickens (16%) | Tee Higgins (7%) | Brock Bowers (5%) |
| 5 | 44 | Tee Higgins (75%) | DeVonta Smith (13%) | Emeka Egbuka (7%) | Brock Bowers (4%) |
| 6 | 57 | Luther Burden III (55%) | Colston Loveland (13%) | Tee Higgins (11%) | Ladd McConkey (9%) |
| 7 | 64 | Luther Burden III (34%) | Jameson Williams (24%) | Tyler Warren (22%) | Drake Maye (4%) |
| 8 | 77 | Justin Herbert (73%) | Tucker Kraft (10%) | Luther Burden III (7%) | Christian Watson (6%) |
| 9 | 84 | Tucker Kraft (36%) | Christian Watson (34%) | Trevor Lawrence (11%) | Justin Herbert (6%) |
| 10 | 97 | Brian Thomas Jr. (50%) | Kyle Monangai (18%) | Parker Washington (10%) | Christian Watson (6%) |
| 11 | 104 | Kyle Monangai (71%) | RJ Harvey (21%) | Jordan Addison (4%) | Brian Thomas Jr. (3%) |
| 12 | 117 | RJ Harvey (60%) | Blake Corum (27%) | Kyle Monangai (6%) | J.K. Dobbins (3%) |

## 3. Most frequent picks by round: balanced / balanced

| Rd | Pick | #1 | #2 | #3 | #4 |
|---|---|---|---|---|---|
| 1 | 4 | Jahmyr Gibbs (97%) | Bijan Robinson (2%) | Ja'Marr Chase (1%) |  |
| 2 | 17 | Justin Jefferson (29%) | James Cook III (27%) | Amon-Ra St. Brown (20%) | Chase Brown (9%) |
| 3 | 24 | Nico Collins (55%) | Chase Brown (34%) | Justin Jefferson (6%) | CeeDee Lamb (2%) |
| 4 | 37 | DeVonta Smith (53%) | Brock Bowers (16%) | George Pickens (13%) | Tee Higgins (4%) |
| 5 | 44 | Colston Loveland (37%) | Tee Higgins (36%) | DeVonta Smith (18%) | Javonte Williams (3%) |
| 6 | 57 | Luther Burden III (50%) | Tee Higgins (30%) | Ladd McConkey (6%) | Colston Loveland (6%) |
| 7 | 64 | Luther Burden III (43%) | Jameson Williams (20%) | Tyler Warren (10%) | Bhayshul Tuten (8%) |
| 8 | 77 | Justin Herbert (74%) | Christian Watson (10%) | Tucker Kraft (5%) | Luther Burden III (4%) |
| 9 | 84 | Christian Watson (40%) | Tucker Kraft (17%) | Jaylen Warren (10%) | Parker Washington (9%) |
| 10 | 97 | Kyle Monangai (70%) | Brian Thomas Jr. (12%) | Christian Watson (4%) | Jaylen Warren (4%) |
| 11 | 104 | RJ Harvey (68%) | Kyle Monangai (25%) | Blake Corum (4%) | Brian Thomas Jr. (1%) |
| 12 | 117 | Blake Corum (57%) | RJ Harvey (22%) | J.K. Dobbins (8%) | Jordan Mason (8%) |

## 4. Chance key players are still there at your picks (simulated, ESPN room)

| player | pos | ADP used | #4 | #17 | #24 | #37 | #44 | #57 | #64 | #77 | #84 | #97 | #104 | #117 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Jahmyr Gibbs | RB | 1.3 | 97% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Bijan Robinson | RB | 2.4 | 98% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Ja'Marr Chase | WR | 4.3 | 100% | 1% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Puka Nacua | WR | 5.3 | 100% | 2% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Jaxon Smith-Njigba | WR | 6.3 | 100% | 6% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Amon-Ra St. Brown | WR | 8.4 | 100% | 22% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Christian McCaffrey | RB | 7.7 | 100% | 19% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Jonathan Taylor | RB | 6.2 | 100% | 7% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| De'Von Achane | RB | 12.4 | 100% | 75% | 6% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Chase Brown | RB | 17.1 | 100% | 97% | 33% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| James Cook III | RB | 10.1 | 100% | 48% | 1% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Kenneth Walker III | RB | 24.8 | 100% | 100% | 96% | 6% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Omarion Hampton | RB | 18.1 | 100% | 96% | 52% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Derrick Henry | RB | 16.5 | 100% | 98% | 36% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Ashton Jeanty | RB | 21.8 | 100% | 100% | 82% | 2% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Saquon Barkley | RB | 14.0 | 100% | 83% | 17% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Brock Bowers | TE | 23.9 | 100% | 94% | 78% | 19% | 2% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Trey McBride | TE | 23.0 | 100% | 94% | 75% | 14% | 4% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Colston Loveland | TE | 42.4 | 100% | 100% | 100% | 88% | 69% | 20% | 1% | 0% | 0% | 0% | 0% | 0% |
| Tyler Warren | TE | 52.1 | 100% | 100% | 100% | 99% | 95% | 57% | 27% | 1% | 0% | 0% | 0% | 0% |
| Josh Allen | QB | 19.1 | 100% | 85% | 55% | 6% | 1% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Lamar Jackson | QB | 34.5 | 100% | 100% | 98% | 64% | 32% | 3% | 0% | 0% | 0% | 0% | 0% | 0% |
| Jayden Daniels | QB | 53.1 | 100% | 100% | 100% | 98% | 92% | 61% | 35% | 5% | 2% | 0% | 0% | 0% |
| Drake Maye | QB | 47.2 | 100% | 100% | 100% | 96% | 85% | 36% | 16% | 0% | 0% | 0% | 0% | 0% |
| Joe Burrow | QB | 53.5 | 100% | 100% | 100% | 100% | 99% | 66% | 34% | 1% | 0% | 0% | 0% | 0% |
| Jalen Hurts | QB | 54.7 | 100% | 100% | 100% | 97% | 91% | 63% | 44% | 11% | 6% | 0% | 0% | 0% |
| Malik Nabers | WR | 35.0 | 100% | 100% | 100% | 80% | 17% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| A.J. Brown | WR | 21.0 | 100% | 100% | 84% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Drake London | WR | 20.4 | 100% | 100% | 82% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Nico Collins | WR | 25.7 | 100% | 100% | 99% | 3% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| DeVonta Smith | WR | 36.6 | 100% | 100% | 100% | 89% | 16% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Zay Flowers | WR | 44.1 | 100% | 100% | 100% | 100% | 89% | 8% | 0% | 0% | 0% | 0% | 0% | 0% |
| Garrett Wilson | WR | 37.1 | 100% | 100% | 100% | 92% | 37% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Breece Hall | RB | 35.9 | 100% | 100% | 100% | 84% | 30% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Jeremiyah Love | RB | 26.0 | 100% | 100% | 98% | 9% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| MarShawn Lloyd | RB | 115.4 | 100% | 100% | 100% | 100% | 100% | 100% | 99% | 94% | 91% | 77% | 70% | 56% |
