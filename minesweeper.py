#Minesweepwer and minesweeper bot coded by Giorgio Sawaya

import pygame
import threading
import random

##Global variables and default sizes
##--------------------------------------

#Window
w_length =  1000
w_height = 750

#Grid
columns = 30
rows = 16
block_size = 27
border = 7

grid2D = [[0]*columns for i in range(rows)]

length = columns*block_size
height = rows*block_size
grid_origin_x = (w_length - length) // 2
grid_origin_y = w_height - height - block_size


#Game variables
timer = 0  
lives = 3
total_boxes = rows*columns
mines = 99
flags_left = 99
revealed = total_boxes - mines


##Starting window and main layout
##--------------------------------------

#Setting background
pygame.init()
screen = pygame.display.set_mode((w_length, w_height))
background = pygame.image.load('Images/background.png')

def display_background():
        screen.blit(background, (0, 0))
        screen.blit(title, ((w_length - title.get_width()) // 2, w_height // 70))

#loading images
title = pygame.image.load("Images/title.png")

life = pygame.transform.scale(pygame.image.load("Images/life.png"),(64,64))
flag = pygame.image.load("Images/flagpole.png")
scoreboard =  pygame.transform.scale(pygame.image.load("Images/scoreboard.png"),(160,121))


hidden = pygame.image.load("Images/hidden tile.png")
revealed_bomb =  pygame.image.load("Images/mine reveal.png")

revealed_0 = pygame.image.load("Images/reveal.png")
revealed_1 = pygame.image.load("Images/reveal1.png")
revealed_2 = pygame.image.load("Images/reveal2.png")
revealed_3 = pygame.image.load("Images/reveal3.png")
revealed_4 = pygame.image.load("Images/reveal4.png")
revealed_5 = pygame.image.load("Images/reveal5.png")
revealed_6 = pygame.image.load("Images/reveal6.png")
revealed_7 = pygame.image.load("Images/reveal7.png")
revealed_8 = pygame.image.load("Images/reveal8.png")

revealed_numbers =  [ revealed_0, revealed_1, revealed_2,revealed_3,revealed_4,revealed_5, revealed_6,revealed_7,revealed_8]

#Fixing top bar of window
pygame.display.set_caption('Minesweeper')
mine = pygame.image.load('Images/mine icon.png')
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
        global flags_left
        if not self.is_hidden:
            return False
        self.is_flagged = not self.is_flagged
        if self.is_flagged:
            flags_left -= 1 
        else: 
            flags_left += 1
        
    def draw(self, x, y):
        screen.blit(self.image, (x, y))

        if self.is_flagged:
            screen.blit(flag, (x + 3, y))


for row in range(rows):
    for col in range (columns):
        grid2D[row][col] = Box(row,col)


##Displaying grid and scores,lives,buttons
##--------------------------------------

#displaying main grid
def draw_grid():

    #Drawing border
    pygame.draw.rect(screen, (25, 25, 25), (grid_origin_x-border//2, grid_origin_y-border//2, length+border, height+border), border)

    ##Drawing the taken squares
    threads = []
    n = len(grid2D)
    for row in range(n):
        t = threading.Thread(target = draw_row(grid2D,row))
        t.daemon = True
        threads.append(t)
    
    for i in range(n):
        threads[i].start()

    for i in range(n):
        threads[i].join()

def draw_row(grid2D, row):
     for col in range(len(grid2D[row])):
         grid2D[row][col].draw(grid_origin_x + col*block_size, grid_origin_y + row*block_size)

def display_lives(x, y):
    live_font =  pygame.font.Font('Uniforme (Font).ttf', 38)
    lives_label = live_font.render("Lives Left" , 1, (51, 51, 181))
    screen.blit(lives_label,(x,y))
    for i in range(lives):
        screen.blit(life, (x+i*50, y+50))


def display_flags_left():
    flag_font =  pygame.font.Font('Uniforme (Font).ttf', 60)
    flags_label = flag_font.render(str(flags_left) , 1, (51, 51, 181))
    screen.blit(flags_label,(80,125))
    screen.blit( pygame.transform.scale(flag,(60,60)), (125,120))


def display_timer():
    time_display= str(timer)
    if timer//10 == 0:
        time_display = "00"+ time_display
    elif timer//100 == 0:
        time_display = "0" + time_display

    screen.blit(scoreboard,((w_length - scoreboard.get_width()) // 2, (w_height - scoreboard.get_height())//4+20))
 
    timer_font =  pygame.font.Font('Uniforme (Font).ttf', 90)
    timer_board = timer_font.render(time_display , 1, (163,15,15))
    screen.blit(timer_board,((w_length - scoreboard.get_width()) // 2+15, (w_height - scoreboard.get_height())//4+27))

#Game controls

def opening(x,y):
    not_bombs = find_nearby_boxes(x,y)
    not_bombs.append((x,y))

    #Randomly generate the bombs outside of player's opening. Quadratic probing to deal with mine collisions.
    for i in range(mines):   
        gap = random.randint(0,total_boxes-1)
        counter = 0
        while True:
            gap = (gap+counter*counter)%total_boxes
            if not grid2D[gap//columns][gap%columns].is_mine and not((gap%columns,gap//columns) in not_bombs):
                break
            counter+=1
        grid2D[gap//columns][gap%columns].is_mine = True
    
    for row in range(rows):
        for col in range (columns):
            grid2D[row][col].nearby = get_nearby_mines(col,row)

    click(x,y)

    return 0

def right_click(x,y):
    grid2D[y][x].flag()

def click(x,y):
    global lives, revealed, flags_left
    box = grid2D[y][x]

    if not box.is_hidden:
        return 
    
    if box.is_flagged:
        box.flag()

    elif not box.is_mine:
        box.image = revealed_numbers[box.nearby]
        box.is_hidden = False
        revealed -=1
        if box.nearby == 0:
            available = find_nearby_boxes(x,y)
            for pos in available:
                col,row = pos
                if grid2D[row][col].is_hidden:
                    click(col,row)
    else:
        box.image = revealed_bomb
        box.is_hidden = False
        flags_left -=1 
        lives -= 1

def reveal_around(x,y):
    if grid2D[y][x].is_mine:
        return 

    available = find_nearby_boxes(x,y)
    no_flags = []
    flags_around = 0
    
    for pos in available:
        col,row = pos
        if  grid2D[row][col].is_flagged:
            flags_around += 1

        elif grid2D[row][col].is_hidden :
            no_flags.append(pos)
     
    if grid2D[y][x].nearby == flags_around:   
        for pos in no_flags:
            col,row = pos
            click(col,row)
 
def find_nearby_boxes(x,y):
    surroundings = [(x+1,y),(x+1,y+1),(x+1,y-1),(x,y-1),(x,y+1),(x-1,y-1),(x-1,y),(x-1,y+1)]
    nearby = []
    for pos in surroundings:
        col , row  = pos
        if col >= 0 and col < columns and row >= 0 and row < rows:  
            nearby.append(pos)
    return nearby

def get_nearby_mines(x,y):
    available = find_nearby_boxes(x,y)
    mines_near = 0
    for pos in available:
            col,row = pos
            if grid2D[row][col].is_mine:
                mines_near += 1
    
    return mines_near

##Game over screens
##--------------------------------------

def game_over_win():

    overFont =  pygame.font.Font('Uniforme (Font).ttf', 60)
    finalScoreFont =  pygame.font.Font('Uniforme (Font).ttf', 40)

    gameOver = overFont.render("YOU WON!", 1, (215,215,215))
    finalScore = finalScoreFont.render("Time needed: " + str(timer) + "Lives left: " + str(lives), 1, (215,215,215))
    play_again = finalScoreFont.render("Click anywhere to play again", 1, (215,215,215))
    screen.blit(gameOver,((w_length - gameOver.get_width()) // 2, (w_height - gameOver.get_height())//2))
    screen.blit(finalScore,((w_length - finalScore.get_width()) // 2, (w_height - finalScore.get_height())//2 - 60))
    screen.blit(finalScore,((w_length - finalScore.get_width()) // 2, (w_height - finalScore.get_height())//2 + 70))
    

    pygame.display.update()
   
    choice = False
    while not choice:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                choice = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                load_new_game()
                    
    pygame.quit()
    return False

def game_over_loss():
    overFont =  pygame.font.Font('Uniforme (Font).ttf', 60)
    finalScoreFont =  pygame.font.Font('Uniforme (Font).ttf', 40)
    mistake_font =  pygame.font.Font('Uniforme (Font).ttf', 25)

    gameOver = overFont.render("YOU LOST... Better luck next time!", 1, (215,215,215))
    finalScore = finalScoreFont.render("Click anywhere to play again", 1, (215,215,215))


    for i in range(len(grid2D)):
        for j in range(len(grid2D[0])):
            if grid2D[i][j].is_hidden and grid2D[i][j].is_mine:
                grid2D[i][j].image == revealed_bomb
            elif grid2D[i][j].is_hidden and grid2D[i][j].is_flagged:
                red_x = mistake_font.render("X", 1, (163,15,15))
                screen.blit(red_x,(grid_origin_x + j*27,grid_origin_y + i*27))
    draw_grid()
    screen.blit(gameOver,((w_length - gameOver.get_width()) // 2, (w_height - gameOver.get_height())//2))
    screen.blit(finalScore,((w_length - finalScore.get_width()) // 2, (w_height - finalScore.get_height())//2 - 60))

    pygame.display.update()

    choice = False
    while not choice:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                choice = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
               load_new_game()
                                
    pygame.quit()
    return False

def load_new_game():
    global timer, lives, timeboard, revealed, flags_left, total_boxes 

    timer = 0
    timeboard = "000"
    lives = 3
    flags_left = mines
    revealed = total_boxes-mines

    for row in range(rows):
        for col in range (columns):
            grid2D[row][col] = Box(row,col)

    main()

def pause():
    print("joj")

def button(text, position):
    button_font =  pygame.font.Font('Uniforme (Font).ttf', 40)
    text_render = button_font.render(text, 1, (0, 0, 0))
    x, y = position
    pygame.draw.rect(screen, (200, 200, 200), (x, y, x+30 , y+50))
    return screen.blit(text_render, (x, y))


##Main Function, Let's play
##--------------------------------------

def main():

    global timer, lives, timeboard 
    playing = True
    opened = False
   
    # initializing clock and time
    clock = pygame.time.Clock()
    time = 1

    #making restart and pause button:
    restart_button = button("Restart",(60,60))
    pause_button = button("Pause",(110,60))

    while playing:
  
        ##Keys and moves
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                playing = False

            elif evt.type == pygame.MOUSEBUTTONDOWN:
                
                x, y = pygame.mouse.get_pos()
                x = (x-grid_origin_x)//block_size
                y = (y - grid_origin_y)//block_size
                if x > -1 and x < columns and y > -1 and y < rows:
                  
                    if pygame.mouse.get_pressed()[0]:  
               
                        if opened: 

                            if grid2D[y][x].is_hidden:
                                click(x,y)
                            else:
                                reveal_around(x,y)
                                                              
                        else:
                            opening(x,y)
                            opened = True  

                        if restart_button.collidepoint(x,y):
                            load_new_game()
                        elif pause_button.collidepoint(x,y):
                            pause()            
                      
                    elif pygame.mouse.get_pressed()[2]:
                        right_click(x,y)
                

        ##Speed control
      
        time += clock.get_rawtime()
        clock.tick()

        if 1000/time <= 1 and timer < 999:
                time = 1
                timer +=1
        

        display_background()
        display_lives(w_length*3//4,w_height//10)
        display_timer() 
        display_flags_left()

        if lives < 1:
            game_over_loss()                                  
        if revealed < 1:
            game_over_win()

        
        draw_grid()


          

        pygame.display.update()

    pygame.quit()

main()

