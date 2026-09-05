# Monte Carlo draft simulation (1000 drafts per strategy)

Generated 2026-09-05 17:04. 10 teams, slot 4, snake, 14 rounds (QB, 2 RB, 2 WR, TE, FLEX, D/ST, K, 5 bench); opponents draft from ESPN ADP with each player's measured spread and simple roster rules; your picks follow the strategy preset. Roster score = optimal lineup (QB, 2 RB, 2 WR, TE, FLEX) on projected points plus a quarter of the best five bench players (bench depth matters in head-to-head); floor and ceiling use the Bayesian p10 / p90. All 12 skill rounds are simulated and reported.

## 1. Strategy comparison

| strategy | profile | lineup proj (mean) | p10 of runs | p90 of runs | floor lineup | ceiling lineup | avg RB / WR / QB / TE drafted |
|---|---|---|---|---|---|---|---|
| hero-rb | balanced | 1440 | 1412 | 1470 | 533 | 1867 | 4.9 / 5.1 / 1.0 / 1.0 |
| robust-rb | balanced | 1439 | 1407 | 1472 | 532 | 1872 | 4.8 / 5.1 / 1.0 / 1.0 |
| balanced | balanced | 1444 | 1413 | 1476 | 537 | 1877 | 4.9 / 5.1 / 1.0 / 1.0 |
| zero-rb | balanced | 1402 | 1379 | 1423 | 514 | 1815 | 5.0 / 5.0 / 1.0 / 1.0 |
| wr-heavy | balanced | 1428 | 1403 | 1455 | 532 | 1845 | 4.9 / 5.1 / 1.0 / 1.0 |
| hero-rb | upside | 1433 | 1407 | 1461 | 517 | 1857 | 4.7 / 5.1 / 1.0 / 1.2 |
| hero-rb | safe | 1440 | 1413 | 1470 | 546 | 1872 | 5.0 / 5.0 / 1.0 / 1.0 |

Best mean lineup: **balanced / balanced**. Differences under ~10 points are noise at this sample size.

## 2. Who to take at your first pick (when available)

Forcing each candidate at pick 4 whenever he is on the board, then drafting normally (hero-rb / balanced). Rows are only comparable on the runs where the candidate was available.

| forced pick | available in % of runs | lineup proj (mean) | floor lineup | ceiling lineup |
|---|---|---|---|---|
| Jahmyr Gibbs | 1% | 1439 | 533 | 1867 |
| Bijan Robinson | 3% | 1439 | 533 | 1867 |
| Ja'Marr Chase | 50% | 1439 | 533 | 1866 |
| Puka Nacua | 85% | 1444 | 533 | 1875 |
| Jaxon Smith-Njigba | 92% | 1435 | 526 | 1862 |
| Amon-Ra St. Brown | 98% | 1415 | 521 | 1839 |
| Jonathan Taylor | 94% | 1465 | 523 | 1882 |
| Christian McCaffrey | 95% | 1449 | 528 | 1887 |

## 3. Most frequent picks by round: hero-rb / balanced

| Rd | Pick | #1 | #2 | #3 | #4 |
|---|---|---|---|---|---|
| 1 | 4 | Puka Nacua (48%) | Ja'Marr Chase (48%) | Bijan Robinson (3%) | Jahmyr Gibbs (1%) |
| 2 | 17 | Kenneth Walker III (49%) | Chase Brown (37%) | Justin Jefferson (6%) | Saquon Barkley (4%) |
| 3 | 24 | Nico Collins (50%) | George Pickens (26%) | Kenneth Walker III (13%) | Brock Bowers (5%) |
| 4 | 37 | Tee Higgins (62%) | DeVonta Smith (25%) | Brock Bowers (11%) | Kyren Williams (1%) |
| 5 | 44 | Colston Loveland (33%) | Tee Higgins (27%) | Emeka Egbuka (10%) | Zay Flowers (8%) |
| 6 | 57 | Luther Burden III (55%) | Bhayshul Tuten (30%) | Jaylen Waddle (5%) | D'Andre Swift (4%) |
| 7 | 64 | Jadarian Price (27%) | Luther Burden III (25%) | TreVeyon Henderson (13%) | Christian Watson (8%) |
| 8 | 77 | Justin Herbert (64%) | Tucker Kraft (11%) | Christian Watson (8%) | Trevor Lawrence (4%) |
| 9 | 84 | Blake Corum (28%) | Tucker Kraft (20%) | Trevor Lawrence (14%) | Jaylen Warren (11%) |
| 10 | 97 | Blake Corum (42%) | Brian Thomas Jr. (26%) | Jordan Mason (16%) | Jordan Addison (9%) |
| 11 | 104 | Jordan Mason (61%) | Blake Corum (16%) | Kyle Monangai (13%) | Jacory Croskey-Merritt (3%) |
| 12 | 117 | Jacory Croskey-Merritt (32%) | Kyle Monangai (29%) | Jordan Mason (13%) | J.K. Dobbins (5%) |

