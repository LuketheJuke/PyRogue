import pygame as pg
import tcod
# import tileset
from mapgen import gen_level
from numpy import loadtxt
from random import randint

# def get_tiles(file, grid):
#     tiles = tileset.make_tileset(file, grid)
#     return tiles

levellist = ["levels/level1.txt", 
            "levels/level2.txt"]

# gameboard tile definitions
# '0' = empty ('.')
# '1' = walkable floor ('*')
# '2' = wall or obstacle ('=')
# '3' = player('p')
# '4' = enemy ('e'')
# '5' = finish ('f')
# '6' = long sword ('w')
# '7' = potion ('o')
# '8' = leather armor ('a')
# '9' = DRAGON ('d')
# '10' = battle axe ('b')
# '11' = plate mail ('m')
def generate(win, gameboard, height, width, level, grid):
    # Load map based on level
    # Read text file, then modify gameboard variable with stage info
    # and write tiles to the screen
    # tiles = get_tiles("sprites/BitsyDungeonTilesby_enui/DungeonTiles.png", grid)
    if level == 1:
        # map = gen_level(width, height, level)
        f = open("levels/level1.txt", "r")
    elif level == 2:
        f = open("levels/level2.txt", "r")
    elif level == 3:
        f = open("levels/level3.txt", "r")
    xinit = 0
    yinit = 0
    leveldata = []
    line = []
    for y in range(0,(height)):
        # print(y)
        line = f.readline()
        leveldata.append(line[0:width])
        for x in range(0,len(gameboard[0])): 
            print(x)
            if line[x] == '.': 
                gameboard[y][x] = 0
            elif line[x] == '*': 
                gameboard[y][x] = 1
            elif line[x] == '=':
                gameboard[y][x] = 2
            elif line[x] == 'p':
                gameboard[y][x] = 3
                xinit = x
                yinit = y
            elif line[x] == 'e':
                gameboard[y][x] = 4
            elif line[x] == 'f':
                gameboard[y][x] = 5
            elif line[x] == 'w':
                gameboard[y][x] = 6
            elif line[x] == 'o':
                gameboard[y][x] = 7
            elif line[x] == 'a':
                gameboard[y][x] = 8
            elif line[x] == 'd':
                gameboard[y][x] = 9
            elif line[x] == 'b':
                gameboard[y][x] = 10
            elif line[x] == 'm':
                gameboard[y][x] = 11
    # print(gameboard)
    f.close()
    return (xinit, yinit)

        # return x_start, y_start

# draw different wall sprites depending on surrounding layout
def draw_stage(win, gameboard, playerx, playery, sight, grid):  
    # tiles = get_tiles("sprites/BitsyDungeonTilesby_enui/DungeonTiles.png", grid)
    # item_tiles = get_tiles("sprites/BitsyDungeonTilesby_enui/ItemTiles.png", grid)
    wall = 2
    floor = (1, 3, 4, 5, 6, 7, 8, 9, 10, 11) #tile types that are treated as a floor
    # (len(gameboard)-1) # ymax
    # len(gameboard[0])-1 # xmax
    for y in range(playery-sight, playery+sight):
        for x in range(playerx-sight, playerx+sight):
            if y >= len(gameboard) or x >= len(gameboard[0]):
                pass
            elif (abs(playerx-x) + abs(playery-y)) < sight:
                if gameboard[y][x] == 1:
                    win.blit(tiles[0][0], (x*grid, y*grid))
                elif gameboard[y][x] == 5:
                    win.blit(tiles[4][3], (x*grid, y*grid))
                elif gameboard[y][x] == 6:
                    win.blit(item_tiles[1][2], (x*grid, y*grid))
                elif gameboard[y][x] == 7:
                    win.blit(item_tiles[1][0], (x*grid, y*grid))
                elif gameboard[y][x] == 8:
                    win.blit(item_tiles[1][5], (x*grid, y*grid))
                elif gameboard[y][x] == 10:
                    win.blit(item_tiles[0][3], (x*grid, y*grid))
                elif gameboard[y][x] == 11:
                    win.blit(item_tiles[1][6], (x*grid, y*grid))
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

# Used to re-draw the floor after a character moves, should make this smarter
def draw_floor(win, x, y, grid):
    # tiles = get_tiles("sprites/BitsyDungeonTilesby_enui/DungeonTiles.png", grid)
    win.blit(tiles[0][0], (x*grid, y*grid))
