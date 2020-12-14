import pygame
import stage
import player
import numpy as np

np.set_printoptions(threshold=np.inf)

pygame.init()

#set window size
screen_width = 1000
screen_height = 600
win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Rogue")

#width of grid is 10 pixels
grid = 10
xinit = 10
yinit = 10
player_x = 20
player_y = 20

gameboard = np.zeros((screen_width//grid, screen_height//grid))
guy = player.p1(10, 1, player_x, player_y)
guy.draw(win)

run = True
    
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
        guy.move_left(keys[pygame.K_LEFT], gameboard, win)
        pygame.time.delay(150)
    if keys[pygame.K_RIGHT]:
        guy.move_right(keys[pygame.K_LEFT], gameboard, win)
        pygame.time.delay(150)
    if keys[pygame.K_UP]:
        guy.move_up(keys[pygame.K_LEFT], gameboard, win)
        pygame.time.delay(150)
    if keys[pygame.K_DOWN]:
        guy.move_down(keys[pygame.K_LEFT], gameboard, win)
        pygame.time.delay(150)
    
    stage.generate(win, gameboard, 1, xinit, yinit)
    
    
    pygame.display.update()

pygame.quit()