## 3. Most frequent picks by round: robust-rb / balanced

| Rd | Pick | #1 | #2 | #3 | #4 |
|---|---|---|---|---|---|
| 1 | 4 | Puka Nacua (48%) | Ja'Marr Chase (48%) | Bijan Robinson (3%) | Jahmyr Gibbs (1%) |
| 2 | 17 | Kenneth Walker III (49%) | Chase Brown (37%) | Justin Jefferson (6%) | Saquon Barkley (4%) |
| 3 | 24 | Nico Collins (37%) | Kenneth Walker III (21%) | Brock Bowers (18%) | Ashton Jeanty (11%) |
| 4 | 37 | Tee Higgins (66%) | DeVonta Smith (25%) | Brock Bowers (9%) | Kyren Williams (0%) |
| 5 | 44 | Colston Loveland (28%) | Tee Higgins (24%) | Emeka Egbuka (12%) | Jaylen Waddle (10%) |
| 6 | 57 | Luther Burden III (83%) | Jaylen Waddle (7%) | Jameson Williams (4%) | Bhayshul Tuten (1%) |
| 7 | 64 | Christian Watson (23%) | Jadarian Price (17%) | Joe Burrow (12%) | Bhayshul Tuten (9%) |
| 8 | 77 | Justin Herbert (52%) | Tucker Kraft (16%) | Trevor Lawrence (9%) | Christian Watson (9%) |
| 9 | 84 | Blake Corum (21%) | Jaylen Warren (17%) | Brian Thomas Jr. (15%) | Tucker Kraft (12%) |
| 10 | 97 | Blake Corum (53%) | Jordan Mason (29%) | Brian Thomas Jr. (9%) | Jordan Addison (4%) |
| 11 | 104 | Jordan Mason (54%) | Kyle Monangai (24%) | Blake Corum (11%) | Jacory Croskey-Merritt (4%) |
| 12 | 117 | Jacory Croskey-Merritt (40%) | Kyle Monangai (24%) | Jordan Mason (8%) | RJ Harvey (7%) |

## 3. Most frequent picks by round: balanced / balanced

| Rd | Pick | #1 | #2 | #3 | #4 |
|---|---|---|---|---|---|
| 1 | 4 | Puka Nacua (48%) | Ja'Marr Chase (48%) | Bijan Robinson (3%) | Jahmyr Gibbs (1%) |
| 2 | 17 | Kenneth Walker III (49%) | Chase Brown (35%) | Justin Jefferson (8%) | Saquon Barkley (4%) |
| 3 | 24 | Nico Collins (41%) | Brock Bowers (22%) | Kenneth Walker III (21%) | George Pickens (5%) |
| 4 | 37 | Tee Higgins (38%) | DeVonta Smith (25%) | Colston Loveland (20%) | Brock Bowers (7%) |
| 5 | 44 | Tee Higgins (37%) | Colston Loveland (21%) | D'Andre Swift (14%) | Emeka Egbuka (9%) |
| 6 | 57 | Luther Burden III (84%) | Jaylen Waddle (7%) | D'Andre Swift (3%) | Jameson Williams (2%) |
| 7 | 64 | Christian Watson (27%) | Jadarian Price (16%) | Joe Burrow (12%) | Bhayshul Tuten (9%) |
| 8 | 77 | Justin Herbert (54%) | Christian Watson (12%) | Tucker Kraft (10%) | Trevor Lawrence (9%) |
| 9 | 84 | Brian Thomas Jr. (20%) | Blake Corum (19%) | Jaylen Warren (17%) | Tucker Kraft (8%) |
| 10 | 97 | Blake Corum (53%) | Jordan Mason (25%) | Brian Thomas Jr. (11%) | Jordan Addison (6%) |
| 11 | 104 | Jordan Mason (55%) | Kyle Monangai (21%) | Blake Corum (14%) | Jacory Croskey-Merritt (4%) |
| 12 | 117 | Jacory Croskey-Merritt (39%) | Kyle Monangai (24%) | Jordan Mason (10%) | RJ Harvey (7%) |

