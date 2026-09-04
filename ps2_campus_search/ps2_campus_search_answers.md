# PS2 answers

## Test case 1 (A to F)

| | Greedy | A* |
|---|---|---|
| Path | A -> C -> E -> F | A -> C -> D -> E -> F |
| Cost | 10 | 10 |
| Nodes expanded | 4 | 5 |

Cost ties on this graph so this one test alone doesn't really show greedy failing. Greedy
expanded fewer nodes since it just beelines toward whatever looks closest, but that's not
reliable, it only worked out because it happened to guess right here. Also worth noting
my greedy path doesn't match the one in the assignment PDF (A -> C -> D -> E -> F), even
though the cost is the same, checked it by hand in the notebook and E genuinely has a
lower heuristic than D so a real greedy search picks E, not D.

## Test case 2 (made up on purpose to show greedy losing)

Graph: S-A cost 1 (h(A)=1), S-B cost 2 (h(B)=2), A-T cost 20, B-T cost 2, h(T)=0.

| | Greedy | A* |
|---|---|---|
| Path | S -> A -> T | S -> B -> T |
| Cost | 21 | 4 |

Here greedy actually loses. It grabs A right away since its heuristic (1) is lower than
B's (2), without knowing the A-T edge is expensive. A* tracks real distance travelled
alongside the estimate, so it isn't fooled.

## Why

Greedy's priority is just f(n) = h(n), so it only ever asks "which neighbor looks closest
to the goal", never how much it already spent getting there. Fast, but not optimal.
A*'s priority is f(n) = g(n) + h(n), it balances what's already spent against the
estimate, which is why it stays correct as long as the heuristic never overestimates.

## Heuristic quality

On the campus graph the heuristic values do generally shrink as you get closer to F, but
h(E)=2 happens to be exactly the true remaining distance from E, which is exactly why
greedy commits to E so eagerly. A tighter/more misleading heuristic would change what
greedy picks, A* would stay correct either way.
