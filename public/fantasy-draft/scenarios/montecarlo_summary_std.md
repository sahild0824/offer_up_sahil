# Monte Carlo draft simulation (1200 drafts per strategy)

Generated 2026-09-05 02:13. 10 teams, slot 4, snake, 16 rounds; opponents draft from ESPN ADP with each player's measured spread and simple roster rules; your picks follow the strategy preset. Roster score = optimal lineup (QB, 2 RB, 2 WR, TE, FLEX) on projected points plus a quarter of the next three RB / WR / TE and the QB2 (bench depth matters in head-to-head); floor and ceiling use the Bayesian p10 / p90. All 14 skill rounds are simulated and reported.

## 1. Strategy comparison

| strategy | profile | lineup proj (mean) | p10 of runs | p90 of runs | floor lineup | ceiling lineup | avg RB / WR / QB / TE drafted |
|---|---|---|---|---|---|---|---|
| hero-rb | balanced | 1514 | 1474 | 1551 | 554 | 1960 | 5.0 / 5.9 / 1.6 / 1.5 |
| robust-rb | balanced | 1514 | 1469 | 1556 | 557 | 1962 | 5.0 / 5.9 / 1.6 / 1.5 |
| balanced | balanced | 1515 | 1473 | 1555 | 558 | 1964 | 5.0 / 5.9 / 1.6 / 1.6 |
| zero-rb | balanced | 1480 | 1437 | 1514 | 538 | 1922 | 5.1 / 5.9 / 1.7 / 1.3 |
| wr-heavy | balanced | 1501 | 1460 | 1534 | 552 | 1938 | 5.0 / 5.9 / 1.6 / 1.5 |
| hero-rb | upside | 1513 | 1476 | 1542 | 538 | 1961 | 5.0 / 5.8 / 1.8 / 1.5 |
| hero-rb | safe | 1522 | 1495 | 1550 | 576 | 1974 | 5.2 / 5.5 / 2.0 / 1.3 |

Best mean lineup: **hero-rb / safe**. Differences under ~10 points are noise at this sample size.

## 2. Who to take at your first pick (when available)

Forcing each candidate at pick 4 whenever he is on the board, then drafting normally (hero-rb / balanced). Rows are only comparable on the runs where the candidate was available.

| forced pick | available in % of runs | lineup proj (mean) | floor lineup | ceiling lineup |
|---|---|---|---|---|
| Jahmyr Gibbs | 0% | 1514 | 552 | 1962 |
| Bijan Robinson | 4% | 1514 | 552 | 1962 |
| Ja'Marr Chase | 47% | 1513 | 552 | 1961 |
| Puka Nacua | 83% | 1518 | 552 | 1969 |
| Jaxon Smith-Njigba | 92% | 1510 | 545 | 1957 |
| Amon-Ra St. Brown | 98% | 1490 | 540 | 1934 |
| Jonathan Taylor | 97% | 1536 | 543 | 1966 |
| Christian McCaffrey | 96% | 1518 | 548 | 1969 |

## 3. Most frequent picks by round: hero-rb / balanced

| Rd | Pick | #1 | #2 | #3 | #4 |
|---|---|---|---|---|---|
| 1 | 4 | Puka Nacua (51%) | Ja'Marr Chase (46%) | Bijan Robinson (4%) | Jahmyr Gibbs (0%) |
| 2 | 17 | Kenneth Walker III (45%) | Chase Brown (45%) | Saquon Barkley (6%) | Justin Jefferson (2%) |
| 3 | 24 | Nico Collins (55%) | George Pickens (25%) | Kenneth Walker III (13%) | A.J. Brown (3%) |
| 4 | 37 | Tee Higgins (63%) | DeVonta Smith (27%) | Brock Bowers (9%) | Kyren Williams (0%) |
| 5 | 44 | Tee Higgins (32%) | Colston Loveland (26%) | Emeka Egbuka (17%) | Zay Flowers (10%) |
| 6 | 57 | Luther Burden III (48%) | Bhayshul Tuten (40%) | D'Andre Swift (3%) | Jaylen Waddle (3%) |
| 7 | 64 | Luther Burden III (36%) | Jadarian Price (20%) | TreVeyon Henderson (14%) | Jameson Williams (8%) |
| 8 | 77 | Tucker Kraft (39%) | Christian Watson (24%) | Justin Herbert (23%) | Parker Washington (3%) |
| 9 | 84 | Justin Herbert (33%) | Trevor Lawrence (29%) | Blake Corum (15%) | Jaylen Warren (8%) |
| 10 | 97 | Blake Corum (51%) | Jordan Mason (21%) | Jordan Addison (8%) | Brian Thomas Jr. (8%) |
| 11 | 104 | Jordan Mason (46%) | Tucker Kraft (13%) | Kyle Monangai (12%) | Kyle Pitts Sr. (9%) |
| 12 | 117 | Jacory Croskey-Merritt (33%) | Kyle Monangai (22%) | Jordan Mason (21%) | RJ Harvey (5%) |
| 13 | 124 | Jayden Reed (40%) | Jacory Croskey-Merritt (10%) | Jordan Addison (8%) | Brock Purdy (7%) |
| 14 | 137 | Kyler Murray (21%) | Dalton Kincaid (17%) | Jayden Reed (11%) | Jared Goff (11%) |