## 4. Chance key players are still there at your picks (simulated, ESPN room)

| player | pos | ADP used | #4 | #17 | #24 | #37 | #44 | #57 | #64 | #77 | #84 | #97 | #104 | #117 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Jahmyr Gibbs | RB | 1.3 | 1% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Bijan Robinson | RB | 2.4 | 3% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Ja'Marr Chase | WR | 4.3 | 50% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Puka Nacua | WR | 5.3 | 85% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Jaxon Smith-Njigba | WR | 6.3 | 92% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Amon-Ra St. Brown | WR | 8.4 | 98% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Christian McCaffrey | RB | 7.7 | 95% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Jonathan Taylor | RB | 6.2 | 94% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| De'Von Achane | RB | 12.4 | 100% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Chase Brown | RB | 17.1 | 100% | 37% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| James Cook III | RB | 10.1 | 100% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Kenneth Walker III | RB | 24.8 | 100% | 96% | 21% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Omarion Hampton | RB | 18.1 | 100% | 53% | 3% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Derrick Henry | RB | 16.5 | 100% | 29% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Ashton Jeanty | RB | 21.8 | 100% | 84% | 14% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Saquon Barkley | RB | 14.0 | 100% | 6% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Brock Bowers | TE | 23.9 | 94% | 77% | 52% | 11% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Trey McBride | TE | 23.0 | 95% | 72% | 44% | 10% | 4% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Colston Loveland | TE | 42.4 | 100% | 99% | 97% | 73% | 49% | 2% | 0% | 0% | 0% | 0% | 0% | 0% |
| Tyler Warren | TE | 52.1 | 100% | 100% | 100% | 95% | 87% | 26% | 9% | 0% | 0% | 0% | 0% | 0% |
| Josh Allen | QB | 19.1 | 95% | 63% | 31% | 3% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Lamar Jackson | QB | 34.5 | 100% | 99% | 91% | 38% | 17% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Jayden Daniels | QB | 53.1 | 100% | 100% | 100% | 96% | 88% | 25% | 9% | 0% | 0% | 0% | 0% | 0% |
| Drake Maye | QB | 47.2 | 100% | 99% | 97% | 78% | 65% | 20% | 10% | 1% | 0% | 0% | 0% | 0% |
| Joe Burrow | QB | 53.5 | 100% | 100% | 100% | 95% | 88% | 35% | 15% | 1% | 0% | 0% | 0% | 0% |
| Jalen Hurts | QB | 54.7 | 100% | 100% | 98% | 86% | 77% | 40% | 28% | 8% | 2% | 0% | 0% | 0% |
| Malik Nabers | WR | 35.0 | 100% | 100% | 98% | 12% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| A.J. Brown | WR | 21.0 | 100% | 90% | 10% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Drake London | WR | 20.4 | 100% | 89% | 5% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Nico Collins | WR | 25.7 | 100% | 100% | 50% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| DeVonta Smith | WR | 36.6 | 100% | 100% | 99% | 27% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Zay Flowers | WR | 44.1 | 100% | 100% | 100% | 72% | 25% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Garrett Wilson | WR | 37.1 | 100% | 100% | 100% | 25% | 1% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Breece Hall | RB | 35.9 | 100% | 100% | 100% | 19% | 1% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Jeremiyah Love | RB | 26.0 | 100% | 98% | 51% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| MarShawn Lloyd | RB | 115.4 | 100% | 100% | 100% | 100% | 100% | 99% | 97% | 89% | 81% | 62% | 52% | 34% |
