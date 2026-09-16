# In-season: start/sit and waivers from screenshots

No front end. You send screenshots, I transcribe them into two small files, run the engine,
and you get a report. This page is the contract so it is fast every week.

## What to send each week

1. **Your roster page** — ESPN "My Team", showing every player and the slot they are in
   (QB / RB / WR / TE / FLEX / D/ST / K / Bench / IR). One screenshot, or two if it scrolls.
2. **The waiver wire** — ESPN "Players" tab filtered to *Available*, sorted however you like.
   The top 25-40 is plenty; scroll once if needed. Position filters are fine (send RB, then WR).
3. Optional but useful: your **opponent's roster** for the week, and the **matchup page** if
   ESPN shows projected scores. Not required.

Send them any time after Tuesday's waivers clear; the engine needs the week's injury reports,
which firm up Wednesday-Friday, so Thursday is the sweet spot for the lineup call and
Tuesday night for the waiver call.

## What I do with them

```
roster.txt   ->  python3 intake.py roster  < roster.txt  > roster.json
waivers.txt  ->  python3 intake.py waivers < waivers.txt > waivers.json
                 python3 weekly.py --week N roster.json waivers.json > week_N.md
```

`intake.py` resolves every name against the 253-player model with the same forgiving matcher
the draft app used, and **refuses to run if any name fails to match** — a transcription slip
is shown, never silently scored. Ambiguous matches are echoed with the alternatives so you can
correct me in one line.

## Roster file format

Slot prefix, then the name as it reads on the page. Bench lines can drop the prefix.

```
QB   Justin Herbert
RB   Chase Brown
RB   Breece Hall
WR   Ja'Marr Chase
WR   George Pickens
TE   Tyler Warren
FLEX DeVonta Smith
DST  Steelers
K    Harrison Butker
BE   Rome Odunze
BE   David Montgomery
BE   Tucker Kraft
BE   Chuba Hubbard
BE   RJ Harvey
```

K and D/ST are carried through but not scored by the player model; the report handles them
with their own matchup table.

## What comes back

One markdown report:

- **Start this** — the lineup, one line per slot saying why (matchup, usage trend, injury).
- **Close calls** — every bench/flex decision with the margin in projected points, so you can
  overrule with a reason.
- **Waivers** — ranked adds with a this-week score and a rest-of-season score, who to drop
  for each, and a FAAB/priority suggestion.
- **Watch list** — injury designations to check before kickoff and the pivot if one is out.
