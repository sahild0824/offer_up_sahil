# Monte Carlo draft simulation (1000 drafts per strategy)

Generated 2026-09-05 02:30. 10 teams, slot 4, snake, 14 rounds (QB, 2 RB, 2 WR, TE, FLEX, D/ST, K, 5 bench); opponents draft from ESPN ADP with each player's measured spread and simple roster rules; your picks follow the strategy preset. Roster score = optimal lineup (QB, 2 RB, 2 WR, TE, FLEX) on projected points plus a quarter of the best five bench players (bench depth matters in head-to-head); floor and ceiling use the Bayesian p10 / p90. All 12 skill rounds are simulated and reported.

## 1. Strategy comparison

| strategy | profile | lineup proj (mean) | p10 of runs | p90 of runs | floor lineup | ceiling lineup | avg RB / WR / QB / TE drafted |
|---|---|---|---|---|---|---|---|
| hero-rb | balanced | 1440 | 1414 | 1469 | 532 | 1867 | 4.8 / 5.0 / 1.0 / 1.1 |
| robust-rb | balanced | 1439 | 1407 | 1473 | 533 | 1870 | 4.7 / 5.1 / 1.0 / 1.2 |
| balanced | balanced | 1441 | 1408 | 1475 | 535 | 1872 | 4.7 / 5.1 / 1.0 / 1.2 |
| zero-rb | balanced | 1402 | 1381 | 1424 | 511 | 1817 | 5.0 / 5.0 / 1.0 / 1.0 |
| wr-heavy | balanced | 1425 | 1402 | 1448 | 529 | 1840 | 4.8 / 5.1 / 1.0 / 1.1 |
| hero-rb | upside | 1433 | 1412 | 1457 | 516 | 1859 | 4.8 / 5.1 / 1.0 / 1.1 |
| hero-rb | safe | 1437 | 1411 | 1463 | 544 | 1867 | 5.0 / 5.0 / 1.0 / 1.0 |

Best mean lineup: **balanced / balanced**. Differences under ~10 points are noise at this sample size.

## 2. Who to take at your first pick (when available)

Forcing each candidate at pick 4 whenever he is on the board, then drafting normally (hero-rb / balanced). Rows are only comparable on the runs where the candidate was available.

| forced pick | available in % of runs | lineup proj (mean) | floor lineup | ceiling lineup |
|---|---|---|---|---|
| Jahmyr Gibbs | 0% | 1439 | 531 | 1867 |
| Bijan Robinson | 4% | 1439 | 531 | 1867 |
| Ja'Marr Chase | 46% | 1438 | 530 | 1866 |
| Puka Nacua | 84% | 1442 | 530 | 1874 |
| Jaxon Smith-Njigba | 92% | 1434 | 524 | 1861 |
| Amon-Ra St. Brown | 98% | 1414 | 519 | 1839 |
| Jonathan Taylor | 97% | 1467 | 522 | 1883 |
| Christian McCaffrey | 96% | 1450 | 528 | 1887 |

## 3. Most frequent picks by round: hero-rb / balanced

| Rd | Pick | #1 | #2 | #3 | #4 |
|---|---|---|---|---|---|
| 1 | 4 | Puka Nacua (51%) | Ja'Marr Chase (45%) | Bijan Robinson (4%) | Jahmyr Gibbs (0%) |
| 2 | 17 | Kenneth Walker III (45%) | Chase Brown (44%) | Saquon Barkley (6%) | Justin Jefferson (2%) |
| 3 | 24 | Nico Collins (56%) | George Pickens (25%) | Kenneth Walker III (13%) | A.J. Brown (3%) |
| 4 | 37 | Tee Higgins (62%) | DeVonta Smith (27%) | Brock Bowers (10%) | Colston Loveland (0%) |
| 5 | 44 | Tee Higgins (33%) | Colston Loveland (26%) | Emeka Egbuka (16%) | Zay Flowers (11%) |
| 6 | 57 | Luther Burden III (48%) | Bhayshul Tuten (40%) | D'Andre Swift (3%) | Jaylen Waddle (3%) |
| 7 | 64 | Luther Burden III (34%) | Jadarian Price (20%) | TreVeyon Henderson (14%) | Jameson Williams (7%) |
| 8 | 77 | Justin Herbert (62%) | Tucker Kraft (15%) | Christian Watson (8%) | Trevor Lawrence (5%) |
| 9 | 84 | Tucker Kraft (22%) | Trevor Lawrence (20%) | Blake Corum (20%) | Jaylen Warren (10%) |
| 10 | 97 | Blake Corum (46%) | Brian Thomas Jr. (18%) | Jordan Mason (13%) | Tucker Kraft (10%) |
| 11 | 104 | Jordan Mason (62%) | Blake Corum (17%) | Kyle Monangai (12%) | Jordan Addison (3%) |
| 12 | 117 | Jacory Croskey-Merritt (37%) | Kyle Monangai (28%) | Jordan Mason (17%) | J.K. Dobbins (4%) |

