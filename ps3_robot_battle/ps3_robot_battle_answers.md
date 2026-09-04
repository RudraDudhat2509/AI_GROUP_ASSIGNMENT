# PS3 answers - Minimax vs Alpha-Beta

## Note on the evaluation function

The original PDF never defined "positional advantage" in the evaluation formula, so it
couldn't be implemented as written. The TA posted a clarification afterward:

```
Evaluation = (MAX Score - MIN Score) + Positional Advantage
Positional Advantage = Distance(B, nearest remaining E) - Distance(A, nearest remaining E)
Manhattan distance, 0 if no energy remains.
```

That's what's implemented here. A higher positional advantage favors MAX, which makes
sense: it means B is farther from the nearest energy cell than A is.

## Note on the spec's Evaluation Score = 20 example

The PDF's Output Format section shows "Best Move: RIGHT, Evaluation Score = 20" right
after the sample input, before the evaluation function is even defined a few pages
later. Running the actual sample board (5x7, depth 5) gives Best Move = RIGHT, matching
that part, but Evaluation Score = 1, not 20. Given the 20 shows up before the formula
that would produce it even exists, it reads as a generic format placeholder rather than
a worked answer for this exact board, so the real computed value (1) is what's reported.

## Sample board 1 (5x7, depth 5)

| | Minimax | Alpha-Beta | Alpha-Beta (heuristic order) |
|---|---|---|---|
| Best Move | RIGHT | RIGHT | RIGHT |
| Evaluation Score | 1 | 1 | 1 |
| Nodes Expanded | 67 | 36 | 36 |
| Nodes Pruned | - | 9 | 9 |

## Sample board 2 (5x7, depth 4)

| | Minimax | Alpha-Beta | Alpha-Beta (heuristic order) |
|---|---|---|---|
| Best Move | RIGHT | RIGHT | RIGHT |
| Evaluation Score | 0 | 0 | 0 |
| Nodes Expanded | 31 | 28 | 28 |
| Nodes Pruned | - | 3 | 3 |

Minimax and Alpha-Beta agree on best move and evaluation score every time, which they
must, alpha-beta pruning only skips branches that provably can't change the final answer,
it never changes the answer itself. Alpha-Beta expands roughly half the nodes Minimax
does on these boards.

## Why heuristic move ordering didn't change anything on the two given boards

On both sample boards, A's very first move from its starting corner is already RIGHT
into open space. Normal order checks UP first (invalid, off the top edge) then RIGHT,
so RIGHT is effectively tried first regardless of whether heuristic reordering is on.
Since the reorder never actually promotes a different move near the root, pruning comes
out identical on these two specific boards.

To confirm the move-ordering logic actually does something (and isn't just silently
broken), built a board where A's energy-collecting neighbor is not already first in
normal order:

```
.....
.A...
.E...
.....
....B
```

Here A's DOWN neighbor is energy, but DOWN is checked 3rd in normal order (UP, RIGHT,
DOWN, LEFT). Results at depth 5:

| | normal order | heuristic order |
|---|---|---|
| Best Move | UP | DOWN |
| Evaluation Score | 10 | 10 |
| Nodes Expanded | 122 | 97 |
| Nodes Pruned | 39 | 47 |

With the energy-first reorder actually mattering, heuristic order expands fewer nodes
and prunes more, exactly what better move ordering is supposed to do: trying the
strongest move first lets alpha-beta establish a tight bound sooner, so later siblings
get cut off more often. The two orderings picked different best moves (UP vs DOWN) while
tying on evaluation score, meaning both moves are equally good here, so either one is a
correct answer, alpha-beta with a different exploration order is allowed to settle on a
different tied optimum.

## Minimax vs Alpha-Beta, summary

- **Nodes expanded**: Alpha-Beta always expands fewer or equal to Minimax, since pruning
  only removes work, never adds it.
- **Nodes pruned**: grows with search depth and branching, and grows further with good
  move ordering (moves likely to be strong, like ones that grab an energy cell, tried
  first).
- **Execution time**: too small to measure meaningfully on these tiny boards (sub-millisecond),
  but the nodes-expanded numbers make the story clear even without a timer.
- **Best move / evaluation score**: identical between Minimax and Alpha-Beta on every
  board tested, as expected. Only differs between two Alpha-Beta runs when there's a tie
  in evaluation score, both moves are then equally correct.
