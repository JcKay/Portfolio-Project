from insertblock import MakeMove


class TwoPlayer:
    def __init__(self, name1, name2, board):
        self.player1_name = name1
        self.player2_name = name2
        self.player1 = "X"
        self.player2 = "O"
        self.board = board

    def player1Move(self):
        position = int(input(f"Enter position for {self.player1}: "))
        make_move = MakeMove(board=self.board)
        make_move.insertPlace(letter=self.player1, position=position,
                              x_name=self.player1_name, o_name=self.player2_name)
        # self.insertPlace(letter=self.player1, position=position)
        return

    def player2Move(self):
        position = int(input(f"Enter position for {self.player2}: "))
        make_move = MakeMove(board=self.board)
        make_move.insertPlace(letter=self.player2, position=position,
                              x_name=self.player1_name, o_name=self.player2_name)
        # self.insertPlace(letter=self.player2, position=position)
        return
