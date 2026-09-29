# Week 4 plan as proposed, and the three-lens verification

The synthesis agent's plan, then three independent skeptics per move (role and injury, opportunity cost, market and timing), each told to refute unless the evidence clearly supports the move. A move dies when two of three refute it. The final report (`reports/week04.md`) applies these verdicts.

**Proposed headline:** Bench Breece Hall. That one move is worth about 18 points of Week 4 win probability (62% if he stays in, 80% if benched). Claim Braelon Allen and drop Herbert, as Hall insurance and Week 5-6 bye cover (he doesn't start in Week 4). Upgrade your backup TE: Juwan Johnson for Kraft. Turn Odunze's spot into a rotating streaming slot: a Week 4 defense rental if MIN or BAL is free, a Week 5 kicker, then a Week 6 QB. Start Hubbard at RB2 and Pickens at FLEX. Expected Week 4 win odds are about 78-80%, or about 82% if you land the MIN defense.

**Hall plan:** BENCH Hall for Week 4 and HOLD him. He's about 95% out @CHI: ESPN projects 0.0 and every outlet expects him to miss. All your FLEX alternatives also kick off at 1 PM, so waiting for inactives buys no pivot. Even an active Hall on a snap limit wouldn't clearly beat Pickens. Leaving him in drops your win odds from about 80% to 62%, the single biggest lever this week. Don't drop him: the MRI was better than feared, IR isn't expected, and SI's best case is 1-2 games. My estimate: back in Week 5 about 25-30%, Week 6 about 35%, Week 7 about 20%, later about 15%; about 2.2 games missed on average. Move him to an IR slot only if your league has one and ESPN changes his tag from Q to Out/IR, then use the freed spot for Move 6 right away. Claim Braelon Allen (Move 1, drop Herbert) as insurance and bye cover, not as a Week 4 starter: he ranks 4th in the Week 4 FLEX order behind Hubbard, Pickens and Montgomery. If Wednesday's Jets update brings IR or a multi-week timeline, Allen becomes a real Week 5-7 starter (start him over Montgomery in Week 5 if the reporting keeps calling him the clear lead). When Hall returns and practices fully, Hall starts and Allen stays on the bench as his handcuff (quad strains re-injure easily).

## Move 1: add Braelon Allen (RB NYJ) / drop Justin Herbert (QB LAC) - SURVIVES (1 of 3 refute)

Kind: claim-now. Condition: None. Claims likely process before the Jets' Wednesday Hall update, so bid on today's information. If you lose the claim, don't chase Gordon or Kamara. Keep Herbert until Week 5 and make him the drop for the Week 5 kicker instead.. FAAB: 20% (range 15-25%). Go to 25-30% only if you'd have to bid after an IR announcement. Consensus range is 15-35%; you don't need the top of it, because he's insurance and bye cover here, not a Week 4 starter..

Rationale: Hall has a right quad injury and is week-to-week. SI says the best case is 1-2 games; my estimates from the reporting: 25-30% he misses 1 game, 35% 2 games, 20% 3 games, 15% 4 or more. Allen took all 17 snaps after Hall left, Isaiah Davis has 0 offensive snaps, and Cimini (via CBS) calls Allen the clear lead rusher. So Allen is your own backfield's replacement. He's a coin flip with Montgomery for RB2 in Week 5 (Hubbard's bye) and fills FLEX in Week 6 if Hall is still out (about 35%). Herbert is the right drop. He's on the week's clearest drop lists (FantasyPros, PFF, Yahoo). His only job is Goff's Week 6 bye, and that game is @KC, the defense allowing the fewest QB points (8.9 per game). Any Week 6 wire streamer (Young @PHI, Love vs DAL) beats him by about 4-6 points. Rolling priority: this is the one contested claim worth your top slot.

- **role-and-injury** - upheld: Verdict: not refuted. Allen's role is real. It only lasts while Hall is out, and the move is sized for exactly that: insurance and bye cover, not a Week 4 starter. The drop (Herbert) is the right one.

1) THE ROLE IS REAL (local data plus 2026 reporting). In nflverse Week 3 snap counts, NYJ ran 66 offensive snaps (Geno Smith 66). Hall had 32 and Allen 34, which adds up to the whole backfield. Isaiah Davis had 0 offensive snaps in Weeks 2 and 3 and played special teams only (16-22 snaps a game). That fits the claim that Allen took all of the roughly 17 snaps after Hall left early in the 4th quarter. Allen's 7 touches that day (4 carries, 3 catches) are consistent with Yahoo's report that he had 6 touches on NYJ's final two drives. SI, via search summary, says Allen "will act as the team's starting running back." Rotowire, CBS and Cimini call him the lead. The engine's heir split (Allen 0.8, Davis 0.2) already allows for Davis mixing in.

2) THE ROLE IS NOT DURABLE, and the plan says so. Its value depends on Hall's absence: MRI better than feared, week-to-week, best case 1-2 games. When Hall is healthy, Allen is a 31-40% snap backup (10/5/4 carries, 4.9 PPR per game). What could change the role:
- Hall returns in Week 5 (about 30% in the plan's estimate). Allen then goes back to handcuff.
- Davis gets a bigger share. Two 9/29 search summaries (Yahoo, LastWordOnSports) say fans should "expect an increased role" for Davis, who caught 21 passes in 2025 after Allen got hurt. That threatens Allen's pass-down work in full PPR.
- The run game is poor. Allen has 3.2 yards per carry (19 carries, 61 yards), Hall averaged 2.0 and 2.5 yards per carry in Weeks 2-3, LG Parham is hurt, and NYJ's Week 4 implied total is 19.5.
- Kene Nwangwu (back) shows as ACT in the Week 4 roster data. He is a return man and no threat to Allen's snaps.
- Allen himself has no 2026 injury-report entries. The "season-ending knee injury (MCL) in Week 4 loss to Miami" that turns up in searches is from 2025 and is stale for his current health. It is a minor durability flag at most.

3) THE ENGINE: A SMALL BUT POSITIVE EDGE. I ran pkg2.py in research mode with its long and short variants.
- FINAL package (with Allen): +7.7 over Weeks 5-17. ALT3 (Raymond instead of Allen): +6.7. ALT2 (Gordon instead of Allen): +6.7.
- Allen adds about +1.0 in the base case (+0.3 Week 5, about +0.7 Week 6), about +2.4 if Hall is out 5 weeks, and 0 if Hall misses only 1 game.
- Allen/Herbert on its own shows -11.3, only because it drops Herbert with nothing to cover Goff's Week 6 bye. The plan's streaming slot (Move 5, Young as the Week 6 proxy) covers that. Herbert @KC (8.9 QB points per game allowed) is worth little.
- Gordon has a longer-lasting role, but MIA's Week 6 bye and Jaylen Wright's return keep him no better on this roster.
- So Allen is the best of several near-equal options, and his main value is the tail case of an IR or multi-week Hall absence.

4) THE CONDITION IS THE RIGHT TRIGGER. Allen is a consensus top-2 add, and claims will likely process before Glenn's Wednesday update, so bidding on Tuesday's information is correct. "Don't chase Gordon or Kamara" is also correct, since neither beats the bench here.

Caveats, not grounds to refute:
(a) Make the Week 5 RB2 choice Montgomery by default, not a coin flip. Start Allen over him only if Allen's Week 4 box score shows a workhorse share (roughly 65% or more of snaps with Davis at 25% or less) and Hall is ruled out.
(b) At an expected value of about +1 lineup point, a bid at the low end of the proposed range (about 15%) fits the role's short life better than 20%. Stay out of the 25-35% consensus top.
  - Better alternative: Make the move as proposed, with two tweaks from the role evidence. First, bid about 15% FAAB (the low end of the proposed range): Allen's value to this roster depends entirely on Hall's absence and is worth about +1 lineup point in the base case (+2.4 if Hall is out a long time, 0 if he misses one game). Second, make Montgomery the default Week 5 RB2. Start Allen over him only if Hall is ruled out and Allen's Week 4 usage shows a workhorse share (roughly 65% or more of snaps, with Davis at 25% or less). Davis is widely expected to 'mix in' and could take the passing-down work that PPR scoring rewards.
- **opportunity-cost** - upheld: Herbert is the right drop, and no other add or drop beats the proposal. The move only holds up as part of the whole plan, though: it depends on Move 5, the Week 6 QB stream, actually happening.

1) The drop costs nothing, as long as a Week 6 QB gets streamed. The only lineup points Herbert gives this roster are Goff's Week 6 bye, at KC. I checked this locally: KC has allowed 8.9 QB points per game in Weeks 1-3, the fewest in the league. The Week 6 streamers face much softer defenses: PHI allows 20.7 and DAL allows 23.5. Herbert averages 11.3 PPR a game (13.3, 7.9, 12.7). I ran the engine three ways: if Allen replaces Herbert and nobody else covers Week 6, Week 6 loses 11.6 points (ROS -11.3). With the plan's Week 6 stream (Young as the stand-in), Week 6 gains 4.0 over keeping Herbert. The streaming slot has a backup plan: Love vs DAL, Darnold, Brissett and Cousins are all on the wire.

2) No other drop is better. Dropping Odunze and keeping Herbert, with the rest of the plan unchanged, scores exactly the same as the proposal under every Hall timeline I tested (ROS +7.7 base, +10.4 long, +6.0 short, +10.5 with Montgomery's rate cut to 10). That's because the plan cuts both players by Week 5 anyway (Move 3 or Move 4). Herbert is also the weaker hold. His FP ROS rank has fallen from QB8 to QB12, and the prior research found him on drop lists at FantasyPros, RotoBaller and PFF. The QB wire is deep in a 10-team, 1-QB league, so he has almost no value as Goff insurance. Odunze has some trade value and a good playoff schedule (WR SOS rank 9). Kraft is already the drop for Move 2. Keeping Kraft instead of adding Juwan comes out worse (+5.7 vs +7.7).

3) No other add is better. With the rest of the plan fixed, Allen at +7.7 (base) beats Gordon, Kamara and Raymond, which all come out at +6.7. He beats them by 2.4 if Hall is out 5 weeks and ties them if Hall returns in Week 5. If Montgomery's rate drops to 10, Allen reaches +10.5 against Gordon's +8.7. Allen fits the byes: NYJ plays Week 5 vs CLE and Week 6 @NE. Gordon's MIA is off in Week 6, the week Chase Brown is also off, and Jaylen Wright threatens his workload. Young beats Herbert in the engine (+4.0), but the Week 6 stream already captures that value.

Caveats. None of these overturns the move:
(a) The margin is thin. The engine values Allen at +1.0 ROS over the next best use of the slot, ranging from 0 to +3.1 across scenarios. Most of his value is insurance the engine doesn't model (Hall re-injuring the quad, or another RB going down). So 20% FAAB is defensible, since it sits in the 15-35% consensus range, but it's on the rich side. 10-15% fits the modeled value better.
(b) Under rolling priority, spending the top slot on Allen is close to a wash with protecting the Juwan claim. Juwan is worth +2.7 against Likely's +1.4 as the fallback, so losing him costs about 1.3.
(c) A small citation error: the rationale says Yahoo put Herbert on a drop list. The prior research documents FantasyPros, RotoBaller and PFF, and cites Yahoo's drop list only for other players.
(d) Execution risk: Herbert's drop only works if Move 5 (the Week 6 QB stream) actually happens. If the plan falls apart before Week 6, a QB still has to be added.
  - Better alternative: Nothing clearly better. Make the move as proposed with two adjustments. First, treat Move 5 (the Week 6 QB stream) as required: this drop depends on it, and without it Week 6 loses about 11.6 points. Second, a lower bid of about 10-15% FAAB fits Allen's modeled value (+1.0 ROS over the next best use of the slot) better than 20%. Dropping Odunze instead of Herbert is exactly as good but no better.
- **market-and-timing** - refuted: Claiming Allen is fine as a cheap flyer. Paying 20% FAAB, or 25-30% after an IR move, and spending the top rolling-priority slot on him is not supported. That includes the plan's own engine.

