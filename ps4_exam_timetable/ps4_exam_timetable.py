import sys
import time


def read_input():
    data = sys.stdin.read().split("\n")
    idx = 0
    n, s = map(int, data[idx].split())
    idx += 1
    k = int(data[idx].strip())
    idx += 1
    conflicts = []
    for _ in range(k):
        a, b = map(int, data[idx].split())
        conflicts.append((a, b))
        idx += 1
    initial = list(map(int, data[idx].split()))
    return n, s, conflicts, initial


def calculate_cost(state, conflicts):
    num_conflicts = 0
    for a, b in conflicts:
        if state[a - 1] == state[b - 1]:
            num_conflicts += 1
    conflict_penalty = num_conflicts * 10

    slot_counts = {}
    for slot in state:
        slot_counts[slot] = slot_counts.get(slot, 0) + 1
    excess_courses = sum(max(0, cnt - 2) for cnt in slot_counts.values())
    distribution_penalty = excess_courses * 2

    total = conflict_penalty + distribution_penalty
    return {
        "num_conflicts": num_conflicts,
        "conflict_penalty": conflict_penalty,
        "excess_courses": excess_courses,
        "distribution_penalty": distribution_penalty,
        "total": total,
    }


def generate_neighbors(state, s):
    neighbors = []
    for i in range(len(state)):
        for slot in range(1, s + 1):
            if slot != state[i]:
                new_state = state[:]
                new_state[i] = slot
                neighbors.append(new_state)
    return neighbors


def print_timetable(state):
    for i, slot in enumerate(state):
        print(f"C{i + 1} -> Slot {slot}")


def hill_climb(initial, conflicts, s, log=True):
    start_time = time.time()
    current = initial[:]
    current_cost = calculate_cost(current, conflicts)

    if log:
        print("=" * 40)
        print("Algorithm: Hill Climbing")
        print("Problem: Exam Timetable Optimization")
        print("=" * 40)
        print()
        print("Initial Timetable:")
        print()
        print_timetable(current)
        print()
        print(f"Initial Conflict Cost = {current_cost['conflict_penalty']}")
        print(f"Initial Distribution Cost = {current_cost['distribution_penalty']}")
        print(f"Initial Total Cost = {current_cost['total']}")
        print()
        print("-" * 40)

    iterations = 0
    total_evaluated = 0

    while True:
        neighbors = generate_neighbors(current, s)
        best_neighbor = None
        best_cost = None
        for neighbor in neighbors:
            cost = calculate_cost(neighbor, conflicts)
            total_evaluated += 1
            if best_cost is None or cost["total"] < best_cost["total"]:
                best_neighbor = neighbor
                best_cost = cost

        if best_cost["total"] < current_cost["total"]:
            iterations += 1
            current = best_neighbor
            current_cost = best_cost
            if log:
                print()
                print(f"Iteration {iterations}")
                print()
                print("Best Neighbor Timetable:")
                print()
                print_timetable(current)
                print()
                print(f"Conflict Cost = {current_cost['conflict_penalty']}")
                print(f"Distribution Cost = {current_cost['distribution_penalty']}")
                print(f"Total Cost = {current_cost['total']}")
                print()
                print("-" * 40)
        else:
            break

    exec_time = time.time() - start_time

    if log:
        print()
        print("=" * 40)
        print()
        print("Final Timetable:")
        print()
        print_timetable(current)
        print()
        print(f"Final Conflict Cost = {current_cost['conflict_penalty']}")
        print(f"Final Distribution Cost = {current_cost['distribution_penalty']}")
        print(f"Final Cost = {current_cost['total']}")
        print()
        print(f"Iterations = {iterations}")
        print(f"Total Neighboring States Evaluated = {total_evaluated}")
        print(f"Execution Time = {exec_time:.6f} seconds")
        print()
        print("Termination Reason: Local Optimum")
        print("=" * 40)

    return current, current_cost, iterations, total_evaluated, exec_time


def main():
    n, s, conflicts, initial = read_input()
    hill_climb(initial, conflicts, s)


if __name__ == "__main__":
    main()
