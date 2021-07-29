#@author Siddhant Attavar
from tkinter import Tk, Frame, Label, CENTER
from random import randrange, random
from copy import deepcopy
from sys import exit

def runGame(playerIsHuman):
    global scoreLabel, score, root
    # Initialize the main display
    root = Tk()
    root.configure(bg = BACKGROUND_COLOR)
    root.protocol('WM_DELETE_WINDOW', exit)
    root.title('2048 AI')
    root.iconbitmap('logo.ico')

    score = 0
    scoreLabel = Label(
        root,
        width = 19,
        height = 1,
        justify = CENTER,
        font = ('Verdana', 40, 'bold'),
        bg = BACKGROUND_COLOR
    )
    scoreLabel.grid(row = 0, padx = CELL_PADDING, pady = CELL_PADDING)

    frame = Frame(
        root,
        width = SCREEN_WIDTH,
        height = SCREEN_HEIGHT,
        bg = BACKGROUND_COLOR
    )
    frame.grid(row = 1, padx = CELL_PADDING, pady = CELL_PADDING)

    if playerIsHuman:
        root.bind('<Key>', onKeyPress)

    # Display board
    for row in range(CELL_COUNT):
        grid.append([])
        for col in range(CELL_COUNT):
            # Add cell to grid
            cell = Frame(
                frame,
                width = CELL_SIZE,
                height = CELL_SIZE
            )
            cell.grid(
                row = row,
                column = col,
                padx = CELL_PADDING,
                pady = CELL_PADDING
            )

            # Label to the cell
            grid[row].append(Label(
                cell,
                width = 4,
                height = 2,
                bg = CELL_COLOR[board[row][col]],
                justify = CENTER,
                font = ('Verdana', 40, 'bold'),
                foreground = TEXT_COLOR
            ))
            grid[row][col].grid()

    # Start the game and add 4 nums
    addNewNum(board, False)
    addNewNum(board, True)
    if playerIsHuman:
        root.mainloop()
    
    return root

def displayBoard():
    # Display the cells in the grid
    for row in range(CELL_COUNT):
        for col in range(CELL_COUNT):
            grid[row][col].configure(
                text = str(board[row][col]) if board[row][col] else '',
                bg = CELL_COLOR[board[row][col]]
            )
    
    # Disply the updated score
    scoreLabel.configure(text = f'Score: {score}')

def addNewNum(board, display):
    # Add 2 new numbers on to the board
    # There is a 1 in 10 chance of the number being 4
    # And a 9 in 10 chance of the number being 2

    # Find the empty cells
    emptyCells = []
    for row in range(CELL_COUNT):
        for col in range(CELL_COUNT):
            if not board[row][col]:
                emptyCells.append((row, col))

    if emptyCells:
        # Find the position of the new tile
        newNumX, newNumY = emptyCells.pop(randrange(len(emptyCells)))
        board[newNumX][newNumY] = 2 #4 if random() < 0.1 else 2
    
    if display:
        displayBoard()

def onKeyPress(event):
    global gameOver, board, score
    # Called when a key is pressed
    # Don't do anything if the game is over
    if gameOver or event.keysym not in KEY_FUNCTIONS:
        return

    # Call the function corresponding to the key
    board, score, flag = KEY_FUNCTIONS[event.keysym](board, score)
    if flag:
        addNewNum(board, True)
        checkGameOver(board)

def checkGameOver(board):
    global gameOver
    # Check if the player has won the game
    for row in range(CELL_COUNT):
        if 2048 in board[row]:
            scoreLabel.configure(
                text = f'You win! Score: {score}',
                font = ('Verdana', 30, 'bold')
            )
            gameOver = True
            return
    
    # Check if the game is over
    flag = False
    for row in board:
        for cell in row:
            if not cell:
                flag = True
                break
        if flag:
            break
    if flag:
        return

    for row in range(CELL_COUNT):
        for col in range(CELL_COUNT):
            if ((row > 0 and board[row][col] == board[row - 1][col]) or 
                (col > 0 and board[row][col] == board[row][col - 1])):
                flag = True
                break
        if flag:
            break
    
    if not flag:
        scoreLabel.configure(
            text = f'You Lose. Score: {score}',
            font = ('Verdana', 40)
        )
        gameOver = True

