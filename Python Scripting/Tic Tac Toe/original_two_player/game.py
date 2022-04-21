from two_player_game import TwoPlayer
from computer_game import SmartAI
from game_board import ShowBoard
from win_draw_lose import CheckGame

## Variables
exampleboard = {n: n for n in range(1, 10)}
playboard = {n: " " for n in range(1, 10)}


## Function
def game_mode_player():
    name1 = input('Player One Name: ')
    name2 = input('Player Two Name: ')

    # print example
    print(" Game Moves ")
    ShowBoard.printBoard(exampleboard)

    # Game codes
    game_type = TwoPlayer(name1=name1, name2=name2, board=playboard)
    while not CheckGame.checkForWin(game_type.board):
        game_type.player1Move()
        game_type.player2Move()


## RUN GAME ##
while True:
    print('"Two Players Mode" or "vs AI Mode"')
    game_mode = input('[player] or [ai] > ')
    if game_mode == 'player':
        game_mode_player()
    elif game_mode == 'ai':
        SmartAI()
    elif game_mode == 'exit':
        exit()
    else:
        print('please type "player" or "ai",\nany other won\'t work,\n"exit" to exit the game.')
