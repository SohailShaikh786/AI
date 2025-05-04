from heapq import heappush, heappop


N = 3

goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]


row = [0, 0, -1, 1]
col = [-1, 1, 0, 0]
move_names = ['Left', 'Right', 'Up', 'Down']


def manhattan_distance(board):
    distance = 0
    for i in range(N):
        for j in range(N):
            val = board[i][j]
            if val != 0:
                goal_x = (val - 1) // N
                goal_y = (val - 1) % N
                distance += abs(i - goal_x) + abs(j - goal_y)
    return distance


def is_goal(board):
    return board == goal_state

def is_valid(x, y):
    return 0 <= x < N and 0 <= y < N


def print_board(board):
    for row in board:
        print(' '.join(map(str, row)))
    print('--------')


def best_first_search(start_board, x, y):
    visited = set()
    heap = []
    heappush(heap, (manhattan_distance(start_board), 0, start_board, x, y, []))

    while heap:
        heur, depth, board, x, y, path = heappop(heap)

        print(f"Step {depth}:")
        print_board(board)

        if is_goal(board):
            print("Goal state reached!")
            print("Moves:", " -> ".join(path))
            print(f"Number of steps to reach goal state: {len(path)}")
            return

        visited.add(tuple(map(tuple, board)))

        for i in range(4):
            new_x = x + row[i]
            new_y = y + col[i]

            if is_valid(new_x, new_y):
                new_board = [r[:] for r in board]
                new_board[x][y], new_board[new_x][new_y] = new_board[new_x][new_y], new_board[x][y]

                if tuple(map(tuple, new_board)) not in visited:
                    new_path = path + [move_names[i]]
                    heappush(heap, (manhattan_distance(new_board), depth + 1, new_board, new_x, new_y, new_path))

    print(" No solution found.")

def get_initial_state():
    print("Enter the initial 3x3 puzzle row by row (use 0 for the blank space):")
    start = []
    for i in range(N):
        row = list(map(int, input(f"Row {i + 1}: ").split()))
        if len(row) != N:
            print(" Invalid input! Each row must have 3 integers.")
            return get_initial_state()
        start.append(row)

    for i in range(N):
        for j in range(N):
            if start[i][j] == 0:
                return start, i, j

if __name__ == '__main__':
    start_board, x, y = get_initial_state()
    print("\nInitial State:")
    print_board(start_board)
    best_first_search(start_board, x, y)
