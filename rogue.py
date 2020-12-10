import pygame
pygame.init()

#set window size
win = pygame.display.set_mode((500, 500))

pygame.display.set_caption("Rogue")

x = 50
y = 50
width = 10
height = 10
vel = 10

# variable to keep loop running 
run = True

# Main loop
while run:
    
    for event in pygame.event.get():
        # if event.type == KEYDOWN:
            # if event.key == K.ESCAPE:
                # run = False
        if event.type == pygame.QUIT:
            run = False
    
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
        x -= vel
        win.fill((0,0,0))
        pygame.draw.rect(win,(255,0,0),(x,y,width,height))
        pygame.time.delay(150); 
    if keys[pygame.K_RIGHT]:
        x += vel
        win.fill((0,0,0))
        pygame.draw.rect(win,(255,0,0),(x,y,width,height))
        pygame.time.delay(150); 
    if keys[pygame.K_UP]:
        y -= vel
        win.fill((0,0,0))
        pygame.draw.rect(win,(255,0,0),(x,y,width,height))
        pygame.time.delay(150); 
    if keys[pygame.K_DOWN]:
        y += vel
        win.fill((0,0,0))
        pygame.draw.rect(win,(255,0,0),(x,y,width,height))
        pygame.time.delay(150); 
    
    
    
    
    pygame.display.update()
    
    
pygame.quit()
