def water_jug_dfs(jug1_capacity, jug2_capacity, goal):
    initial_state = (0, 0)
    visited = set()
    stack = [(initial_state, [], [])]

    while stack:
        (jug1, jug2), path, actions = stack.pop()


        if jug1 == goal or jug2 == goal:
            print("\n Solution found:")
            for i in range(len(path)):
                print(f"Jug1: {path[i][0]}L | Jug2: {path[i][1]}L -> {actions[i]}")
            print(f"Jug1: {jug1}L | Jug2: {jug2}L -> Goal reached!")
            return

        if (jug1, jug2) in visited:
            continue
        visited.add((jug1, jug2))


        next_moves = [
            ((jug1_capacity, jug2), "Fill Jug1"),
            ((jug1, jug2_capacity), "Fill Jug2"),
            ((0, jug2), "Empty Jug1"),
            ((jug1, 0), "Empty Jug2"),

            ((jug1 - min(jug1, jug2_capacity - jug2), jug2 + min(jug1, jug2_capacity - jug2)), "Pour Jug1 → Jug2"),

            ((jug1 + min(jug2, jug1_capacity - jug1), jug2 - min(jug2, jug1_capacity - jug1)), "Pour Jug2 → Jug1")
        ]

        for (new_state, action) in next_moves:
            if new_state not in visited:
                stack.append((new_state, path + [(jug1, jug2)], actions + [action]))

    print("\n No solution found.")


if __name__ == "__main__":
    print("Water Jug Problem (DFS-Based Solver with Action Descriptions)")
    jug1_capacity = int(input("Enter capacity of Jug 1: "))
    jug2_capacity = int(input("Enter capacity of Jug 2: "))
    goal = int(input("Enter the amount to measure: "))

    if goal > max(jug1_capacity, jug2_capacity):
        print("\n The goal amount is greater than both jug capacities. No solution possible.")
    else:
        water_jug_dfs(jug1_capacity, jug2_capacity, goal)