1) Value to this roster is about 1 point. I re-ran the cited engine (synth/pkg2.py, research mode, Hall spread 30/35/20/15%) and isolated Allen. The full plan is +7.7 over Weeks 5-17. The same plan without Allen, keeping Herbert (Juwan/Kraft + Young/Odunze), is +6.7. So Allen adds about +1.0: +0.3 in Week 5, +0.7 in Week 6, and 0 in Week 4 and Weeks 7-17.
- If Hall is back in Week 5 (news_short): 0.
- If Hall is out through Week 8 (news_long): +2.4. Even then Allen doesn't start in Weeks 7-8, because Pickens (13.8) projects above Allen's lead-back rate (13.0). This case is what the plan's "25-30% after IR" rule is priced for, and it only reaches +2.4.
- With a pessimistic bench (Pickens 11.5, Montgomery 11.0): +2.5 expected, +6.8 in the worst case.
- The plan admits the same thing. Allen is 4th in the Week 4 FLEX order and a coin flip with Montgomery in Week 5. In Week 6 he only beats Juwan at FLEX, and only in the roughly 35% case that Hall is still out.

2) The price is anchored to the wrong market. The 15-35% consensus is what a team that would start Allen pays. This team has five RBs of depth, counting Pickens at FLEX. Sources already in the research files argue for restraint:
- SI's range is 7-15%.
- DK Network says not to unload FAAB on him.
- CBS calls him "not a rest-of-season solution".
- prior/roster-injuries.md says "Moderate FAAB bid, not all-in".
- prior/ros-forecasts.md says "SHORT-TERM ONLY... claim only as Hall insurance if the Wednesday update suggests a multi-week absence".
Twenty percent of a season's budget in Week 4, for about 1 expected point, gives up option value on later injury replacements. A 10-team wire will keep producing those.

3) Timing: it isn't now-or-never, and losing him costs little. If he clears waivers, he's a free agent on Wednesday morning, before Glenn's update, and costs $0. If someone outbids a low bid, the loss is about 1 point, or about 2.4 in the bad Hall case.

4) The claim order is backwards. The plan says Allen is "the one contested claim worth your top slot". The engine disagrees: Juwan/Kraft alone is +2.7, mostly Weeks 9-17. Losing Juwan to the Likely fallback costs 1.3 points, more than Allen's whole marginal value of 1.0. Under rolling priority, winning Allen first would push the Juwan claim to the back of the order.

The Herbert drop itself is defensible: he's on the drop lists, and a Week 6 stream is +4.0 over him @KC. My objection is to the price and priority, not the roster logic.

This rests on the engine's rate assumptions and an unknown league format (FAAB vs rolling, budget size). None of the other adds is modeled as a lock either.
  - Better alternative: Keep the Allen claim with Herbert as the drop, but bid what he is worth to this roster:
- FAAB: about 5-8% (at or below SI's 7-15%).
- Rolling priority: don't use the top slot. Order the claims Juwan Johnson/Kraft first, Likely/Kraft as the fallback, then Allen/Herbert.
- If Allen clears waivers, add him as a free agent right after waivers process Wednesday, before Glenn's update.
- If you're outbid, let him go and don't chase him, Gordon or Kamara.
- Drop the rule to go to 25-30% after an IR announcement. Even with Hall out through Week 8, the engine values Allen at +2.4 because Pickens outscores him at FLEX.

## Move 2: add Juwan Johnson (TE NO); fallback Isaiah Likely (TE NYG) with the same drop if Juwan is claimed first / drop Tucker Kraft (TE GB) - DIES (3 of 3 refute)

Kind: claim-now. Condition: Put Likely on a second claim with the same drop; it only processes if the Juwan claim fails.. FAAB: Juwan 4-6%. Likely 2-4%. Skip Squawk's 10-18%: that's starter money, and this is a backup TE..

Rationale: Juwan has 16.1 PPR per game (15-173-3 on 19 targets). He's NFL.com's headline TE add, in a pass-heavy NO offense with the 2nd-easiest TE schedule for Weeks 5-17. His Week 8 bye covers Warren's Week 13 bye. Kraft is at 6.5 PPR per game with two drops in Week 3; his workload is back but the production isn't. Risks: Noah Fant's snaps (57% in Week 3) and TD-driven scoring. Likely is the fallback: better role (84% of snaps, 24-31% target share), but only 5.8 PPR per game with Winston, who starts the rest of the year, and a poor TE playoff schedule. Sadiq doesn't fit: his Week 13 bye is the same as Warren's.

- **role-and-injury** - refuted: Refuted as proposed (claim now, 4-6% FAAB, with Likely as the fallback). I'd hold this claim until after Week 4, not drop the idea. The swap is slightly positive on paper, but the gain is tiny and fragile. Juwan's role is less durable than the rationale says, and waiting a week costs almost nothing, because a backup TE only matters in Week 13 or if Warren gets hurt.

1) Juwan's role is shrinking into a platoon (nflverse snaps).
- Juwan's snap share: 84% / 53% / 62% (76, 36, 46 snaps).
- Noah Fant's snap share: 41% / 44% / 57% (37, 30, 42 snaps). In Week 3 the split was nearly even, 46 to 42.
- The strong route share people cite is from Week 1 only: DraftSharks has Juwan on 84% of routes to Fant's 30%. I found no Week 2-3 route data, and the snaps point the other way.
- Fant has 12 targets and 3 TDs of his own, so he takes red-zone work from the same pool that inflates Juwan's numbers.

2) The 16.1 PPG is propped up by TDs and short throws.
- He has 3 TDs on 19 targets (16%) and lost a fumble in Week 3.
- His air yards fell from 77 to 11 to 15, and his air-yards share from 16% to 5% to 5%. Weeks 2-3 were almost all short catches.
- Week 3's 8-53-2 came in a shootout where the four TEs in the game scored six TDs between them, which ties the NFL record for the position (NBC, RotoWire).
- Without TDs he's about 10 PPR a game. That still beats Kraft's 6.5, but it isn't a TE1 role.

3) His role could change soon. Jordyn Tyson, the #8 overall pick, is on the reserve list through Week 4 in nflverse's weekly rosters and is listed at WR5 on the 9/29 depth chart. The prior research says he's eligible to return in Week 5, which adds target competition behind Olave's 10-13 targets a week.

4) Kraft's role is actually the steadier one. He's GB's clear TE1 on the 9/29 depth chart, with 66% / 98% / 76% of snaps. Jonnu Smith, the TE2, played 47% / 22% / 33%. Kraft's target share is 15% / 10% / 16%, and he gets about as many targets as Juwan (5.7 a game vs 6.3). His problem is production: 2 drops and a 53% catch rate. He's also coming back from an ACL tear and was the TE2 in fantasy scoring in 2025 before he got hurt. FantasyPros' 9/25 rest-of-season ranks have Kraft TE7 and Juwan TE12.

5) The bye argument doesn't separate the two players. Kraft's Week 11 bye covers Warren's Week 13 bye just as well as Juwan's Week 8 bye does. In Week 13, GB plays at NO, so both backups are in the same game.

6) I ran the engine, and the gain is small and fragile.
- With the synth research overrides (Juwan 11.0 a game, Kraft 9.0), Juwan-for-Kraft adds 2.7 points over Weeks 5-17, almost all of it the Week 13 start.
- In pure-data mode it adds 4.5. Pure data prefers Likely at +10.6 (rates: Juwan 11.7, Likely 12.2, Kraft 9.3).
- The result flips with small changes. With Juwan at 9.5 a game it's +0.7. With both at 10 it's 0. With Juwan 9.5 and Kraft 10.5 it's -1.3.

7) The fallback has problems too.
- The mechanics are fine on ESPN: with the same drop, the second claim fails once the first processes.
- Likely's value is only about +1.4 in research mode.
- The rationale itself says Likely's role is better (84% of snaps, 24-31% target share, a team-high 23 targets), so ordering him as the fallback contradicts the role data.
- "Winston starts the rest of the year" is overstated. NYG traded for J.J. McCarthy, who is already QB2 on the 9/29 depth chart.

Bottom line: the case for Juwan leans on a TD spike and on a bye point that doesn't separate him from Kraft, while the snap data shows the role getting weaker. The upside is at most a few points, all in Week 13. Waiting through one game (Juwan plays Monday night, before Week 5 waivers) settles the Fant split and Tyson questions at almost no cost.
  - Better alternative: Don't put in a claim this week. Keep Kraft through Week 4, and save the FAAB and waiver priority for the Hall and D/ST moves due before Thursday.

Revisit on Week 5 waivers, after Juwan's Monday-night game against ATL. Claim Juwan (drop Kraft) only if all of these hold:
- He out-snaps Fant again with at least 60% of snaps.
- He gets at least 6 targets.
- The Saints haven't opened Jordyn Tyson's practice window, or Tyson is back only in a limited role.

If someone else claims Juwan in the meantime, don't chase him. Kraft is only about 3 points behind over the rest of the season and has the steadier TE1 role.

Drop the Likely fallback, or rank Likely first if you want to upgrade purely on role. His role is the most durable of the three, but with Winston throwing, and McCarthy already on the roster, he's only worth about +1.4 points over Kraft.
- **opportunity-cost** - refuted: The add is defensible, but dropping Kraft is the wrong drop, and dropping him now gives up value for nothing.

1) Dropping Kraft is not needed to capture Juwan's value. I ran the engine (verify/oc_move2.py, same synth inputs the plan used). "Juwan / drop Odunze" gives exactly the same lineup gain for Weeks 4-17 as "Juwan / drop Kraft": +2.7 in research mode and +4.5 in engine mode. That holds with Braelon Allen/Herbert applied too (-9.3 vs -9.3, and -10.7 vs -10.7). The engine values Odunze at 0.0-0.2 lineup points; the plan already treats him as a zero-value rotating slot. Once Juwan is rostered, Kraft becomes the redundant piece, so Kraft can take over that rotating slot:
- Use him as the drop for the Move 3 D/ST claim or the Friday Addison pickup if either happens. The end state is then identical to the plan.
- If neither happens, hold both TEs through Week 4 (Kraft @TB Sun 1 PM; Juwan vs ATL Mon night). Cut the worse one for the Week 5 kicker in Move 4, or trade Kraft first.
That costs nothing in the plan's own numbers and gains one week of information. It also keeps a 1 PM pivot if Warren is a surprise inactive for his 9:30 AM London game.

2) The upgrade being paid for is small and depends on the model. The engine gives Juwan over Kraft only +2.7 to +4.5 points across Weeks 5-17 (about 0.2-0.35 a week). Almost all of it comes from the one guaranteed TE2 start (Warren's Week 13 bye) plus about 0.7 points of Week 6 FLEX. In engine (usage) mode, the fallback Likely over Kraft is +10.6, more than twice Juwan's gain. The research-rate overrides flip that to Juwan +2.7 vs Likely +1.4. So even which add is better is unresolved.

3) The rationale's bye and schedule points don't separate the two players:
- Kraft's Week 11 bye covers Warren's Week 13 bye just as well as Juwan's Week 8 bye does. Juwan's bye actually adds a Week 8 hole that Kraft doesn't have.
- Week 13 is GB @ NO, the same game. Kraft faces NO (12.8 TE PPR allowed per game, rank 17) and Juwan faces GB (12.4, rank 20). For the one week that matters, the matchups are equal, so NO's 2nd-easiest Week 5-17 TE schedule is irrelevant for a backup TE.

4) Usage and consensus don't show Juwan clearly ahead:
- Targets are nearly equal. Juwan has 19 (13/12/20% share, air-yards share 16/5/5%); Kraft has 17 (15/10/16%).
- Kraft has the bigger snap role (66/98/76%) than Juwan (84/53/62%, with Fant at 41/44/57%).
- Juwan's expected points are 12.4 per game vs Kraft's 8.8. The 16.1 vs 6.5 PPR gap is mostly Juwan's 3 TDs (+3.7 per game over expected) and Kraft's drops (-2.3 per game under expected).
- FantasyPros rest-of-season PPR TE consensus on 9/25, after Kraft's Thursday Week 3 flop: Kraft 8.0 (range 6-11), Likely 10.4, Juwan 12.8 (range 9-17).
- Kraft's pre-ACL 2025 was 14.6 PPR per game over 8 games; Juwan's 2025 was 10.6. Dropping the higher-consensus player for a spike week hands a possibly tradeable asset (94.6% rostered on ESPN) to the wire.

