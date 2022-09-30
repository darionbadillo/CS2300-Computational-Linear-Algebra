# Darion Badillo
# Assignment 2 - Linear Domination Game
# 9/20/2022
import math

#Obtains board size from file
def readFile(path):
    with open(path, 'r') as newFile:
        #Creates an empty array to be passed two values into
        emptyArray = []

        # Reads the first line for N and K
        str1 = newFile.readline().split(' ')
        for item in str1:
            emptyArray.append((int(item)))
        
        N = emptyArray[0]
        K = emptyArray[1]

        # Read-in N value creates an N*N matrix for the game board
        tempArray = N*[' ']
        matrixBoard = []
        for i in range(N):
            matrixBoard.append(tempArray[:])

        #The rest of the file is written to a matrix of moves to be played
        movesArray = []
        for line in newFile:
            arr = line.rstrip("\n").split(' ')
            tempArr = []
            for item in arr:
                #Ensures an empty value isn't being passed through
                if item != '':
                    tempArr.append(item)
            movesArray.append(tempArr)
        # Turns string values into int values    
        for row in range (len(movesArray)):
            for column in range(0,len(movesArray[row])):
                movesArray[row][column] = int(movesArray[row][column])
    print('Read in file successfully')                
    return matrixBoard, K, movesArray

#Linear Domination Game function
def playGame(gameBoard, K, movesArray):
    #Determines the amount of total moves in the movesArray
    playerMoves = len(movesArray)
    playedMoves = []
    i = 0
    K = K*2
    print('Begin Linear Domination', file=f)
        
    # Loops until the assigned amount of moves runs out
    while i < playerMoves:
        #Player 1 move
        if ((i % 2) == 0):
            print('Player 1\'s turn:', file=f)
            #boolean that flags as false when an invalid move is made
            player1 = True
            player1, playedMoves, gameBoard = playerMove(movesArray, i, playedMoves, 1, gameBoard, K)

        #Player 2 move
        else:
            print('Player 2\'s turn:', file=f)
            #boolean that flags as false when an invalid move is made
            player2 = True
            player2, playedMoves, gameBoard = playerMove(movesArray, i, playedMoves, 2, gameBoard, K)

        # Game ending condition where two consecutive invalid moves were made by both players
        if (not player1 and not player2):
            print('Two invalid moves', file=f)
            return gameBoard

        # Game ending condition where there are no available spots left on the board
        count = 0
        for row in gameBoard:
            for column in row:
                if column == ' ':
                    count = count + 1
        if count == 0:
            print('No more playable cells', file=f)
            return gameBoard
        
        # i increments each time it loops
        i = i + 1

#Handles each player's move and calls the necessary functions to check for move validity and plays the move
def playerMove(movesArray, i, playedMoves, player, gameBoard, K):

    # Assigns the player's move to a variable
    move = movesArray[i]
    print(f'Player {player} plays ({move[1]},{move[0]}) to ({move[3]},{move[2]})', file=f)

    # Verifies the move is valid
    validMove, playedMoves = playValidity(move, playedMoves, K, gameBoard, i)

    # Calls updateBoard to play the move if the move is valid
    if validMove:
        gameBoard = updateBoard(gameBoard, move, player)

    #Calls for the score to be shown
    scores = computeScore(gameBoard)

    #Prints the most up-to-date board
    printBoard(gameBoard,scores)

    
    print('', file=f)    
    return validMove, playedMoves, gameBoard

