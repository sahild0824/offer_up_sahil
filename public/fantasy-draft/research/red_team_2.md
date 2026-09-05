# Red team: attacking the board's own claims (Sept 5, 2026)

Each section is a claim the app makes, and a test designed to break it. Run `python3 redteam.py`
and `python3 redteam2.py` to reproduce. Findings are ordered by how much they should change what
you do on draft night.

## Confirmed defects

### 1. The printed roster is a conditional, not an expectation — 6.6%

Multiplying each pick's simulated availability along branch A:

| rd | pick | player | there | chain so far |
|---|---|---|---|---|
| 2 | 17 | Chase Brown | 38% | 38.0% |
| 3 | 24 | Kenneth Walker III | 47% | 17.9% |
| 6 | 57 | Jameson Williams | 74% | 13.1% |
| 8 | 77 | Tucker Kraft | 72% | 8.8% |
| 12 | 117 | KC Concepcion | 99% | **6.6%** |

The exact twelve-man roster the scenario prints occurs in about one draft in fifteen. Its
projected 1902 is the score *if everything falls*, so it cannot be read as an expected outcome.
The Monte Carlo numbers do not have this problem — the simulator re-picks against whatever is
actually on the board — which is why the build comparison is the trustworthy table and the
scenario roster is not. **Fixed in the app:** the branch card now says so directly.

### 2. Eight of twelve rounds showed no recommendation

The candidate rows come from the research verdicts; the ▸ marker comes from the scenario runner.
They disagreed in eight rounds, so the user saw a list of candidates with nothing marked — the
one thing the board exists to tell you. **Fixed:** the runner's pick is merged into the list,
labelled `sim`, with a note saying no outlet wrote him up at that slot.

### 3. Fourteen candidates were displayed that the simulation says are gone

Round 3 listed Drake London at **1%**, round 6 listed Drake Maye at **9%**, round 8 listed
Jadarian Price at **1%** and TreVeyon Henderson at **5%**. These are the rounds the research
assigned them; the simulation disagrees. Showing them as options at that pick is misleading.
**Fixed:** anything under 15% is struck through, dimmed, sorted below the live options and
labelled "gone before this pick in N% of drafts."

### 4. The tables sent in chat had already gone stale

Applying the ADP calibration changed the composites, which changed four of branch A's twelve
picks after the tables were sent (R9 Monangai→Harvey, R10 Corum→Monangai, R11 Reed→Corum,
R12 Mason→KC Concepcion). Any static export of this model is only true for the build that
produced it. **Corrected tables** are in `scenarios/OPTIMAL.md`.

### 5. The gap bar was unreadable

Scaled linearly to a 25-pick cap, the median row (3.7 picks) filled a seventh of the bar and the
four rows past the cap were indistinguishable. **Fixed:** square-root scale to a 20-pick cap.

## Structural weaknesses — not fixed, and you should know them

### 6. The composite is largely a smoothed ADP (r = 0.976)

Across the 140 drafted picks the composite correlates with the blended ADP at **r = 0.976**, with
a median absolute gap of **3.7 picks**. So "value vs ADP" is close to self-referential: the model
mostly agrees with the market by construction, because 19 of its inputs are consensus rankings
that are themselves anchored to ADP. The genuinely independent signals are the projections,
the 2024-25 game logs, the injury model and the situation layer — not the composite.

### 7. The calibration is partly circular

`espn_live` is both the calibration reference *and* half the fresh-feed weight in the blend.
Correcting every other feed onto ESPN's positional structure removes some of the cross-platform
disagreement the blend exists to capture, pulling the result closer to pure ESPN. That is
defensible — we draft on ESPN — but it is a narrowing, not a pure improvement, and it means the
blend's apparent consensus is partly manufactured.

### 8. Outlet counts measure coverage, not truth

248 "for" citations against 122 "against" (67% positive), and 11 of 77 players have no recorded
counter-argument at all. A search for reasons to draft someone surfaces bullish copy; the
for/against split is a record of what was written, not of what is right. It should be read as
"how contested is this name", never as a probability.

### 9. The simulated opponents cannot start a run

Each opponent draws a draft position per player from `Normal(ADP, sd)` once per draft and takes
the smallest available subject to roster caps. Nothing in the loop reacts to what was just taken,
so positional runs — the single most common way a real draft goes sideways — never happen. Real
availability variance is therefore wider than the simulation shows, and the tight availability
numbers (99%, 100%) are overconfident.

### 10. Half the ADP inputs are eight to twelve days old

Draft Sharks, Underdog, FFPC, UDK, Yahoo and the older Sleeper and FFC pulls are dated Aug 24-29.
`build.py` down-weights them to 0.1x once three Sept 4 feeds exist, which is right, but the
**calibration offsets are computed with no recency weighting at all**, so stale boards still shape
the corrections applied to fresh ones.

## One criticism that did not survive testing

I expected the calibration to be corrupted by a scale mismatch: offsets fitted in rank space but
applied to raw pick numbers, where a 12-team feed's numbers run to 192 and ESPN's to 140. Measured
over the 110 shared players inside the drafted range, the mean raw ADP is ESPN 70.4 against FFC
64.5, a ratio of **0.93** — the raw scales already agree, and FFC is if anything slightly earlier.
The concern is cosmetic. It is recorded here because a red team that only confirms its own
suspicions is not a red team.
