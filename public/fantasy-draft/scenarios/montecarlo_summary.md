# Monte Carlo draft simulation (1500 drafts per strategy)

Generated 2026-09-05 02:01. 10 teams, slot 4, snake, 16 rounds; opponents draft from ESPN ADP with each player's measured spread and simple roster rules; your picks follow the strategy preset. Lineup = QB, 2 RB, 2 WR, TE, FLEX scored on projected PPR points; floor and ceiling use the Bayesian p10 / p90.

## 1. Strategy comparison

| strategy | profile | lineup proj (mean) | p10 of runs | p90 of runs | floor lineup | ceiling lineup | avg RB / WR / QB / TE drafted |
|---|---|---|---|---|---|---|---|
| hero-rb | balanced | 1691 | 1660 | 1724 | 668 | 2196 | 5.5 / 6.0 / 1.4 / 1.2 |
| robust-rb | balanced | 1706 | 1671 | 1740 | 675 | 2207 | 5.4 / 6.0 / 1.4 / 1.2 |
| balanced | balanced | 1689 | 1645 | 1732 | 669 | 2190 | 5.4 / 6.0 / 1.4 / 1.3 |
| zero-rb | balanced | 1660 | 1631 | 1684 | 655 | 2166 | 5.5 / 5.9 / 1.4 / 1.1 |
| wr-heavy | balanced | 1670 | 1642 | 1699 | 672 | 2184 | 5.5 / 6.0 / 1.4 / 1.2 |
| hero-rb | upside | 1700 | 1663 | 1739 | 660 | 2201 | 5.1 / 5.8 / 1.7 / 1.4 |
| hero-rb | safe | 1701 | 1669 | 1731 | 687 | 2218 | 5.1 / 5.8 / 2.0 / 1.1 |

Best mean lineup: **robust-rb / balanced**. Differences under ~10 points are noise at this sample size.

## 2. Who to take at your first pick (when available)

Forcing each candidate at pick 4 whenever he is on the board, then drafting normally (hero-rb / balanced). Rows are only comparable on the runs where the candidate was available.

| forced pick | available in % of runs | lineup proj (mean) | floor lineup | ceiling lineup |
|---|---|---|---|---|
| Jahmyr Gibbs | 0% | 1691 | 668 | 2195 |
| Bijan Robinson | 4% | 1691 | 668 | 2195 |
| Ja'Marr Chase | 41% | 1690 | 668 | 2195 |
| Puka Nacua | 83% | 1692 | 662 | 2190 |
| Jaxon Smith-Njigba | 95% | 1677 | 653 | 2170 |
| Amon-Ra St. Brown | 100% | 1661 | 657 | 2168 |
| Jonathan Taylor | 87% | 1687 | 641 | 2166 |
| Christian McCaffrey | 98% | 1695 | 648 | 2189 |

## 3. Most frequent picks by round: hero-rb / balanced

| Rd | Pick | #1 | #2 | #3 | #4 |
|---|---|---|---|---|---|
| 1 | 4 | Puka Nacua (56%) | Ja'Marr Chase (41%) | Bijan Robinson (3%) | Jahmyr Gibbs (0%) |
| 2 | 17 | Chase Brown (37%) | Omarion Hampton (37%) | Ashton Jeanty (22%) | Kenneth Walker III (1%) |
| 3 | 24 | Nico Collins (55%) | George Pickens (36%) | Brock Bowers (3%) | Ashton Jeanty (2%) |
| 4 | 37 | Tee Higgins (79%) | DeVonta Smith (19%) | Brock Bowers (1%) | Ladd McConkey (0%) |
| 5 | 44 | Ladd McConkey (41%) | Emeka Egbuka (19%) | Tee Higgins (18%) | Zay Flowers (9%) |
| 6 | 57 | Luther Burden III (88%) | Colston Loveland (3%) | Bhayshul Tuten (3%) | D'Andre Swift (3%) |
| 7 | 64 | TreVeyon Henderson (42%) | Jadarian Price (33%) | Bhayshul Tuten (7%) | Tyler Warren (5%) |
| 8 | 77 | Justin Herbert (62%) | Jaylen Warren (20%) | Tucker Kraft (5%) | TreVeyon Henderson (5%) |
| 9 | 84 | Tucker Kraft (41%) | Trevor Lawrence (18%) | Rico Dowdle (7%) | Kyle Pitts Sr. (6%) |
| 10 | 97 | RJ Harvey (55%) | Dalton Kincaid (12%) | Trevor Lawrence (10%) | Brian Thomas Jr. (7%) |
| 11 | 104 | Kyle Monangai (48%) | RJ Harvey (26%) | Blake Corum (16%) | Tucker Kraft (3%) |
| 12 | 117 | Blake Corum (35%) | Jordan Mason (30%) | Kyle Monangai (13%) | Jacory Croskey-Merritt (7%) |
| 13 | 124 | Jayden Reed (34%) | Jordan Addison (16%) | Brock Purdy (14%) | Chris Godwin Jr. (12%) |
| 14 | 137 | Jordan Mason (21%) | Jayden Reed (17%) | Jacory Croskey-Merritt (17%) | Dalton Kincaid (13%) |