#Checks if move is valid against four conditions
def playValidity(move, playedMoves, K, gameBoard, i):
    #boolean that will flag as false once a condition is triggered
    valid = True

    # Splits move into four variables
    sr = move[0] #x1
    sc = move[1] #y1
    er = move[2] #x2
    ec = move[3] #y2

    #Calculates the vector from the given move
    vector1 = [(ec-sc),(er-sr)]

    #Checks for perpendicular move against a dot product of already played moves
    for item in playedMoves:
        x1 = item[0]
        y1 = item[1]
        x2 = item[2]
        y2 = item[3]
        vector2 = [(y2-y1),(x2-x1)]
        dot = (vector1[0]*vector2[0] + vector1[1]*vector2[1])
        if (dot == 0):
            print('Invalid Move: Perpendicular to existing line\n', file=f)
            return False, playedMoves

    #Checks current move against a matrix of already played moves to ensure the move's originality
    for item in playedMoves:
        if item == move:
            print('Invalid Move: Move already exists\n', file=f)
            return False, playedMoves
        # Condition checks for reverse existing move 
        tempItem = [item[2], item[3], item[0], item[1]]
        if tempItem == move:
            print('Invalid Move: Move already exists\n', file=f)
            return False, playedMoves

    #Checks if starting point/ending point are the same
    if (move[0] == move[2]) and (move[1] == move[3]):
        print('Invalid Move: Line of 0 length\n', file=f)
        return False, playedMoves

    #Checks gameBoard for an empty cell but only if the first K amount of moves has past
    if ((gameBoard[sr-1][sc-1] != ' ') or (gameBoard[er-1][ec-1] != ' ')) and (i+1 > K):
        print('Invalid Move: Cell already occupied\n', file=f)
        return False, playedMoves

    #After the move passes all conditions, the move is added to an array of played moves and returns bool True
    if valid:
        playedMoves.append(move)
        return True, playedMoves

#Creates several variables to update the board with the move to be played
def updateBoard(gameBoard, move, player):
    sr = move[0]-1 #y1
    sc = move[1]-1 #x1
    er = move[2]-1 #y2
    ec = move[3]-1 #x2

    #Implicit line calculations
    a = ec-sc
    b = er-sr
    c = (er*sc)-(ec*sr)
    v = math.sqrt((a*a)+(b*b))

    #Passes implicit line calculations to flip the cells of on the board
    gameBoard = flipCells(gameBoard, a, b, c, v, player,sr,sc,er,ec)

    return gameBoard

# Marks the Board with the specified player's move
def flipCells(gameBoard, a, b, c, v, player,sr,sc,er,ec):
    #Player 1 move
    if (player == 1):
        for row in range(len(gameBoard)):
            for column in range(len(gameBoard[row])):
                #Calculates the distance of a point to a line
                d = abs(((a*(sc-column)) - (b*(sr-row))))/v
                flag = True
                if (row > er and row > sr) or (row < er and row < sr):
                    flag = False
                elif (column > ec and column > sc) or (column < ec and column < sc):
                    flag = False
                if d <= 0.5 and flag:
                    gameBoard[row][column] = 'X'
    #Player 2 move 
    else:
        for row in range(len(gameBoard)):
            for column in range(len(gameBoard[row])):
                #Calculates the distance of a point to a line
                d = abs(((a*(sc-column)) - (b*(sr-row))))/v
                flag = True
                if (row > er and row > sr) or (row < er and row < sr):
                    flag = False
                elif (column > ec and column > sc) or (column < ec and column < sc):
                    flag = False
                if d <= 0.5 and flag:
                    gameBoard[row][column] = 'O'
    #returns updated board with move
    return gameBoard

#Computes the score for each player
def computeScore(gameBoard):
    p1Score = 0
    p2Score = 0

    #Iterates through matrix and updates the player's score 
    for row in range(len(gameBoard)):
        for column in range(len(gameBoard[row])):
            # Player 1 condition
            if gameBoard[row][column] == 'X':
                p1Score = p1Score + 1
            #Player 2 condition
            if gameBoard[row][column] == 'O':
                p2Score = p2Score + 1

    return [p1Score,p2Score]

#Prints the board 
def printBoard(gameBoard,scores):
    for row in reversed(gameBoard):
        print(row, file=f)
    print(f'Player 1 Score: {scores[0]} \tPlayer 2 Score: {scores[1]} ', file=f)
    
    return None

##main

#Asks user for the input file
fileName = input('Please enter file name (Example: "./p2-1.txt"\n')
#Creates an output file
outputFile = fileName[:-4] + '_output.txt'

#Writes to an output file 
with open(outputFile, 'w') as f:

    #Reads the opened file for moves
    gameBoard, K, movesArray = readFile(fileName)

    #Calls for the game to be played
    gameBoard = playGame(gameBoard, K, movesArray)

    #Calculates the score to be displayed with the board one final time
    scores = computeScore(gameBoard)

    printBoard(gameBoard,scores)

    # Determines the winner of Linear Domination
    if scores[0] > scores [1]:
        print('Player 1 wins!', file=f)
    elif scores[0] < scores [1]:
        print('Player 2 wins!', file=f)
    else:
        print('Tie game!', file=f)

    print('Game over!', file=f)
print(f'Outputted to file: {outputFile}')
