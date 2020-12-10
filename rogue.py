import pygame
pygame.init()

#set window size
win = pygame.display.set_mode((500, 500))

pygame.display.set_caption("Rogue")

x = 50
y = 50
width = 40
height = 60
vel = 40

# variable to keep loop running 
run = True

# Main loop
while run:
    pygame.time.delay(100)
    
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K.ESCAPE:
                run = False
        if event.type == pygame.QUIT:
            run = False
    
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
        x -= vel
    if keys[pygame.K_RIGHT]:
        x += vel
    if keys[pygame.K_UP]:
        y -= vel
    if keys[pygame.K_DOWN]:
        y += vel
    win.fill((0,0,0))
    
    pygame.draw.rect(win,(255,0,0),(x,y,width,height))
    pygame.display.update()
    
    
pygame.quit()