## 3. Most frequent picks by round: robust-rb / balanced

| Rd | Pick | #1 | #2 | #3 | #4 |
|---|---|---|---|---|---|
| 1 | 4 | Puka Nacua (56%) | Ja'Marr Chase (40%) | Bijan Robinson (4%) | Jahmyr Gibbs (0%) |
| 2 | 17 | Chase Brown (37%) | Omarion Hampton (37%) | Ashton Jeanty (22%) | Kenneth Walker III (1%) |
| 3 | 24 | Kenneth Walker III (41%) | Nico Collins (28%) | Ashton Jeanty (14%) | Brock Bowers (10%) |
| 4 | 37 | Tee Higgins (79%) | DeVonta Smith (19%) | Brock Bowers (1%) | Ladd McConkey (0%) |
| 5 | 44 | Ladd McConkey (41%) | Emeka Egbuka (20%) | Tee Higgins (18%) | Zay Flowers (9%) |
| 6 | 57 | Luther Burden III (91%) | Jameson Williams (3%) | Colston Loveland (3%) | Tyler Warren (1%) |
| 7 | 64 | Justin Herbert (47%) | Jadarian Price (14%) | Jameson Williams (9%) | Bhayshul Tuten (6%) |
| 8 | 77 | Justin Herbert (30%) | Christian Watson (23%) | Tucker Kraft (14%) | Jaylen Warren (11%) |
| 9 | 84 | Tucker Kraft (31%) | Trevor Lawrence (13%) | Rico Dowdle (11%) | Brian Thomas Jr. (9%) |
| 10 | 97 | RJ Harvey (69%) | Kyle Monangai (12%) | Dalton Kincaid (9%) | Brian Thomas Jr. (5%) |
| 11 | 104 | Kyle Monangai (55%) | Blake Corum (20%) | RJ Harvey (13%) | Tucker Kraft (5%) |
| 12 | 117 | Blake Corum (37%) | Jordan Mason (35%) | Jacory Croskey-Merritt (7%) | J.K. Dobbins (6%) |
| 13 | 124 | Jayden Reed (34%) | Jordan Addison (16%) | Brock Purdy (14%) | Chris Godwin Jr. (11%) |
| 14 | 137 | Jordan Mason (19%) | Jacory Croskey-Merritt (18%) | Jayden Reed (18%) | Dalton Kincaid (14%) |

## 3. Most frequent picks by round: balanced / balanced

| Rd | Pick | #1 | #2 | #3 | #4 |
|---|---|---|---|---|---|
| 1 | 4 | Puka Nacua (56%) | Ja'Marr Chase (40%) | Bijan Robinson (4%) | Jahmyr Gibbs (0%) |
| 2 | 17 | Nico Collins (61%) | Chase Brown (37%) | Justin Jefferson (1%) | CeeDee Lamb (1%) |
| 3 | 24 | Brock Bowers (28%) | George Pickens (24%) | Nico Collins (22%) | Ashton Jeanty (17%) |
| 4 | 37 | Tee Higgins (70%) | DeVonta Smith (19%) | Javonte Williams (6%) | Kyren Williams (4%) |
| 5 | 44 | Ladd McConkey (27%) | Tee Higgins (26%) | Colston Loveland (22%) | Emeka Egbuka (12%) |
| 6 | 57 | Luther Burden III (85%) | Bhayshul Tuten (6%) | Jadarian Price (3%) | Tyler Warren (3%) |
| 7 | 64 | Justin Herbert (27%) | Jadarian Price (26%) | TreVeyon Henderson (12%) | Bhayshul Tuten (7%) |
| 8 | 77 | Justin Herbert (45%) | Jaylen Warren (20%) | Christian Watson (10%) | Tucker Kraft (7%) |
| 9 | 84 | Rico Dowdle (22%) | Tucker Kraft (18%) | Trevor Lawrence (15%) | RJ Harvey (14%) |
| 10 | 97 | RJ Harvey (69%) | Kyle Monangai (18%) | Dalton Kincaid (5%) | Blake Corum (2%) |
| 11 | 104 | Kyle Monangai (54%) | Blake Corum (21%) | Tucker Kraft (11%) | RJ Harvey (6%) |
| 12 | 117 | Blake Corum (38%) | Jordan Mason (37%) | Jacory Croskey-Merritt (8%) | J.K. Dobbins (7%) |
| 13 | 124 | Jayden Reed (31%) | Jordan Addison (14%) | Brock Purdy (13%) | Chris Godwin Jr. (10%) |
| 14 | 137 | Jacory Croskey-Merritt (18%) | Jayden Reed (18%) | Jordan Mason (16%) | Dalton Kincaid (14%) |

