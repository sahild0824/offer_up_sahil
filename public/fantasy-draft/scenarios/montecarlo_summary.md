# Monte Carlo draft simulation (1500 drafts per strategy)

Generated 2026-09-05 17:04. 10 teams, slot 4, snake, 14 rounds (QB, 2 RB, 2 WR, TE, FLEX, D/ST, K, 5 bench); opponents draft from ESPN ADP with each player's measured spread and simple roster rules; your picks follow the strategy preset. Roster score = optimal lineup (QB, 2 RB, 2 WR, TE, FLEX) on projected points plus a quarter of the best five bench players (bench depth matters in head-to-head); floor and ceiling use the Bayesian p10 / p90. All 12 skill rounds are simulated and reported.

## 1. Strategy comparison

| strategy | profile | lineup proj (mean) | p10 of runs | p90 of runs | floor lineup | ceiling lineup | avg RB / WR / QB / TE drafted |
|---|---|---|---|---|---|---|---|
| hero-rb | balanced | 1909 | 1877 | 1942 | 720 | 2484 | 5.0 / 5.0 / 1.0 / 1.0 |
| robust-rb | balanced | 1916 | 1882 | 1948 | 722 | 2492 | 5.0 / 5.0 / 1.0 / 1.0 |
| balanced | balanced | 1905 | 1865 | 1944 | 722 | 2482 | 4.9 / 5.1 / 1.0 / 1.0 |
| zero-rb | balanced | 1872 | 1848 | 1897 | 710 | 2453 | 5.1 / 4.9 / 1.0 / 1.0 |
| wr-heavy | balanced | 1882 | 1854 | 1911 | 723 | 2464 | 5.0 / 5.0 / 1.0 / 1.0 |
| hero-rb | upside | 1911 | 1877 | 1946 | 712 | 2484 | 4.9 / 5.0 / 1.0 / 1.1 |
| hero-rb | safe | 1918 | 1888 | 1949 | 744 | 2514 | 5.0 / 5.0 / 1.0 / 1.0 |

Best mean lineup: **hero-rb / safe**. Differences under ~10 points are noise at this sample size.

## 2. Who to take at your first pick (when available)

Forcing each candidate at pick 4 whenever he is on the board, then drafting normally (hero-rb / balanced). Rows are only comparable on the runs where the candidate was available.

| forced pick | available in % of runs | lineup proj (mean) | floor lineup | ceiling lineup |
|---|---|---|---|---|
| Jahmyr Gibbs | 0% | 1909 | 720 | 2482 |
| Bijan Robinson | 3% | 1909 | 720 | 2482 |
| Ja'Marr Chase | 45% | 1909 | 720 | 2481 |
| Puka Nacua | 84% | 1911 | 714 | 2477 |
| Jaxon Smith-Njigba | 95% | 1896 | 705 | 2456 |
| Amon-Ra St. Brown | 100% | 1880 | 709 | 2454 |
| Jonathan Taylor | 85% | 1902 | 693 | 2457 |
| Christian McCaffrey | 98% | 1908 | 698 | 2479 |

## 3. Most frequent picks by round: hero-rb / balanced

| Rd | Pick | #1 | #2 | #3 | #4 |
|---|---|---|---|---|---|
| 1 | 4 | Puka Nacua (52%) | Ja'Marr Chase (45%) | Bijan Robinson (2%) |  |
| 2 | 17 | Omarion Hampton (33%) | Ashton Jeanty (30%) | Chase Brown (30%) | Justin Jefferson (4%) |
| 3 | 24 | Nico Collins (51%) | George Pickens (35%) | Brock Bowers (7%) | Ashton Jeanty (3%) |
| 4 | 37 | Tee Higgins (78%) | DeVonta Smith (17%) | Brock Bowers (3%) | Ladd McConkey (1%) |
| 5 | 44 | Ladd McConkey (26%) | Colston Loveland (22%) | Tee Higgins (16%) | Luther Burden III (14%) |
| 6 | 57 | Luther Burden III (77%) | Bhayshul Tuten (7%) | Tyler Warren (4%) | Jadarian Price (4%) |
| 7 | 64 | TreVeyon Henderson (35%) | Jadarian Price (32%) | Bhayshul Tuten (11%) | Tyler Warren (5%) |
| 8 | 77 | Justin Herbert (72%) | Tucker Kraft (9%) | Jaylen Warren (8%) | Trevor Lawrence (5%) |
| 9 | 84 | Tucker Kraft (31%) | Trevor Lawrence (16%) | Rico Dowdle (13%) | Christian Watson (8%) |
| 10 | 97 | RJ Harvey (52%) | Brian Thomas Jr. (23%) | Rico Dowdle (7%) | Dalton Kincaid (7%) |
| 11 | 104 | Kyle Monangai (48%) | RJ Harvey (31%) | Blake Corum (13%) | Jordan Mason (2%) |
| 12 | 117 | Blake Corum (36%) | Jordan Mason (24%) | Kyle Monangai (16%) | J.K. Dobbins (7%) |