The rationale's facts are accurate (15-173-3 on 19 targets, 16.1 PPR per game, Fant 57%, Likely 5.8 with Winston, Sadiq's Week 13 bye). The error is in the valuation. Skeptical verdict: as proposed, with Kraft as the drop, the move should not be made.
  - Better alternative: Keep the claim but change the drop.

- Claim Juwan Johnson (FAAB 4-6% is fine), with Isaiah Likely as the fallback, and DROP Rome Odunze instead of Kraft.
- Kraft then becomes the plan's rotating slot:
  - If the Move 3 D/ST claim (MIN/BAL/SEA) is placed, list Kraft as its drop. Same end state as the plan.
  - If Jefferson sits and you add Addison Friday, drop Kraft.
  - Otherwise hold both TEs through Week 4. At the Week 5 kicker pickup (Move 4, about Wed 10/7), cut whichever of Kraft and Juwan looks worse after Week 4, or trade Kraft first.
- If you won't carry two TEs for even a week, the next-best option is to skip the TE move entirely. The engine values it at no more than +4.5 points over 13 weeks, and FantasyPros consensus ranks Kraft above both adds. Also consider putting Likely ahead of Juwan: he wins by 2.4x in engine usage mode and ranks higher in rest-of-season consensus (10.4 vs 12.8).
- **market-and-timing** - refuted: This move should not be made as proposed: claim now, ranked #2 ahead of the D/ST claim, 4-6% FAAB on Juwan plus a 2-4% Likely fallback. The swap is small but real in expectation. The timing, the price anchor and the claim order are all wrong for a backup TE.

1) The price anchor has no source. The consensus file says outright "No FAAB range found for ... Juwan Johnson" (waiver-consensus.md line 310). "Squawk's 10-18%" appears nowhere in the prior research. The consensus file places Juwan in its lowest tier, with Bell, Harris and Raymond, and its own verdict for this roster is "Low priority; claim him only if a bench spot is left after the RB moves." For comparison, Sadiq, the top TE add and a potential starter, goes for 7-13%, and Kamara, an RB with a lead role, for 5-8%. 4-6% on a TE2 prices him like a Kamara-level add.

2) This is buying high and selling low. Actual points and expected points (EP) from nflverse in weekly_2026.json:
- Juwan: 16.1 PPG, but EP is 14.65/6.67/16.0 (12.4 per game). He has 3 TDs on 19 targets and an air-yards share of only 5% in Weeks 2-3.
- Kraft: 6.5 PPG, but EP is 10.69/4.87/10.87 (8.8 per game), with 2 drops.
- Their target shares are nearly identical: Juwan 13/12/20%, Kraft 15/10/16%.
So the 16.1 vs 6.5 gap the rationale leans on is mostly TD and drop variance. The real expected gap is about 3.6 per game. FantasyPros ROS ECR (9/25, before Week 3) still has Kraft TE8 over Likely TE10.4 and Juwan TE12.8. Kraft is also on post-ACL workload management and has second-half upside (ros-forecasts.md). Dropping him gives a rival a TE the market ranks above the player you're paying for.

3) It is not now-or-never. On this roster the TE2 only matters in Warren's Week 13 bye, plus the rare Week 6 FLEX. The engine confirms this:
- te_test research mode: Juwan/Kraft +0.0 in Week 4 and +2.7 over Weeks 5-17.
- Engine mode: +4.5.
- With regression assumptions (Juwan 10.5, Kraft 9.8): +0.9.
- On EP rates (12.4 vs 8.8): +13.8.
- Likely/Kraft: +0.3 to +1.6 (research) and +10.6 in engine mode, which runs on 3-week form (includes his 27.8-point Week 1 with Dart).

The bye point doesn't separate the two players either. GB and NO play each other in Week 13 (games.csv: GB @NO), so Kraft covers Warren's bye just as well as Juwan. TE depth on this wire is also extreme: Likely, 91% rostered on ESPN, and Juwan at 55% are both free. So a Week 13 TE will be easy to find later, and losing Juwan to another team costs roughly 1-4 points. If he goes unclaimed, he becomes a free agent at no cost after waivers clear. Waiting also answers open questions: whether Jordyn Tyson is activated from IR (as early as Week 5), how Fant's snaps (57% in Week 3) trend, and whether Kraft's usage keeps ramping.

4) The claim order is backwards. The league's waiver format (FAAB or rolling priority) is unknown. Under rolling priority, if the Braelon Allen claim fails, this claim burns your top priority on a roughly 3-point backup-TE upgrade. It also sits ahead of Move 3, the time-sensitive D/ST claim that has to process before Thursday and that the plan credits with about +2-4% Week 4 win probability. It could also cost you priority you'll want next week if Hall's Wednesday update means IR. The Likely fallback adds a second claim for near-zero value: ros-forecasts.md says PASS, the TE playoff schedule ranks 24th, and he has 5.8 PPG with Winston.
  - Better alternative: Hold Kraft this week and file no Likely fallback.
- If you still want Juwan, file one minimum-bid claim ($0-1% FAAB) as your LAST claim, below the Braelon Allen claim and the Move 3 D/ST claim. Under rolling priority, don't file a waiver claim at all.
- If he clears waivers, add him as a free agent Wednesday or Thursday at no cost.
- Otherwise, look again after Week 4, once Tyson's activation, Fant's snaps and Kraft's workload are clearer.
- Save the FAAB and the priority for RB fallout from Hall's Wednesday update, and for the Week 5 kicker and Week 6 QB streams.

## Move 3: add Minnesota D/ST (fallback Baltimore D/ST; Seattle if somehow free). If none is available: Jordan Addison as a Friday free-agent pickup / drop Rome Odunze (WR CHI) - DIES (2 of 3 refute)

Kind: conditional. Condition: Only if MIN, BAL or SEA D/ST is on your wire, and the claim processes before PIT@CLE locks Thursday 10/1 at 8:15 PM ET. Otherwise PIT has to be in your lineup by then. If no D/ST is free: once waivers clear, add Addison as a free agent on Friday only if Justin Jefferson hasn't practiced fully Wednesday-Thursday. If Jefferson practices fully, make no move and keep Odunze until Week 5.. FAAB: MIN 1-2%, BAL 1%, Addison $0 (free agent).

Rationale: Consensus Week 4 D/ST order: MIN (vs MIA, implied 14.0; MIA without Achane) > SEA > BAL (vs TEN 16.0) > BUF > your PIT (about 5th). Keep PIT: it's needed for Weeks 5-8 (Week 6 @TB against the undrafted rookie QB is the best Week 6 spot). MIN's defense also tends to score in the same game script that helps Teemo's Jefferson, Hockenson and Reichard. That lowers the variance of your matchup, which helps you as the favorite. The Addison fallback exists because once claims clear he's the only 4:05 PM replacement Teemo could grab if Jefferson (about 50% to play) is a late scratch. Odunze is the drop: 7.2/7.3/7.4 PPR, fourth on CHI in targets, a backup QB until Williams returns around Week 6, and with your RBs covering FLEX a 4th WR almost never starts for you.

- **role-and-injury** - refuted: Only the MIN branch holds up. It probably won't fire, and the branches that would fire in its place are either worthless or triggered wrong.

1) The MIN D/ST branch is well supported.
- MIA scored 13, 13 and 10 points in Weeks 1-3. Malik Willis has started every game at 100% of snaps.
- Achane is on reserve for the season. WR Caleb Douglas was Out in Week 3 with an ankle injury.
- MIN's defense had 14 sacks (4/4/6) and 5 takeaways through three games. It has no defensive injuries of note: the Week 3 report showed only full or limited practices, and Week 3 snap shares held.
- Opponent implied totals: MIA 13.5 vs CLE 18.0.
- My extended sim (MIN D/ST mean 9.0, correlated with MIN game script) raises win probability from 0.797 to 0.823, about +2.6 points.
- The catch is availability. Current write-ups call MIN the No. 1 fantasy D/ST, with double-digit scores in three straight weeks, and it was about 64% rostered in the 9/25 FantasyPros snapshot. In a 10-team league it is very likely already rostered, so the fallbacks are what would actually run.

2) The BAL and SEA fallbacks are not real upgrades over PIT.
- BAL's unit has been poor: 6 sacks, 3 takeaways, and 23/24/31 points allowed.
- TEN's offense has 1 giveaway in 3 games and allowed 0 sacks in Week 3. PIT's unit has 8 sacks, 6 takeaways and 1 TD; CLE's offense has allowed 9 sacks.
- SEA's opponent LAC is implied at 17.75, against CLE's 18.0.
- Even with a generous +0.3 over PIT, the sim barely moves (0.797 to 0.800).
- SEA is about 97% rostered, so it won't be available anyway.
- Under rolling waivers, a winning BAL claim sends you to the back of the order for essentially nothing.

3) The Addison fallback has a role problem and a trigger problem.
- Role: his value depends entirely on Jefferson missing the game. With Jefferson healthy in Weeks 1-2, Addison had 2 and 5 targets and scored 0.0 and 4.1 PPR. Only after Jefferson left Week 3 did he play 98% of snaps, draw 9 targets and score 20.0.
- Jefferson news (9/28): the MRI showed only a sprain, nothing long-term, and he "could play" Week 4. The hurdle is swelling.
- Trigger: "hasn't practiced fully Wed-Thu" fires in the common case where a star with an ankle sprain is limited and then plays. In that case Addison is worth nothing to you or as a block.
- Timing: once waivers clear Wednesday, free agents go to whoever acts first. Teemo owns Jefferson and has the most reason to grab Addison right after a Wednesday DNP (did not practice), so a Friday pickup likely loses the race and the blocking rationale falls apart.
- The claim that Addison is "the only 4:05 PM replacement Teemo could grab" is false. Malik Washington (MIA, same 4:05 game, ESPN 10.0) and Tre Tucker (LV, KC@LV at 4:25) are on the wire, plus Sunday-night and Monday-night players.
- In the sim, the Addison add is worth only about 1-2 points of win probability, and most of that comes from the scenario where Jefferson is ruled out early.

4) Minor point on the drop: Odunze is 3rd on CHI in targets, not 4th. He has 13 targets to Burden's 23 and Raymond's 21, and his snaps are rising (48%, 84%, 85%). Dropping him is still fine, since he is the planned Week 5 drop anyway and never starts for you.

5) The Thursday-lock condition itself is correct. PIT kicks off Thursday at 8:15 PM ET, and ESPN claims clear before then.
  - Better alternative: Narrow the move and fix the Addison trigger.

1) Put in a claim for MIN D/ST only (FAAB 1-2%, or your lowest-priority claim), dropping Odunze. Start MIN over PIT if the claim clears Wednesday. Remove the BAL and SEA branches: neither is a real upgrade over PIT, and SEA is about 97% rostered.

2) If MIN isn't available, add Addison as a free agent on Wednesday evening, right after waivers clear, and only if Jefferson is DNP (did not practice) on Wednesday's report. Otherwise do it Thursday evening if he is DNP on Thursday. Don't wait for Friday: Teemo can grab him first, and that defeats the block. A "limited" practice does not trigger the add. Understand the block is partial, because Malik Washington (4:05) and Tre Tucker (4:25) stay on the wire as late pivots.

3) If Jefferson practices at all (limited or full) by Thursday, make no move. Keep Odunze as Week 4 WR injury cover and drop him for the Week 5 kicker as planned in Move 4.
- **opportunity-cost** - upheld: The drop is right, and adding MIN D/ST is a small gain that costs almost nothing. Only the fallback legs and parts of the rationale are weak. None of them turns the move negative.

