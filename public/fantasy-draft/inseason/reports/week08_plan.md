# Rest-of-season plan (Tuesday 10/27, before Week 8)

**Roster:** no trades went through; Ollie Gordon II added (assumed for Marvin Harrison Jr.).

**How this was built**
- **Data:** nflverse through Week 7 and FantasyPros ROS ranks from 10/23.
- **Research:** three agents.
  - Latest news on your roster, including the Monday-night game.
  - The RB trade market.
  - Targets, playoff schedules, trade-deadline rules and Week 8 waivers.
- **Research limits:** full-page fetches fail here and Reddit is blocked, so every source is a
  search summary. No Week 8 trade charts were out yet, so chart values are Week 7 (RotoStreetJournal,
  CBS, FantasyPros).
- **Engine:** exact injury-scenario checks with the updated news file (`examples/news_week08.json`).
  Gains are lineup points over Weeks 8-17.

## News since Week 7

| Player | Status |
|---|---|
| **DeVonta Smith** | **Out on Monday night** (hamstring again; it has lingered since camp). Sirianni did not rule out a longer shutdown. PHI is 2-5 with McKee at QB. |
| **Jaylen Waddle** | **Left Week 7 with a chest injury**; no diagnosis. WR49 in points per game. |
| Lamb / Pickens | 24.4 and 15.7 on Monday night. |
| Lamar Jackson | Rapoport: likely back Week 8 vs BUF. |
| Breece Hall | Week 8 return "appears likely" (Yahoo). |
| Kyle Monangai | No practice yet; possible Week 8 on MNF. |
| Ollie Gordon II | 25-103-1 on 83% of snaps; a TD in four straight games. Jaylen Wright (quad) left Week 7. Good pickup. |
| Chuba Hubbard | 61% of snaps in a 43-13 blowout loss. No Brooks return date found. |
| Chase Brown | 75% of snaps, but Perine is taking goal-line work. RB2. |
| Butker | KC scored 3 points in Week 7, and he missed kicks in Week 6. Consider streaming K. |

## Trades (Weeks 8-17)