def moveUp(board, score):
    # Move the numbers up
    # Iterate through the columns
    flag = False
    finBoard = deepcopy(board)
    for col in range(CELL_COUNT):
        # For each column start at the top and move down
        curr = 0
        for row in range(CELL_COUNT):
            if finBoard[row][col]:
                if curr == row:
                    continue

                if finBoard[curr][col] == finBoard[row][col]:
                    # Add the 2 values and increase the score
                    finBoard[row][col] = 0
                    finBoard[curr][col] *= 2
                    score += finBoard[curr][col]
                    curr += 1
                    flag = True
                elif finBoard[curr][col] == 0:
                    finBoard[curr][col] = finBoard[row][col]
                    finBoard[row][col] = 0
                    flag = True
                else:
                    curr += 1
                    if curr != row:
                        finBoard[curr][col] = finBoard[row][col]
                        finBoard[row][col] = 0
                        flag = True

    return finBoard, score, flag

def moveDown(board, score):
    # Move the numbers down
    # Iterate through the columns
    flag = False
    finBoard = deepcopy(board)
    for col in range(CELL_COUNT):
        # For each column start at the down and move top
        curr = CELL_COUNT - 1
        for row in range(CELL_COUNT - 1, -1, -1):
            if finBoard[row][col]:
                if curr == row:
                    continue

                if finBoard[curr][col] == finBoard[row][col]:
                    # Add the 2 values and increase the score
                    finBoard[row][col] = 0
                    finBoard[curr][col] *= 2
                    score += finBoard[curr][col]
                    curr -= 1
                    flag = True
                elif finBoard[curr][col] == 0:
                    finBoard[curr][col] = finBoard[row][col]
                    finBoard[row][col] = 0
                    flag = True
                else:
                    curr -= 1
                    if curr != row:
                        finBoard[curr][col] = finBoard[row][col]
                        finBoard[row][col] = 0
                        flag = True

    return finBoard, score, flag

def moveLeft(board, score):
    # Move the numbers left
    # Iterate through the rows
    flag = False
    finBoard = deepcopy(board)
    for row in range(CELL_COUNT):
        # For each row start at the left and move right
        curr = 0
        for col in range(CELL_COUNT):
            if finBoard[row][col]:
                if curr == col:
                    continue

                if finBoard[row][curr] == finBoard[row][col]:
                    # Add the 2 values and increase the score
                    finBoard[row][col] = 0
                    finBoard[row][curr] *= 2
                    score += finBoard[row][curr]
                    curr += 1
                    flag = True
                elif finBoard[row][curr] == 0:
                    finBoard[row][curr] = finBoard[row][col]
                    finBoard[row][col] = 0
                    flag = True
                else:
                    curr += 1
                    if curr != col:
                        finBoard[row][curr] = finBoard[row][col]
                        finBoard[row][col] = 0
                        flag = True

    return finBoard, score, flag


def moveRight(board, score):
    # Move the numbers right
    # Iterate through the rows
    flag = False
    finBoard = deepcopy(board)
    for row in range(CELL_COUNT):
        # For each row start at the right and move love
        curr = CELL_COUNT - 1
        for col in range(CELL_COUNT - 1, -1, -1):
            if finBoard[row][col]:
                if curr == col:
                    continue

                if finBoard[row][curr] == finBoard[row][col]:
                    # Add the 2 values and increase the score
                    finBoard[row][col] = 0
                    finBoard[row][curr] *= 2
                    score += finBoard[row][curr]
                    curr -= 1
                    flag = True
                elif finBoard[row][curr] == 0:
                    finBoard[row][curr] = finBoard[row][col]
                    finBoard[row][col] = 0
                    flag = True
                else:
                    curr -= 1
                    if curr != col:
                        finBoard[row][curr] = finBoard[row][col]
                        finBoard[row][col] = 0
                        flag = True

    return finBoard, score, flag

# Constants for display
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
BACKGROUND_COLOR = '#BBADA0'
CELL_PADDING = 10

# Constants for game
CELL_COUNT = 4
CELL_SIZE = 100
TEXT_COLOR = '#776E64'
CELL_COLOR = {
    0: '#9E948A',
    2: '#EEE4DA',
    4: '#EDE0C8',
    8: '#F2B179',
    16: '#F59563',
    32: '#F67C5F',
    64: '#F65E3B',
    128: '#EDCF72',
    256: '#EDCC61',
    512: '#EDC850',
    1024: '#EDC53F',
    2048: '#EDC22E'
}

# Initialize the KEY_FUNCTIONS dictionary
KEY_FUNCTIONS = {
    'Up': moveUp,
    'w': moveUp,
    'Down': moveDown,
    's': moveDown,
    'Left': moveLeft,
    'a': moveLeft,
    'Right': moveRight,
    'd': moveRight
}

# Game variables
score = 0
board = [[0] * CELL_COUNT for _ in range(CELL_COUNT)]
grid = []
gameOver = False
scoreLabel = None
root = None

if __name__ == '__main__':
    runGame(True)