## 3. Most frequent picks by round: robust-rb / balanced

| Rd | Pick | #1 | #2 | #3 | #4 |
|---|---|---|---|---|---|
| 1 | 4 | Puka Nacua (51%) | Ja'Marr Chase (46%) | Bijan Robinson (4%) | Jahmyr Gibbs (0%) |
| 2 | 17 | Kenneth Walker III (45%) | Chase Brown (45%) | Saquon Barkley (6%) | Justin Jefferson (2%) |
| 3 | 24 | Nico Collins (36%) | Kenneth Walker III (24%) | Brock Bowers (14%) | Ashton Jeanty (13%) |
| 4 | 37 | Tee Higgins (65%) | DeVonta Smith (28%) | Brock Bowers (6%) | Emeka Egbuka (0%) |
| 5 | 44 | Tee Higgins (30%) | Colston Loveland (23%) | Emeka Egbuka (18%) | Zay Flowers (11%) |
| 6 | 57 | Luther Burden III (89%) | Jaylen Waddle (6%) | Jameson Williams (2%) | Colston Loveland (1%) |
| 7 | 64 | Christian Watson (23%) | Jadarian Price (15%) | Jameson Williams (12%) | Justin Herbert (11%) |
| 8 | 77 | Tucker Kraft (35%) | Justin Herbert (28%) | Christian Watson (18%) | Parker Washington (4%) |
| 9 | 84 | Trevor Lawrence (21%) | Justin Herbert (20%) | Blake Corum (19%) | Jaylen Warren (13%) |
| 10 | 97 | Blake Corum (53%) | Jordan Mason (35%) | Jordan Addison (3%) | Brian Thomas Jr. (3%) |
| 11 | 104 | Jordan Mason (38%) | Kyle Monangai (18%) | Tucker Kraft (15%) | Kyle Pitts Sr. (8%) |
| 12 | 117 | Jacory Croskey-Merritt (37%) | Kyle Monangai (22%) | Jordan Mason (16%) | RJ Harvey (7%) |
| 13 | 124 | Jayden Reed (38%) | Jacory Croskey-Merritt (12%) | Brock Purdy (7%) | Jordan Addison (7%) |
| 14 | 137 | Kyler Murray (20%) | Dalton Kincaid (16%) | Jared Goff (12%) | Jayden Reed (12%) |

## 3. Most frequent picks by round: balanced / balanced

| Rd | Pick | #1 | #2 | #3 | #4 |
|---|---|---|---|---|---|
| 1 | 4 | Puka Nacua (51%) | Ja'Marr Chase (46%) | Bijan Robinson (4%) | Jahmyr Gibbs (0%) |
| 2 | 17 | Kenneth Walker III (45%) | Chase Brown (43%) | Saquon Barkley (6%) | Justin Jefferson (4%) |
| 3 | 24 | Nico Collins (43%) | Kenneth Walker III (24%) | Brock Bowers (18%) | George Pickens (7%) |
| 4 | 37 | Tee Higgins (38%) | DeVonta Smith (28%) | Colston Loveland (21%) | Brock Bowers (5%) |
| 5 | 44 | Tee Higgins (46%) | Colston Loveland (17%) | Emeka Egbuka (14%) | Zay Flowers (9%) |
| 6 | 57 | Luther Burden III (87%) | Jaylen Waddle (6%) | D'Andre Swift (3%) | Jameson Williams (2%) |
| 7 | 64 | Christian Watson (25%) | Jadarian Price (16%) | Jameson Williams (14%) | Luther Burden III (7%) |
| 8 | 77 | Justin Herbert (32%) | Tucker Kraft (23%) | Christian Watson (23%) | Parker Washington (5%) |
| 9 | 84 | Trevor Lawrence (21%) | Blake Corum (21%) | Justin Herbert (19%) | Jaylen Warren (12%) |
| 10 | 97 | Blake Corum (51%) | Jordan Mason (37%) | Jordan Addison (3%) | Brian Thomas Jr. (3%) |
| 11 | 104 | Jordan Mason (34%) | Tucker Kraft (19%) | Kyle Monangai (19%) | Kyle Pitts Sr. (8%) |
| 12 | 117 | Jacory Croskey-Merritt (37%) | Kyle Monangai (20%) | Jordan Mason (18%) | RJ Harvey (7%) |
| 13 | 124 | Jayden Reed (37%) | Jacory Croskey-Merritt (13%) | Brock Purdy (7%) | Jordan Addison (7%) |
| 14 | 137 | Kyler Murray (20%) | Dalton Kincaid (16%) | Jayden Reed (12%) | Jared Goff (12%) |

