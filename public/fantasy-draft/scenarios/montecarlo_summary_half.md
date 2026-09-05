# Monte Carlo draft simulation (1200 drafts per strategy)

Generated 2026-09-05 02:10. 10 teams, slot 4, snake, 16 rounds; opponents draft from ESPN ADP with each player's measured spread and simple roster rules; your picks follow the strategy preset. Roster score = optimal lineup (QB, 2 RB, 2 WR, TE, FLEX) on projected points plus a quarter of the next three RB / WR / TE and the QB2 (bench depth matters in head-to-head); floor and ceiling use the Bayesian p10 / p90. All 14 skill rounds are simulated and reported.

## 1. Strategy comparison

| strategy | profile | lineup proj (mean) | p10 of runs | p90 of runs | floor lineup | ceiling lineup | avg RB / WR / QB / TE drafted |
|---|---|---|---|---|---|---|---|
| hero-rb | balanced | 1846 | 1804 | 1898 | 702 | 2394 | 5.1 / 5.9 / 1.4 / 1.6 |
| robust-rb | balanced | 1837 | 1789 | 1898 | 693 | 2377 | 5.1 / 5.9 / 1.5 / 1.5 |
| balanced | balanced | 1842 | 1791 | 1896 | 704 | 2391 | 5.0 / 5.9 / 1.4 / 1.7 |
| zero-rb | balanced | 1761 | 1713 | 1810 | 683 | 2305 | 5.1 / 6.0 / 1.6 / 1.3 |
| wr-heavy | balanced | 1830 | 1784 | 1880 | 705 | 2378 | 5.0 / 5.9 / 1.4 / 1.6 |
| hero-rb | upside | 1859 | 1811 | 1911 | 690 | 2408 | 5.1 / 5.8 / 1.7 / 1.4 |
| hero-rb | safe | 1863 | 1822 | 1912 | 721 | 2411 | 5.1 / 5.7 / 2.0 / 1.2 |

Best mean lineup: **hero-rb / safe**. Differences under ~10 points are noise at this sample size.

## 2. Who to take at your first pick (when available)

Forcing each candidate at pick 4 whenever he is on the board, then drafting normally (hero-rb / balanced). Rows are only comparable on the runs where the candidate was available.

| forced pick | available in % of runs | lineup proj (mean) | floor lineup | ceiling lineup |
|---|---|---|---|---|
| Jahmyr Gibbs | 97% | 1844 | 702 | 2391 |
| Bijan Robinson | 98% | 1838 | 713 | 2385 |
| Ja'Marr Chase | 100% | 1791 | 694 | 2333 |
| Puka Nacua | 100% | 1805 | 686 | 2342 |
| Jaxon Smith-Njigba | 100% | 1791 | 678 | 2323 |
| Amon-Ra St. Brown | 100% | 1775 | 678 | 2313 |
| Jonathan Taylor | 100% | 1796 | 661 | 2312 |
| Christian McCaffrey | 100% | 1792 | 670 | 2329 |

## 3. Most frequent picks by round: hero-rb / balanced

| Rd | Pick | #1 | #2 | #3 | #4 |
|---|---|---|---|---|---|
| 1 | 4 | Jahmyr Gibbs (97%) | Bijan Robinson (2%) | Ja'Marr Chase (1%) |  |
| 2 | 17 | Chase Brown (40%) | James Cook III (27%) | Amon-Ra St. Brown (17%) | Jonathan Taylor (6%) |
| 3 | 24 | Nico Collins (63%) | Chase Brown (26%) | Justin Jefferson (7%) | CeeDee Lamb (2%) |
| 4 | 37 | DeVonta Smith (57%) | George Pickens (14%) | Brock Bowers (14%) | Tee Higgins (7%) |
| 5 | 44 | Tee Higgins (73%) | DeVonta Smith (15%) | Emeka Egbuka (7%) | Trey McBride (2%) |
| 6 | 57 | Luther Burden III (53%) | Colston Loveland (17%) | Tee Higgins (11%) | Ladd McConkey (7%) |
| 7 | 64 | Luther Burden III (44%) | Bhayshul Tuten (21%) | Tyler Warren (10%) | Jameson Williams (9%) |
| 8 | 77 | Christian Watson (52%) | Tucker Kraft (18%) | Jadarian Price (17%) | Justin Herbert (2%) |
| 9 | 84 | Justin Herbert (69%) | Tucker Kraft (8%) | Jaylen Warren (8%) | Trevor Lawrence (4%) |
| 10 | 97 | Kyle Monangai (36%) | Tucker Kraft (19%) | Trevor Lawrence (18%) | Brian Thomas Jr. (12%) |
| 11 | 104 | Tucker Kraft (29%) | Kyle Monangai (28%) | RJ Harvey (21%) | Kyle Pitts Sr. (10%) |
| 12 | 117 | RJ Harvey (40%) | Blake Corum (25%) | Kyle Monangai (19%) | Jordan Mason (5%) |
| 13 | 124 | Brock Purdy (15%) | Blake Corum (14%) | Jordan Addison (12%) | Jordan Mason (11%) |
| 14 | 137 | Jayden Reed (31%) | Dalton Kincaid (16%) | Jordan Addison (11%) | Chris Godwin Jr. (10%) |

