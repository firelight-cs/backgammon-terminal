import random

# s = black
# a = white
def start_game(): #initializing the start game field 
    game = [[] for _ in range(26)]
    game[1] = ['b'] * 2
    game[6] = ['w'] * 5
    game[8] = ['w'] * 3
    game[12] = ['b'] * 5
    game[13] = ['w'] * 5
    game[17] = ['b'] * 3
    game[19] = ['b'] * 5
    game[24] = ['w'] * 2
    return game

def roll_dice():
    return random.randint(1, 6), random.randint(1, 6)

def is_double(dice):
    return dice[0] == dice[1]

def print_board(board):
    for i in range(5, -1, -1):
        line = f"{i:2d}|"
        for j in range(1, 25):
            if i < len(board[j]):
                line += f" {board[j][i]} |"
            else:
                line += "   |"
        print(line)
    print("--+" + "--+" * 32)
    print("  | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |10 |11 |12 |13 |14 |15 |16 |17 |18 |19 |20 |21 |22 |23 |24 |")
    
# def bear_off(board, player):
#     home_board = range(19, 25) if player == 'b' else range(1, 7)
#     for point in home_board:
#         while player in board[point]:
#             board[point].remove(player)

def move_checker(board, player, src, dst):
    board[dst].append(player)
    board[src].remove(player)

def valid_moves(board, player, dice):
    moves = []
    for move in dice:
        for src in range(1, 25):
            if player in board[src]:
                dst = src - move if player == 'b' else src + move
                if 1 <= dst <= 24:
                    if len(board[dst]) <= 1 or (len(board[dst]) == 2 and board[dst][0] == player):
                        moves.append((src, dst))
                    elif len(board[dst]) == 1 and board[dst][0] != player:
                        # Hitting an opponent's checker
                        moves.append((src, dst))
    
    # Check if bearing off is possible
    home_board = range(19, 25) if player == 'b' else range(1, 7)
    for point in home_board:
        if player in board[point]:
            for move in dice:
                dst = point - move if player == 'b' else point + move
                if dst <= 0:
                    moves.append((point, 0))  # Bear off

    return moves

def eat_checker(board, player, dst):
    opponent = 'w' if player == 'b' else 'b'
    if len(board[dst]) == 1 and board[dst][0] == opponent:
        board[dst].remove(opponent)


def play_turn(board, player, dice): 
    print_board(board)
    print(f"{player} turn")
    print(f"Dice: {dice}")
    moves = valid_moves(board, player, dice)
    if not moves:
        input("No valid moves. Press Enter to continue.")
        return
    while True:
        print("Valid moves:")
        for i, (src, dst) in enumerate(moves, start = 1):
            print(f"{i}: Move checker from {src} to {dst}")
        choice = input("Enter the number of the move or 'q' to quit: ")
        if choice == 'q':
            break
        try:
            choice = int(choice) - 1
            if 0 <= choice < len(moves):
                src, dst = moves[choice]
                move_checker(board, player, src, dst)
                eat_checker(board, player, dst)
                moves.remove((src, dst))
                print_board(board)
            else:
                print("Invalid move number. Try again.")
        except ValueError:
            print("Invalid input. Enter a move number or 'q' to quit.")

def main():
    game_board = start_game() # draw board
    players = ['b', 'w'] # adjust player's roles
    
    while True: # game state
        for player in players: # update game state when both players make move
            input(f"\n\n{player} Start! Press Enter to roll the dice...")
            dice = roll_dice() 
            if is_double(dice):
                dice *= 2  # Double dice, use all four values
            else:
                dice = (dice[0], dice[1])  # Use only two values
            play_turn(game_board, player, dice) #
            # bear_off(game_board, player)
            if not any(game_board[1:25]):
                print(f"{player} wins!")
                return

if __name__ == "__main__":
    main()