## 3. Most frequent picks by round: robust-rb / balanced

| Rd | Pick | #1 | #2 | #3 | #4 |
|---|---|---|---|---|---|
| 1 | 4 | Puka Nacua (51%) | Ja'Marr Chase (45%) | Bijan Robinson (4%) | Jahmyr Gibbs (0%) |
| 2 | 17 | Kenneth Walker III (45%) | Chase Brown (44%) | Saquon Barkley (6%) | Justin Jefferson (2%) |
| 3 | 24 | Nico Collins (36%) | Kenneth Walker III (24%) | Brock Bowers (14%) | Ashton Jeanty (13%) |
| 4 | 37 | Tee Higgins (64%) | DeVonta Smith (28%) | Brock Bowers (7%) | Colston Loveland (0%) |
| 5 | 44 | Tee Higgins (31%) | Colston Loveland (23%) | Emeka Egbuka (18%) | Zay Flowers (12%) |
| 6 | 57 | Luther Burden III (90%) | Jaylen Waddle (5%) | Jameson Williams (2%) | Colston Loveland (1%) |
| 7 | 64 | Christian Watson (23%) | Jadarian Price (14%) | Jameson Williams (12%) | Tucker Kraft (12%) |
| 8 | 77 | Justin Herbert (58%) | Trevor Lawrence (14%) | Tucker Kraft (13%) | Christian Watson (8%) |
| 9 | 84 | Blake Corum (22%) | Jaylen Warren (15%) | Tucker Kraft (13%) | Brian Thomas Jr. (10%) |
| 10 | 97 | Blake Corum (47%) | Jordan Mason (24%) | Tucker Kraft (16%) | Brian Thomas Jr. (6%) |
| 11 | 104 | Jordan Mason (56%) | Kyle Monangai (21%) | Blake Corum (15%) | J.K. Dobbins (4%) |
| 12 | 117 | Jacory Croskey-Merritt (42%) | Kyle Monangai (28%) | Jordan Mason (12%) | RJ Harvey (4%) |

## 3. Most frequent picks by round: balanced / balanced

| Rd | Pick | #1 | #2 | #3 | #4 |
|---|---|---|---|---|---|
| 1 | 4 | Puka Nacua (51%) | Ja'Marr Chase (45%) | Bijan Robinson (4%) | Jahmyr Gibbs (0%) |
| 2 | 17 | Kenneth Walker III (45%) | Chase Brown (42%) | Saquon Barkley (6%) | Justin Jefferson (4%) |
| 3 | 24 | Nico Collins (43%) | Kenneth Walker III (24%) | Brock Bowers (18%) | George Pickens (6%) |
| 4 | 37 | Tee Higgins (37%) | DeVonta Smith (28%) | Colston Loveland (21%) | Brock Bowers (6%) |
| 5 | 44 | Tee Higgins (47%) | Colston Loveland (17%) | Emeka Egbuka (13%) | Zay Flowers (9%) |
| 6 | 57 | Luther Burden III (87%) | Jaylen Waddle (6%) | D'Andre Swift (3%) | Jameson Williams (1%) |
| 7 | 64 | Christian Watson (24%) | Jadarian Price (16%) | Jameson Williams (14%) | Joe Burrow (8%) |
| 8 | 77 | Justin Herbert (57%) | Trevor Lawrence (14%) | Christian Watson (10%) | Tucker Kraft (10%) |
| 9 | 84 | Blake Corum (24%) | Jaylen Warren (16%) | Brian Thomas Jr. (11%) | Tucker Kraft (10%) |
| 10 | 97 | Blake Corum (43%) | Jordan Mason (24%) | Tucker Kraft (21%) | Brian Thomas Jr. (6%) |
| 11 | 104 | Jordan Mason (54%) | Kyle Monangai (21%) | Blake Corum (17%) | J.K. Dobbins (4%) |
| 12 | 117 | Jacory Croskey-Merritt (41%) | Kyle Monangai (26%) | Jordan Mason (14%) | J.K. Dobbins (4%) |

