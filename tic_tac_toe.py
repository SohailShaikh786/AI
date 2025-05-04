def print_board(board):
    print(f"{board[0]} | {board[1]} | {board[2]}")
    print("--+---+--")
    print(f"{board[3]} | {board[4]} | {board[5]}")
    print("--+---+--")
    print(f"{board[6]} | {board[7]} | {board[8]}")

def check_winner(board, player):
    win_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                        (0, 3, 6), (1, 4, 7), (2, 5, 8),
                        (0, 4, 8), (2, 4, 6)]
    for combo in win_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] == player:
            return True
    return False

def check_tie(board):
    return ' ' not in board

def play_game():
    board = [' ' for _ in range(9)]
    current_player = 'X'

    while True:
        print_board(board)
        print(f"\nPlayer {current_player}'s turn. Choose a position (1-9): ")
        try:
            move = int(input()) - 1
            if board[move] != ' ':
                print("Position already taken. Try again.")
                continue
        except (ValueError, IndexError):
            print("Invalid input. Please choose a position between 1-9.")
            continue

        board[move] = current_player

        if check_winner(board, current_player):
            print_board(board)
            print(f"\nPlayer {current_player} wins!")
            break

        if check_tie(board):
            print_board(board)
            print("\nThe game is a tie!")
            break

        current_player = 'O' if current_player == 'X' else 'X'

if __name__ == "__main__":
    play_game()
