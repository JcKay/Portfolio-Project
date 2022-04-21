import random

from two_player_game import TwoPlayer
from vs_ai_game import SmartAI
from game_board import ShowBoard
from insertblock import MakeMove

# Variables
exampleboard = {n: n for n in range(1, 10)}
playboard = {n: " " for n in range(1, 10)}
play_board = {n: " " for n in range(1, 10)}


## Function
def exampleBoard():
    # print example
    print(" Game Moves ")
    ShowBoard.printBoard(exampleboard)


###     WITH HUMAN PLAY
def game_mode_player():
    name1 = input('Player One Name: ')
    name2 = input('Player Two Name: ')
    OnGoing = True
    exampleBoard()

    # Game codes (Two players)
    game_type = TwoPlayer(name1=name1, name2=name2, board=playboard)
    while OnGoing:
        OnGoing = game_type.player1Move()
        if OnGoing == True:
            OnGoing = game_type.player2Move()
            if OnGoing == False:
                return question()
        else:
            return question()


###     WITH AI PLAY
def game_mode_ai():
    makemove = MakeMove(board=play_board)
    winner = makemove.winner

    name1 = input('Player Name: ')
    print("AI name is: QuantumAI")
    OnGoing = True
    exampleBoard()

    # Game codes vs AI
    game_type = SmartAI(name1=name1, board=playboard)

    ## Change
    if winner == "QuantumAI":
        while OnGoing:
            OnGoing = game_type.playerMove()
            if OnGoing == True:
                OnGoing = game_type.aiMove()
                if OnGoing == False:
                    return question()
            else:
                return question()
    elif winner == "draw":
        choice = random.choice(['ai', 'player'])
        if choice == 'ai':
            while OnGoing:
                OnGoing = game_type.aiMove()
                if OnGoing == True:
                    OnGoing = game_type.playerMove()
                    if OnGoing == False:
                        return question()
                else:
                    return question()

        else:
            while OnGoing:
                OnGoing = game_type.playerMove()
                if OnGoing == True:
                    OnGoing = game_type.aiMove()
                    if OnGoing == False:
                        return question()
                else:
                    return question()

    else:
        while OnGoing:
            OnGoing = game_type.aiMove()
            if OnGoing == True:
                OnGoing = game_type.playerMove()
                if OnGoing == False:
                    return question()
            else:
                return question()

    # ## PREVIOUS CODE
    # if winner == "QuantumAI":  # winner AI, go player
    #     game_battle(game_type.playerMove(), game_type.aiMove())
    #
    # elif winner == "draw":  # Draw ? random choice
    #     choice = random.choice(['ai', 'player'])
    #     if choice == 'ai':
    #         game_battle(game_type.aiMove(), game_type.playerMove())
    #     else:
    #         game_battle(game_type.playerMove(), game_type.aiMove())
    #
    # else:  # winner player, go AI
    #     game_battle(game_type.aiMove(), game_type.playerMove())
    #


def question():
    global playboard
    print("")
    ask = input("Type any key to play again.\nIf not type 'exit' > ")
    print('')
    if ask == "exit":
        return False
    else:
        playboard = play_board.copy()
        return True


## RUN GAME ##
PROCESS = True
while PROCESS:
    print('"Two Players Mode" or "vs AI Mode"')
    game_mode = input('[player] or [ai] > ')
    if game_mode == 'player':
        PROCESS = game_mode_player()
    elif game_mode == 'ai':
        PROCESS = game_mode_ai()
    elif game_mode == 'exit':
        exit()
    else:
        print('please type "player" or "ai",\nany other won\'t work,\n"exit" to exit the game.')
