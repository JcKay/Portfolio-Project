class CheckGame:

    def checkForWin(board):
        if (board[1] == board[2] and board[1] == board[3] and board[1] != ' '):
            return True
        elif (board[4] == board[5] and board[4] == board[6] and board[4] != ' '):
            return True
        elif (board[7] == board[8] and board[7] == board[9] and board[7] != ' '):
            return True
        elif (board[1] == board[4] and board[1] == board[7] and board[1] != ' '):
            return True
        elif (board[2] == board[5] and board[2] == board[8] and board[2] != ' '):
            return True
        elif (board[3] == board[6] and board[3] == board[9] and board[3] != ' '):
            return True
        elif (board[1] == board[5] and board[1] == board[9] and board[1] != ' '):
            return True
        elif (board[7] == board[5] and board[7] == board[3] and board[7] != ' '):
            return True
        else:
            return False

    def checkDraw(board):
        for key in board.keys():
            if board[key] == " ":
                return False
        return True

    def checkWhichMarkWon(mark, board):
        if (board[1] == board[2] and board[1] == board[3] and board[1] == mark):
            return True
        elif (board[4] == board[5] and board[4] == board[6] and board[4] == mark):
            return True
        elif (board[7] == board[8] and board[7] == board[9] and board[7] == mark):
            return True
        elif (board[1] == board[4] and board[1] == board[7] and board[1] == mark):
            return True
        elif (board[2] == board[5] and board[2] == board[8] and board[2] == mark):
            return True
        elif (board[3] == board[6] and board[3] == board[9] and board[3] == mark):
            return True
        elif (board[1] == board[5] and board[1] == board[9] and board[1] == mark):
            return True
        elif (board[7] == board[5] and board[7] == board[3] and board[7] == mark):
            return True
        else:
            return False
