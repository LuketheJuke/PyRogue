import pygame
import tileset
from numpy import loadtxt
from random import randint

grid = 24

def get_tiles():
    tiles = tileset.make_tileset("sprites/BitsyDungeonTilesby_enui/DungeonTiles.png")
    return tiles

# gameboard tile definitions
# '0' = empty
# '1' = walkable floor
# '2' = wall or obstacle
# '3' = player
# '4' = enemy
# '5' = start
# '6' = finish
def generate(win, gameboard, level):
    # Load map based on level
    # Read text file, then modify gameboard variable with stage info
    # and write tiles to the screen
    tiles = get_tiles()
    if level == 1:
        f = open("levels/level1.txt", "r")
        xinit = 0
        yinit = 0
        leveldata = []
        line = []
        for y in range(0,(len(gameboard))):
            line = f.readline()
            leveldata.append(line[0:50])
            for x in range(0,len(gameboard[0])):
                if line[x] == '.':
                    gameboard[y][x] = '0'
                    win.blit(tiles[4][4], (x*grid, y*grid))
                elif line[x] == '#':
                    gameboard[y][x] = '1'
                    win.blit(tiles[0][0], (x*grid, y*grid))
                elif line[x] == '=':
                    gameboard[y][x] = '2'
                elif line[x] == 's':
                    gameboard[y][x] = '5'
                    xinit = x
                    yinit = y
                elif line[x] == 'f':
                    gameboard[y][x] = '6'
                    win.blit(tiles[4][3], (x*grid, y*grid))
        draw_walls(win, gameboard)
        return (xinit, yinit)

        # return x_start, y_start

# draw different wall sprites depending on surrounding layout
def draw_walls(win, gameboard):  
    tiles = get_tiles()
    for y in range(1,(len(gameboard)-1)):
        for x in range(1,len(gameboard[0])-1):
            if gameboard[y][x] == 2:
                north = gameboard[y-1][x] 
                south = gameboard[y+1][x] 
                west = gameboard[y][x-1] 
                east = gameboard[y][x+1]

                # Check were walls are (2) and floor is (1), and draw the appropriate wall
                if north == 2 and south == 2:
                    if west == 1:
                        win.blit(tiles[4][1], (x*grid, y*grid))
                    elif east == 1:
                        win.blit(tiles[0][2], (x*grid, y*grid))
                    else:
                        pass
                elif east == 2:
                    if west == 2:
                        if south == 1:
                            win.blit(tiles[3][0], (x*grid, y*grid))
                        elif north == 1:
                            win.blit(pygame.transform.flip(tiles[3][0],0,1), (x*grid, y*grid))
                    elif south == 2:
                        if west == 1 and north == 1:
                            win.blit(tiles[0][1], (x*grid, y*grid))
                        else:
                            win.blit(tiles[1][2], (x*grid, y*grid))
                    elif north == 2:
                        if south == 1 and west == 1:
                            win.blit(tiles[2][1], (x*grid, y*grid))
                        else:
                            win.blit(pygame.transform.flip(tiles[1][2],0,1), (x*grid, y*grid))
                elif west == 2:
                    if south == 2:
                        if east == 1 and north == 1:
                            win.blit(tiles[1][1], (x*grid, y*grid))
                        else:
                            win.blit(tiles[4][2], (x*grid, y*grid))
                    elif north == 2:
                        if south == 1 and east == 1:
                            win.blit(tiles[3][1], (x*grid, y*grid))
                        else:
                            win.blit(pygame.transform.flip(tiles[4][2],0,1), (x*grid, y*grid))

def draw_floor(win, x, y):
    tiles = get_tiles()
    win.blit(tiles[0][0], (x*grid, y*grid))



