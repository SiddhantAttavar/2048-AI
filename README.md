# 2048 AI
This is a algorithm, written in Python, which plays the game [2048](https://en.wikipedia.org/wiki/2048_(video_game)). It reaches the 2048 tile about 60% of the time and 1024 tile nearly 100% of the time.

![Image](/screenshot.png)

The algorithm is based on the [Monte Carlo Tree Search](https://en.wikipedia.org/wiki/Monte_Carlo_tree_search) algorithm. At each move, the algorithm performs a number of simulations, each of which is a random game of 2048. The algorithm then selects the move that has the best score.

## Prerequisites <a name = "prerequisites"></a>
 - Python 3+
 - Tkinter

## How to run <a name = "how_to_run"></a>
To run the 2048 algorithm on your system, follow these steps:
 - Clone the repository
 - Open the folder on the terminal / command line
 - Run the following command:
```python3 main.py```