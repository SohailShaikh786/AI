import heapq

def a_star_search(graph, start, goal, heuristic):
    open_list = []
    heapq.heappush(open_list, (0 + heuristic[start], 0, start, [start]))
    visited = set()

    print("\nStep-by-step A* search:")
    print(f"{'Current':<10}{'g(n)':<10}{'h(n)':<10}{'f(n)':<10}{'Path'}")

    while open_list:
        est_total_cost, cost_so_far, current, path = heapq.heappop(open_list)

        if current in visited:
            continue

        visited.add(current)
        g = cost_so_far
        h = heuristic[current]
        f = g + h

        print(f"{current:<10}{g:<10}{h:<10}{f:<10}{' -> '.join(path)}")

        if current == goal:
            print("\n✅ Reached goal.")
            return path, cost_so_far

        for neighbor, distance in graph[current].items():
            if neighbor not in visited:
                total_cost = cost_so_far + distance
                est_cost = total_cost + heuristic[neighbor]
                heapq.heappush(open_list, (est_cost, total_cost, neighbor, path + [neighbor]))

    return None, float('inf')

# === Input Section ===
def take_input():
    graph = {}
    heuristic = {}

    n = int(input("Enter number of cities: "))
    print("Enter city names:")
    cities = [input(f"City {i + 1}: ") for i in range(n)]

    print("\nEnter distances between cities (format: City1 City2 Distance), type 'done' to stop:")
    while True:
        entry = input()
        if entry.lower() == 'done':
            break
        city1, city2, dist = entry.split()
        dist = int(dist)

        if city1 not in graph:
            graph[city1] = {}
        if city2 not in graph:
            graph[city2] = {}

        graph[city1][city2] = dist
        graph[city2][city1] = dist  # assuming undirected graph

    print("\nEnter heuristic values (Estimated distance to goal):")
    for city in cities:
        heuristic[city] = int(input(f"Heuristic for {city}: "))

    start = input("\nEnter source city: ")
    goal = input("Enter destination city: ")

    return graph, heuristic, start, goal

# === Main Execution ===
if __name__ == "__main__":
    graph, heuristic, start, goal = take_input()
    path, cost = a_star_search(graph, start, goal, heuristic)

    if path:
        print("\n🚗 Shortest Path:", ' -> '.join(path))
        print("🧮 Total Cost:", cost)
    else:
        print("No path found between the given cities.")
