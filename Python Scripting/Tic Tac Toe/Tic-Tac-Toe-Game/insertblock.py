from game_board import ShowBoard
from win_draw_lose import CheckGame


class MakeMove:

    def __init__(self, board):
        self.board = board

    def spaceIsFree(self, position):
        if self.board[position] == " ":
            return True
        else:
            return False

    def insertPlace(self, letter, position, x_name, o_name):
        if self.spaceIsFree(position):
            self.board[position] = letter
            print("\n")  # seperate
            ShowBoard.printBoard(self.board)
            if CheckGame.checkForWin(self.board):
                if letter == "X":
                    print(f'{x_name} Wins!')
                    return False

                else:
                    print(f'{o_name} Wins!')
                    return False

            if CheckGame.checkDraw(self.board):
                print('Draw Game')
                return False

            return True
        else:
            position = int(
                input('This square is not blank\nChoose another number: '))
            self.insertPlace(letter, position, x_name, o_name)
            return
