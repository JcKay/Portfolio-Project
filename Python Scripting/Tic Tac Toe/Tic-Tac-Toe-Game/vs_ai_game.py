from insertblock import MakeMove
from win_draw_lose import CheckGame


class SmartAI:

    def __init__(self, name1, board):
        self.player_name = name1
        self.ai_name = "QuantumAI"
        self.player = "O"
        self.ai = "X"
        self.board = board

    def minimax(self, board, depth, isMaximizingPlayer):

        if CheckGame.checkWhichMarkWon(self.ai, self.board):
            return 100

        elif CheckGame.checkWhichMarkWon(self.player, self.board):
            return -100

        elif CheckGame.checkDraw(self.board):
            return 0

        if isMaximizingPlayer:
            bestVal = -1000

            for key in self.board.keys():
                if self.board[key] == " ":
                    self.board[key] = self.ai
                    value = self.minimax(self.board, 0, False)
                    bestVal = max(bestVal, value)
                    self.board[key] = " "
            return bestVal

        else:
            bestVal = 1000

            for key in self.board.keys():
                if self.board[key] == " ":
                    self.board[key] = self.player
                    value = self.minimax(self.board, depth + 1, True)
                    bestVal = min(bestVal, value)
                    self.board[key] = " "
            return bestVal

    def aiMove(self):
        bestVal = -1000
        bestMove = 0

        for key in self.board.keys():
            if self.board[key] == " ":
                self.board[key] = self.ai
                moveVal = self.minimax(
                    board=self.board,
                    depth=0,
                    isMaximizingPlayer=False
                )
                self.board[key] = " "
                if moveVal > bestVal:
                    bestVal = moveVal
                    bestMove = key

        print(f"AI move position for X: {bestMove}")
        make_move = MakeMove(board=self.board)
        return make_move.insertPlace(letter=self.ai, position=bestMove, x_name=self.ai_name, o_name=self.player_name)


    def playerMove(self):
        position = int(input(f"Enter position for {self.player}: "))
        make_move = MakeMove(board=self.board)
        return make_move.insertPlace(letter=self.player, position=position, x_name=self.ai_name, o_name=self.player_name)

