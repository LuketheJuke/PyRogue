import pygame
import stage
import player
import tileset
import numpy as np

np.set_printoptions(threshold=np.inf)
pygame.init()

# set window size and label
screen_width = 1200
screen_height = 960
win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Rogue")
win.fill((0,0,0))

# width of grid is 24 pixels
grid = 24

# initialize gameboard array - defines each location in the grid
gameboard = np.zeros((screen_height//grid, screen_width//grid))

# import GRAPHICS
stage.get_tiles
people = tileset.make_tileset("sprites/BitsyDungeonTilesby_enui/MonsterTiles.png")

# Generate and draw the stage
(xinit, yinit) = stage.generate(win, gameboard, 1)

# Define initial player location and draw
guy = player.p1(10, 1, xinit, yinit, [people[0][0], people[1][0]])
guy.draw(win)

run = True

#### NEED TO IMPROVE THIS LOOP TO BE ABLE TO PROCESS INPUTS, ANIMATION, STAGE GENERATION, ETC ALL AT ONCE ###
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
        guy.move(-1,0, gameboard, win)
        pygame.time.delay(125)
    if keys[pygame.K_RIGHT]:
        guy.move(1,0, gameboard, win)
        pygame.time.delay(125)
    if keys[pygame.K_UP]:
        guy.move(0,-1, gameboard, win)
        pygame.time.delay(125)
    if keys[pygame.K_DOWN]:
        guy.move(0,1, gameboard, win)
        pygame.time.delay(125)

    pygame.display.update()

pygame.quit()
