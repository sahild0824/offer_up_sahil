# The projection gap in the pick scoring model

Status: **investigated, not shipped.** The scoring model is unchanged.

## The gap

`liveScore` (index.html) and `pick_score` (scenario.py) rank a player almost
entirely on market composite rank, `-ln(comp)`, with a coefficient of 1.0 and an
observed span of 5.92. Projected fantasy points never enter the score at all.
The five quality terms (boom, bust, risk, situation, playoff SoS) contribute a
combined sd of 0.152, so they cannot move a player past a composite-rank
neighbour either.

The visible symptom: at pick 57 of a 10-team full-PPR draft with no quarterback
rostered, the model prefers Justin Herbert (281 projected) to Jalen Hurts (298),
because Herbert's ADP is better. Within a position, the model does not know
which player scores more.

## What was measured

Five candidate fixes were designed independently, each backtested inside
`montecarlo.py` in its own worktree, then the winner was checked by three
adversarial reviewers. 16 agents, ~2.35M tokens.

Ranked by measured gain over baseline (mean lineup value, slot 4, hero-rb):

| candidate | best weight | delta | notes |
|---|---|---|---|
| scarcity-cliff (live replacement) | 0.35 | +12.50 | winner on the sweep |
| vor-static (fixed baselines) | 0.25-0.35 | +12.81 | indistinguishable, far simpler |
| within-tier tiebreak | - | smaller | |
| opportunity-cost | - | smaller | |
| roster-aware | - | smaller | |

The effect is real. On a held-out grader the term never read (CBS projections
alone, 222/253 players, r = 0.946 against the blend the term used), the winner
still gained **+7.10** at w=0.35 — about 43% smaller than the in-sim number,
which is the size of the self-fulfilling component, measured rather than assumed.

## Why it did not ship

All three adversarial lenses refuted it.

**1. The advertised mechanism is inert.** The winner was sold as VONA — a live,
board-aware replacement level recomputed every pick. It is static VBD in a
costume. Because `adj = clamp((proj - repl) / SCALE)` and `repl` is a
per-position constant, the replacement level cannot reorder any within-position
pair: **0 of 9872 within-position pairs reorder** between the live baseline and a
fixed one. Swapping the live apparatus for board-independent constants moves the
result by +0.20 ±0.48 — indistinguishable. The per-pick sort, the mutable module
global, the ctx-before-score ordering dependency and a third JS mirror buy
nothing. `vor-static` is the same effect with none of the machinery.

**2. The objective is broken, which is why the sweep ran to its grid edge.**
`lineup_value` ends in `0.25 * best five leftovers`, ranked on raw cross-position
points. An unstartable QB2 at 286 projected is worth 0.25 x 286 = 71.5 to the
metric; the RB6 he displaces is worth 35.0. The objective pays +36 for a second
quarterback that can never start in a 1-QB league. At w=10 in half-PPR, 53.5% of
drafts take two quarterbacks and 51.5% hit the RB cap — and lineup_value is at
its **maximum**. Every weight sweep will run to its edge until this is fixed.

**3. The headline slot cell is one player flip.** The +59.8 gain at slot 2 that
made the per-slot curve look 15x dispersed is Ja'Marr Chase -> Bijan Robinson in
1097 of 1500 sims; 92% of the delta is that single substitution. It rests on a
24-point projection gap between two players whose own source blends disagree by
projSd 30.0 and 16.2 — the decision sits inside the noise of its own input, and
is then graded on the quantity that made it.

**4. The noise floor used was the wrong one.** ±1.02 measures draft noise with
the projection file frozen. Resampling `proj ~ N(proj, projSd)` — projSd is
present on all 253 players — puts the real floor near **5 points** at slot 4. The
+12.5 is roughly 2.5x the floor, not 12x.

### Integration defects found along the way

- **`draft_review.py` is a silent no-op.** It calls `sc.pick_score` without ever
  calling `sc.scarcity_ctx`, so the module global stays empty and the term
  returns 0.0 for every player. Byte-identical output to the pristine repo, same
  md5. The tool that grades a real draft would have scored against the old model
  while the app recommended with the new one, with no error.
- **The planner and the app disagree on replacement level for the same pick.**
  `scenario.py` builds the scarcity pool from a board already filtered by
  `p_avail >= min_avail`, then `scarcity_ctx` subtracts `gap` players again — the
  same departures twice. RB replacement 233.8 in the planner, 245.2 in the app.
- **The clamp is already saturated on today's data**, not at future risk: at
  slot 1 pick 1, Gibbs's raw cliff is 1.027 and pins at 1.000.
- **The format toggle changes the recommendation.** `SCAR_SCALE = 120` is
  PPR-calibrated, but QB projections are identical across formats while
  RB/WR/TE compress 20-45%. In standard scoring at pick 57 the top pick flips
  from Luther Burden to Jalen Hurts purely from the dropdown.
- **It overrides the user's chosen strategy.** wr-heavy's round-2 pick goes from
  WR 99% / RB 0% to WR 73% / RB 27%.

## If this is picked up again

Do these in order. The first is a prerequisite for any further tuning.

1. **Fix `lineup_value` first.** Exclude surplus quarterbacks from the bench
   term and value the rest against each position's waiver replacement (the data
   is already present). Until then no weight sweep means anything.
2. **Ship `vor-static`, not the scarcity term** — same measured gain, none of
   the machinery, and `draft_review.py` stays correct for free:

   ```python
   VOR_BASE = {"QB": 283.0, "RB": 184.0, "WR": 191.0, "TE": 171.0}  # build.py:128, :616-623
   def vor_adj(p):
       b = VOR_BASE.get(p["pos"])
       if b is None or not p.get("proj"):
           return 0.0
       return max(-1.0, min(1.0, (p["proj"] - b) / 120.0))
   ```

   then `s += VOR_W * vor_adj(p)` at the one hook in each mirror, `VOR_W` in the
   0.25-0.35 band. Never at the grid edge.
3. **Re-derive the weight against a projection-resampled floor**, not the
   paired-sim one: let the term read a resample, grade on the shipped proj,
   report the between-replicate sd.
4. **Recalibrate `SCALE` per scoring format**, or the toggle keeps changing the
   recommendation.
5. **Keep the formula in one place.** It already exists in three mirrors
   (scenario.py, montecarlo.py, index.html) and a fourth caller drifted silently
   the moment a term was added.
