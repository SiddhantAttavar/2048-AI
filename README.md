# 2048 AI
This is a algorithm, written in Python, which plays the game [2048](https://en.wikipedia.org/wiki/2048_(video_game)). It reaches an average score of 8,000 and high score of 15,000.

![Image](/screenshot.png)

The algorithm is based on the [minimax](https://en.wikipedia.org/wiki/Minimax) algorithm. At each move, the algorithm looks into all possible moves, to a certain depth, and chooses the one with the best score. There is an element of randomness in the game, about where the 2s and 4s will appear on the board, so the algorithm take the average of scores for each possible position of the new tile.

The score of each move is determined by a heuristic function. This function returns a score for a given game board which is based on common strategies for the game like:
 - Increasing the score
 - Placing higher value tiles in a single corner
 - Sorting tiles in increasing order so that it will be easy to merge them
 - Keeping higher numbers of empty tiles

## Prerequisites <a name = "prerequisites"></a>
 - Python 3+
 - Tkinter

## How to run <a name = "how_to_run"></a>
To run the 2048 algorithm on your system, follow these steps:
 - Clone the repository
 - Open the folder on the terminal / command line
 - Run the following command:
```python3 main.py```