## 4. Chance key players are still there at your picks (simulated, ESPN room)

| player | pos | ADP used | #4 | #17 | #24 | #37 | #44 | #57 | #64 | #77 | #84 | #97 | #104 | #117 | #124 | #137 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Jahmyr Gibbs | RB | 1.3 | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Bijan Robinson | RB | 2.4 | 4% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Ja'Marr Chase | WR | 4.3 | 47% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Puka Nacua | WR | 5.3 | 83% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Jaxon Smith-Njigba | WR | 6.3 | 92% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Amon-Ra St. Brown | WR | 8.4 | 98% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Christian McCaffrey | RB | 7.7 | 96% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Jonathan Taylor | RB | 6.2 | 97% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| De'Von Achane | RB | 12.4 | 100% | 2% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Chase Brown | RB | 17.1 | 100% | 45% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| James Cook III | RB | 10.1 | 100% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Kenneth Walker III | RB | 24.8 | 100% | 97% | 24% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Omarion Hampton | RB | 18.1 | 100% | 58% | 3% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Derrick Henry | RB | 16.5 | 100% | 36% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Ashton Jeanty | RB | 21.8 | 100% | 89% | 16% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Saquon Barkley | RB | 14.0 | 100% | 9% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Brock Bowers | TE | 23.9 | 95% | 70% | 43% | 9% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Trey McBride | TE | 23.0 | 95% | 68% | 39% | 7% | 3% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Colston Loveland | TE | 42.4 | 100% | 100% | 96% | 62% | 38% | 2% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Tyler Warren | TE | 52.1 | 100% | 100% | 100% | 91% | 75% | 20% | 7% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Josh Allen | QB | 19.1 | 95% | 56% | 26% | 2% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Lamar Jackson | QB | 34.5 | 100% | 98% | 87% | 28% | 9% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Jayden Daniels | QB | 53.1 | 100% | 100% | 100% | 94% | 81% | 19% | 4% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Drake Maye | QB | 47.2 | 100% | 99% | 96% | 72% | 55% | 15% | 7% | 1% | 0% | 0% | 0% | 0% | 0% | 0% |
| Joe Burrow | QB | 53.5 | 100% | 100% | 100% | 94% | 81% | 25% | 10% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Jalen Hurts | QB | 54.7 | 100% | 99% | 97% | 86% | 73% | 36% | 19% | 5% | 3% | 1% | 0% | 0% | 0% | 0% |
| Malik Nabers | WR | 35.0 | 100% | 100% | 98% | 15% | 1% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| A.J. Brown | WR | 21.0 | 100% | 88% | 8% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Drake London | WR | 20.4 | 100% | 86% | 3% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Nico Collins | WR | 25.7 | 100% | 100% | 55% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| DeVonta Smith | WR | 36.6 | 100% | 100% | 99% | 30% | 1% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Zay Flowers | WR | 44.1 | 100% | 100% | 100% | 78% | 40% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Garrett Wilson | WR | 37.1 | 100% | 100% | 100% | 28% | 3% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Breece Hall | RB | 35.9 | 100% | 100% | 100% | 17% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Jeremiyah Love | RB | 26.0 | 100% | 98% | 56% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| MarShawn Lloyd | RB | 115.4 | 100% | 100% | 100% | 100% | 100% | 99% | 98% | 90% | 81% | 52% | 44% | 31% | 20% | 11% |
