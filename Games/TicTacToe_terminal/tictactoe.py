from os import system
from random import choice
from time import sleep

def display_table():
    for r in ls:
        print("|".join(r))

def get_player_move():
    display_table()
    while True:
        try:
            player_turn = int(input(">> "))
            if 1 <= player_turn <= 9:
                row_index = (player_turn-1) // 3
                col_index = (player_turn-1) % 3
                return row_index, col_index
            else:
                print("Please, enter nu ber from 1 to 9")
        except ValueError:
            print("Invalid input. Try again...")

def change_turn(CURRENT_TURN):
    return "o" if CURRENT_TURN == "x" else "x"

def change_player(CURRENT_PLAYER, PLAYERS):
    return PLAYERS[1] if CURRENT_PLAYER == PLAYERS[0] else PLAYERS[0]


def select_players(player_mode):
    if player_mode == 0:
        PLAYERS = ["Player 1", "Computer"]
    elif player_mode == 1:
        PLAYERS = ["Player 1", "player 2"]

    
    CURRENT_PLAYER = PLAYERS[0]
    print(f"""
    {PLAYERS[0]} plays as X.
    {PLAYERS[1]} plays as O.
""")
    return PLAYERS, CURRENT_PLAYER

def check_winner(ls):

    for r in range(3):
        if all(ls[r][c] == "x" for c in range(3)) or all(ls[c][r] == "x" for c in range(3)):
            return True
        elif all(ls[r][c] == "o" for c in range(3)) or all(ls[c][r] == "o" for c in range(3)):
            return True
       
    # diagonal and reverse diagonal
    if all(ls[i][i] == "x" for i in range(3)) or all(ls[i][2-i] == "x" for i in range(3)):
        return True
    elif all(ls[i][i] == "o" for i in range(3)) or all(ls[i][2-i] == "o" for i in range(3)):
        return True
    return False


def find_best_move(move, ls):
    for r, c in [(r, c) for r in range(3) for c in range(3) if ls[r][c] not in ["x", "o"]]:
        previous_value = ls[r][c]
        ls[r][c] = move
        if check_winner(ls):
            ls[r][c] = previous_value
            return r, c
        ls[r][c] = previous_value
    return None

while True:
    ls = [
        [f"{x+y}" for y in range(3)]
        for x in range(1, 9, 3)     
    ] 
    try:
        player_mode = int(input("Who would you like to play with: the Computer(0) / Player 2 (1)? \n>> ")) 
        if player_mode not in [0, 1]:
            raise ValueError
    except ValueError:
        print("Invalid input. Try again...")
        continue

    PLAYERS, CURRENT_PLAYER = select_players(player_mode)
    TURNS = ["x", "o"]  
    CURRENT_TURN = "x"

    while True:
        sleep(1)
        system("clear")
        print(f"The {CURRENT_PLAYER} is playing now...")
        
        if player_mode == 0 and CURRENT_PLAYER == "Computer":
            print("Computer thinking...")
            sleep(1)
            empty_cells = [(r, c) for r in range(3) for c in range(3) if ls[r][c] not in TURNS]
            computer_move = find_best_move("o", ls) or find_best_move("x", ls) or tuple(choice(empty_cells))
    
            row_index, col_index = computer_move
            ls[row_index][col_index] = CURRENT_TURN  
            display_table()
   
        else:
            row_index, col_index = get_player_move()
            ls[row_index][col_index] = CURRENT_TURN
        
        if check_winner(ls):
            sleep(1)
            system("clear")
            display_table()
            print(f"{CURRENT_PLAYER} is WINNERRR!!!")
            break

        if all(cell in ["x", "o"] for row in ls  for cell in row):
            print("DRAW!")
            display_table()
            break
        
        CURRENT_TURN = change_turn(CURRENT_TURN)
        CURRENT_PLAYER = change_player(CURRENT_PLAYER, PLAYERS)

    asking_play = input("Do you want to play again? (yes/no): \n>> ")
    if asking_play.lower() != "yes":
        print("BYEE")
        break 
