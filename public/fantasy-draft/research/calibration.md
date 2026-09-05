# Translating 20+ sources onto our league's scale

Our league is ESPN, 10 teams, full PPR. Most of the sources feeding the model are not: Underdog and
Draft Sharks publish half PPR, FFPC is TE-premium, and the Fantasy Football Calculator and UDK
feeds are 12-team. Blending those raw imports their format. This is how each one is measured and
corrected. Run `python3 calibrate_adp.py` and `python3 calibrate_ranks.py` to reproduce.

## Method

Every feed is reduced to an ordinal rank **over the players it shares with the reference**, so a
feed's coverage cannot masquerade as bias, and 12-team pick numbers and best-ball boards become
comparable. For each feed and position we take the median of `log(rank_feed) - log(rank_ref)`, then
subtract the feed's own overall offset. What is left is pure positional bias: *this feed ranks tight
ends x% later than it ranks everyone else, compared with the reference*. That is the number applied.

Two properties make the result trustworthy rather than asserted:

- **The method validates itself.** `udk_espn_pick` and `fantasypros_espn` are ESPN-derived feeds and
  calibrate to ~0.0 on every position, which is the correct answer for a feed being compared with
  itself.
- **The corrections match the formats.** FFPC, the TE-premium feed, comes out at TE −5.4 and QB
  +11.2 picks: exactly what TE premium does to a board. Nobody told the script which feeds were
  TE-premium.

## ADP feeds vs ESPN (reference: `espn_live`)

Picks relative to where ESPN puts a player at pick 40. Negative = that feed drafts the position earlier.

| feed | format | QB | RB | WR | TE |
|---|---|---|---|---|---|
| `ffpc` | TE premium | +11.2 | −1.7 | +0.0 | **−5.4** |
| `flock_ffpc_rank` | TE premium | +12.9 | −1.3 | −0.2 | **−4.1** |
| `nfc_ppr` (FFC) | full PPR, 12-team | +3.2 | +0.4 | −5.3 | **+9.9** |
| `nfc_ppr_aug28` | full PPR, 12-team | +4.5 | +0.4 | −5.1 | +8.1 |
| `underdog` | half PPR, best ball | +1.5 | −0.3 | −2.8 | +5.5 |
| `udk_underdog_pick` | half PPR, best ball | +1.6 | −0.3 | −2.4 | +5.6 |
| `draftsharks_half_consensus` | half PPR | +1.3 | −1.8 | −0.5 | +1.6 |
| `fantasypros_rtsports` | full PPR | +8.3 | −5.0 | +0.0 | +4.8 |
| `udk_espn_pick` | 12-team ESPN | +0.0 | +0.0 | +0.0 | +0.0 |
| `fantasypros_espn` | full PPR | +0.0 | +1.2 | +0.0 | −0.8 |

The two 12-team FFC feeds are the clearest league-size signal: with 12 teams more receivers are
needed, so they go earlier and tight ends slide about ten picks later than they do in a 10-team room.

## What correcting it actually changed

Honestly: not much, and that is the right answer. `espn_live` already carries 3x the weight of any
other feed, so the blend was anchored to our platform before any of this. Inside the 140 drafted
picks the average moves are

| position | mean move | largest |
|---|---|---|
| QB | −1.80 picks | −2.8 (Baker Mayfield) |
| TE | −0.84 picks | −1.2 |
| RB | +0.19 picks | +0.5 |
| WR | +0.23 picks | +0.6 |

The practical consequence is that the late quarterbacks are about two picks less of a bargain than
the uncorrected blend claimed: Herbert's value over our composite drops from +9.8 to +7.8, Lawrence
from +5.2 to +3.3, Dart from +2.2 to −0.1. No recommendation changes, but the numbers behind them
are now measured in our league's units. Outside the drafted range the corrections are larger
(up to 8 picks), which matters for deep-bench darts.

## Ranking lists

A positional tilt in a *ranking* is usually an opinion, not an error, and the model's expert-spread
metric depends on that disagreement being preserved. So the same measurement is run against the
full-PPR consensus (FantasyPros PPR ECR) purely as a format check, and only a list whose tilt is
structural *and* matches a format it does not claim gets corrected.

One list qualifies. `lineupexperts` publishes an unlabelled "Rk" board that ranks tight ends about
16 picks earlier than every full-PPR list while sitting near zero on QB, RB and WR — the TE-premium
signature. That column is translated; nothing else is touched. The next-largest tilts
(`rotowire_rank` at RB −8.6, `subvertadown` at TE −9.5, `bdge_top50` at RB −11.9 on 50 players) are
left alone as genuine analyst positions.

Effect: the elite tight ends barely move (Bowers 20.8 → 20.3), while deep tight ends fall 5-9 ranks,
which is the correct direction for a full-PPR board.

## Limits

- The reference is ESPN's own board, so this corrects *toward the room we draft in*, not toward an
  abstract "true" full-PPR ranking. That is the right target for this league and the wrong one for
  any other.
- Offsets are medians over roughly 130-160 shared players inside the drafted range; positions with
  fewer than 12 shared players fall back to the feed's overall offset.
- The half-PPR and standard overlays in the app are *not* calibrated this way — they use
  format-native feeds (FFC half/standard, Sleeper half/standard) directly, which is more accurate
  than translating a full-PPR board.
