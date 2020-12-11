import pygame
import stage
import numpy as np #Use numpy 1.19.3
#import player

np.set_printoptions(threshold=np.inf)

pygame.init()

#set window size
screen_width = 1000
screen_height = 600
win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Rogue")

#width of grid is 10 pixels
grid = 10
xinit = 20
yinit = 20
player_x = 20
player_y = 20

gameboard = np.zeros((screen_width//grid, screen_height//grid))
pygame.draw.rect(win,(255,0,0),(player_x*grid,player_y*grid,grid,grid))

run = True
    
while run:
    
    for event in pygame.event.get():
        # if event.type == KEYDOWN:
            # if event.key == K.ESCAPE:
                # run = False
        if event.type == pygame.QUIT:
            run = False
    
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
        player_x -= 1
        win.fill((0,0,0))
        pygame.draw.rect(win,(255,0,0),(player_x*grid,player_y*grid,grid,grid))
        pygame.time.delay(150); 
    if keys[pygame.K_RIGHT]:
        player_x += 1
        win.fill((0,0,0))
        pygame.draw.rect(win,(255,0,0),(player_x*grid,player_y*grid,grid,grid))
        pygame.time.delay(150); 
    if keys[pygame.K_UP]:
        player_y -= 1
        win.fill((0,0,0))
        pygame.draw.rect(win,(255,0,0),(player_x*grid,player_y*grid,grid,grid))
        pygame.time.delay(150); 
    if keys[pygame.K_DOWN]:
        player_y += 1
        win.fill((0,0,0))
        pygame.draw.rect(win,(255,0,0),(player_x*grid,player_y*grid,grid,grid))
        pygame.time.delay(150); 
    
    stage.generate(win, gameboard, 1, xinit, yinit)
    
    
    pygame.display.update()

print(gameboard)
pygame.quit()
