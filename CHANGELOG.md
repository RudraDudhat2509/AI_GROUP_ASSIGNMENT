# Changelog

## [Unreleased]
### Fixed
- All 4 notebooks: execution time now measured with `time.perf_counter()` instead of `time.time()`, which was printing 0.000000 on tiny runs
- PS1: BFS vs DFS comparison block now prints execution time
- PS2: added `parse_graph` for the PDF's stated input format (`N M` / edge lines / `S G` / heuristic lines); comparison block now reports path, cost, nodes expanded and time for both graphs
- PS3: `print_result` now prints Execution Time; board 2 gets the same full Minimax/Alpha-Beta report as board 1; Alpha-Beta without-vs-with move ordering is now printed for boards 1 and 2, not just the custom test board
- PS4: added `parse_timetable_input` for the PDF's stated input format; full run now matches the PDF's section 14 output exactly (initial timetable and costs, per-iteration best-neighbor timetable with conflict/distribution cost split, final conflict/distribution costs, execution time, dynamic termination reason); comparison table in the answers file has an Execution Time column

## [0.7.1] - 2026-09-08
### Removed
- PS2 visualizations (#23, #24)

## [0.7.0] - 2026-09-08
### Added
- Graph diagrams (PS2), nodes-expanded bar charts (PS3), convergence line plot (PS4) (#21, #22)

## [0.6.0] - 2026-09-08
### Changed
- Restructured all 4 notebooks: one function per cell instead of one giant dump cell, markdown cut to short headers (#19, #20)

## [0.5.0] - 2026-09-05
### Changed
- Dropped standalone .py scripts, notebooks are the single deliverable per PS (#9, #10)
- Added toy-example experiments to all 4 notebooks before each real grid/graph/board (#11-#18)
- Trimmed the README and all 3 answers.md files

## [0.4.0] - 2026-09-05
### Added
- PS4: exam timetable optimization, Hill Climbing (#7, #8)
- All 4 problem statements complete.

## [0.3.0] - 2026-09-05
### Added
- PS3: robot strategy battle, Minimax + Alpha-Beta (#5, #6)

## [0.2.0] - 2026-09-04
### Added
- PS2: campus route search, Greedy Best-First + A* (#3, #4)

## [0.1.0] - 2026-09-04
### Added
- PS1: rescue robot BFS/DFS pathfinding (#1, #2)