## 3. Most frequent picks by round: robust-rb / balanced

| Rd | Pick | #1 | #2 | #3 | #4 |
|---|---|---|---|---|---|
| 1 | 4 | Jahmyr Gibbs (97%) | Bijan Robinson (2%) | Ja'Marr Chase (1%) |  |
| 2 | 17 | Chase Brown (40%) | James Cook III (27%) | Amon-Ra St. Brown (17%) | Jonathan Taylor (6%) |
| 3 | 24 | Chase Brown (32%) | Omarion Hampton (29%) | Ashton Jeanty (25%) | Kenneth Walker III (7%) |
| 4 | 37 | DeVonta Smith (65%) | George Pickens (15%) | Tee Higgins (7%) | Brock Bowers (6%) |
| 5 | 44 | Tee Higgins (75%) | DeVonta Smith (13%) | Emeka Egbuka (7%) | Brock Bowers (4%) |
| 6 | 57 | Luther Burden III (56%) | Colston Loveland (12%) | Tee Higgins (11%) | Ladd McConkey (9%) |
| 7 | 64 | Luther Burden III (41%) | Jameson Williams (24%) | Tyler Warren (13%) | Drake Maye (5%) |
| 8 | 77 | Christian Watson (76%) | Tucker Kraft (9%) | Jadarian Price (4%) | Bhayshul Tuten (2%) |
| 9 | 84 | Justin Herbert (66%) | Tucker Kraft (15%) | Trevor Lawrence (11%) | Jalen Hurts (1%) |
| 10 | 97 | Brian Thomas Jr. (26%) | Tucker Kraft (26%) | Kyle Monangai (17%) | Trevor Lawrence (10%) |
| 11 | 104 | Kyle Monangai (45%) | Tucker Kraft (25%) | RJ Harvey (12%) | Kyle Pitts Sr. (11%) |
| 12 | 117 | RJ Harvey (48%) | Kyle Monangai (23%) | Blake Corum (19%) | Jordan Mason (4%) |
| 13 | 124 | Brock Purdy (16%) | Jordan Addison (13%) | RJ Harvey (13%) | Blake Corum (12%) |
| 14 | 137 | Jayden Reed (31%) | Dalton Kincaid (15%) | Jordan Addison (12%) | Chris Godwin Jr. (10%) |

## 3. Most frequent picks by round: balanced / balanced

| Rd | Pick | #1 | #2 | #3 | #4 |
|---|---|---|---|---|---|
| 1 | 4 | Jahmyr Gibbs (97%) | Bijan Robinson (2%) | Ja'Marr Chase (1%) |  |
| 2 | 17 | Justin Jefferson (28%) | James Cook III (27%) | Amon-Ra St. Brown (20%) | Chase Brown (9%) |
| 3 | 24 | Nico Collins (54%) | Chase Brown (34%) | Justin Jefferson (6%) | CeeDee Lamb (2%) |
| 4 | 37 | DeVonta Smith (53%) | Brock Bowers (17%) | George Pickens (12%) | Tee Higgins (4%) |
| 5 | 44 | Colston Loveland (37%) | Tee Higgins (36%) | DeVonta Smith (17%) | Javonte Williams (2%) |
| 6 | 57 | Luther Burden III (51%) | Tee Higgins (30%) | Ladd McConkey (6%) | Colston Loveland (5%) |
| 7 | 64 | Luther Burden III (46%) | Jameson Williams (19%) | Bhayshul Tuten (9%) | Tyler Warren (6%) |
| 8 | 77 | Christian Watson (57%) | Justin Herbert (14%) | Tucker Kraft (12%) | Jadarian Price (7%) |
| 9 | 84 | Justin Herbert (56%) | Trevor Lawrence (16%) | Jaylen Warren (8%) | Tucker Kraft (4%) |
| 10 | 97 | Kyle Monangai (69%) | Tucker Kraft (8%) | Brian Thomas Jr. (8%) | Trevor Lawrence (3%) |
| 11 | 104 | Tucker Kraft (44%) | RJ Harvey (30%) | Kyle Monangai (13%) | Kyle Pitts Sr. (9%) |
| 12 | 117 | RJ Harvey (43%) | Blake Corum (32%) | Kyle Monangai (10%) | Jordan Mason (8%) |
| 13 | 124 | Blake Corum (20%) | Jordan Mason (18%) | Brock Purdy (11%) | Jordan Addison (10%) |
| 14 | 137 | Jayden Reed (30%) | Dalton Kincaid (14%) | Jordan Addison (13%) | Chris Godwin Jr. (11%) |

