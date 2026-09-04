# PS2 answers - Greedy Best-First vs A*

## Note on the spec's sample output

The PDF's sample output shows Greedy Best-First taking the path A -> C -> D -> E -> F.
Running an actual h(n)-only priority search on that graph gives A -> C -> E -> F instead,
since E's heuristic (2) is much lower than D's (4), so a real greedy search picks E as
soon as it's in the frontier. Both routes cost 10 on this particular graph (2+6+2 = 2+3+3+2),
so the total cost in the PDF is still right, it's just the path string for Greedy that
doesn't match a faithful simulation. Went with the correct simulation.

## Comparison (sample test case 1: A to F)

| | Greedy Best-First | A* |
|---|---|---|
| Path | A -> C -> E -> F | A -> C -> D -> E -> F |
| Path cost | 10 | 10 |
| Nodes expanded | 4 | 5 |
| Optimal? | yes, but by luck | yes, guaranteed |

Path cost tied on this graph, so this one test case alone doesn't show Greedy failing.
Greedy expanded fewer nodes (4 vs 5) since it beelines toward whatever looks closest
to the goal instead of checking the accumulated cost, but that speed is not reliable,
it's only cheap here because it happened to guess right.

## Comparison (sample test case 2, made up to expose the gap)

Graph: S-A cost 1 (h(A)=1), S-B cost 2 (h(B)=2), A-T cost 20, B-T cost 2, h(T)=0.

| | Greedy Best-First | A* |
|---|---|---|
| Path | S -> A -> T | S -> B -> T |
| Path cost | 21 | 4 |
| Nodes expanded | 3 | 4 |

Here Greedy really does lose. It sees A has the lowest heuristic (1) right next to the
start and commits to it immediately, without knowing the A-T edge costs 20. A* keeps
track of the real distance travelled (g) alongside the estimate (h), so it doesn't get
fooled, it finds the actually cheap S -> B -> T route even though B looked slightly
worse than A at the very first step.

## Why the difference

Greedy's priority is f(n) = h(n) only, it is basically asking "which neighbor looks
closest to the goal right now" and never reconsiders past cost. That makes it fast
(fewer nodes expanded, no bookkeeping of g) but not optimal, it can walk straight into
an expensive dead end if the heuristic is misleading close to the start.

A*'s priority is f(n) = g(n) + h(n), so it balances "how much have I already spent" against
"how much do I estimate is left". As long as the heuristic never overestimates the true
remaining cost (admissible), A* is guaranteed to find the cheapest path, at the cost of
expanding more nodes and tracking g for every node it touches.

## Effectiveness of the heuristic

On the original campus graph the heuristic values (A=7, B=8, C=5, D=4, E=2, F=0) do
generally decrease as you get closer to F, so they're directionally useful, but they're
not perfectly calibrated. h(E)=2 makes E look extremely close to the goal (real remaining
cost from E is 2, so h(E) is actually exact here), which is exactly why Greedy commits to
it. If the heuristic had been less optimistic about E relative to D, Greedy might have
picked D instead. This shows heuristic quality directly drives how good (or bad) Greedy's
decisions are, while A* stays correct regardless as long as the heuristic doesn't
overestimate.
