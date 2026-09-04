# PS4 answers - Hill Climbing exam timetable

## Comparison table

| Experiment | Initial State | Initial Cost | Final State | Final Cost | Iterations | Neighbors Evaluated | Execution Time |
|---|---|---|---|---|---|---|---|
| 1 | [1,1,2,3,4,2] | 20 | [3,1,1,3,4,2] | 0 | 2 | 54 | ~0.0005s |
| 2 | [2,3,1,1,4,4] | 20 | [2,3,3,1,2,4] | 0 | 2 | 54 | ~0.0004s |
| 3 | [4,2,3,1,2,3] | 20 | [4,2,2,1,4,3] | 0 | 2 | 54 | ~0.0003s |

## Discussion

**1. Which initial timetable produced the best final solution?**
All three tie: every experiment reaches total cost 0, meaning every conflict is resolved
and no slot has more than 2 courses. There's no "winner" here, the algorithm always
finds the ideal outcome (Conflict Penalty = 0, Distribution Penalty = 0) regardless of
where it starts.

**2. Did all initial states reach the same final timetable?**
No. Same final cost (0), but three different actual assignments (different slot numbers
per course). Multiple valid conflict-free timetables exist for this course set, hill
climbing just finds whichever one is reachable from its own starting point.

**3. Did Hill Climbing get stuck in different local optima?**
No, and this is worth calling out honestly rather than forcing a different-sounding
answer: since all three runs hit cost 0, none of them got stuck in a local optimum that
wasn't also the global optimum. Cost 0 is the best any timetable can score here (the
formula can't go negative), so once you're at 0 you're at the true optimum, not just
a local one.

**4. How did the initial state affect the number of iterations?**
It didn't, here. All three took exactly 2 iterations and evaluated exactly 54 neighboring
states (2 rounds of 18, plus one more failed round of 18 that confirmed no better neighbor
exists = 3 x 18 = 54). That's a coincidence of this specific conflict graph being small
and easy, not a general rule, a harder or more tightly constrained graph would very
plausibly show different iteration counts, or even get stuck below cost 0's reach.

**5. How did the initial state affect the final cost?**
Not at all in this case, every run reached 0. The reason is structural: the conflict
graph here (8 conflicting pairs among 6 courses) has a max degree of 3 per course
(course 2, 3, 4 and 5 each conflict with exactly 3 others), and there are 4 slots
available. A course only ever needs to avoid at most 3 specific slots being taken by
its conflicting neighbors, and with 4 slots to choose from there's always room to dodge
every conflict. That's why hill climbing converges to a perfect timetable so reliably
here, the underlying constraint satisfaction problem is genuinely easy, not because hill
climbing is guaranteed to find the global optimum in general (it usually isn't, on a
harder graph it absolutely could get stuck above 0).
