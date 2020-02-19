def generateBoard(boardSize):
    board = []
    x = 0
    while x < boardSize:
        board.append([0] * boardSize)
        x += 1
    return board

def generateWinConditions(boardSize):
    wins = []
    #row wins & column wins
    for row in range(boardSize):
        rowWin = []
        colWin = []
        for col in range(boardSize):
            rowWin.append([row, col])
            colWin.append([col, row])
        wins.append(rowWin)
        wins.append(colWin)
    #diagonal wins
    row = 0
    col = boardSize - 1
    diagRight = []
    diagLeft = []
    while row < boardSize:
        diagRight.append([row, row])
        diagLeft.append([row, col])
        row += 1
        col -= 1
    wins.append(diagRight)
    wins.append(diagLeft)
    return wins

def display_board(board):
    boardSize = len(board)
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

            if cellCount < boardSize - 1:
                txt += "|"
            cellCount += 1
            print(txt, end="")
        if x < boardSize - 1:
            print("\n", end="")
            txt = ("---+" * boardSize)[:-1]
            print(txt)
        x += 1
    print("\n")

def getPlayer(xPlayerTurn):
    if xPlayerTurn == True:
        player = "X"
    else:
        player = "O"
    return player
        
def playerTurn(xPlayerTurn):
    player = getPlayer(xPlayerTurn)
    txt = "Your move {}"
    print(txt.format(player))
    try:
        row, col = input("Enter move (row, column):").split(',', maxsplit=1)
    except:
        return False, 0, 0
    else:
        return True, row, col

def playerMove(row, col, xPlayerTurn):
    try:
        iRow = int(row) - 1
        iCol = int(col) - 1
    except:
        print("Please enter a integer value")
        return False
    player = getPlayer(xPlayerTurn)
    if xPlayerTurn == True:
        playerValue = 1
    else:
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

def checkWin(board, winConditions):
    for win in winConditions:
       total = 0
       for cell in win:
            row = cell[0]
            col = cell[1]
            total += board[row][col]
       if abs(total) == len(board):
           return True
    
    return False

def checkBoardFull(board):
    moveAvailable = False
    for row in board:
        for cell in row:
            if cell == 0:
                moveAvailable = True
    return moveAvailable

def gameFunction(board, winConditions):
    xPlayerTurn = False
    bGameOver = False
    bMoveAvailable = True

    while bGameOver == False and bMoveAvailable == True:
        validMove = False
        validMoveInput = False
        display_board(board)

        while validMove == False:
            while validMoveInput == False:
                validMoveInput, row, col = playerTurn(xPlayerTurn)
            validMoveInput = False
            validMove = playerMove(row, col, xPlayerTurn)

        bGameOver = checkWin(board, winConditions)

        if bGameOver == True:
            player = getPlayer(xPlayerTurn)
            txt = "Congratulations player {} you have won"
            print(txt.format(player))
            break

        bMoveAvailable = checkBoardFull(board)

        if bMoveAvailable == False:
            txt = "No more moves the game is tied"
            print(txt)
            break
        xPlayerTurn = not(xPlayerTurn)

    display_board(board)

bPlayAgain = True
while bPlayAgain == True:
    boardSize = 4
    board = generateBoard(boardSize)
    winConditions = generateWinConditions(boardSize)

    gameFunction(board, winConditions)
    sPlayAgain = input("Do you want to play again (y/n)?")
    print(sPlayAgain.lower())
    if sPlayAgain.lower() == "n":
        bPlayAgain == False
        break