## 4. Chance key players are still there at your picks (simulated, ESPN room)

| player | pos | ADP used | #4 | #17 | #24 | #37 | #44 | #57 | #64 | #77 |
|---|---|---|---|---|---|---|---|---|---|---|
| Jahmyr Gibbs | RB | 1.3 | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Bijan Robinson | RB | 2.4 | 4% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Ja'Marr Chase | WR | 4.3 | 41% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Puka Nacua | WR | 5.3 | 83% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Jaxon Smith-Njigba | WR | 6.3 | 95% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Amon-Ra St. Brown | WR | 8.4 | 100% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Christian McCaffrey | RB | 7.7 | 98% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| Jonathan Taylor | RB | 6.2 | 87% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| De'Von Achane | RB | 12.4 | 100% | 1% | 0% | 0% | 0% | 0% | 0% | 0% |
| Chase Brown | RB | 17.1 | 100% | 38% | 0% | 0% | 0% | 0% | 0% | 0% |
| James Cook III | RB | 10.1 | 98% | 1% | 0% | 0% | 0% | 0% | 0% | 0% |
| Kenneth Walker III | RB | 24.8 | 100% | 97% | 47% | 0% | 0% | 0% | 0% | 0% |
| Omarion Hampton | RB | 18.1 | 100% | 54% | 1% | 0% | 0% | 0% | 0% | 0% |
| Derrick Henry | RB | 16.5 | 100% | 29% | 0% | 0% | 0% | 0% | 0% | 0% |
| Ashton Jeanty | RB | 21.8 | 100% | 86% | 14% | 0% | 0% | 0% | 0% | 0% |
| Saquon Barkley | RB | 14.0 | 100% | 13% | 0% | 0% | 0% | 0% | 0% | 0% |
| Brock Bowers | TE | 23.9 | 100% | 80% | 40% | 1% | 0% | 0% | 0% | 0% |
| Trey McBride | TE | 23.0 | 100% | 83% | 32% | 0% | 0% | 0% | 0% | 0% |
| Colston Loveland | TE | 42.4 | 100% | 100% | 96% | 65% | 40% | 3% | 0% | 0% |
| Tyler Warren | TE | 52.1 | 100% | 100% | 100% | 94% | 81% | 21% | 6% | 0% |
| Josh Allen | QB | 19.1 | 97% | 54% | 20% | 0% | 0% | 0% | 0% | 0% |
| Lamar Jackson | QB | 34.5 | 100% | 98% | 88% | 27% | 10% | 0% | 0% | 0% |
| Jayden Daniels | QB | 53.1 | 100% | 100% | 99% | 90% | 75% | 27% | 12% | 1% |
| Drake Maye | QB | 47.2 | 100% | 100% | 99% | 81% | 58% | 9% | 2% | 0% |
| Joe Burrow | QB | 53.5 | 100% | 100% | 100% | 97% | 85% | 24% | 7% | 0% |
| Jalen Hurts | QB | 54.7 | 100% | 100% | 100% | 92% | 80% | 36% | 17% | 3% |
| Malik Nabers | WR | 35.0 | 100% | 100% | 100% | 12% | 0% | 0% | 0% | 0% |
| A.J. Brown | WR | 21.0 | 100% | 88% | 7% | 0% | 0% | 0% | 0% | 0% |
| Drake London | WR | 20.4 | 100% | 89% | 1% | 0% | 0% | 0% | 0% | 0% |
| Nico Collins | WR | 25.7 | 100% | 99% | 55% | 0% | 0% | 0% | 0% | 0% |
| DeVonta Smith | WR | 36.6 | 100% | 100% | 100% | 19% | 0% | 0% | 0% | 0% |
| Zay Flowers | WR | 44.1 | 100% | 100% | 100% | 93% | 33% | 0% | 0% | 0% |
| Garrett Wilson | WR | 37.1 | 100% | 100% | 100% | 24% | 1% | 0% | 0% | 0% |
| Breece Hall | RB | 35.9 | 100% | 100% | 100% | 18% | 1% | 0% | 0% | 0% |
| Jeremiyah Love | RB | 26.0 | 100% | 99% | 58% | 0% | 0% | 0% | 0% | 0% |
| MarShawn Lloyd | RB | 115.4 | 100% | 100% | 100% | 99% | 99% | 97% | 95% | 85% |
