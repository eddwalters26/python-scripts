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
            txt = " " + playerDict[cell] + " "
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
        
def playerTurn(iPlayerTurn):
    txt = "Your move {}"
    print(txt.format(playerDict[iPlayerTurn]))
    try:
        row, col = input("Enter move (row, column):").split(',', maxsplit=1)
    except:
        return False, 0, 0
    else:
        return True, row, col

def playerMove(row, col, iPlayerTurn):
    try:
        iRow = int(row) - 1
        iCol = int(col) - 1
    except:
        print("Please enter a integer value")
        return False
      
    try:
        if board[iRow][iCol] != 0:
            invalidMoveTxt = "Invalid move by {}"
            print(invalidMoveTxt.format(playerDict[iPlayerTurn]))
            return False
        else:
            board[iRow][iCol] = iPlayerTurn
            return True
    except:
        invalidMoveTxt = "Invalid move by {}"
        print(invalidMoveTxt.format(playerDict[iPlayerTurn]))
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
    iPlayerTurn = -1
    bGameOver = False
    bMoveAvailable = True

    while bGameOver == False and bMoveAvailable == True:
        validMove = False
        validMoveInput = False
        display_board(board)

        while validMove == False:
            while validMoveInput == False:
                validMoveInput, row, col = playerTurn(iPlayerTurn)
            validMoveInput = False
            validMove = playerMove(row, col, iPlayerTurn)

        bGameOver = checkWin(board, winConditions)

        if bGameOver == True:
            txt = "Congratulations player {} you have won"
            print(txt.format(playerDict[iPlayerTurn]))
            break

        bMoveAvailable = checkBoardFull(board)

        if bMoveAvailable == False:
            txt = "No more moves the game is tied"
            print(txt)
            break
        playerTurn *= -1 

    display_board(board)

playerDict = {
    -1: "O",
    0: " ",
    1: "X"
}
bPlayAgain = True
while bPlayAgain == True:
    try:
        boardSize = int(input("Please enter size of board: "))
        if boardSize < 2 or boardSize > 10:
            raise Exception()
    except:
        print("Please enter a valid board size between 2 and 10")
    else:    
        board = generateBoard(boardSize)
        winConditions = generateWinConditions(boardSize)

        gameFunction(board, winConditions)
        sPlayAgain = input("Do you want to play again (y/n)?")
        print(sPlayAgain.lower())
        if sPlayAgain.lower() == "n":
            bPlayAgain == False
            break
