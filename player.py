import pygame
grid = 10

class p1():
    def __init__(self, health, attack, x, y):
        self.health = health
        self.attack = attack
        self.x = x
        self.y = y
        self.location = (x, y)

    def draw(self, win):
        win.fill((0,0,0))
        pygame.draw.rect(win,(255,0,0),(self.x*grid, self.y*grid, grid, grid))

    def move_left(self, input, gameboard, win):
        if gameboard[self.x-1][self.y]:
            print("It's a wall!")
        else:
            self.x -= 1
            self.draw(win)
    
    def move_right(self, input, gameboard, win):
        if gameboard[self.x+1][self.y]:
            print("It's a wall!")
        else:
            self.x += 1 
            self.draw(win)

    def move_up(self, input, gameboard, win):
        if gameboard[self.x][self.y-1]:
            print("It's a wall!")
        else:
            self.y -= 1
            self.draw(win)

    def move_down(self, input, gameboard, win):
        if gameboard[self.x][self.y+1]:
            print("It's a wall!")
        else:
            self.y += 1
            self.draw(win)

    # def attack():
        
    def hurt(self, damage):
        self.health -= damage