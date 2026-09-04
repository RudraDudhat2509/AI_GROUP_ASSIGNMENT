# PS3 answers

The original PDF's eval formula mentioned "positional advantage" but never actually
defined it. The TA clarified it afterward:

```
Evaluation = (MAX Score - MIN Score) + Positional Advantage
Positional Advantage = Distance(B, nearest remaining E) - Distance(A, nearest remaining E)
Manhattan distance, 0 if no energy remains.
```

that's what's implemented. Also the PDF's Output Format section shows "Evaluation Score
= 20" as an example, but that's printed before the eval formula is even defined a few
pages later in the doc, so treating it as a placeholder rather than a real target,
running the actual board gives 1, not 20 (Best Move = RIGHT does match though).

## Results

Board 1 (5x7, depth 5): Minimax and both Alpha-Beta variants all agree, Best Move RIGHT,
Evaluation Score 1. Minimax expands 67 nodes, Alpha-Beta 36 (9 pruned).

Board 2 (5x7, depth 4): same story, Best Move RIGHT, Evaluation Score 0. Minimax expands
31 nodes, Alpha-Beta 28 (3 pruned).

Alpha-Beta always agrees with Minimax on the value and best move, it should, pruning
only skips branches that can't change the answer.

Heuristic move ordering pruned the exact same amount as normal order on both boards
above, which looked wrong at first. Turns out on both boards A's first move out of its
starting corner is already RIGHT (UP is invalid off the top edge), so there's nothing
for the reorder to actually change near the root. Built a separate board to check the
ordering logic isn't just broken:

```
.....
.A...
.E...
.....
....B
```

Here A's energy neighbor is DOWN, which is 3rd in normal order, not 1st. At depth 5,
normal order expands 122 nodes (39 pruned), heuristic order expands 97 (47 pruned). Best
move differs between the two (UP vs DOWN) but the evaluation score is the same (10) for
both, so they're just two different optimal moves, not a bug.