1) Odunze is the cheapest player to cut. I ran the engine on the roster after Moves 1 and 2 (Herbert out for Braelon Allen, Kraft out for Juwan) and measured what each possible cut costs the Weeks 5-17 lineup. Odunze costs +0.00 in both research and engine mode, because he never makes a best lineup. The other cuts all cost points: Juwan -11.0 (research) / -13.2 (engine), since he covers Warren's Week 13 bye; Montgomery -1.5 / -4.5; Braelon Allen -1.0 / -0.5. Odunze can't cover any bye either. CHI's Week 10 bye is the same week as DeVonta Smith's. In Week 6, Juwan (11.0-11.7 per game) beats him for FLEX, and in Weeks 10 and 14 the WR holes are filled by Pickens or an RB. The local data confirms his low volume: 3/4/6 targets, 11-18% target share, expected points around 6.5 per game. Under the plan he's dropped for the Week 5 kicker anyway (Move 4), so cutting him one week early only loses a week of waiting for Caleb Williams to return. Receivers of similar rest-of-season value (Tate, Boston, Raymond) are available now in a 10-team league. His real cost is rest-of-season upside once Williams is back, plus some trade value (FP rest-of-season WR32 as of 9/25). That is small, and he can probably be re-added later.

2) MIN is the right add. The local Vegas lines give MIA an implied 13.5, the lowest of the week, against 18.0 for CLE (PIT's opponent). The 2026 box scores back it up: MIN has 14 sacks and 4 INTs and has allowed 22/3/16 points, while MIA has scored 13/13/10. Historically (games.csv 2015-25), the points-allowed tier alone is worth about +1.7 at 12-15 implied versus about +0.4 at 17-19, which supports the roughly +2-point edge. I extended sim2 with a D/ST choice and a MIN game-script factor. Win odds go from 0.795 with PIT to 0.817 with MIN (0.806 if the edge is only +1). The only cost is a 1-2% FAAB bid or a waiver claim.

3) Weaknesses, none fatal:
(a) The correlation / "lowers variance" argument doesn't matter. Win odds are 0.817 with the correlation and 0.816 without it.
(b) The BAL fallback is close to a coin flip against PIT. BAL's defense has 6 sacks and 1 INT and has allowed 23/24/31. PIT has 8 sacks, 6 takeaways and a TD. TEN has only 1 giveaway all season. Taking BAL is worth about +0-1.0% in the sim. It also rules out the Addison fallback: once BAL starts over PIT on Thursday, it can't be swapped for Addison later.
(c) SEA gives no Week 4 edge over PIT. LAC's implied total is 17.75 versus CLE's 18.0, and SEA is 97% rostered anyway.
(d) The Addison fallback's premise is wrong. Addison is not the only 4:05 PM pivot. Malik Washington plays in the same 4:05 game (MIA@MIN; 8/5/10 targets, about 28% share, on the wire), Tre Tucker in LV-KC at 4:25, plus SEA-LAC at 4:25 and the SNF/MNF games. Blocking Addison is worth +1.9% only if Teemo would otherwise add him (the sim's 60% assumption) and I get there first. It's about +0.2% if Teemo is passive. Waiting until Friday also gives Teemo Wednesday and Thursday to take him as a free agent.
(e) Under rolling priority rather than FAAB, a successful rental claim after a failed Allen claim drops you to last in waiver priority for a gain of about 2 points.

Is any alternative strictly better? Among cuts, no: every other drop costs rest-of-season points. Among adds for this slot, whoever holds it is cut in Week 5 for the kicker, so only Week 4 value counts. MIN (+2.2%) beats Addison (+0.2 to +1.9%, and he may not be there) and BAL (0 to +1%). Dropping PIT for MIN and using Odunze's spot for Addison would trade away PIT's Weeks 5-8, so it isn't strictly better either. Keep the move, but tighten the fallbacks as described below.
  - Better alternative: Keep Move 3, with Odunze as the drop, but tighten it:
(1) Claim MIN D/ST only, ranked below the Allen and Juwan/Likely claims. Use 1-2% FAAB. Under rolling priority, accept that it may push you to last.
(2) Drop the SEA leg: it has no Week 4 edge over PIT (LAC 17.75 vs CLE 18.0). Treat BAL as optional at best. It's roughly a coin flip against PIT, given BAL's poor defense and TEN's single giveaway, and claiming it rules out the Addison option.
(3) If MIN isn't available, move the Addison trigger up. Add him as a free agent Wednesday, as soon as waivers clear, if Jefferson doesn't practice or is limited Wednesday. Don't wait until Friday, by which time Teemo may already have him. Present it as a partial block worth about 0-2% win odds. It does not remove Teemo's late pivot: Malik Washington (same 4:05 game) and Tre Tucker (4:25) stay on the wire.
(4) Remove the correlation / variance-reduction argument from the rationale. It changes win odds by only 0.1%.
- **market-and-timing** - refuted: The core of the move holds up. Claiming the MIN D/ST, if it's on your wire, for 1-2% and dropping Odunze is the right time and price. The move as written doesn't hold up, because its two fallbacks are mistimed or unsupported.

What holds (MIN D/ST):
- Local lines have MIA implied at 13.5, the lowest of Week 4 (the 9/29 re-pull had 14.0). MIA scores 12.0 points a game and allowed 9 sacks.
- Minnesota's defense is the best unit so far: 14 sacks, 4 INT and 2 fumble recoveries in 3 games.
- My two re-runs of the existing D/ST sims give PIT 0.795-0.797 and MIN 0.817-0.823, so MIN adds about 2.2-2.6 points of win probability.
- Odunze costs nothing in lineup terms: the ROS engine scores dropping him at +0.00 for Weeks 5-17, and Move 4 drops him in Week 5 anyway if Move 3 never fires.
- Timing works if the league uses ESPN's usual Wednesday processing. That default is my assumption and not verified; check the league setting. The claim clears before PIT@CLE kicks off Thursday 10/1 at 8:15 PM ET.
- The price is fine. The consensus file has no D/ST FAAB number, and a one-week rental worth about 2 points of win probability doesn't justify more than 2%. Bid the top of the range, because MIN is every column's No. 1 streamer and 64% rostered, so another manager may bid.
- Under rolling priority, ranking it third behind Allen and Juwan/Likely costs almost nothing extra.

What fails:
1. The BAL fallback isn't clearly better than keeping PIT.
   - TEN has only 1 giveaway in 3 games. BAL's defense has 6 sacks and 3 takeaways, while PIT has 8 sacks, 6 takeaways and a TD, and faces CLE (implied 18.0, 2 giveaways).
   - The prior research calls BAL 'marginal over PIT'. The sims give 0.796-0.805 against 0.795, so +0.1 to +1.0 points.
   - That isn't worth benching PIT on Thursday or using the claim.
2. The Friday timing for Addison is backwards.
   - Once waivers clear Wednesday, Addison is first-come first-served.
   - The trigger (Jefferson not practicing fully Wed-Thu) is public Wednesday and Thursday afternoon. That is exactly the news that would lead Teemo, the Jefferson owner, or anyone else to add Addison before Friday.
   - So the plan loses the race in the scenario where Addison matters most, when Jefferson doesn't practice all week and is ruled out early.
   - Waiting also gains nothing, since Odunze has no lineup value to protect.
   - The trigger is too loose as well. An ankle sprain usually means limited-limited practices even for a player who suits up, and the cited reports (FantasyPros 'avoids serious injury, could play Week 4', and the ESPN 'play week' story) point toward Jefferson playing.
3. The denial premise is wrong. Addison is not the only 4:05+ WR Teemo could pick up.
   - Malik Washington (MIA, same 4:05 game, 13% rostered, ESPN 10.0) and Tre Tucker (LV vs KC at 4:25, 42%, 9.8) are also on your wire.
   - Teemo's own backups do lock early (Diggs 9:30 AM, Harrison Jr. 1 PM), but he keeps a pivot worth about 10 points, so taking Addison removes only about 1.5-4 points in the roughly 8% late-scratch case.
   - The sims value the Addison hedge at +1.7 to +1.9 points only if you get him before Teemo reacts, and +0.9 if Jefferson's chance to play is 75%.
   - The waiver-consensus verdict on Addison for your team was 'Not needed for you; skip'. The ros-forecasts file says to keep Odunze through Williams' return because 'he still ranks above every wire WR' (FantasyPros ROS WR32), so an Addison-for-Odunze swap is a slight downgrade for the rest of the season if Jefferson plays.
4. The claim order is inconsistent with the plan's own numbers. Addison (+0.9 to +1.9) is worth at least as much as BAL (+0.1 to +1.0), yet the plan ranks BAL as a claim now and pushes Addison to a Friday free-agent add.
  - Better alternative: Keep only the MIN leg and fix the timing. Place these claims now, in this order:
1. Braelon Allen / drop Herbert
2. Juwan Johnson / drop Kraft
3. Isaiah Likely / drop Kraft
4. Minnesota D/ST / drop Odunze, bid 2%

Drop the BAL fallback, since it's a coin flip against PIT. If you get MIN, bench PIT before Thursday 8:15 PM ET. If you don't, keep PIT in and keep Odunze; he's the Week 5 kicker drop anyway.

If you want the Jefferson hedge, time it early. Either add a 5th claim for Addison now ($0-1, same Odunze drop, only fires if the MIN claim fails), or pick him up as a free agent right after waivers clear Wednesday. Don't wait until Friday. Taking Addison only removes about 1.5-4 points from Teemo's late pivot, because Malik Washington and Tre Tucker are also on the wire. If you skip the hedge entirely, you lose at most about 1 point of win probability.

## Move 4: add Week 5 kicker (check in order: McPherson CIN @MIA, Loop BAL @ATL, Aubrey DAL vs TB Thu, Bates DET @ARI, Mevis LAR vs BUF. Realistic: Tyler Bass BUF @LAR indoors, then Chad Ryland ARI, Jason Myers SEA, Spencer Shrader IND) / drop Whoever holds the Move 3 slot (MIN/BAL D/ST or Addison). If Move 3 never fired, Rome Odunze. - SURVIVES (0 of 3 refute)

