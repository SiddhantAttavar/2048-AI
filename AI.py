#@author Siddhant Attavar
from threading import Thread
from time import sleep, time
from copy import deepcopy
from random import sample, choice

import Game

def heuristicValue(board, score):
    # Calculat the heuristic value of the current state
    value = 0

    flag = False
    freq = {}
    for row in range(Game.CELL_COUNT):
        for col in range(Game.CELL_COUNT):
            freq[board[row][col]] = freq.get(board[row][col], 0) + 1
            value += (2 ** SCORE_MATRIX[row][col] * board[row][col])
            if not value:
                value += FREE_TILE_WEIGHT
                flag = True

            if (row > 0 and board[row][col] == board[row - 1][col] or 
                col > 0 and board[row][col] == board[row][col - 1]):
                value += board[row][col] / 4
                flag = True
            
            if row > 0:
                value -= max(0, board[row - 1][col] - board[row][col])
            if col > 0:
                value -= max(0, board[row][col - 1] - board[row][col])
    
    if not flag:
        return 0
    
    for freq in freq.values():
        value += freq * freq / 4

    return value + score

def move(board, depth, alpha, score):
    global debug, MAX_CHILDREN, possibleMoves
    value = heuristicValue(board, score)
    if not depth:
        return None, value
    
    if value < alpha:
        return None, value
    
    bestScore = -1
    bestMove = -1

    for moveCount, res in enumerate(doMove(board, score) for doMove in possibleMoves):
        nextBoard, nextScore, nextFlag = res
        if not nextFlag:
            continue
        
        emptyCells = []
        for row in range(Game.CELL_COUNT):
            for col in range(Game.CELL_COUNT):
                if not board[row][col]:
                    emptyCells.append((row, col))
        
        if not emptyCells:
            nextValue = heuristicValue(nextBoard, nextScore)
            if nextValue > bestScore:
                bestScore = nextValue
                bestMove = moveCount
            continue
        
        currScore = 0
        for row, col in sample(emptyCells, min(MAX_CHILDREN, len(emptyCells))):
            nextBoard[row][col] = 2
            currScore += move(deepcopy(nextBoard), depth - 1, bestScore, nextScore)[1]
            nextBoard[row][col] = 0
        currScore /= len(emptyCells)
        
        if currScore > bestScore:
            bestScore = currScore
            bestMove = moveCount
    
    return bestMove, bestScore

def moveMonteCarlo(board, score):
    global debug, possibleMoves, MAX_SEARCH_DEPTH, MAX_SEARCH_MOVES

    moveScores = [0] * len(possibleMoves)
    for moveCount, res in enumerate(doMove(board, score) for doMove in possibleMoves):
        nextBoard, nextScore, nextFlag = res

        if not nextFlag:
            # The move was not played
            continue

        for _ in range(MAX_SEARCH_MOVES):
            searchDepth = 1
            currBoard = deepcopy(nextBoard)
            flag = True
            currScore = nextScore

            while flag and searchDepth < MAX_SEARCH_DEPTH:
                searchDepth += 1
                Game.addNewNum(currBoard, False)
                currBoard, currScore, flag = choice(possibleMoves)(currBoard, currScore)

            moveScores[moveCount] += currScore
    
    topMove = 0
    for moveCount in range(len(possibleMoves)):
        if moveScores[topMove] < moveScores[moveCount]:
            topMove = moveCount
    
    return topMove

def startAI():
    global debug
    while not Game.gameOver:
        startTime = time()
        #bestMove, _ = move(Game.board, MAX_DEPTH, 0, Game.score)
        bestMove = moveMonteCarlo(Game.board, Game.score)
        Game.board, Game.score, _ = possibleMoves[bestMove](Game.board, Game.score)
        try:
            Game.addNewNum(Game.board, True)
        except:
            return
        Game.checkGameOver(Game.board)
        sleep(SLEEP_TIME - min(SLEEP_TIME, time() - startTime))

def runAI():
    # Run the game with algorithm
    root = Game.runGame(False)
    thread = Thread(target = startAI)
    thread.start()
    root.mainloop()

# AI Constants
SLEEP_TIME = 0.05
MAX_SEARCH_DEPTH = 7
MAX_SEARCH_MOVES = 30
MAX_DEPTH = 3
MAX_CHILDREN = 14
FREE_TILE_WEIGHT = 8
SCORE_MATRIX = [
    [8, 7, 6, 5, 4],
    [7, 6, 5, 4, 3],
    [6, 5, 4, 3, 2],
    [5, 4, 3, 2, 1]
]

# AI variables
possibleMoves = [Game.moveUp, Game.moveDown, Game.moveLeft, Game.moveRight]

if __name__ == '__main__':
    runAI()