# PS4 answers

## Comparison table

| Experiment | Initial State | Initial Cost | Final State | Final Cost | Iterations | Neighbors Evaluated |
|---|---|---|---|---|---|---|
| 1 | [1,1,2,3,4,2] | 20 | [3,1,1,3,4,2] | 0 | 2 | 54 |
| 2 | [2,3,1,1,4,4] | 20 | [2,3,3,1,2,4] | 0 | 2 | 54 |
| 3 | [4,2,3,1,2,3] | 20 | [4,2,2,1,4,3] | 0 | 2 | 54 |

## Discussion

**Which initial timetable won?** All three tie, every run reaches cost 0.

**Same final timetable?** No, different final slot assignments each time, but all
conflict-free and cost 0.

**Stuck in different local optima?** No. Since all three hit cost 0, and cost can't go
below 0, none of them are stuck below the true optimum.

**Effect of initial state on iterations / final cost?** None here, all three took exactly
2 iterations and 54 evaluations. That's specific to this conflict graph though, not a
general property of hill climbing. The reason it converges so easily: max degree in the
conflict graph is 3 (courses 2, 3, 4 and 5 each conflict with exactly 3 others) against 4
available slots, so there's always room to dodge every conflict. A tighter graph (more
conflicts per course, fewer slots) would very plausibly get stuck above 0 depending on
where it starts.
