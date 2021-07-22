#@author Siddhant Attavar

from AI import runAI
from Game import runGame

while True:
    gameMode = input('Run AI (Y/N): ')
    if gameMode[0].upper() == 'Y':
        runAI()
        break
    elif gameMode[0].upper() == 'N':
        runGame(True)
        break
    else:
        print('Invalid input. Please enter Y or N.')