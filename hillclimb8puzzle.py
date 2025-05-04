# Input 1:
# Row 1: 1 2 3
# Row 2: 4 0 6
# Row 3: 7 5 8


import copy

class PuzzleState:
    def __init__(self, board, parent=None, move=""):
        self.board = board
        self.parent = parent
        self.move = move
        self.empty_pos = self.find_empty()

    def find_empty(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    return (i, j)
        return None

    def generate_neighbors(self):
        neighbors = []
        i, j = self.empty_pos
        moves = {
            "UP": (i-1, j),
            "DOWN": (i+1, j),
            "LEFT": (i, j-1),
            "RIGHT": (i, j+1)
        }

        for move, (x, y) in moves.items():
            if 0 <= x < 3 and 0 <= y < 3:
                new_board = copy.deepcopy(self.board)
                new_board[i][j], new_board[x][y] = new_board[x][y], new_board[i][j]
                neighbors.append(PuzzleState(new_board, self, move))
        return neighbors

    def manhattan_distance(self):
        distance = 0
        goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        for i in range(3):
            for j in range(3):
                if self.board[i][j] != 0:
                    x, y = divmod(self.board[i][j] - 1, 3)
                    distance += abs(i - x) + abs(j - y)
        return distance

    def is_goal(self):
        return self.board == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    def __lt__(self, other):
        return self.manhattan_distance() < other.manhattan_distance()


def hill_climbing(initial_state):
    current = initial_state
    while True:
        if current.is_goal():
            return current, True
        neighbors = current.generate_neighbors()
        best_neighbor = min(neighbors)
        if best_neighbor.manhattan_distance() >= current.manhattan_distance():
            return current, False
        current = best_neighbor


def print_solution(solution):
    path = []
    while solution:
        path.append(solution)
        solution = solution.parent
    for state in reversed(path):
        print(f"Move: {state.move if state.move else 'Start'}")
        for row in state.board:
            print(" ".join(str(x) if x != 0 else " " for x in row))
        print()


def get_user_input():
    print("Enter the puzzle row by row (use 0 for the empty space):")
    board = []
    seen = set()
    for i in range(3):
        while True:
            try:
                row = list(map(int, input(f"Row {i + 1}: ").strip().split()))
                if len(row) != 3 or any(n < 0 or n > 8 for n in row):
                    raise ValueError
                if any(n in seen for n in row):
                    raise ValueError("Duplicate numbers detected.")
                seen.update(row)
                board.append(row)
                break
            except ValueError:
                print("Invalid input. Please enter 3 unique numbers between 0 and 8.")
    return board


if __name__ == "__main__":
    user_board = get_user_input()
    initial_state = PuzzleState(user_board)
    solution, goal_reached = hill_climbing(initial_state)
    print_solution(solution)

    if goal_reached:
        print(" Goal state reached successfully!")
    else:
        print(" Stuck in a local minimum. Try a different starting state or use random restarts.")
