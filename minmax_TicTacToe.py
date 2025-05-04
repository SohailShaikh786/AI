import math

board = [' ' for _ in range(9)]

def print_board():
    for row in [board[i*3:(i+1)*3] for i in range(3)]:
        print('| ' + ' | '.join(row) + ' |')

def is_winner(brd, player):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    return any(all(brd[i] == player for i in combo) for combo in win_conditions)

def is_full(brd):
    return ' ' not in brd

def get_available_moves(brd):
    return [i for i, val in enumerate(brd) if val == ' ']

def minimax(brd, depth, is_maximizing):
    if is_winner(brd, 'X'):
        return 1
    elif is_winner(brd, 'O'):
        return -1
    elif is_full(brd):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in get_available_moves(brd):
            brd[i] = 'X'
            score = minimax(brd, depth + 1, False)
            brd[i] = ' '
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in get_available_moves(brd):
            brd[i] = 'O'
            score = minimax(brd, depth + 1, True)
            brd[i] = ' '
            best_score = min(score, best_score)
        return best_score

def best_move():
    best_score = -math.inf
    move = -1
    for i in get_available_moves(board):
        board[i] = 'X'
        score = minimax(board, 0, False)
        board[i] = ' '
        if score > best_score:
            best_score = score
            move = i
    return move

def play_game():
    print("Welcome to Tic Tac Toe!")
    print_board()

    while True:

        user_move = int(input("Enter your move (0-8): "))
        if board[user_move] != ' ':
            print("Invalid move. Try again.")
            continue
        board[user_move] = 'O'
        
        

        print_board()

        if is_winner(board, 'O'):
            print("You win!")
            break
        if is_full(board):
            print("It's a draw!")
            break


        print("AI's turn...")
        ai_move = best_move()
        board[ai_move] = 'X'
        print_board()

        if is_winner(board, 'X'):
            print("AI wins!")
            break
        if is_full(board):
            print("It's a draw!")
            break

if __name__ == "__main__":
    play_game()