Kind: stream. Condition: Week 5 only (Butker's bye). Pick him up as a free agent after Week 5 waivers clear (about Wed 10/7). Kickers are rarely claimed.. FAAB: 0-1%.

Rationale: Butker (KC) is on bye in Week 5. MIN goes @NO in Week 5 and has a Week 6 bye, so the rental is done. Keep PIT (vs IND in Week 5, @TB in Week 6). Bass is the most likely to be free (about 15% rostered): indoors on Monday night, game total 52.5, 4 of 4 on field goals.

- **role-and-injury** - upheld: The move holds up. It is a zero-cost, one-week kicker rental for Butker's bye, and it uses the roster slot the plan already set aside for churn.

Checks against the data:
- Butker's bye is real. KC and CAR are the only teams without a game in Week 5 in the live nflverse games.csv I pulled today (LAR shows up only because nflverse spells it "LA"). weekly_2026.json lists KC bye = 5.
- Bass's role is real and he is the only kicker. roster_weekly_2026.csv shows him ACT/A01 as BUF's sole K in Weeks 1-4, with no other BUF kicker on the roster; the Bills cut Prater-type insurance after he returned. nflverse stats: 4 of 4 field goals and 11 of 12 PATs. My reconstruction of ESPN scoring gives 13/4/6, 23 points total and about 7.7 per game.
- He carries no 2026 injury designation. He does not appear in injuries_2026.csv for Weeks 1-3.
- Web check: he missed all of 2025 with a pelvic injury, was cleared for 2026 camp, and went 3 for 3 in Week 1 (46, 34 and 33 yards). That matches nflverse's Week 1 row.
- Nothing in the data points to a role change. Josh Allen is ACT for Week 4, and BUF's only Week 3 injury tags are WR/DL/OL.
- The matchup matches the rationale. The live line is BUF @LA, Monday 10/12 at 8:15 PM, dome, total 52.5, BUF implied 25.0.
- Availability looks good: 12.7% average rostered (FantasyPros, 9/25). His redraft rank is K14.3 against Butker's K12.7, so a one-week stream beats a permanent swap.
- The candidate order also checks out on implied totals: McPherson (CIN 27.5, 8 of 8 FG, four from 50+), Loop (27.75), Bates (DET 29.0, mostly PATs), Aubrey (Thursday).
- The Week 5 condition is the right trigger. Only managers holding KC or CAR kickers need a K that week, and Fitzgerald is about 1% rostered, so competition is minimal.
- The drop is right when Move 3 fired. MIN D/ST is dead after Week 4 (MIN has a Week 6 bye). BAL's Week 5 matchup is weaker than PIT's. Addison would sit behind Pickens at FLEX in Week 5, and the plan refills a 4th WR in Week 7.

Flaws that don't refute the move:
- (a) The drop field leaves out the Move 1 failure branch. Move 1 says that if the Allen claim is lost, Herbert stays and becomes the drop for the Week 5 kicker. Move 4 only names the Move 3 slot or Odunze, so the plan contradicts itself.
- (b) The "realistic" fallback list includes Jason Myers, who is 92.8% rostered. Prior research lists him as very likely rostered. Its realistic fallbacks were Smack (GB vs CHI, implied 24.0), Borregales (NE vs LV, 24.0) and Boswell (PIT vs IND, 23.5), plus Shrader (8 of 8 FG, 37 points).
- (c) Waiting to pick him up as a free agent on Wednesday 10/7 is looser than it needs to be. On ESPN, players whose Week 4 game has started stay locked on waivers until the process runs. A $0 claim entered Tuesday 10/6, once the Move 3 D/ST's game is over, beats any rival's Wednesday free-agent add. Aubrey, if he were somehow free, would need to be added before Thursday 10/8 at 8:15 PM.
- (d) The PFN link is a Week 4 kicker ranking and could not be fetched (blocked), so it is not Week 5 evidence. The case rests on the nflverse lines and stats.
  - Better alternative: Make the move, with these refinements:

1. **Drop field.**
   - If the Braelon Allen claim (Move 1) failed, drop Herbert, as Move 1 already says.
   - Otherwise drop whoever holds the Move 3 slot.
   - If Move 3 never fired, drop Odunze.
2. **Timing.** Enter $0 / lowest-priority claims Tuesday night 10/6, after the Move 3 D/ST's Week 4 game is over, instead of waiting for free-agent status on Wednesday 10/7. List the claims in this order:
   1. McPherson
   2. Loop
   3. Bates
   4. Bass
   5. Smack
   6. Borregales
   7. Boswell
   8. Shrader
   9. Ryland
3. **Fallback list.** Drop Myers (about 93% rostered) from the realistic list.
4. **Permanent swap instead of a stream.** If Loop (K10.6 rest of season, bye 13) or Mevis (K9.1, bye 11, LA implied 27.5 vs BUF) is free, drop Butker for him permanently instead of burning the flex slot. Otherwise stream Bass and keep Butker.
- **opportunity-cost** - upheld: The drop holds up. The spot being given up is the cheapest one on the roster, and keeping Butker while renting a kicker for one week uses the fewest roster slots.

1) What the dropped player is worth. After Moves 1-2 the bench is Hall, Hubbard (Week 5 bye), Allen or Montgomery (whichever doesn't start), Juwan, Butker (bye), plus the Odunze/Move-3 spot. I re-ran the existing ROS script (verify/oc_move3_ros.py, research mode) on that roster. It measures how many lineup points each drop costs over Weeks 5-17:
   - Odunze: 0.00 in every week. He never makes the best lineup.
   - Braelon Allen: -1.01
   - Montgomery: -1.50
   - Juwan Johnson: -11.0 (he covers Warren's Week 13 bye)
   - Addison in the same spot: also 0.00
   The earlier Week 5 engine output (main/w5_test.md) agrees: "Cheapest drop: Rome Odunze... 0.4 points." FantasyPros ROS on 9/25 had Odunze at WR32 and falling (Caleb Williams has a Grade 2 hamstring and Keenum is starting). He isn't needed in the Week 5 or Week 6 lineups, and Move 6 refills a WR in Week 7. A D/ST rental in that spot is worth nothing after Week 4.

2) Why not drop Butker instead and keep a new kicker for good? That's worse. Week 5 is Butker's only bye, so after this one-week rental he never needs cover again. Every realistic replacement still has a bye ahead, which would cost another streaming slot later:
   - Bass: Week 7
   - McLaughlin: Week 10, same week as Smith's bye and Odunze/Raymond's
   - Mevis: Week 11
   - Loop: Week 13, same week as Warren, Hall and Allen
   - Aubrey: Week 14
   On quality, Butker is FantasyPros ROS K12 (ecr 12.7). Loop is K11 and Bates K13, both equal to him. Bass (K14), Shrader (K23) and Ryland (K24) are worse.

3) The facts in the rationale check out against local nflverse data (games_live_rev4.csv, a copy of https://raw.githubusercontent.com/nflverse/nfldata/master/data/games.csv, and data/raw/inseason/stats_player_week_2026.csv):
   - KC and CAR have no Week 5 game.
   - MIN plays @NO in Week 5 and has no Week 6 game.
   - PIT hosts IND in Week 5 and plays @TB in Week 6.
   - BUF @LA is Monday 10/12, indoors, total 52.5, LA -2.5, so BUF's implied total is 25.0.
   - Bass (BUF) is 4 of 4 on field goals with 11 PATs, about 23 points by my reconstruction of ESPN default kicker scoring. He is 12.7% rostered on the FantasyPros ESPN/Yahoo average, so he is probably free in a 10-team league.
   - Implied totals: Bates/DET 29.0, Aubrey/DAL 28.5, Loop/BAL 27.75, McPherson/CIN 27.5 (8 of 8), Mevis/LAR 27.5.

4) Adding him as a free agent after waivers clear spends no priority or FAAB. That's right, since kickers are rarely claimed and CAR's Fitzgerald is 1.1% rostered, so few managers need the same fill-in.

Small fixes, none of which changes the verdict:
   (a) Myers is not a realistic target (92.8% rostered, ROS K4). Borregales (NE vs LV, 24.0), Smack (GB vs CHI, 24.0) and Boswell (PIT vs IND, 23.5) belong ahead of Shrader. Shrader's IND plays @PIT, so his points work against your PIT D/ST.
   (b) If the one-week kicker turns out to be Aubrey (ROS K1), keep him and make Butker the Week 6 drop instead.
   (c) Move 4's drop field leaves out a case that Move 1 already covers: if the Allen claim fails, Herbert should be the drop.
   (d) The cited PFN link is a Week 4 kicker article and does not support the Week 5 claims; games.csv does.
  - Better alternative: No strictly better drop or add; make the move as proposed, with four fixes:
(1) Order of kickers to check for Week 5:
  - Likely rostered, check first: McPherson, Loop, Bates, Mevis, Aubrey.
  - Most likely free: Bass (BUF @LA, implied 25.0, indoors).
  - Next if Bass is gone: Borregales (NE vs LV, 24.0), then Smack (GB vs CHI, 24.0), then Boswell (PIT vs IND, 23.5, pulls the same way as your PIT D/ST), then Ryland (ARI vs DET, 23.5, indoors).
  - Drop Myers from the list (about 93% rostered). Put Shrader last: his IND plays @PIT, so his points work against your D/ST.
(2) If Move 1 failed, drop Herbert rather than Odunze, as Move 1's condition already says.
(3) If the kicker you land is Aubrey, keep him and drop Butker in Week 6 rather than the new kicker.
(4) If Move 3 put Addison in the slot and Jefferson is still out in Week 5, Addison and whichever of Allen/Montgomery sits in Week 5 cost about the same to drop, so dropping Addison is still fine: MIN has a Week 6 bye.
- **market-and-timing** - upheld: The move holds up under this lens. The timing and price are right, and its place in the chain makes sense. Only the fallback list needs a small cleanup.