## 4. Chance key players are still there at your picks (simulated, ESPN room)

| player | pos | ADP used | #4 | #17 | #24 | #37 | #44 | #57 | #64 | #77 | #84 | #97 | #104 | #117 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Jahmyr Gibbs | RB | 1.3 | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Bijan Robinson | RB | 2.4 | 4% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Ja'Marr Chase | WR | 4.3 | 46% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Puka Nacua | WR | 5.3 | 84% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Jaxon Smith-Njigba | WR | 6.3 | 92% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Amon-Ra St. Brown | WR | 8.4 | 98% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Christian McCaffrey | RB | 7.7 | 96% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Jonathan Taylor | RB | 6.2 | 97% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| De'Von Achane | RB | 12.4 | 100% | 1% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Chase Brown | RB | 17.1 | 100% | 44% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| James Cook III | RB | 10.1 | 100% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Kenneth Walker III | RB | 24.8 | 100% | 97% | 24% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Omarion Hampton | RB | 18.1 | 100% | 58% | 3% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Derrick Henry | RB | 16.5 | 100% | 36% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Ashton Jeanty | RB | 21.8 | 100% | 89% | 15% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Saquon Barkley | RB | 14.0 | 100% | 9% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Brock Bowers | TE | 23.9 | 95% | 70% | 43% | 10% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Trey McBride | TE | 23.0 | 95% | 68% | 39% | 7% | 3% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Colston Loveland | TE | 42.4 | 100% | 100% | 97% | 62% | 37% | 2% | 0% | 0% | 0% | 0% | 0% | 0% |
| Tyler Warren | TE | 52.1 | 100% | 100% | 100% | 91% | 75% | 20% | 7% | 0% | 0% | 0% | 0% | 0% |
| Josh Allen | QB | 19.1 | 95% | 56% | 25% | 1% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Lamar Jackson | QB | 34.5 | 100% | 98% | 87% | 28% | 9% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Jayden Daniels | QB | 53.1 | 100% | 100% | 100% | 95% | 81% | 19% | 5% | 0% | 0% | 0% | 0% | 0% |
| Drake Maye | QB | 47.2 | 100% | 99% | 96% | 74% | 56% | 16% | 7% | 1% | 0% | 0% | 0% | 0% |
| Joe Burrow | QB | 53.5 | 100% | 100% | 100% | 94% | 81% | 27% | 11% | 0% | 0% | 0% | 0% | 0% |
| Jalen Hurts | QB | 54.7 | 100% | 99% | 97% | 87% | 74% | 36% | 19% | 5% | 2% | 0% | 0% | 0% |
| Malik Nabers | WR | 35.0 | 100% | 100% | 98% | 14% | 1% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| A.J. Brown | WR | 21.0 | 100% | 88% | 8% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Drake London | WR | 20.4 | 100% | 86% | 3% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Nico Collins | WR | 25.7 | 100% | 100% | 56% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| DeVonta Smith | WR | 36.6 | 100% | 100% | 99% | 30% | 1% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Zay Flowers | WR | 44.1 | 100% | 100% | 100% | 77% | 40% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Garrett Wilson | WR | 37.1 | 100% | 100% | 100% | 27% | 3% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Breece Hall | RB | 35.9 | 100% | 100% | 100% | 16% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Jeremiyah Love | RB | 26.0 | 100% | 98% | 56% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| MarShawn Lloyd | RB | 115.4 | 100% | 100% | 100% | 100% | 100% | 99% | 98% | 90% | 81% | 61% | 52% | 36% |
