import sys
import time
import heapq


def read_input():
    data = sys.stdin.read().split("\n")
    idx = 0
    n, m = map(int, data[idx].split())
    idx += 1

    graph = {}
    for _ in range(m):
        u, v, c = data[idx].split()
        c = int(c)
        graph.setdefault(u, []).append((v, c))
        graph.setdefault(v, []).append((u, c))
        idx += 1

    start, goal = data[idx].split()
    idx += 1

    h = {}
    for _ in range(n):
        node, val = data[idx].split()
        h[node] = int(val)
        idx += 1

    return graph, h, start, goal


def path_cost(graph, path):
    total = 0
    for i in range(len(path) - 1):
        for nb, c in graph[path[i]]:
            if nb == path[i + 1]:
                total += c
                break
    return total


def greedy_best_first(graph, h, start, goal):
    start_time = time.time()
    closed = set()
    parent = {}
    frontier = [(h[start], start)]
    nodes_expanded = 0

    while frontier:
        _, cur = heapq.heappop(frontier)
        if cur in closed:
            continue
        closed.add(cur)
        nodes_expanded += 1

        if cur == goal:
            path = [cur]
            while path[-1] != start:
                path.append(parent[path[-1]])
            path.reverse()
            return True, path, path_cost(graph, path), nodes_expanded, time.time() - start_time

        for nb, cost in graph.get(cur, []):
            if nb not in closed:
                if nb not in parent:
                    parent[nb] = cur
                heapq.heappush(frontier, (h[nb], nb))

    return False, [], 0, nodes_expanded, time.time() - start_time


def a_star(graph, h, start, goal):
    start_time = time.time()
    best_g = {start: 0}
    parent = {}
    frontier = [(h[start], start)]
    closed = set()
    nodes_expanded = 0

    while frontier:
        f, cur = heapq.heappop(frontier)
        if cur in closed:
            continue
        closed.add(cur)
        nodes_expanded += 1

        if cur == goal:
            path = [cur]
            while path[-1] != start:
                path.append(parent[path[-1]])
            path.reverse()
            return True, path, best_g[goal], nodes_expanded, time.time() - start_time

        for nb, cost in graph.get(cur, []):
            new_g = best_g[cur] + cost
            if nb not in best_g or new_g <= best_g[nb]:
                best_g[nb] = new_g
                parent[nb] = cur
                heapq.heappush(frontier, (new_g + h[nb], nb))

    return False, [], 0, nodes_expanded, time.time() - start_time


def print_result(algo_name, found, path, cost, nodes_expanded, exec_time):
    print(f"Algorithm: {algo_name}")
    if not found:
        print("Path Found: No")
        print(f"Nodes Expanded = {nodes_expanded}")
        print(f"Execution Time = {exec_time:.6f}")
        return
    print("Path Found: Yes")
    print("Path: " + " -> ".join(path))
    print(f"Total Cost = {cost}")
    print(f"Nodes Expanded = {nodes_expanded}")
    print(f"Execution Time = {exec_time:.6f}")


def main():
    graph, h, start, goal = read_input()

    g_found, g_path, g_cost, g_nodes, g_time = greedy_best_first(graph, h, start, goal)
    print_result("Greedy Best-First Search", g_found, g_path, g_cost, g_nodes, g_time)

    print()

    a_found, a_path, a_cost, a_nodes, a_time = a_star(graph, h, start, goal)
    print_result("A* Search", a_found, a_path, a_cost, a_nodes, a_time)

    print()
    print("Comparison:")
    if g_found and a_found:
        print(f"Path cost -> Greedy = {g_cost}, A* = {a_cost}")
    print(f"Nodes expanded -> Greedy = {g_nodes}, A* = {a_nodes}")
    print(f"Execution time -> Greedy = {g_time:.6f}, A* = {a_time:.6f}")
    print("A* is optimal since it accounts for both the cost so far (g) and the")
    print("estimated cost to goal (h). Greedy only looks at h, so it can walk into")
    print("a locally attractive but globally worse route.")


if __name__ == "__main__":
    main()