1. **Demand is low, so waiting and paying $0 is right.** Week 5 has only two byes, CAR and KC (games.csv lists 15 Week 5 games; neither team plays). Besides you, at most one other manager (whoever holds CAR's Ryan Fitzgerald) is forced to replace a kicker. Kickers get no FAAB guidance in waiver-consensus.md; the lowest tier it prices is QB streamers at 1-3%. Spending priority or FAAB on a kicker would be waste. Picking one up as a free agent after Week 5 processing (about Wed 10/7) also gives you updated lines and Week 5 injury news. You have time: the only Thursday game is TB@DAL on 10/8, and Bass plays Monday 10/12.

2. **The "check first" names are correctly treated as long shots.** League-wide rostered % from FantasyPros, 9/28 scrape: Aubrey 99%, Mevis 67%, Bates 65%, Loop 63%, McPherson 59%. The realistic targets really are free: Bass 14.7% and Ryland 1.3%.

3. **Keeping Butker is correct, and the case is stronger than the plan says.** After Week 5, Butker never has a bye again. Any permanent replacement still has one ahead: McLaughlin Week 10, Bass Week 7, Aubrey Week 14. So the research's alternative of dropping Butker for McLaughlin would create a new hole in Week 10, which is already your Smith/Odunze bye week. The engine agrees that kickers aren't worth chasing: "week-to-week spread is noise, keep yours."

4. **The order in the chain works.** It runs Move 3 slot → Week 5 K → Week 6 QB → Week 7 WR. Your roster count never changes, and each drop is a player who has no use left:
   - MIN is @NO in Week 5, then on bye in Week 6.
   - BAL's Week 6 game (@CLE) would lose out to PIT @TB anyway.
   - PIT's schedule is confirmed: IND @PIT in Week 5, PIT @TB in Week 6.
   - Bass plays Monday night, and Week 6 claims process about Wednesday, so dropping him for the Week 6 QB causes no conflict.

**What's wrong is minor, and it's in the fallback list:**
- **Jason Myers** is 92% rostered, so he isn't a "realistic" option.
- **Spencer Shrader** kicks for IND @PIT. That's the game your own PIT D/ST is playing, so his points come from IND scoring against your defense. Rank him last, or drop him from the list.
- **Better deep fallbacks:**
  - Borregales: NE vs LV, NE implied 24.0, 8.6% rostered.
  - Smack: GB vs CHI, 24.0, 22%.
  - Boswell: PIT vs IND, 23.5, 35%. He scores when your D/ST's game goes well.
- **How to pick up:** if the league uses FAAB, put in a $0 claim in the Week 5 run. It costs nothing and gets first pick. If it uses rolling priority, don't burn priority; take him as a free agent after processing, as proposed.
- **If Move 3 went to Addison and Jefferson is out for weeks:** dropping Addison for a one-week kicker and then adding Kalif Raymond in Week 7 loses value. In that case, drop Juwan Johnson for the kicker instead, keep Addison, and skip Move 6.

**Evidence citation:** the move cites PFN's Week 4 kicker rankings. That's the wrong week, so it doesn't support a Week 5 pick. The nflverse lines do.
  - Better alternative: Make the move as proposed: keep Butker and stream one kicker for Week 5 at $0. Make the drop from the Move 3 slot, then pass that roster spot to the Week 6 QB. Refinements:

1. **Pickup timing:**
   - If the league uses FAAB, place a $0 claim in the Week 5 waiver run (about Tue/Wed 10/6-10/7).
   - If it uses rolling priority, take the kicker as a free agent after processing, not with a claim.
2. **Target order, re-ranked on the Wed 10/7 lines:**
   - First check McPherson, Loop, Bates, Aubrey and Mevis. They're probably rostered, but checking costs nothing.
   - Then Bass (BUF @LAR, Monday, dome), then Ryland (ARI vs DET, 1.3% rostered, 7/8 FG).
   - Then Borregales (NE vs LV), Smack (GB vs CHI), Boswell (PIT vs IND, which lines up with your D/ST).
   - Remove Myers (92% rostered). Put Shrader last or remove him, since IND plays @PIT against your own D/ST.
3. **If the Move 3 slot holds Addison and Jefferson has a multi-week injury:** drop Juwan Johnson for the kicker instead, keep Addison as the 4th WR, and skip Move 6.

## Move 5: add Week 6 QB stream (Bryce Young @PHI > Jordan Love vs DAL > Sam Darnold @DEN Thu > Jacoby Brissett @LAR > Kirk Cousins vs BUF) / drop The Week 5 kicker streamer - SURVIVES (0 of 3 refute)

Kind: stream. Condition: Week 6 only (Goff's bye). Avoid Stroud @JAX, Geno Smith @NE, Daniel Jones, and Mariota on Monday night (Daniels is likely back).. FAAB: 0-2%.

Rationale: The QB pool in a 10-team league is deep. PHI allows 20.7 QB points per game and DAL 23.5; KC (Herbert's Week 6 opponent) allows 8.9. Claiming Young now would waste a bench spot through his Week 5 bye.

- **role-and-injury** - upheld: I couldn't find a reason to reject this move. Every QB in the add list is a full-time starter with no current injury tag, the trigger (Week 6 only, for Goff's bye) is the right one, and the drop costs nothing.

Schedule check (nflverse games file): DET does not play in Week 6, so Goff's bye is real. Butker plays in Week 6 (LAC @KC), so the Week 5 kicker streamer is dead weight by then and is the correct drop. The listed games are all right: CAR @PHI, DAL @GB on Sunday night, SEA @DEN on Thursday 10/15, ARI @LA indoors, BUF @LV indoors. Week 6 claims should clear Wednesday 10/14, after Monday's BUF@LA game and before Darnold's Thursday kickoff.

Is each add's role real and durable?
- **Bryce Young:** 90%, 94% and 100% of snaps in Weeks 1-3; 23.1 PPR points a game against 22.6 expected; no injury entry. The 'benched' search result is a stale 2024 item. He is the only QB on CAR's active roster behind whom Kenny Pickett is the backup.
- **Jordan Love:** 100% of snaps all three weeks; 17.3 points a game; no injury entry.
- **Sam Darnold:** left Week 1 after 5 snaps (glute) and was out Week 2. He then practiced fully and played 100% of snaps in Week 3 (27.7 points). His role is real, but he has a recent soft-tissue injury and a Thursday game, so he is correctly ranked third.
- **Jacoby Brissett:** 100% of snaps all three weeks (87 in Week 3). A hip note on the Week 3 practice report, but he practiced fully. Kyler Murray is now on MIN, and ARI's other QBs are Gardner Minshew and rookie Carson Beck, who has been inactive. No threat to his job.
- **Kirk Cousins:** 100% of snaps; LV is 3-0 (27-13, 26-14, 35-27) with Cousins starting. The No. 1 pick, Fernando Mendoza, is the named backup. Coach Kubiak named Cousins the season starter, and I found no reporting of a switch.

The avoid list holds up. The research file said it could not confirm Daniels' timeline; my search now supports 'Daniels is likely back'. It was a dislocated left (non-throwing) elbow on 9/20, and RotoWire says he is set to practice in Week 4, so Mariota's role probably ends before Week 6 Monday night. The KC (8.9), JAX (11.1) and TEN (10.5) avoids match the data.

I rebuilt the matchup numbers from nflverse stats:
- **PHI 20.7:** Daniels 17.7, Cam Ward 20.0, Case Keenum 24.5, so PHI's number is spread across three QBs, not driven by one blowup.
- **DAL 23.5:** Dart 26.6, Commanders 23.5, Lamar Jackson 20.4.
- **DEN 16.2, LAR 16.2, BUF 19.7:** all match.
- **KC 8.9:** came against weak QBs (Bo Nix, Daniel Jones, Malik Willis), so it overstates KC's defense. That changes nothing here, because Herbert is gone after Move 1.

Caveats. These refine the move rather than reject it:
1. Young is only 24% available across ESPN leagues, and several QBs are hurt league-wide (Mayfield, Caleb Williams, Daniels, Dart), so Young and Love may be claimed before Week 6. The realistic pickup may be Darnold, Cousins or Brissett. That is fine given how deep the QB pool is.
2. The order is fixed from three weeks of defensive data, 2.5 weeks early. Re-rank at Week 6 waivers using posted lines and the Week 5 injury reports.
3. Cousins arguably belongs above Brissett: LV is 3-0 and scoring 29.3 points a game, he is tied for the league lead with 9 TD passes, and he plays indoors against BUF.
4. Tyler Shough (NO @NYG, 23.1 points a game, 100% of snaps, NYG allows 16.9 to QBs) is missing from the list. He wasn't in your screenshot, so check whether he's free.
5. The games file lists Drew Lock as SEA's Week 3 QB, but the snap data shows Darnold played all 67 snaps. That field is a pre-game placeholder, not a role change.
  - Better alternative: Keep the move, with these changes:
- Re-rank at Week 6 waivers (about Wed 10/14) using the posted Week 6 lines and the Week 5 injury reports, instead of locking in the order now.
- Add Tyler Shough (NO @NYG) at or near the top if he is free.
- Consider moving Cousins (LV 3-0, indoors vs BUF) above Brissett.
- If both Young and Love are gone, Darnold on Thursday is the default, as long as his glute stays off the injury report.
- **opportunity-cost** - upheld: Not refuted. The drop is correct, the add is needed, and the first two targets are the right ones. The fallback order after them is wrong, though.

1) Drop. Goff, Chase Brown and Ja'Marr Chase all have Week 6 byes (CIN and DET are on the Week 6 bye list, confirmed in games.csv). Every other spot on the Week 6 roster has a job:
- Hall, or Allen if Hall is out, fills FLEX.
- Montgomery and Hubbard start at RB.
- Juwan Johnson is the FLEX fallback.
- Butker is back from his Week 5 bye.
The Week 5 kicker streamer is the only roster spot worth nothing in Week 6. The engine's own docstring says kickers are not streamable ('keep yours'), so that kicker has no value after Week 5. No other drop is better. The kicker's last game can be as late as MNF 10/12 (BUF@LA), and Week 6 claims process around Wed 10/14. The earliest Week 6 game is SEA@DEN on Thu 10/15, so the timing works.

2) Add. Without a streamer the QB slot scores zero, because Move 1 drops Herbert. I ran the engine's per-game usage rate through its Week 6 matchup term (DvP and home/away; there are no Week 6 Vegas lines yet). Results:
- Young @PHI 18.0
- Love vs DAL 18.0
- Cousins vs BUF 17.6
- Watson vs BAL 16.4
- Herbert @KC 14.7
- Brissett @LAR 14.5
- Stroud @JAX 14.0
- D. Jones vs TEN 12.8
- Geno @NE 12.6
- Darnold @DEN 10.5 (the engine counts his missed Week 1-2 as zeros; as a full-time starter he rates about 14-15)
- Mariota 6.5
Streaming Young or Love beats keeping Herbert by about 3 points, and Herbert would have cost a bench spot in Weeks 4-6. The 'avoid' list (Stroud, Geno, Jones, Mariota) holds up. The rationale's numbers check out as raw Week 1-3 averages: PHI 20.7, DAL 23.5, KC 8.9. After the engine's shrinkage, though, PHI is neutral (17.2, x1.03), so Young's value comes from his own form (31.4/24.1/13.6), not the matchup. DAL (x1.20) really is a soft matchup. CAR's Week 5 bye is confirmed, so waiting until Week 6 to claim is right. FAAB of 0-2% is right too, because the top three are within 0.4 points of each other.

3) Where the move is flawed: the fallback order.
- Cousins (17.6) should be third, not fifth.
- Deshaun Watson is on the wire (8% rostered, 14.0/19.7/20.3 so far, vs BAL at home) and rates 16.4, but he is missing from the list.
- Darnold (one real game in 2026, 27.7 against WAS, the second-softest QB defense) and Brissett (6.5 in Week 2) belong below Watson.
This only matters if Young and Love are claimed. That is a real risk: Young is 76% rostered with DET (30.0 QB points allowed per game) in Week 4, and Week 6 also has Burrow, Caleb Williams, Daniels and Mayfield managers looking for QBs.

Minor points:
- If the Week 5 kicker turns out to be an elite leg (Aubrey, Loop, McPherson, Bates), drop Butker instead and keep him.
- Tyler Shough (NO @NYG) rates 19.7, the best Week 6 option, but he isn't on the waiver list, so check whether he's available.
- The quoted fantraxhq article covers Week 4 streamers and doesn't support any Week 6 claim.
- 'Daniels is likely back' has no source; it doesn't change anything because Mariota is avoided anyway.
  - Better alternative: Make the move as planned: a Week 6 QB claim that drops the Week 5 kicker, bid 0-2%, placed in the Week 6 waiver run around Wed 10/14. Reorder the fallbacks to Bryce Young (@PHI) = Jordan Love (vs DAL) > Kirk Cousins (vs BUF) > Deshaun Watson (vs BAL, add him) > Jacoby Brissett (@LAR) > Sam Darnold (@DEN, Thursday). First check whether Tyler Shough (NO @NYG, 19.7) is somehow available; if he is, he's the top choice. If the Week 5 kicker is an elite one (Aubrey, Loop, McPherson, Bates), drop Butker instead of the streamer.
- **market-and-timing** - upheld: The timing and the price both hold up. The move doesn't need to happen now, and 0-2% is the right price.

1. The facts check out. I recomputed QB fantasy points allowed per game (Weeks 1-3) from weekly_2026.json: PHI 20.7, DAL 23.5, KC 8.9, BUF 19.7, DEN 16.2, LAR 16.2, JAX 11.1, NE 12.5, TEN 10.5, SF 14.5. These match the rationale exactly. The Week 6 schedule in games_live_rev4.csv also matches: CAR@PHI; DAL@GB on Sunday night; SEA@DEN on Thursday 10/15; ARI@LA; BUF@LV indoors; HOU@JAX at 9:30 AM; NYJ@NE; TEN@IND; WAS@SF on Monday night; LAC@KC.

2. Waiting until Week 6 is right, not a missed chance. I ran the engine's usage and matchup formula for Week 6 with no Vegas term and without the stale Week 3 FantasyPros numbers:
- Young @PHI 18.0
- Love vs DAL 18.0
- Cousins vs BUF 17.6
- Watson vs BAL 16.4
- Herbert @KC 14.7
- Brissett @LAR 14.5
- Stroud @JAX 14.0
- Jones vs TEN 12.8
- Geno @NE 12.6

If Young is claimed before Week 6, the drop to Love or Cousins costs about 0-0.4 points. That matters because Young is 76% rostered nationally, averages 23.1 per game (Goff averages 21.9) and faces DET on Sunday night in Week 4. With Mayfield, Daniels and Caleb Williams hurt, another manager could reasonably grab him. Demand in Week 6 is thin: only the CIN, DET, MIA and MIN QBs are on bye. In a 10-team league there are 5 or more viable options, so the move isn't now-or-never.

3. You can't hold Young through Week 5. In Week 5 all 14 spots are full: 9 starters including the kicker streamer, plus Hall, Allen or Montgomery, Juwan, Hubbard (bye) and Butker (bye) on the bench. The prior research said "claim Young now, drop Herbert" (qb-k-dst.md line 57). That conflicts with Move 1, which is worth more, and the ~0-point scarcity cost above doesn't justify it.

4. The price fits the consensus. Waiver-consensus.md line 21 puts QB streamers at 1-3% in 1-QB leagues. The proposed 0-2% sits at the low end, which is right for a one-week rental with deep supply.

5. The drop is right. Butker comes back in Week 6, so the Week 5 kicker has no value left. The kicker unlocks when the Week 6 scoring period starts on Tuesday 10/13, even if he played Monday night (Bass or Mevis in BUF@LA).

Three flaws are worth fixing, but none of them breaks the move:
(a) The fallback order swaps Brissett and Cousins. The engine has Cousins (17.6, vs BUF indoors, BUF allows 19.7) about 3 points ahead of Brissett (14.5, @LAR, LAR allows 16.2). The prior research also ranked Cousins 4th and Brissett 5th. Darnold at 3rd is fragile: he played 10% of snaps in Week 1 (0.5 points), missed Week 2 (Drew Lock started), scored 27.7 in Week 3, and plays Thursday, so you'd have to commit early. games.csv still lists Lock as SEA's QB for Weeks 3-4, but that field is wrong: Darnold played 100% of snaps in Week 3.
(b) A claim is mostly unnecessary. CAR is on bye in Week 5, so Young never locks that week. On ESPN he should be a free agent rather than on waivers once the ~10/7 run clears. That means you can add him first-come, first-served on Tuesday 10/13 as soon as the kicker unlocks, before anyone's Wednesday claims process, at no FAAB or priority cost. Love, Cousins and Brissett all play in Week 5, so they'll be on waivers until ~10/14. They clear before their own games, so you can pick them up as free agents on Wednesday. Only Darnold, who plays Thursday, really needs a claim. If the league uses rolling priority rather than FAAB, don't spend priority on this.
(c) Two names were missed. Deshaun Watson (CLE vs BAL, 16.4, 8% rostered) is a better deep option than Brissett. Tyler Shough (NO @NYG, 19.7) should be checked for availability, since he isn't in the screenshots.
  - Better alternative: Keep Move 5 as written, with three changes to execution and order.