## 3. Most frequent picks by round: robust-rb / balanced

| Rd | Pick | #1 | #2 | #3 | #4 |
|---|---|---|---|---|---|
| 1 | 4 | Puka Nacua (52%) | Ja'Marr Chase (44%) | Bijan Robinson (3%) |  |
| 2 | 17 | Omarion Hampton (33%) | Ashton Jeanty (30%) | Chase Brown (29%) | Justin Jefferson (4%) |
| 3 | 24 | Kenneth Walker III (41%) | Nico Collins (30%) | Brock Bowers (12%) | Ashton Jeanty (11%) |
| 4 | 37 | Tee Higgins (79%) | DeVonta Smith (17%) | Brock Bowers (3%) | Ladd McConkey (1%) |
| 5 | 44 | Ladd McConkey (28%) | Colston Loveland (20%) | Luther Burden III (17%) | Tee Higgins (15%) |
| 6 | 57 | Luther Burden III (78%) | Jameson Williams (9%) | Tyler Warren (4%) | Colston Loveland (3%) |
| 7 | 64 | Justin Herbert (38%) | Jadarian Price (16%) | Bhayshul Tuten (12%) | Joe Burrow (10%) |
| 8 | 77 | Justin Herbert (35%) | Tucker Kraft (28%) | Christian Watson (11%) | Trevor Lawrence (7%) |
| 9 | 84 | Brian Thomas Jr. (18%) | Parker Washington (12%) | Tucker Kraft (11%) | Christian Watson (11%) |
| 10 | 97 | RJ Harvey (66%) | Brian Thomas Jr. (12%) | Rico Dowdle (10%) | Kyle Monangai (8%) |
| 11 | 104 | Kyle Monangai (54%) | RJ Harvey (20%) | Blake Corum (18%) | Jordan Mason (2%) |
| 12 | 117 | Blake Corum (35%) | Jordan Mason (28%) | Kyle Monangai (11%) | J.K. Dobbins (8%) |

## 3. Most frequent picks by round: balanced / balanced

| Rd | Pick | #1 | #2 | #3 | #4 |
|---|---|---|---|---|---|
| 1 | 4 | Puka Nacua (52%) | Ja'Marr Chase (44%) | Bijan Robinson (3%) |  |
| 2 | 17 | Nico Collins (65%) | Chase Brown (29%) | Justin Jefferson (4%) | CeeDee Lamb (1%) |
| 3 | 24 | Brock Bowers (36%) | George Pickens (20%) | Nico Collins (19%) | Ashton Jeanty (16%) |
| 4 | 37 | Tee Higgins (65%) | DeVonta Smith (17%) | Javonte Williams (9%) | Kyren Williams (7%) |
| 5 | 44 | Colston Loveland (27%) | Tee Higgins (26%) | Ladd McConkey (16%) | D'Andre Swift (11%) |
| 6 | 57 | Luther Burden III (84%) | Bhayshul Tuten (5%) | Jameson Williams (3%) | Tyler Warren (3%) |
| 7 | 64 | Jadarian Price (26%) | Justin Herbert (24%) | Bhayshul Tuten (13%) | Joe Burrow (9%) |
| 8 | 77 | Justin Herbert (48%) | Tucker Kraft (14%) | Jaylen Warren (11%) | Christian Watson (8%) |
| 9 | 84 | Rico Dowdle (20%) | RJ Harvey (14%) | Brian Thomas Jr. (13%) | Jaylen Warren (9%) |
| 10 | 97 | RJ Harvey (66%) | Kyle Monangai (16%) | Rico Dowdle (9%) | Brian Thomas Jr. (5%) |
| 11 | 104 | Kyle Monangai (53%) | Blake Corum (24%) | RJ Harvey (13%) | J.K. Dobbins (4%) |
| 12 | 117 | Blake Corum (35%) | Jordan Mason (33%) | Jacory Croskey-Merritt (9%) | J.K. Dobbins (9%) |

