import sys
import time
from collections import deque

# moves must be generated in this order: UP RIGHT DOWN LEFT
MOVES = [("UP", -1, 0), ("RIGHT", 0, 1), ("DOWN", 1, 0), ("LEFT", 0, -1)]


def read_grid():
    data = sys.stdin.read().split("\n")
    r, c = map(int, data[0].split())
    grid = [data[i + 1] for i in range(r)]
    start = goal = None
    for i in range(r):
        for j in range(c):
            if grid[i][j] == "S":
                start = (i, j)
            elif grid[i][j] == "G":
                goal = (i, j)
    return grid, r, c, start, goal


def in_bounds(r, c, R, C):
    return 0 <= r < R and 0 <= c < C


def build_path(parent, node):
    directions = []
    while node in parent:
        prev, d = parent[node]
        directions.append(d)
        node = prev
    directions.reverse()
    return directions


def bfs(grid, R, C, start, goal):
    start_time = time.time()
    visited = {start}
    parent = {}
    queue = deque([start])
    nodes_expanded = 0

    while queue:
        cur = queue.popleft()
        nodes_expanded += 1
        if cur == goal:
            path = build_path(parent, cur)
            return True, path, nodes_expanded, time.time() - start_time

        r, c = cur
        for name, dr, dc in MOVES:
            nr, nc = r + dr, c + dc
            if in_bounds(nr, nc, R, C) and grid[nr][nc] != "#" and (nr, nc) not in visited:
                visited.add((nr, nc))
                parent[(nr, nc)] = (cur, name)
                queue.append((nr, nc))

    return False, [], nodes_expanded, time.time() - start_time


def dfs(grid, R, C, start, goal):
    start_time = time.time()
    visited = {start}
    parent = {}
    stack = [start]
    nodes_expanded = 0

    while stack:
        cur = stack.pop()
        nodes_expanded += 1
        if cur == goal:
            path = build_path(parent, cur)
            return True, path, nodes_expanded, time.time() - start_time

        r, c = cur
        # push in reverse so UP is popped first, keeping generation order UP RIGHT DOWN LEFT
        for name, dr, dc in reversed(MOVES):
            nr, nc = r + dr, c + dc
            if in_bounds(nr, nc, R, C) and grid[nr][nc] != "#" and (nr, nc) not in visited:
                visited.add((nr, nc))
                parent[(nr, nc)] = (cur, name)
                stack.append((nr, nc))

    return False, [], nodes_expanded, time.time() - start_time


def print_result(algo_name, found, path, nodes_expanded, exec_time):
    print(f"Algorithm: {algo_name}")
    if not found:
        print("Path Found: No")
        print(f"Nodes Expanded = {nodes_expanded}")
        print(f"Execution Time = {exec_time:.6f}")
        return
    print("Path Found: Yes")
    print("Path: " + " ".join(path))
    print(f"Number of Moves = {len(path)}")
    print(f"Nodes Expanded = {nodes_expanded}")
    print(f"Execution Time = {exec_time:.6f}")


def main():
    grid, R, C, start, goal = read_grid()

    bfs_found, bfs_path, bfs_nodes, bfs_time = bfs(grid, R, C, start, goal)
    print_result("BFS", bfs_found, bfs_path, bfs_nodes, bfs_time)

    print()

    dfs_found, dfs_path, dfs_nodes, dfs_time = dfs(grid, R, C, start, goal)
    print_result("DFS", dfs_found, dfs_path, dfs_nodes, dfs_time)

    print()
    print("Comparison:")
    if bfs_found and dfs_found:
        print(f"Path length -> BFS = {len(bfs_path)}, DFS = {len(dfs_path)}")
    print(f"Nodes expanded -> BFS = {bfs_nodes}, DFS = {dfs_nodes}")
    print(f"Execution time -> BFS = {bfs_time:.6f}, DFS = {dfs_time:.6f}")
    print("BFS is optimal (shortest path) since it explores level by level.")
    print("DFS is not guaranteed optimal, it just goes deep first.")


if __name__ == "__main__":
    main()