(1) On Tuesday 10/13, as soon as the Week 5 kicker unlocks, add Bryce Young as a free agent. He's on bye in Week 5, so he never goes back on waivers. This happens before Wednesday's claims, needs no FAAB and uses no priority.
(2) If Young is gone, pick up Jordan Love (Sunday night vs DAL) as a free agent Wednesday after waivers clear, or put in a $0-1 claim. Next come Kirk Cousins (vs BUF indoors), then Deshaun Watson (vs BAL), then Jacoby Brissett.
(3) Use Sam Darnold only as a Wednesday claim (0-2%) and only if Young and Love are both gone, because he plays Thursday and has an injury history.
Check Tyler Shough (NO @NYG) for availability. If the league uses rolling priority rather than FAAB, never spend a claim on this move.

## Move 6: add 4th-WR refill: Kalif Raymond (take Carnell Tate instead if you weight Weeks 9-17 and playoffs; Keenan Allen only if his suspension still hasn't been scheduled) / drop The Week 6 QB streamer - DIES (3 of 3 refute)

Kind: conditional. Condition: Week 7 waivers, after Goff's bye. Do it immediately, with no drop, if Hall goes on the NFL's IR, ESPN tags him Out, and your league has an IR slot.. FAAB: $0-2% (Raymond is 10% rostered; Tate 3-5% if contested).

Rationale: This refills the rotating slot with the best depth receiver. Raymond has out-targeted Odunze even with Williams at QB (14-7 over Weeks 1-2) and is scoring about 10.5-11 expected PPR per game. Risks: age 32, a catch rate that should regress, and Burden rising. Tate is the safest Weeks 8-17 hold: #4 overall pick, 21-29% target share, bye Week 9, but in a capped TEN offense. Keenan Allen fades after about Week 7 because of Pierce's return and a minimum 3-game suspension.

- **role-and-injury** - refuted: Raymond's role is real for now, but it is the least durable of the three options. On top of that, two of the move's clauses (Keenan Allen and the Hall IR trigger) are built on the wrong condition.

1) What the data (nflverse, weekly_2026.json) shows for Raymond:
- Snaps 60%, 62%, 75%: a part-time role.
- Targets 9, 5, 7.
- Expected points 13.75, 8.56, 11.41. The 3-game average of 11.2 matches the rationale, but the Weeks 2-3 average is only 10.0.
- He caught 19 of 21 targets (90%). That puts him 12.7 points above expected (46.4 scored vs 33.7 expected), so his 15.5 PPR per game is mostly efficiency that should regress.
- The rationale's "14-7 over Odunze with Williams" comes mostly from Week 1, when Odunze was limited by a calf injury (48% snaps). In Week 2, with Williams at QB and Odunze healthy (84% snaps), targets were 5 to 4. Raymond had 17% of targets and just 4% of air yards.
- In Week 3 Odunze had more opportunity than Raymond: expected points 12.64 vs 11.41, air-yard share 42% vs 28%, snaps 85% vs 75%. Burden is rising: 5, 7, then 11 targets, 32% share and 22.1 expected points in Week 3.
- In fairness, SI confirms Raymond was Williams' most-targeted receiver through Weeks 1-2 (25% target rate). So Williams' return, expected around Week 6-7 on a 3-4 week timeline, is not the main risk. SI also says Burden's slot role is the one to watch once Williams is back and game scripts are normal.
- FantasyPros rest-of-season PPR WR consensus (9/25): Raymond WR87 (spread ±25, worst rank 124); Tate WR40; Odunze WR33.

2) Tate has the durable role:
- Snaps 88%, 75%, 88%; target share 21%, 29%, 26%; air-yard share 35%, 36%, 45%.
- Expected points 9.0, 7.8, 13.3 and rising. He is scoring below expectation (8.4 vs 10.0 per game), so he should improve.
- He is the #4 overall pick and there is no returning starter ahead of him (Ridley's snaps fell from 62% to 33%). His only real target competitor is Wan'Dale Robinson.

3) The bye weeks work against Raymond. CHI's bye is Week 10, the same week as DeVonta Smith's, the only starting-WR bye left before Week 14. I ran the synth engine (rev_m6/m6_ins.py):
- On a healthy roster, no 4th WR ever makes the lineup in research mode. The slot is only injury insurance.
- If Ja'Marr Chase misses Weeks 7-17, Tate adds +20.0 and Raymond +11.0, even with Raymond's rate set higher (11 vs 10).
- With regressed rates (Raymond 9.5, Tate 10.5), it's +21.0 vs +9.5. Raymond comes out ahead in only one scenario (Smith and Hubbard both missing).
- Engine mode favors Raymond (+7.2) only because its rate is his 14.1 recent average, which includes the 90% catch-rate luck.

4) The Keenan Allen clause looks at the wrong event. Pierce went on IR in Week 3, so he can come back in Week 7, exactly when this add would happen. With Pierce playing in Weeks 1-2, Allen had 51-67% snaps and scored 9.2 and 1.5. The suspension depends on an Oct 26 court date whether or not it has been "scheduled". Allen should not be on a Week 7 menu at all.

5) The Hall trigger can never fire as written. ESPN's IR slot accepts players tagged O or IR. A player the NFL puts on IR shows as "IR" on ESPN, not "Out", so "NFL IR AND ESPN Out" will not both be true. The right trigger is "ESPN tags Hall O or IR and the league has an IR slot." That can happen as early as Friday 10/2 if he is ruled out for @CHI. A Questionable or Doubtful tag later doesn't make the roster illegal; only a fully cleared Hall forces a drop.
  - Better alternative: - Make Carnell Tate the default 4th-WR refill. His bye (Week 9) doesn't collide with Smith's Week 10 bye, and he has the steadiest snaps and air-yard share on the wire.
- Choose Raymond instead only if, after Week 6, all of these hold:
  - Williams is still out.
  - Raymond has kept a 20% or higher target share on 70% or more of snaps in Weeks 4-6.
  - You care most about Weeks 7-8.
- Remove Keenan Allen from the list (Pierce can return Week 7 and the suspension is still pending).
- Rewrite the early trigger as: "If ESPN tags Hall O or IR and your league has an IR slot, move him there and add Tate right away with no drop." This can fire as soon as Friday 10/2. A Q or D tag later is fine; only a fully cleared Hall forces a drop.
- Watch for Odunze on waivers after Move 3/4 drops him. If Williams is back and Odunze is still unclaimed, re-adding him is a reasonable pick; FantasyPros ranks him WR33 for the rest of the season, and he had more expected points than Raymond in Week 3.
- **opportunity-cost** - refuted: THE DROP IS RIGHT. After Goff's Week 6 bye, the QB streamer's only job is backup QB. My Monte Carlo (7% chance per player per week of missing a game, Weeks 7-17) puts Bryce Young as a held QB2 at only +1.5 points over simply adding a 15-point free-agent QB when Goff misses. The QB wire is deep (16 QBs listed, several projecting 15-17). Keeping him is not a better use of the spot, and no other drop is clearly worse to lose. Braelon Allen is the Hall handcuff, and Juwan Johnson covers Week 13 TE.

THE ADD AS PROPOSED IS NOT SUPPORTED:
(1) A 4th WR never makes the lineup when everyone is healthy. Using the plan's own per-game rates (Raymond 11, Tate 10, K. Allen 10), rev_m6/m6.py shows +0.00 for all three in every week from 7 to 17. The third RB (Montgomery, Hall or B. Allen, 12.5 or more) holds FLEX, even during the Smith (Week 10) and Pickens (Week 14) byes. The IR branch ('do it immediately, no drop') is also worth +0.00 in Weeks 4-8 for every WR tested (verify/oc_move6_ir.py). The move is pure injury insurance.
(2) As insurance, Raymond is the worst of the three named options. Expected value Weeks 7-17 against an empty spot: Tate +4.5, K. Allen +4.1, Raymond +3.6. Against adding a 9.5-point free-agent WR when needed: Tate +0.1, K. Allen -0.3, Raymond -0.8. At a 10% injury rate: Tate +7.2, K. Allen +6.6, Raymond +6.3. The reason is structural. Raymond's bye is Week 10, the same as DeVonta Smith's, so he cannot cover the one bye week a 4th WR would matter. m6_ins.py: if Chase misses Weeks 7-17, Tate adds +20 and Raymond +11; if Pickens misses, Tate +10 and Raymond 0. Raymond only ranks first under the engine's raw 14.1-point rate. That rate comes from his actual scoring (16.4/9.0/21.0, 15.5 per game), not his expected points (13.8/8.6/11.4, 11.3). Even the plan says 10.5-11.
(3) The Raymond rationale checks out but cuts against him. 14-7 targets over Odunze in Weeks 1-2 is correct (9+5 vs 3+4). But in Week 3 Luther Burden III had 11 targets (32% share, 22.1 expected points) to Raymond's 7 (21%, 11.4). Odunze (calf, Questionable) played 85% of snaps with 12.6 expected points. Raymond is due for regression down to a third or fourth option.
(4) The Tate claims hold in the data: target share 21%/29%/26%, snaps 88%/75%/88%, bye Week 9 (no overlap with Chase 6 / Smith 10 / Pickens 14). The only thing working against Tate is availability: he is 86% rostered on ESPN, so he may be gone by Week 7.
(5) Could not verify: Keenan Allen's 'minimum 3-game suspension' (the CBS link) and Tate as the '#4 overall pick'. No web search was available and neither is in the local data. The local data does confirm Pierce is on reserve (heel), and K. Allen's share is 21%/17%/26% at 51-73% snaps.
(6) The condition is garbled. 'Goes on the NFL's IR AND ESPN tags him Out' cannot both be true at once, because NFL IR shows as IR on ESPN. It should read 'OR, whichever your IR slot accepts'. And because the immediate add is worth +0 in Weeks 4-8, there is no urgency anyway.

Net: dropping the streamer at Week 7 is fine, but naming Raymond as the default add is wrong for this roster. The move is worth about 0-5 points whichever WR is chosen, so FAAB should be $0-1, not 3-5% for Tate.
  - Better alternative: Keep the drop and timing: drop the Week 6 QB streamer at Week 7 waivers; don't keep him as QB2, which is worth +1.5 points over a free-agent QB. Change the add order to Carnell Tate first (if still available), then Keenan Allen (only if the suspension timing is confirmed and Pierce is still out), then Kalif Raymond last. Raymond's Week 10 bye matches DeVonta Smith's, his scoring runs above his expected points, and Burden and Odunze threaten his targets. Bid $0-1 FAAB; the spot is worth about 0-5 points whichever WR you pick. Treat it as the spot you give up for the Week 9 D/ST stream (PIT bye). Fix the IR condition to 'if ESPN makes Hall eligible for your IR slot (IR or Out, whichever your league allows)'. That branch isn't urgent, since any WR added there projects +0 in Weeks 4-8.
- **market-and-timing** - refuted: I reject this move as written. The FAAB figure is fine; the timing and the choice of player are the problem.

1) A 4th WR in Week 7 is worth about nothing in expected points, so there is no reason to commit to a claim now. I re-ran the synth engine on the plan's roster (Braelon Allen in for Herbert, Juwan in for Kraft, Odunze dropped). In research mode, adding Raymond, Tate, Keenan Allen, Boston or Meyers with no drop gains +0.0 points in every week from 4 to 17. That holds with the base Hall news and with a Hall-on-IR scenario (out Weeks 4-7). Even in Week 6, when Chase is on bye, the FLEX goes to Braelon Allen as Hall's heir, not a 4th WR. Only engine mode shows Raymond gaining anything (+7.2 over Weeks 7-17), and that comes from a 14.1-point rate inflated by his 19-of-21 catch rate. The slot's value is insurance only, and Raymond-type WR4s can be added for $0 as free agents when an injury actually happens. On top of that, PIT's Week 9 bye will probably take this slot back for a defense stream, so a Week 7 WR is likely a two-week hold.

