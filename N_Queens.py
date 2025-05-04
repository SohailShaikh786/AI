def is_safe(board, row, col, n):
    for i in range(row):
        if board[i][col] == 1:
            return False
        
    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False

    for i, j in zip(range(row, -1, -1), range(col, n)):
        if board[i][j] == 1:
            return False

    return True

def solve_nqueens(board, row, n):
    if row >= n:
        return True

    for col in range(n):
        if is_safe(board, row, col, n):
            board[row][col] = 1

            if solve_nqueens(board, row + 1, n):
                return True

            board[row][col] = 0

    return False

def print_board(board, n):
    for row in board:
        print(" ".join('Q' if x == 1 else '.' for x in row))
    print()

def nqueens(n):
    board = [[0 for _ in range(n)] for _ in range(n)]

    if not solve_nqueens(board, 0, n):
        print(f"No solution exists for {n}-Queens problem.")
        return

    print_board(board, n)

if __name__ == "__main__":
    N = int(input("Enter the value of N: "))
    nqueens(N)
