# Pygame-Minesweeper

A twist on the classic game of minesweeper! This time you are given **3 lives** so you can power through these minesweeper game and avoid the frustration of a guess at the very end of a game :)

By Giorgio Sawaya, built using pygame.


## How to play Minesweeper

The goal of Minesweeper is to reveal an entire landscape while avoiding hidden mines and in the shortest time possible.

You are given hints from opened boxes that indicate how many landmines are adjacent to that particular box. You need to use these hints to deduce where the mines are located. 

The game ends when all the numbers (none-mines) boxes are opened.  

## Game controls

   Click: When you click on a box, it will reveal what is under it. The first opening click is always a safe box.
    
   Right Click: You can right click on a box to put a flag where you believe a landmine is found.
     
   If you have the good amount of flags around a certain box, you can click that revealed number to reveal all boxes around it instead of clicking all of them individually. This      will help you get a faster time and a better score!  Make sure the flagged boxes are indeed the boxes with the landmines or you will lose lives when you open a landmine.


## How to get the game

This game requires python 3 and pygame which can be installed from here
    1. Install python on your computer: https://www.python.org/downloads/
    2. Install pygame with a single command line depending on you environnement: https://www.pygame.org/wiki/GettingStarted

Once that is done all that is needed is to download this repository from Github (see image) and click the minesweeper shortcut or minesweeper.py file.

![image](https://user-images.githubusercontent.com/55166171/118590273-1a46cd80-b770-11eb-970a-dc9bd3351331.png)
