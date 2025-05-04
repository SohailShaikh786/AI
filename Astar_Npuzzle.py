import heapq
from copy import deepcopy

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def input_state(prompt_text):
    print(f"Enter the {prompt_text} configuration (use 0 for the blank tile):")
    state = []
    for i in range(3):
        while True:
            try:
                row = list(map(int, input(f"{prompt_text} Row {i+1}: ").split()))
                if len(row) == 3 and all(0 <= x <= 8 for x in row):
                    state.append(row)
                    break
                else:
                    print("Invalid row. Enter exactly 3 integers between 0 and 8.")
            except ValueError:
                print("Invalid input. Enter integers only.")
    return state

def get_blank_position(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

def serialize(state):
    return tuple(tuple(row) for row in state)

def is_goal(state, goal):
    return state == goal

def manhattan_distance(state, goal):
    distance = 0
    goal_positions = {}
    for i in range(3):
        for j in range(3):
            val = goal[i][j]
            goal_positions[val] = (i, j)
    for i in range(3):
        for j in range(3):
            val = state[i][j]
            if val != 0:
                goal_i, goal_j = goal_positions[val]
                distance += abs(goal_i - i) + abs(goal_j - j)
    return distance

def get_neighbors(state):
    neighbors = []
    x, y = get_blank_position(state)
    for dx, dy in DIRECTIONS:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < 3 and 0 <= new_y < 3:
            new_state = deepcopy(state)
            new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y]
            neighbors.append(new_state)
    return neighbors

def reconstruct_path(came_from, current):
    path = [current]
    while serialize(current) in came_from:
        current = came_from[serialize(current)]
        path.append(current)
    return path[::-1]

def a_star(start_state, goal_state):
    start_h = manhattan_distance(start_state, goal_state)
    open_set = []
    heapq.heappush(open_set, (start_h, 0, start_state))

    came_from = {}
    g_score = {serialize(start_state): 0}

    while open_set:
        _, current_g, current = heapq.heappop(open_set)

        if is_goal(current, goal_state):
            return reconstruct_path(came_from, current)

        for neighbor in get_neighbors(current):
            neighbor_serial = serialize(neighbor)
            tentative_g = current_g + 1
            if neighbor_serial not in g_score or tentative_g < g_score[neighbor_serial]:
                came_from[neighbor_serial] = current
                g_score[neighbor_serial] = tentative_g
                f_score = tentative_g + manhattan_distance(neighbor, goal_state)
                heapq.heappush(open_set, (f_score, tentative_g, neighbor))

    return None


start = input_state("START")
goal = input_state("GOAL")
solution_path = a_star(start, goal)

if solution_path:
    print("\nSteps to solve the puzzle:")
    for i, step in enumerate(solution_path):
        print(f"Step {i}:")
        for row in step:
            print(row)
        print("-----")
    print(f"Total moves: {len(solution_path) - 1}")
else:
    print("No solution found.")
