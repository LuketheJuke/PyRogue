import pygame
from random import randint

grid = 10

# Create rectangles which will have impassable walls at their edges
# x and y define the top left corner of the room
def draw_room(win, gameboard, x, y, width, height):
    x = x*grid
    y = y*grid
    width = width*grid
    height = height*grid
    # north wall
    pygame.draw.rect(win,(230,230,230),(x,y,width,grid))
    # south wall
    pygame.draw.rect(win,(230,230,230),(x,y+height,width+grid,grid))
    # east wall
    pygame.draw.rect(win,(230,230,230),(x+width,y,grid,height))
    # west wall
    pygame.draw.rect(win,(230,230,230),(x,y,grid,height))
    
    # modify gameboard, then use that info to draw the walls, instead of just drawing rectangles like this
    for i in range(x,width):
        gameboard[x][y] = '1'
        gameboard[x][y+height] = '1'
    # for i in range(x, width):
        
def generate(win, gameboard, level, xinit, yinit):
    if level == 1:
        # room1 = 
        # room2 = 
        draw_room(win, gameboard, xinit-2, yinit-2, 10, 4)
        draw_room(win, gameboard, 20, 40, 10, 20)
        # draw_halls(room1, room2)