| Trade | You | Them | Charts (RSJ Wk7) | Research verdict |
|---|---|---|---|---|
| **Lamar + Lamb for Bijan Robinson** (Rowan's) | +35 raw / +39 adj | +7.5 | 3703 for 3725 (even) | **Accept: best of the four.** Rowan's needs WRs (Evans and Egbuka out) and a QB2 (Dak only). |
| **Love + Waddle for Isaiah Likely** (Teemo) | +34 / +37 | +25 | 1388 for 1604 (fair) | **Yes, with Love.** Teemo needs a QB and a WR; Hockenson makes Likely spare. |
| **Then (Week 9 on): Kraft for Tee Higgins** (Hurts so Good) | about +22 on top of the two above | +6 | | Warren is out, so they need a TE. Higgins rebuilds your WR room after Lamb leaves. |
| **All three** | **+81 / +88** | | | |
| Fallback: Love + Hubbard for Swift, plus Lamar + Waddle for Likely | +58 / +72 | Rowan +45, Teemo +12 | Swift deal overpays on charts (Hubbard alone is worth about Swift) | Use only if Rowan's says no to Bijan. |
| Love + Chase Brown for Derrick Henry | +17 | +32 | about even | **Skip.** Henry is 32 with two straight duds; DraftKings says buy only at a lowball. |

**Kraft for Higgins: timing and caution.**
- Keep Kraft through Week 8: Likely's NYG is on bye.
- Kraft for Higgins on its own, without Likely, loses 75 points because it leaves you with no TE.
  Only do it after Likely arrives.
- Higgins' health has not been re-checked; confirm before offering.

### After the plan

| Position | Players |
|---|---|
| QB | Goff |
| RB | Bijan, Chase Brown, Hubbard, Gordon, Hall, Monangai (IR) |
| WR | Pickens, Higgins, Smith (when healthy), plus 1-2 wire WRs |
| TE | Likely |

- Use the roster spots opened by the 2-for-1s on WRs: Omar Cooper Jr. (NYJ), Keenan Allen,
  Josh Downs.
- Bye coverage:
  - Week 10 (Smith; Monangai): Bijan, Brown, Hubbard and Gordon cover.
  - Week 11 (Bijan; Love and Kraft gone): Likely plays.
  - Week 14 (Pickens): Higgins and Smith cover.
- Going down to one QB is fine: Goff's bye has already passed.

## Week 8 lineup

| Slot | Player | Note |
|---|---|---|
| QB | **Goff** | 22.2 a game, 14 TD / 0 INT. Start him over Lamar even if Lamar plays: first game back from a high-ankle sprain, vs BUF. |
| RB | Chase Brown, Ollie Gordon II | Gordon may get workhorse volume with Wright hurt. |
| WR | Lamb, Pickens | |
| TE | Kraft | |
| FLEX | Hubbard | Smith and Waddle are both doubtful. Put Hall here only if he practices fully. |
| D/ST | Steelers | **PIT is on bye in Week 9**, so stream next week. |
| K | Stream if a better kicker is free | |

## Trade deadline

- I found no 2026 date. Check League > Settings > Trade Rules.
- ESPN's default is usually around Week 13 (late November).
- The review period is 1-2 days, and 4 of 10 managers can veto.
- Send the Bijan and Likely offers **this week.**

## Week 8 waivers (Wednesday 10/28)

**Sources**
- The engine ran with the FantasyPros Week 8 consensus (scraped 10/28) and the 10/27 news. Output:
  `reports/week08_engine.md`.
- The free-agent list is every player on none of the ten rosters, plus Tuesday's consensus adds:
  - **RB:** Jonah Coleman, Seth McGowan, Dylan Sampson, Kimani Vidal.
  - **WR:** Omar Cooper Jr., Antonio Williams, Caleb Douglas.
  - **TE:** Mason Taylor, Brenton Strange.
- No Wednesday practice news on Smith or Waddle was indexed yet.

**Do now**
- **Kicker: drop Harrison Butker (FantasyPros K18, 7.4) and add Evan McPherson** (CIN vs TEN; K3,
  9.1; 40% rostered nationally, on no roster here). CIN's bye is done.
- If McPherson is gone: Spencer Shrader (IND @JAX; K5, 8.9) or Chase McLaughlin (TB; K7, 8.8).

**Hold until the trades resolve.** The Bijan and Likely deals are both 2-for-1, so each opens a
roster spot.

| Spot opens because | Add | Engine gain (Weeks 9-17) |
|---|---|---|
| Lamb trade | **Tre Tucker** (WR, LV, 82% snaps) | +4.7 |
| Second spot | **KC Concepcion** (WR, CLE; 23.2 last week) | |
| Likely trade fails | **Brenton Strange** (TE2 for Kraft's Week 11 bye) | +9.3 |

- **Do not drop Waddle, Lamar or Love** while they are in pending offers.
- **Hall** is the engine's cheapest drop (0.7), but he is about to return, so keep him.

**Not worth a spot on this roster:**
- Omar Cooper Jr., Jonah Coleman, Keenan Allen, Josh Downs: they are consensus adds, but they would
  not start for you.
- Kamara and every other wire RB.

**D/ST**
- **Week 8:** start the Steelers (DST3 vs CLE).
- **Week 9:** PIT is on bye, so stream. Pick next Tuesday from that week's rankings; this week's top
  free options are JAX, LAR and CIN.

**Week 8 lineup update.** With FantasyPros' Week 8 numbers the engine starts:
- QB: Love (19.1) over Goff, a coin flip.
- RB: Hubbard and Brown.
- WR: Lamb and Pickens.
- TE: Kraft (FP TE3).
- FLEX: Gordon (11.5).
- If the Love trade processes before Sunday, start Goff.