## 4. Chance key players are still there at your picks (simulated, ESPN room)

| player | pos | ADP used | #4 | #17 | #24 | #37 | #44 | #57 | #64 | #77 | #84 | #97 | #104 | #117 | #124 | #137 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Jahmyr Gibbs | RB | 1.3 | 97% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Bijan Robinson | RB | 2.4 | 98% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Ja'Marr Chase | WR | 4.3 | 100% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Puka Nacua | WR | 5.3 | 100% | 2% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Jaxon Smith-Njigba | WR | 6.3 | 100% | 5% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Amon-Ra St. Brown | WR | 8.4 | 100% | 22% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Christian McCaffrey | RB | 7.7 | 100% | 18% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Jonathan Taylor | RB | 6.2 | 100% | 8% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| De'Von Achane | RB | 12.4 | 100% | 76% | 6% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Chase Brown | RB | 17.1 | 100% | 97% | 33% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| James Cook III | RB | 10.1 | 100% | 48% | 1% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Kenneth Walker III | RB | 24.8 | 100% | 100% | 96% | 6% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Omarion Hampton | RB | 18.1 | 100% | 96% | 52% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Derrick Henry | RB | 16.5 | 100% | 99% | 36% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Ashton Jeanty | RB | 21.8 | 100% | 100% | 81% | 2% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Saquon Barkley | RB | 14.0 | 100% | 84% | 16% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Brock Bowers | TE | 23.9 | 100% | 94% | 78% | 20% | 2% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Trey McBride | TE | 23.0 | 100% | 94% | 75% | 15% | 4% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Colston Loveland | TE | 42.4 | 100% | 100% | 100% | 88% | 69% | 20% | 1% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Tyler Warren | TE | 52.1 | 100% | 100% | 100% | 99% | 95% | 57% | 26% | 2% | 0% | 0% | 0% | 0% | 0% | 0% |
| Josh Allen | QB | 19.1 | 100% | 85% | 55% | 6% | 1% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Lamar Jackson | QB | 34.5 | 100% | 100% | 98% | 64% | 31% | 2% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Jayden Daniels | QB | 53.1 | 100% | 100% | 100% | 97% | 92% | 61% | 35% | 5% | 2% | 0% | 0% | 0% | 0% | 0% |
| Drake Maye | QB | 47.2 | 100% | 100% | 100% | 96% | 84% | 36% | 16% | 1% | 0% | 0% | 0% | 0% | 0% | 0% |
| Joe Burrow | QB | 53.5 | 100% | 100% | 100% | 100% | 99% | 66% | 34% | 1% | 0% | 0% | 0% | 0% | 0% | 0% |
| Jalen Hurts | QB | 54.7 | 100% | 100% | 100% | 97% | 91% | 63% | 45% | 11% | 6% | 1% | 0% | 0% | 0% | 0% |
| Malik Nabers | WR | 35.0 | 100% | 100% | 100% | 80% | 17% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| A.J. Brown | WR | 21.0 | 100% | 100% | 84% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Drake London | WR | 20.4 | 100% | 100% | 81% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Nico Collins | WR | 25.7 | 100% | 100% | 99% | 3% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| DeVonta Smith | WR | 36.6 | 100% | 100% | 100% | 88% | 16% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Zay Flowers | WR | 44.1 | 100% | 100% | 100% | 100% | 89% | 8% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Garrett Wilson | WR | 37.1 | 100% | 100% | 100% | 92% | 37% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Breece Hall | RB | 35.9 | 100% | 100% | 100% | 85% | 30% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Jeremiyah Love | RB | 26.0 | 100% | 100% | 98% | 9% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| MarShawn Lloyd | RB | 115.4 | 100% | 100% | 100% | 100% | 100% | 100% | 99% | 94% | 91% | 72% | 65% | 52% | 41% | 23% |
