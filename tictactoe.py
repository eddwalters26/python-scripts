def display_board():
    x = 0
    print("\n")
    for row in board:
        cellCount = 0
        for cell in row:
            if cell == 0:
                txt = "   "
            elif cell == 1:
                txt = " X "
            else:
                txt = " O "

            if cellCount < 2:
                txt += "|"
            cellCount += 1
            print(txt, end="")
        if x < 2:
            print("\n", "-" * 10)
        x += 1
    print("")

def getPlayer(xPlayerTurn):
    if xPlayerTurn == True:
        player = "X"
    else:
        player = "O"
    return player
        
def playerTurn(xTurn):
    player = getPlayer(xPlayerTurn)
    txt = "Your move {}"
    print(txt.format(player))
    try:
        row, col = input("Enter move (row, column):").split(',', maxsplit=1)
    except:
        return False, 0, 0
    else:
        return True, row, col

def playerMove(row, col, xTurn):
    try:
        iRow = int(row) - 1
        iCol = int(col) - 1
    except:
        print("Please enter a integer value")
        return False
    
    if xTurn == True:
        player = "X"
        playerValue = 1
    else:
        player = "O"
        playerValue = -1

    try:
        if board[iRow][iCol] != 0:
            invalidMoveTxt = "Invalid move by {}"
            print(invalidMoveTxt.format(player))
            return False
        else:
            board[iRow][iCol] = playerValue
            return True
    except:
        invalidMoveTxt = "Invalid move by {}"
        print(invalidMoveTxt.format(player))
        return False

def checkWin():
    for win in winConditions:
       total = 0
       for cell in win:
            row = cell[0]
            col = cell[1]
            total += board[row][col]
       if abs(total) == 3:
           return True
    
    return False

def checkBoardFull():
    moveAvailable = False
    for row in board:
        for cell in row:
            if cell == 0:
                moveAvailable = True
    return moveAvailable


board = [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]]

winConditions = [[[0,0], [0,1], [0,2]],
                     [[1,0], [1,1], [1,2]],
                     [[2,0], [2,1], [2,2]],
                     [[0,0], [1,0], [2,0]],
                     [[0,1], [1,1], [2,1]],
                     [[0,2], [1,2], [2,2]],
                     [[0,0], [1,1], [2,2]],
                     [[0,2], [1,1], [2,0]]]

xPlayerTurn = False
bGameOver = False
bMoveAvailable = True

while bGameOver == False and bMoveAvailable == True:
    validMove = False
    validMoveInput = False
    display_board()

    while validMove == False:
        while validMoveInput == False:
            validMoveInput, row, col = playerTurn(xPlayerTurn)
        validMoveInput = False
        validMove = playerMove(row, col, xPlayerTurn)

    bGameOver = checkWin()

    if bGameOver == True:
        player = getPlayer(xPlayerTurn)
        txt = "Congratulations player {} you have won"
        print(txt.format(player))
        break

    bMoveAvailable = checkBoardFull()

    if bMoveAvailable == False:
        txt = "No more moves the game is tied"
        print(txt)
        break
    xPlayerTurn = not(xPlayerTurn)

display_board()