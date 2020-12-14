import pygame
from random import randint

grid = 10

# Create rectangles which will have impassable walls at their edges
# x and y define the top left corner of the room
def draw_room(win, gameboard, x, y, width, height):  
    # modify gameboard, then use that info to draw the walls, 
    for i in range(x,x+width):
        #draw top wall
        gameboard[i][y] = '1'
        pygame.draw.rect(win,(230, 230, 230),(i*grid, y*grid, grid, grid))
        #draw bottom wall
        gameboard[i][y+height] = '1'
        pygame.draw.rect(win,(230, 230, 230),(i*grid, (y+height)*grid, grid, grid))
    for i in range(y,y+height+1):
        #draw left wall
        gameboard[x][i] = '1'
        pygame.draw.rect(win,(230, 230, 230),(x*grid, i*grid, grid, grid))
        #draw right wall
        gameboard[x+width][i] = '1'
        pygame.draw.rect(win,(230, 230, 230),((x+width)*grid, i*grid, grid, grid))
        
def generate(win, gameboard, level, xinit, yinit):
    if level == 1:
        # room1 = 
        # room2 = 
        draw_room(win, gameboard, xinit-2, yinit-2, 10, 4)
        draw_room(win, gameboard, 18, 18, 10, 20)
        draw_room(win, gameboard, 40, 40, 15, 10)
        # draw_halls(room1, room2)