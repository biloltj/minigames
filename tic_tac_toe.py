import random
import os
from colorama import Fore, Style, init


init(autoreset=True)


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_board(board):
    clear()
    print("\n    TIC TAC TOE 🎮\n")
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]} \n")

def check_winner(board, symbol):
    wins = [(0,1,2), (3,4,5), (6,7,8),
            (0,3,6), (1,4,7), (2,5,8),
            (0,4,8), (2,4,6)]
    return any(board[a] == board[b] == board[c] == symbol for a,b,c in wins)

def player_move(board, player_name, symbol):
    while True:
        try:
            move = int(input(f"{player_name} ({symbol}), choose a cell (1-9): ")) - 1
            if 0 <= move < 9 and board[move] == ' ':
                board[move] = symbol
                break
            else:
                print(Fore.YELLOW + "⚠️  Invalid move! Try again.")
        except ValueError:
            print(Fore.YELLOW + "⚠️  Enter a valid number (1–9).")

def bot_move(board, symbol):
    print(Fore.CYAN + "🤖 Bot is thinking...")
    possible_moves = [i for i, spot in enumerate(board) if spot == ' ']
    move = random.choice(possible_moves)
    board[move] = symbol


def play_game():
    clear()
    print(Fore.CYAN + "🎮 Welcome to Tic Tac Toe!")
    print("Choose game mode:")
    print("1️⃣  Single Player (vs Bot)")
    print("2️⃣  Two Player\n")

    mode = input("Enter 1 or 2: ").strip()

    board = [' '] * 9
    player1 = input("\nEnter Player 1 name: ").strip() or "Player 1"
    player2 = "Bot" if mode == '1' else (input("Enter Player 2 name: ").strip() or "Player 2")

    symbols = {player1: Fore.GREEN + 'X' + Style.RESET_ALL, 
               player2: Fore.RED + 'O' + Style.RESET_ALL}

    current_player = player1
    show_board(board)

    for turn in range(9):
        if mode == '1' and current_player == "Bot":
            bot_move(board, symbols[current_player])
        else:
            player_move(board, current_player, symbols[current_player])

        show_board(board)

        
        if check_winner(board, symbols[current_player]):
            print(Fore.MAGENTA + f"🏆 {current_player} wins the game!\n")
            break

      
        current_player = player2 if current_player == player1 else player1
    else:
        print(Fore.YELLOW + "😐 It's a draw!\n")


while True:
    play_game()
    again = input("Play again? (y/n): ").lower()
    if again != 'y':
        print(Fore.CYAN + "\n👋 Thanks for playing Tic Tac Toe!")
        break
