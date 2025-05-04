from collections import deque

def is_valid(state, m, n, visited):
    return 0 <= state[0] <= m and 0 <= state[1] <= n and state not in visited

def bfs(m, n, d):
    visited = set()
    queue = deque()
    parent = dict()
    initial_state = (0, 0)
    
    queue.append((initial_state, 0))
    visited.add(initial_state)
    parent[initial_state] = (None, "Start")

    while queue:
        (a, b), steps = queue.popleft()

        if a == d or b == d:
            path = []
            current = (a, b)
            while current:
                prev, op = parent[current]
                path.append((current, op))
                current = prev
            path.reverse()
            return steps, path


        operations = [
            ((m, b), "Fill Jug1"),
            ((a, n), "Fill Jug2"),
            ((0, b), "Empty Jug1"),
            ((a, 0), "Empty Jug2"),
            ((a - min(a, n - b), b + min(a, n - b)), "Pour Jug1 → Jug2"),
            ((a + min(b, m - a), b - min(b, m - a)), "Pour Jug2 → Jug1")
        ]

        for state, op in operations:
            if is_valid(state, m, n, visited):
                visited.add(state)
                queue.append((state, steps + 1))
                parent[state] = ((a, b), op)

    return -1, []

def main():
    try:
        m = int(input("Enter capacity of Jug 1 (m): "))
        n = int(input("Enter capacity of Jug 2 (n): "))
        d = int(input("Enter the amount to measure (d): "))

        if d > max(m, n):
            print(f"\nIt's not possible to measure {d} liters because it's more than the max jug capacity.")
            return

        from math import gcd
        if d % gcd(m, n) != 0:
            print(f"\nIt's not possible to measure {d} liters with jug capacities {m} and {n} due to GCD constraint.")
            return

        steps, path = bfs(m, n, d)

        if steps == -1:
            print(" It's not possible to measure the given amount.")
        else:
            print(f"\n Minimum number of steps required is: {steps}")
            print("Steps to achieve this:\n")
            for i, (state, op) in enumerate(path):
                a, b = state
                marker = ""
                if (a == d or b == d) and i == len(path) - 1:
                    if a == d:
                        marker = f" (Target {d}L in Jug1)"
                    else:
                        marker = f" (Target {d}L in Jug2)"
                print(f"Jug1: {a}L, Jug2: {b}L → {op} {marker}")

    except ValueError:
        print("Please enter valid integers for jug capacities and target amount.")

if __name__ == "__main__":
    main()
