#Minesweepwer and minesweeper bot coded by Giorgio Sawaya

import pygame
from pygame import mixer
import random

##Global variables and default sizes
##--------------------------------------

#Window
wLength =  1000
wHeight = 750

#Grid
columns = 30
rows = 16
block_size = 27
border = 7

grid2D = [[0]*columns for i in range(rows)]

length = columns*block_size
height = rows*block_size
gridOriginX = (wLength - length) // 2
gridOriginY = wHeight - height - block_size


#Game variables
timer = 0  
lives = 3


##Starting window and main layout
##--------------------------------------

#Setting background
pygame.init()
screen = pygame.display.set_mode((wLength, wHeight))
background = pygame.image.load('Background.png')

def display_background():
        screen.blit(background, (0, 0))
        screen.blit(title, ((wLength - title.get_width()) // 2, wHeight // 70))

#initializing sounds
zoneSound = mixer.Sound("Zone.wav")
tetrisSound = mixer.Sound("Tetris!.wav")

#loading images
title = pygame.image.load('Title.png')
hidden = pygame.image.load("hidden tile.png")
revealed_number =  pygame.image.load("reveal.png")
revealed_bomb =  pygame.image.load("mine reveal.png")
life = pygame.transform.scale(pygame.image.load("life.png"),(64,64))
flag = pygame.image.load("flagpole.png")

#Fixing top bar of window
pygame.display.set_caption('Minesweeper')
mine = pygame.image.load('mine icon.png')
pygame.display.set_icon(mine)


##Creating Box class and initializing grid
##--------------------------------------

class Box(object):
    def __init__(self, posX, posY):
        self.posX = posX
        self.posY = posY
        self.is_hidden = True
        self.is_flagged = False
        self.image = hidden
        self.is_mine = False
        self.nearby  = 0
    
    def flag(self):
        if not self.is_hidden:
            return False
        self.is_flagged = not self.is_flagged

    def draw(self, posX, posY):
        screen.blit(self.image, (posX, posY))
        if self.is_flagged:
            screen.blit(flag, (posX + 3, posY))


for row in range(rows):
    for col in range (columns):
        grid2D[row][col] = Box(row,col)
      
 
##Displaying grid and scores,lives,buttons
##--------------------------------------

#displaying main grid
def draw_grid(grid2D):

    #Drawing border
    pygame.draw.rect(screen, (163, 15, 15), (gridOriginX-border//2, gridOriginY-border//2, length+border, height+border), border)

    ##Drawing the taken squares
    for row in range(len(grid2D)):
        for col in range(len(grid2D[row])):
            grid2D[row][col].draw(gridOriginX + col*block_size, gridOriginY + row*block_size)
         
    for horizontalLine in range(rows+1):
        pygame.draw.line(screen, (215,215,215), (gridOriginX, gridOriginY+ horizontalLine*block_size), (gridOriginX + length, gridOriginY + horizontalLine * block_size))
        for verticalLine in range(columns+1):
            pygame.draw.line(screen, (215,215,215), (gridOriginX + verticalLine * block_size, gridOriginY), (gridOriginX + verticalLine * block_size, gridOriginY + height))


def display_lives(x, y):
    for i in range(lives):
        screen.blit(life, (x+i*50, y))

def display_timer():
    time_display= str(timer)
    if timer//10 == 0:
        time_display = "00"+ time_display
    elif timer//100 == 0:
        time_display = "0" + time_display
 
    timer_font =  pygame.font.Font('Uniforme (Font).ttf', 90)
    timer_board = timer_font.render(time_display , 1, (215,215,215))
    screen.blit(timer_board,((wLength - timer_board.get_width()) // 2, (wHeight - timer_board.get_height())//4))

#Game controls

def opening(x,y):
    return 0

def right_click(x,y):
    return 0

def click(x,y):
    print("test")


 

##Calculating Zones, changing score and adjusting blocks above
##--------------------------------------



def game_over():
    
    global timeboard, timer,  lives 
    overFont =  pygame.font.Font('Uniforme (Font).ttf', 40)
    finalScoreFont =  pygame.font.Font('Uniforme (Font).ttf', 20)

    gameOver = overFont.render("Game Over, press space to play again", 1, (215,215,215))
    finalScore = finalScoreFont.render("Time to complete: " + str(timer) + "Lives left: " + str(lives), 1, (215,215,215))
    screen.blit(gameOver,((wLength - gameOver.get_width()) // 2, (wHeight - gameOver.get_height())//2))
    screen.blit(finalScore,((wLength - finalScore.get_width()) // 2, (wHeight - finalScore.get_height())//2 - 60))

    pygame.display.update()
   

    choice = False
    while not choice:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                choice = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    timer = 0
                    timeboard = "000"
                    lives = 3

                    grid2D = [[-1 for x in range(columns)] for x in range(rows)]
                    print("Starting new game")
                    main()
                    
    pygame.quit()
    return False


##Main Function, Let's play
##--------------------------------------

def main():

    global timer, lives, timeboard 
    playing = True

    # initializing clock and time
    clock = pygame.time.Clock()
    time = 1

    while playing:

        # ##Keys and moves
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                playing = False

            elif evt.type == pygame.MOUSEBUTTONDOWN:
          
                x, y = pygame.mouse.get_pos()
                x = (x-gridOriginX)//block_size

                print(str(x) + " " +str(y))

                if pygame.mouse.get_pressed()[0]:
              
                     game_over()
                if pygame.mouse.get_pressed()[2]:
                    print("right click")
                # if bot.collidepoint(x, y):
                #     pygame.quit()
                # elif b2.collidepoint(x, y):
                #     start()

        # ##Speed control
        time += clock.get_rawtime()
        clock.tick()

        if 1000/time <= 1 and timer < 1000:
                time = 1
                timer +=1
     

        display_background()
        display_lives(wLength*3//4,wHeight//10)
        display_timer()
        draw_grid(grid2D)


        pygame.display.update()

    pygame.quit()

main()