## 4. Chance key players are still there at your picks (simulated, ESPN room)

| player | pos | ADP used | #4 | #17 | #24 | #37 | #44 | #57 | #64 | #77 | #84 | #97 | #104 | #117 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Jahmyr Gibbs | RB | 1.3 | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Bijan Robinson | RB | 2.4 | 3% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Ja'Marr Chase | WR | 4.3 | 45% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Puka Nacua | WR | 5.3 | 84% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Jaxon Smith-Njigba | WR | 6.3 | 95% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Amon-Ra St. Brown | WR | 8.4 | 100% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Christian McCaffrey | RB | 7.7 | 98% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Jonathan Taylor | RB | 6.2 | 85% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| De'Von Achane | RB | 12.4 | 100% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Chase Brown | RB | 17.1 | 100% | 30% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| James Cook III | RB | 10.1 | 98% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Kenneth Walker III | RB | 24.8 | 100% | 95% | 45% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Omarion Hampton | RB | 18.1 | 100% | 46% | 1% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Derrick Henry | RB | 16.5 | 100% | 20% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Ashton Jeanty | RB | 21.8 | 100% | 82% | 11% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Saquon Barkley | RB | 14.0 | 99% | 10% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Brock Bowers | TE | 23.9 | 100% | 87% | 51% | 3% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Trey McBride | TE | 23.0 | 100% | 90% | 42% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Colston Loveland | TE | 42.4 | 100% | 100% | 97% | 74% | 54% | 3% | 0% | 0% | 0% | 0% | 0% | 0% |
| Tyler Warren | TE | 52.1 | 100% | 100% | 100% | 97% | 90% | 27% | 8% | 0% | 0% | 0% | 0% | 0% |
| Josh Allen | QB | 19.1 | 97% | 65% | 26% | 1% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Lamar Jackson | QB | 34.5 | 100% | 98% | 91% | 38% | 19% | 1% | 0% | 0% | 0% | 0% | 0% | 0% |
| Jayden Daniels | QB | 53.1 | 100% | 100% | 99% | 92% | 82% | 33% | 17% | 4% | 1% | 0% | 0% | 0% |
| Drake Maye | QB | 47.2 | 100% | 100% | 99% | 87% | 71% | 12% | 4% | 0% | 0% | 0% | 0% | 0% |
| Joe Burrow | QB | 53.5 | 100% | 100% | 100% | 98% | 91% | 33% | 13% | 1% | 0% | 0% | 0% | 0% |
| Jalen Hurts | QB | 54.7 | 100% | 100% | 100% | 94% | 87% | 42% | 23% | 4% | 1% | 0% | 0% | 0% |
| Malik Nabers | WR | 35.0 | 100% | 100% | 99% | 11% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| A.J. Brown | WR | 21.0 | 100% | 91% | 7% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Drake London | WR | 20.4 | 100% | 93% | 2% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Nico Collins | WR | 25.7 | 100% | 100% | 51% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| DeVonta Smith | WR | 36.6 | 100% | 100% | 100% | 18% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Zay Flowers | WR | 44.1 | 100% | 100% | 100% | 87% | 17% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Garrett Wilson | WR | 37.1 | 100% | 100% | 100% | 20% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Breece Hall | RB | 35.9 | 100% | 100% | 99% | 23% | 3% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Jeremiyah Love | RB | 26.0 | 100% | 98% | 55% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| MarShawn Lloyd | RB | 115.4 | 100% | 100% | 100% | 99% | 99% | 97% | 95% | 86% | 78% | 63% | 54% | 41% |
