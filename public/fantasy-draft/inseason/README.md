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

Two optional inputs cover what the data files cannot see yet:

```
python3 weekly.py --week N roster.json waivers.json --news news.json > week_N.md
```

- **`news.json`** - players ruled out by news that has not reached the official injury file
  (Tuesday's MRI, a season-ending IR move). Each one projects to zero for the stated weeks, and
  70% of his per-game role passes to his healthy same-position teammates by recent snap share,
  or by the split you name in `heirs` when the beat reporting is clearer than the snap counts:

  `weeks` is a count, `"season"`, or a spread of outcomes for a week-to-week injury
  (`{"1": 0.45, "2": 0.35, "4": 0.2}`), in which case every combination is simulated and
  averaged, so a handcuff earns credit only in the weeks he would actually start.

  ```json
  {"out": [{"name": "Breece Hall", "pos": "RB", "weeks": {"1": 0.45, "2": 0.35, "4": 0.2}, "note": "quad"},
           {"name": "De'Von Achane", "pos": "RB", "weeks": "season", "note": "torn ACL"},
           {"name": "Travis Etienne", "pos": "RB", "weeks": 3,
            "heirs": {"Alvin Kamara": 0.65, "Kendre Miller": 0.35}}]}
  ```

- **FantasyPros freshness** - `ingest.py` drops any FantasyPros row whose game is not this
  week's game. The mirror can lag: the 2026-09-28 scrape still held Week 3 rankings on the
  Tuesday of Week 4. When every row is stale the report says so in its header, projections run
  on usage and matchup alone, and the D/ST table ranks by opponent implied total instead.

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
- **Bench** — each bench player's rest-of-season points and, more usefully, how many points
  your season lineup loses without him. That is the real price of a drop: a backup quarterback
  costs exactly his starter's bye week; a receiver who never starts costs nothing.
- **Waivers** — ranked adds, each paired with the drop that leaves the best season lineup, with
  a this-week lineup gain and a rest-of-season lineup gain. Rest of season is simulated one
  week at a time through Week 17: byes zeroed, known absences zeroed, heirs promoted, and for
  a week-to-week injury averaged over the return dates in `news.json`.
- **Watch list** — injury designations to check before kickoff and the pivot if one is out.