2) The immediate Hall-IR trigger adds about zero. In the IR scenario the engine gives +0.0 for Weeks 4-6 for every candidate. If a WR is wanted for Weeks 4-6 anyway, Keenan Allen fits that window, not Raymond. Pierce has been on IR since Week 3, so Allen's role is locked through Week 6, and Week 4 at WAS is the best WR matchup on the wire. Raymond, meanwhile, has Keenum or Bagent at QB. The research files disagree on whether that hurts him: waiver-consensus says it downgrades him, while ros-forecasts says Keenum's short passing suits him and his role may shrink when Williams returns.

3) The Keenan Allen clause is backwards. His court date is Oct 26, and the research says the 3-game suspension is unlikely to be served before the legal case ends. At Week 7 waivers (around Oct 20-21) the suspension will therefore always be unscheduled, so the condition always fires. It would send you to Allen exactly when Pierce becomes eligible to return (Week 7) and while the suspension can still land later in the season, possibly in the fantasy playoffs. That is buying at the top.

4) Raymond is the weakest long-term default of the three, and he has little scarcity value:
- He is 10% rostered on ESPN, the consensus research found no FAAB range for him, and FantasyPros ranks him WR85 rest of season (#231 overall). Tate is WR39 and Boston WR37.
- All three internal research passes rated him "depth only", "pass" or "skip".
- He will almost certainly clear waivers, so there is no reason to name him three weeks early or spend a claim on him. If he breaks out and gets taken, equivalent WR4s will still be there.
- His target share is being squeezed. Burden's share went from 19% to 23% to 32%, with 22.1 expected points in Week 3. Odunze had higher expected points than Raymond in Week 3 (12.6 vs 11.4) with a 42% air-yards share, and the plan drops Odunze.
- His Week 10 bye is the same week as DeVonta Smith's.

The expected-points case is real (about 11.2 per game, verified). But it was built with Keenum at QB, and Williams (a Grade 2 hamstring, 3-4 weeks from his Week 2 injury) should be back by about Week 7, when this add would happen.

5) Tate is the one candidate whose price can rise. He is 86% rostered across ESPN, was the #4 overall pick, has a 0.57-0.70 WOPR, and has the 3rd-easiest WR playoff schedule. Waiting until Week 7 is the wrong time for the player the plan itself calls the safest Weeks 8-17 hold. On pricing: $0-2% for Raymond is in line with consensus ("not a big spend"), and Tate at 3-5% is fine. Neither is the issue.
  - Better alternative: Don't commit to a named Week 7 claim.
- Leave the slot open after dropping the Week 6 QB streamer, or use it for the Week 9 defense stream (PIT bye).
- Add a WR only when an injury opens a real hole, as a $0 free agent after waivers clear. That preserves waiver priority if the league uses rolling waivers.
- If you want a long-term 4th WR anyway, make it Carnell Tate (1-3% FAAB, more if he breaks out). Claim him the first time a slot opens, including an IR-freed slot, rather than waiting for Week 7. He is the only candidate whose price is likely to rise. Denzel Boston is the fallback.
- If Hall goes on IR early and you want a Weeks 4-6 WR, take Keenan Allen for $0, since Pierce is out through Week 6. Cut him at Week 7.
- Drop the Week 7 Keenan Allen clause entirely.
- Treat Raymond only as a $0 injury replacement. If you want a CHI receiver once Williams is back, consider re-adding Odunze if he is still on the wire: he ranks higher rest of season than Raymond (WR32 vs WR85) and had the higher Week 3 expected points.

## Passes

- **Ollie Gordon II (RB MIA)**: A committee risk: Jaylen Wright is about 55-60% to play Week 4 and is listed ahead of him on the depth chart. MIA has the lowest implied total (13.5), and MIN has held every RB under 50 rushing yards. His Week 6 bye lands on your worst bye week. With Brown, Hubbard, Hall, Montgomery and Allen he'd never start (engine: 0.0 lineup points even at 7-12 PPR per game). As the most-added player on Sleeper he'll also cost real FAAB. Fine for teams short on RBs, not for you.
- **Alvin Kamara (RB NO)**: Worth something only while Etienne is out. Kendre Miller splits the work, ATL is stingy against RBs, and his Week 8 bye is the same as Montgomery's. Engine +0.3.
- **Kenyon Sadiq (TE NYJ, check availability)**: His Week 13 bye is the same as Warren's, so he can't cover it. His breakout came with Mason Taylor and Adonai Mitchell both out. Only a trade chip for you.
- **Isaiah Likely (TE NYG)**: Only the fallback if the Juwan claim fails. Winston starts all season (5.8 PPR per game in their two games together) and his playoff TE schedule ranks 24th.
- **Keenan Allen (WR IND)**: Good for Weeks 4-7, but a 4th WR doesn't start for you. Pierce returns around Week 7-8, and a 3-game-minimum suspension could hit from about Week 8. His Week 13 bye is the same as Warren's and Hall's. Engine +0.3.
- **Carnell Tate (WR TEN)**: The best long-term WR on the wire, but TEN is implied for 16.0 and a 4th WR rarely starts. Saved as the Week 7 refill option.
- **Kalif Raymond (WR CHI)**: Not a claim now: the spot is better used for the Week 4-6 streams. He's 10% rostered and likely still available in Week 7 (Move 6).
- **Jordan Addison (WR MIN)**: Not a claim. Jefferson's sprain 'avoided anything long-term' and he's about 50% to play. His Week 6 bye is in your crunch. Kept only as the Friday free-agent fallback in Move 3, for denial.
- **Bryce Young / Jordan Love / Darnold / Brissett / Mariota / Geno Smith (QBs)**: Goff starts Week 4. Stream one in Week 6 (Move 5) instead of carrying a backup QB through Young's Week 5 bye.
- **Justin Herbert (hold)**: Rejected as a hold. He's under 230 passing yards every week, and his Week 6 game (the Goff-bye week) is @KC, the defense allowing the fewest QB points. Every Week 6 streamer beats him.
- **Tyreek Hill (WR FA)**: Unsigned, with no reported visit or offer, about a year after a major knee injury. Watch only; reconsider if he signs with a team that has a real WR opening.
- **Malik Washington / Chris Bell (WR MIA)**: MIA's offense is implied for 13.5 and both have a Week 6 bye in your crunch.
- **Jaylen Wright (RB MIA)**: Only a hedge if you owned Gordon. Stinger plus foot injury.
- **Adonai Mitchell (WR NYJ)**: Splinted finger with 'some concern'. Pass until he practices fully.
- **Jakobi Meyers, Denzel Boston, Mack Hollins, Tre Tucker, Khalil Shakir, Michael Pittman Jr.**: Depth at best. Swinging or low volume, bad Week 4 spots, and Pittman appears on drop lists. None beats Pickens for FLEX.
- **RJ Harvey, Emanuel Wilson**: No role for them on this roster. Wilson is on a drop list, and Charbonnet returns soon.

## D/ST and kicker

WEEK 4 D/ST: Keep the Steelers @CLE Thursday unless a top-3 defense is free. PIT is about DST5 in the published consensus: CLE implied 18.0, a 38.5 total (tied for lowest), CLE's starting center in the concussion protocol, its RG out and RT limited, and Watson has taken 9 sacks in 3 games. Risks: Jalen Ramsey (wrist, sling) and Echols (concussion) are uncertain. Check availability in this order: 1) MIN vs MIA (MIA implied 14.0, the unanimous DST1), 2) SEA vs LAC (97% rostered, unlikely), 3) BAL vs TEN (16.0). Only those three are worth a switch. BUF vs NE is about equal to PIT, and GB @TB and CHI vs NYJ rank below it. A switch needs the claim to process before PIT locks Thursday 8:15 PM ET, and you keep PIT on the roster for Weeks 5-8 (vs IND, @TB, @NO, vs CLE). WEEK 5 KICKER (Butker bye): add as a free agent after Week 5 waivers. Check first: McPherson (CIN @MIA, 27.5 implied), Loop (BAL @ATL indoors), Aubrey (DAL vs TB Thursday, indoors), Bates (DET @ARI, 29.0), Mevis (LAR vs BUF Monday night, indoors). Realistic: Tyler Bass (BUF @LAR indoors on Monday night, total 52.5), then Chad Ryland (ARI vs DET), Jason Myers (SEA vs SF), Spencer Shrader (IND @PIT; 8 of 8 FG). Drop the Move 3 rental (or Odunze), then swap the kicker for the Week 6 QB. Week 5 D/ST: hold PIT. The best free streamers if you ever need one: NYJ vs CLE, DAL vs TB (Thursday), CIN @MIA. Week 9 is PIT's bye, so plan a stream then.

## Bye plan

WEEK 5 (Hubbard and Butker out; Hall about 70% still out): QB Goff | RB Chase Brown + Montgomery (Braelon Allen instead if he's the clear NYJ lead vs CLE and projects higher; it's a coin flip) | WR Ja'Marr Chase + DeVonta Smith | TE Warren | FLEX Pickens | D/ST PIT vs IND (hold) | K: streamer (Move 4). If Hall practices fully and is active, he takes RB2 over Montgomery or Allen, though a first game back from a quad injury may come with a pitch count, so Montgomery is the safer floor.
WEEK 6 (Goff, Chase Brown and Ja'Marr Chase out): QB: streamer (Move 5: Young @PHI > Love vs DAL > Darnold, Thursday). RB Hubbard + Montgomery | WR Smith + Pickens | TE Warren | FLEX: Hall if active (about 65%), otherwise Braelon Allen (NYJ @NE), otherwise Juwan Johnson | D/ST PIT @TB (best Week 6 spot; TB's rookie QB) | K Butker.
WEEK 7 (only Herbert's bye, and he's gone): full lineup. Drop the QB streamer and add a 4th WR (Move 6). Once Hall has a full game back, Allen stays as his handcuff; he's the first cut if a better stash appears.
WEEK 8 (Montgomery out; Juwan's NO bye too): RB Brown + Hubbard | WR Chase + Smith | TE Warren | FLEX Hall (or Pickens if Hall isn't back; Allen if Hall is still out). No hole.
LOOKING AHEAD: Week 9, PIT D/ST bye, so stream a defense. Week 10, Smith's bye (Raymond/Odunze share CHI's Week 10 bye), but Pickens and a RB cover it. Week 13, Warren/Hall/Allen byes, so Juwan (bye Week 8) covers TE. Week 14, Pickens' bye.

## Win odds

Simulation (opp2/sim2.py, extended in synth to add D/ST options; 400k draws): Hall benched with PIT is about 79.7% (me about 124 vs Teemo about 102.5). Leaving Hall in at 0 drops it to 62.1%. Starting Montgomery instead of Pickens at FLEX: 78.6%. MIN D/ST instead of PIT: 82.2% (+2.5), and its correlation with Teemo's Jefferson, Hockenson and Reichard trims variance, which helps the favorite. BAL D/ST: 81.3%. Adding Addison as a denial: 81.5%. MIN plus Addison: 83.8%. The ESPN-scale cross-check (you about 128-130 once Hall is replaced, vs Teemo 114.7) gives about 73-75%, so a realistic range is 75-80%. Teemo notes: Jefferson is about 50% to play; if he sits, Teemo's pivots are Diggs (locks 9:30 AM) or a 4:05 PM free agent like Addison. Barkley's stinger is behind him. Lamar is healthy but BAL starts a rookie at center. Nacua (groin) may return and cap Davante Adams. Teemo's Panthers D/ST faces DET without its top two CBs, which also helps your Goff (and is mildly positive for Hubbard). Your late-game exposure is Goff and Hubbard on Sunday night; Juwan (bench) plays Monday. Engine files: /tmp/claude-0/-home-user-offer-up-sahil/15ecf03d-2c93-5d86-bddc-acdc9e55ecba/scratchpad/wf_w4/synth/pkg.py and pkg2.py (package tests with research-based rates, since the raw engine inflates Raymond and Likely enough that it would start them over Smith and Warren). news.json holds the Hall spread 1/2/3/5 weeks = 30/35/20/15%, Achane heirs Gordon/Wright, Etienne heirs Kamara/Miller, and Pierce heirs K. Allen/Downs. Caveat: the engine assumes your healthy starters stay healthy all season, so every bench and handcuff value above is a floor.