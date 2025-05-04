import heapq

class GridProblem:
    def __init__(self, initial_state, goal_state, grid):
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.grid = grid

    def is_goal(self, state):
        return state == self.goal_state

    def is_valid_cell(self, row, col):
        return 0 <= row < len(self.grid) and 0 <= col < len(self.grid[0]) and self.grid[row][col] == 0

    def expand(self, node):
        row, col = node.state
        children = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_row, new_col = row + dr, col + dc
            if self.is_valid_cell(new_row, new_col):
                child_state = (new_row, new_col)
                child_node = Node(child_state, parent=node)
                children.append(child_node)
        return children


class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.cost = 0
        self.heuristic = 0

    def __lt__(self, other):
        return self.heuristic < other.heuristic


def manhattan_distance(state, goal_state):
    return abs(state[0] - goal_state[0]) + abs(state[1] - goal_state[1])


def best_first_search(problem):
    start_node = Node(problem.initial_state)
    start_node.heuristic = manhattan_distance(problem.initial_state, problem.goal_state)

    if problem.is_goal(start_node.state):
        return start_node

    frontier = []
    heapq.heappush(frontier, start_node)
    reached = {problem.initial_state}

    while frontier:
        node = heapq.heappop(frontier)

        if problem.is_goal(node.state):
            return node

        for child in problem.expand(node):
            child.heuristic = manhattan_distance(child.state, problem.goal_state)
            if child.state not in reached:
                reached.add(child.state)
                heapq.heappush(frontier, child)

    return None


def reconstruct_path(node):
    path = []
    while node:
        path.append(node.state)
        node = node.parent
    return list(reversed(path))


def print_complete_path(path):
    if path:
        print("\nComplete Path:")
        for step, point in enumerate(path):
            print(f"Step {step}: {point}")
    else:
        print("No solution found")


def print_grid_with_path(grid, path, start, goal):
    visual = [['1' if cell else '0' for cell in row] for row in grid]
    for r, c in path:
        visual[r][c] = '*'
    sr, sc = start
    gr, gc = goal
    visual[sr][sc] = 'S'
    visual[gr][gc] = 'G'

    print("\nGrid with path:")
    for row in visual:
        print(' '.join(row))


def get_user_input():
    rows = int(input("Enter number of rows in the grid: "))
    cols = int(input("Enter number of columns in the grid: "))

    print("\nEnter grid row by row (0 for free, 1 for obstacle):")
    grid = []
    for i in range(rows):
        row = list(map(int, input(f"Row {i + 1}: ").strip().split()))
        if len(row) != cols:
            raise ValueError("Row length must match the number of columns.")
        grid.append(row)

    initial_state = tuple(map(int, input("Enter start position (row col): ").split()))
    goal_state = tuple(map(int, input("Enter goal position (row col): ").split()))

    return initial_state, goal_state, grid


if __name__ == "__main__":
    print("=== Best-First Search (BestFS) Grid Pathfinding ===")
    try:
        initial_state, goal_state, grid = get_user_input()
        problem = GridProblem(initial_state, goal_state, grid)
        solution_node = best_first_search(problem)

        if solution_node:
            print("\n!! Reached the Goal !!")
            solution_path = reconstruct_path(solution_node)
            print_complete_path(solution_path)
            print_grid_with_path(grid, solution_path, initial_state, goal_state)
        else:
            print("\nNo solution found from the given initial to goal state.")
    except Exception as e:
        print(f"Error: {e}")
