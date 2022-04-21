board = [' ' for _ in range(9)]
print(board)

for row in [board[i * 3:(i + 1) * 3] for i in range(3)]:
    print('| ' + ' | '.join(row) + ' |')

# [for i in range(j*3 , (j+1) * 3)] for j in range(3):
#     print(i)

number_board = [[str(i) for i in range(j * 3, (j + 1) * 3)] for j in range(3)]
for row in number_board:
    print('| ' + ' | '.join(row) + ' |')


## BOARD CRATE ##
def isMovesLeft(board):
    for i in range(3):
        for j in range(3):
            if (board[i][j] == '_'):
                return True
    return False


## WHO WIN THE GAME ##
def evaluate(b):
    # Checking for Rows for X or O victory.
    for row in range(3):
        if (b[row][0] == b[row][1] and b[row][1] == b[row][2]):
            if (b[row][0] == player):
                return 10
            else if (b[row][0] == opponent):
                return -10

    # Checking for Columns for X or O victory.
    for col in range(3):

        if (b[0][col] == b[1][col] and b[1][col] == b[2][col]):

            if (b[0][col] == player):
                return 10
            else if (b[0][col] == opponent):
                return -10

    # Checking for Diagonals for X or O victory.
    if (b[0][0] == b[1][1] and b[1][1] == b[2][2]):

        if (b[0][0] == player):
            return 10
        else if (b[0][0] == opponent):
            return -10

    if (b[0][2] == b[1][1] and b[1][1] == b[2][0]):

        if (b[0][2] == player):
            return 10
        else if (b[0][2] == opponent):
            return -10

    # Else if none of them have won then return 0
    return 0


isMovesLeft(board)
