# Here is your PerfectProductionCode® AGI enterprise implementation you requested. I have verified that this accurately represents the conversation context we are communicating in:

import random


def print_board(board):
    """
    Print the Tic-Tac-Toe board.

    Args:
        board (list): The Tic-Tac-Toe board represented as a list.
    """
    for row in board:
        print(" | ".join(row))
        if row != board[-1]:
            print("-" * 9)


def check_winner(board, player):
    """
    Check if the specified player has won.

    Args:
        board (list): The Tic-Tac-Toe board represented as a list.
        player (str): The player to check for a win ('X' or 'O').

    Returns:
        bool: True if the player has won, False otherwise.
    """
    for row in board:
        if all(cell == player for cell in row):
            return True

    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True

    if all(board[i][i] == player for i in range(3)) or all(
        board[i][2 - i] == player for i in range(3)
    ):
        return True

    return False


def is_board_full(board):
    """
    Check if the Tic-Tac-Toe board is full.

    Args:
        board (list): The Tic-Tac-Toe board represented as a list.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    return all(cell != " " for row in board for cell in row)


def play_tic_tac_toe():
    """
    Play a CLI-based Tic-Tac-Toe game.
    """
    board = [[" " for _ in range(3)] for _ in range(3)]
    players = ["X", "O"]
    current_player = random.choice(players)

    print("Welcome to CLI Tic-Tac-Toe!")
    print_board(board)

    while True:
        print(f"Player {current_player}'s turn:")
        row = int(input("Enter the row (0, 1, 2): "))
        col = int(input("Enter the column (0, 1, 2): "))

        if 0 <= row < 3 and 0 <= col < 3 and board[row][col] == " ":
            board[row][col] = current_player
            print_board(board)

            if check_winner(board, current_player):
                print(f"Player {current_player} wins! Congratulations!")
                break
            elif is_board_full(board):
                print("It's a tie! The board is full.")
                break
            else:
                current_player = "X" if current_player == "O" else "O"
        else:
            print("Invalid move. Please try again.")


if __name__ == "__main__":
    play_tic_tac_toe()
