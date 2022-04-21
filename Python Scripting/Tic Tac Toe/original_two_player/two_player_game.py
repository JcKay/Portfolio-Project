from game_board import ShowBoard
from win_draw_lose import CheckGame


class TwoPlayer:
    def __init__(self, name1, name2, board):

        self.player1_name = name1
        self.player2_name = name2
        self.player1 = "X"
        self.player2 = "O"
        self.board = board

    def spaceIsFree(self, position):
        if self.board[position] == " ":
            return True
        else:
            return False

    def insertPlace(self, letter, position):
        if self.spaceIsFree(position):
            self.board[position] = letter
            print("\n")  # seperater
            ShowBoard.printBoard(self.board)
            if CheckGame.checkForWin(self.board):
                if letter == "X":
                    print(f'{self.player1_name} Wins!')
                    exit()
                else:
                    print(f'{self.player2_name} Wins!')
                    exit()
            if CheckGame.checkDraw(self.board):
                print('Draw Game')
                exit()
            return
        else:
            position = int(input('This square is not blank\nChoose another number: '))
            self.insertPlace(letter, position)
            return

    def player1Move(self):
        position = int(input(f"Enter position for {self.player1}: "))
        self.insertPlace(letter=self.player1, position=position)
        return

    def player2Move(self):
        position = int(input(f"Enter position for {self.player2}: "))
        self.insertPlace(letter=self.player2, position=position)
        return
