from two_player_game import TwoPlayer
from vs_ai_game import SmartAI
from game_board import ShowBoard
from win_draw_lose import CheckGame

# Variables
exampleboard = {n: n for n in range(1, 10)}
playboard = {n: " " for n in range(1, 10)}


## Function
def exampleBoard():
    # print example
    print(" Game Moves ")
    ShowBoard.printBoard(exampleboard)


def game_mode_player():
    name1 = input('Player One Name: ')
    name2 = input('Player Two Name: ')
    exampleBoard()

    # Game codes (Two players)
    game_type = TwoPlayer(name1=name1, name2=name2, board=playboard)
    while not CheckGame.checkForWin(game_type.board):
        game_type.player1Move()
        game_type.player2Move()


def game_mode_ai():
    name1 = input('Player Name: ')
    print("AI name is: QuantumAI")
    exampleBoard()

    # Game codes vs AI
    game_type = SmartAI(name1=name1, board=playboard)
    while not CheckGame.checkForWin(board=game_type.board):
        game_type.aiMove()
        game_type.playerMove()

def question():
    ask = input("Play Again? type any key.\nIf not: e")
    if ask == 'e':
        return False
    else:
        return True

## RUN GAME ##
PROCESSING = True
while PROCESSING:
    print('"Two Players Mode" or "vs AI Mode"')
    game_mode = input('[player] or [ai] > ')
    if game_mode == 'player':
        game_mode_player()
        PROCESSING = question()
    elif game_mode == 'ai':
        game_mode_ai()
        PROCESSING = question()
    elif game_mode == 'exit':
        exit()
    else:
        print('please type "player" or "ai",\nany other won\'t work,\n"exit" to exit the game.')
