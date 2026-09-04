import sys
import time

MOVES_NORMAL = [("UP", -1, 0), ("RIGHT", 0, 1), ("DOWN", 1, 0), ("LEFT", 0, -1)]


def read_input():
    data = sys.stdin.read().split("\n")
    idx = 0
    r, c = map(int, data[idx].split())
    idx += 1
    grid = [data[idx + i] for i in range(r)]
    idx += r
    turn = data[idx].strip()
    idx += 1
    depth = int(data[idx].strip())
    idx += 1
    return grid, r, c, turn, depth


def find_positions(grid, r, c):
    a_pos = b_pos = None
    energy = set()
    for i in range(r):
        for j in range(c):
            ch = grid[i][j]
            if ch == "A":
                a_pos = (i, j)
            elif ch == "B":
                b_pos = (i, j)
            elif ch == "E":
                energy.add((i, j))
    return a_pos, b_pos, energy


def in_bounds(r, c, R, C):
    return 0 <= r < R and 0 <= c < C


def manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def nearest_dist(pos, energy):
    if not energy:
        return 0
    return min(manhattan(pos, e) for e in energy)


def evaluate(a_pos, b_pos, energy, max_score, min_score):
    if energy:
        positional_advantage = nearest_dist(b_pos, energy) - nearest_dist(a_pos, energy)
    else:
        positional_advantage = 0
    return (max_score - min_score) + positional_advantage


def get_moves(pos, grid, R, C, energy, use_heuristic_order):
    moves = []
    for name, dr, dc in MOVES_NORMAL:
        nr, nc = pos[0] + dr, pos[1] + dc
        if in_bounds(nr, nc, R, C) and grid[nr][nc] != "#":
            moves.append((name, nr, nc))
    if use_heuristic_order:
        moves.sort(key=lambda m: 0 if (m[1], m[2]) in energy else 1)
    return moves


def search(grid, R, C, a_pos, b_pos, energy, turn, depth, use_ab, use_heuristic_order):
    stats = {"generated": 0, "expanded": 0, "pruned": 0}

    def recurse(a_pos, b_pos, energy, max_score, min_score, turn, depth, alpha, beta):
        stats["expanded"] += 1
        cur_pos = a_pos if turn == "MAX" else b_pos
        moves = get_moves(cur_pos, grid, R, C, energy, use_heuristic_order)

        if depth == 0 or not moves:
            return evaluate(a_pos, b_pos, energy, max_score, min_score), None

        maximizing = turn == "MAX"
        best_val = float("-inf") if maximizing else float("inf")
        best_move = moves[0][0]

        for i, (name, nr, nc) in enumerate(moves):
            stats["generated"] += 1
            new_a, new_b, new_energy = a_pos, b_pos, energy
            new_max, new_min = max_score, min_score

            if turn == "MAX":
                new_a = (nr, nc)
                if (nr, nc) in energy:
                    new_energy = energy - {(nr, nc)}
                    new_max = max_score + 10
            else:
                new_b = (nr, nc)
                if (nr, nc) in energy:
                    new_energy = energy - {(nr, nc)}
                    new_min = min_score + 10

            next_turn = "MIN" if turn == "MAX" else "MAX"
            val, _ = recurse(new_a, new_b, new_energy, new_max, new_min, next_turn, depth - 1, alpha, beta)

            if maximizing and val > best_val:
                best_val, best_move = val, name
            if (not maximizing) and val < best_val:
                best_val, best_move = val, name

            if use_ab:
                if maximizing:
                    alpha = max(alpha, best_val)
                else:
                    beta = min(beta, best_val)
                if alpha >= beta:
                    stats["pruned"] += len(moves) - i - 1
                    break

        return best_val, best_move

    value, move = recurse(a_pos, b_pos, energy, 0, 0, turn, depth, float("-inf"), float("inf"))
    return value, move, stats


def print_result(algo_name, move, value, stats, depth, exec_time, show_pruned):
    print(f"Algorithm: {algo_name}")
    print(f"Best Move: {move}")
    print(f"Evaluation Score = {value}")
    print(f"Nodes Generated = {stats['generated']}")
    print(f"Nodes Expanded = {stats['expanded']}")
    if show_pruned:
        print(f"Nodes Pruned = {stats['pruned']}")
    print(f"Search Depth = {depth}")
    print(f"Execution Time = {exec_time:.6f}")


def main():
    grid, R, C, turn, depth = read_input()
    a_pos, b_pos, energy = find_positions(grid, R, C)

    start = time.time()
    mm_value, mm_move, mm_stats = search(grid, R, C, a_pos, b_pos, energy, turn, depth, False, False)
    mm_time = time.time() - start
    print_result("Minimax", mm_move, mm_value, mm_stats, depth, mm_time, False)

    print()

    start = time.time()
    ab_value, ab_move, ab_stats = search(grid, R, C, a_pos, b_pos, energy, turn, depth, True, False)
    ab_time = time.time() - start
    print_result("Alpha-Beta", ab_move, ab_value, ab_stats, depth, ab_time, True)

    print()

    start = time.time()
    ab2_value, ab2_move, ab2_stats = search(grid, R, C, a_pos, b_pos, energy, turn, depth, True, True)
    ab2_time = time.time() - start
    print_result("Alpha-Beta (heuristic move order)", ab2_move, ab2_value, ab2_stats, depth, ab2_time, True)

    print()
    print("Comparison: Minimax vs Alpha-Beta (normal move order)")
    print(f"Best move -> Minimax = {mm_move}, Alpha-Beta = {ab_move}")
    print(f"Evaluation score -> Minimax = {mm_value}, Alpha-Beta = {ab_value}")
    print(f"Nodes expanded -> Minimax = {mm_stats['expanded']}, Alpha-Beta = {ab_stats['expanded']}")
    print(f"Nodes pruned -> Alpha-Beta = {ab_stats['pruned']}")
    print(f"Execution time -> Minimax = {mm_time:.6f}, Alpha-Beta = {ab_time:.6f}")

    print()
    print("Comparison: Alpha-Beta without move ordering vs with heuristic move ordering")
    print(f"Nodes expanded -> normal order = {ab_stats['expanded']}, heuristic order = {ab2_stats['expanded']}")
    print(f"Nodes pruned -> normal order = {ab_stats['pruned']}, heuristic order = {ab2_stats['pruned']}")
    print(f"Execution time -> normal order = {ab_time:.6f}, heuristic order = {ab2_time:.6f}")


if __name__ == "__main__":
    main()
