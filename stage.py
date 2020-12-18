import pygame as pg
import tileset
from numpy import loadtxt
from random import randint

def get_tiles():
    tiles = tileset.make_tileset("sprites/BitsyDungeonTilesby_enui/DungeonTiles.png")
    return tiles

# gameboard tile definitions
# '0' = empty ('.')
# '1' = walkable floor ('#')
# '2' = wall or obstacle ('=')
# '3' = player('p')
# '4' = enemy ('e'')
# '5' = finish ('f')
def generate(win, gameboard, height, grid_w, level):
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
        for y in range(0,(height)):
            # print(y)
            line = f.readline()
            leveldata.append(line[0:grid_w])
            for x in range(0,len(gameboard[0])): 
                # print(x)
                if line[x] == '.': 
                    gameboard[y][x] = '0'
                elif line[x] == '*': 
                    gameboard[y][x] = '1'
                elif line[x] == '=':
                    gameboard[y][x] = '2'
                elif line[x] == 'p':
                    gameboard[y][x] = '3'
                    xinit = x
                    yinit = y
                elif line[x] == 'e':
                    gameboard[y][x] = '4'
                elif line[x] == 'f':
                    gameboard[y][x] = '5'
        return (xinit, yinit)

        # return x_start, y_start

# draw different wall sprites depending on surrounding layout
def draw_stage(win, gameboard, playerx, playery, sight, grid):  
    tiles = get_tiles()
    wall = 2
    floor = (1, 3, 4, 5)
    # (len(gameboard)-1) # ymax
    # len(gameboard[0])-1 # xmax
    for y in range(playery-sight, playery+sight):
        for x in range(playerx-sight, playerx+sight):
            if (abs(playerx-x) + abs(playery-y)) < sight:
                if gameboard[y][x] == 1:
                    win.blit(tiles[0][0], (x*grid, y*grid))
                elif gameboard[y][x] == 5:
                    win.blit(tiles[4][3], (x*grid, y*grid))
                elif gameboard[y][x] == 2:
                    north = gameboard[y-1][x] 
                    south = gameboard[y+1][x] 
                    west = gameboard[y][x-1] 
                    east = gameboard[y][x+1]

                    # Check were walls are (2) and floor is (1), and draw the appropriate wall
                    if north == wall and south == wall:
                        if west in floor:
                            win.blit(tiles[4][1], (x*grid, y*grid))
                        elif east in floor:
                            win.blit(tiles[0][2], (x*grid, y*grid))
                        else:
                            pass
                    elif east == wall:
                        if west == wall:
                            if south in floor:
                                win.blit(tiles[3][0], (x*grid, y*grid))
                            elif north in floor:
                                win.blit(pg.transform.flip(tiles[3][0],0,1), (x*grid, y*grid))
                        elif south == wall:
                            if west in floor and north in floor:
                                win.blit(tiles[0][1], (x*grid, y*grid))
                            else:
                                win.blit(tiles[1][2], (x*grid, y*grid))
                        elif north == wall:
                            if south in floor and west in floor:
                                win.blit(tiles[2][1], (x*grid, y*grid))
                            else:
                                win.blit(pg.transform.flip(tiles[1][2],0,1), (x*grid, y*grid))
                    elif west == wall:
                        if south == wall:
                            if east in floor and north in floor:
                                win.blit(tiles[1][1], (x*grid, y*grid))
                            else:
                                win.blit(tiles[4][2], (x*grid, y*grid))
                        elif north == wall:
                            if south in floor:
                                win.blit(tiles[3][1], (x*grid, y*grid))
                            else:
                                win.blit(pg.transform.flip(tiles[4][2],0,1), (x*grid, y*grid))

def draw_floor(win, x, y, grid):
    tiles = get_tiles()
    win.blit(tiles[0][0], (x*grid, y*grid))
