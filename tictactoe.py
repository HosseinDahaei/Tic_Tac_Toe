import pygame as pg,sys
from pygame.locals import *
import time
import random

#initialize global variables
XO = 'x'
winner = None
draw = False
width = 800
height = 800
white = (255, 255, 255)
line_color = (10,10,10)

#TicTacToe 3x3 board
game_board = [[None]*3,[None]*3,[None]*3]

#initializing pygame window
pg.init()
fps = 30
CLOCK = pg.time.Clock()
screen = pg.display.set_mode((width, height+100),0,32)
pg.display.set_caption("Tic Tac Toe")

#loading the images
opening = pg.image.load('tic tac opening.png')
x_img = pg.image.load('X.png')
o_img = pg.image.load('O.png')

#resizing images
x_img = pg.transform.scale(x_img, (160,160))
o_img = pg.transform.scale(o_img, (160,160))
opening = pg.transform.scale(opening, (width, height+100))


def game_opening():
    screen.blit(opening,(0,0))
    pg.display.update()
    time.sleep(1)
    screen.fill(white)
    
    # Drawing vertical lines
    pg.draw.line(screen,line_color,(width/3,0),(width/3, height),7)
    pg.draw.line(screen,line_color,(width/3*2,0),(width/3*2, height),7)
    # Drawing horizontal lines
    pg.draw.line(screen,line_color,(0,height/3),(width, height/3),7)
    pg.draw.line(screen,line_color,(0,height/3*2),(width, height/3*2),7)
    draw_status()
    

def draw_status():
    global draw

    if winner is None:
        message = XO.upper() + "'s Turn"
    else:
        message = winner.upper() + " won!"
    if draw:
        message = 'Game Draw!'

    font = pg.font.Font(None, 50)
    text = font.render(message, 1, (200, 0, 0))

    # copy the rendered message onto the board
    screen.fill ((0, 0, 0), (0, 800, 900, 200))
    text_rect = text.get_rect(center=(width/2, 850))
    screen.blit(text, text_rect)
    pg.display.update()

def check_win():
    global game_board, winner,draw
    padding = 25
    win_line_color = (3, 155, 229)
    # check for winning rows
    for row in range (0,3):
        if ((game_board [row][0] == game_board[row][1] == game_board[row][2]) and(game_board [row][0] is not None)):
            # this row won
            winner = game_board[row][0]
            pg.draw.line(screen, win_line_color, (0+padding, (row + 1)*height/3 -height/6),\
                              (width-padding, (row + 1)*height/3 - height/6 ), 12)
            break

    # check for winning columns
    for col in range (0, 3):
        if (game_board[0][col] == game_board[1][col] == game_board[2][col]) and (game_board[0][col] is not None):
            # this column won
            winner = game_board[0][col]
            #draw winning line
            pg.draw.line (screen, win_line_color,((col + 1)* width/3 - width/6, 0+padding),\
                          ((col + 1)* width/3 - width/6, height-padding), 12)
            break

    # check for diagonal winners
    if (game_board[0][0] == game_board[1][1] == game_board[2][2]) and (game_board[0][0] is not None):
        # game won diagonally left to right
        winner = game_board[0][0]
        pg.draw.line (screen, win_line_color, (50, 50), (700, 700), 12)
       

    if (game_board[0][2] == game_board[1][1] == game_board[2][0]) and (game_board[0][2] is not None):
        # game won diagonally right to left
        winner = game_board[0][2]
        pg.draw.line (screen, win_line_color, (700, 50), (50, 700), 12)
    
    if(all([all(row) for row in game_board]) and winner is None ):
        draw = True
    draw_status()


def drawXO(row,col):
    global game_board,XO
    if row==1:
        posx = 30
    if row==2:
        posx = width/3 + 30
    if row==3:
        posx = width/3*2 + 30

    if col==1:
        posy = 30
    if col==2:
        posy = height/3 + 30
    if col==3:
        posy = height/3*2 + 30
    game_board[row-1][col-1] = XO
    if(XO == 'x'):
        screen.blit(x_img,(posy,posx))
        XO= 'o'
    else:
        screen.blit(o_img,(posy,posx))
        XO= 'x'
    pg.display.update()
    #print(posx,posy)
    #print(game_board)
   
    
def play_computer():
    options = [(i+1,j+1) for i in range(3) for j in range(3) if game_board[i][j] is None]
    selected = random.choice(options)
    # print(selected)
    drawXO(*selected)
    check_win()


def userClick():
    #get coordinates of mouse click
    x,y = pg.mouse.get_pos()

    #get column of mouse click (1-3)
    if(x<width/3):
        col = 1
    elif (x<width/3*2):
        col = 2
    elif(x<width):
        col = 3
    else:
        col = None
        
    #get row of mouse click (1-3)
    if(y<height/3):
        row = 1
    elif (y<height/3*2):
        row = 2
    elif(y<height):
        row = 3
    else:
        row = None
    #print(row,col)
    

    if(row and col and game_board[row-1][col-1] is None):
        global XO
        
        #draw the x or o on screen
        drawXO(row,col)
        check_win()
        
        

def reset_game():
    global game_board, winner,XO, draw
    time.sleep(5)
    XO = 'x'
    draw = False
    game_opening()
    winner=None
    game_board = [[None]*3,[None]*3,[None]*3]
    

game_opening()

# run the game loop forever
while(True):
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            # the user clicked; place an X or O
            userClick()
            if(winner or draw):
                reset_game()
    if(XO == 'o'):
        play_computer()
        if(winner or draw):
            reset_game()       
    pg.display.update()
    CLOCK.tick(fps)
