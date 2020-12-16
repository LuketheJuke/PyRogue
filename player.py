import pygame
import stage

grid = 24

class p1():
    def __init__(self, health, attack, x, y, spritelist):
        self.health = health
        self.attack = attack
        self.prev_x = x
        self.x = x
        self.prev_y = y
        self.y = y
        self.location = (x, y)
        self.spritelist = spritelist
        self.frame = 0

    def draw(self, win):
        if self.frame == 0:
            self.frame = 1
        else:
            self.frame = 0
        win.blit(self.spritelist[self.frame], (self.x*grid, self.y*grid))

    def move(self, cx, cy, gameboard, win):
        self.prev_x = self.x
        self.prev_y = self.y

        nx = self.x + cx
        ny = self.y + cy
        
        newpos = gameboard[ny][nx]
        if newpos == 1:
            self.x = nx
            self.y = ny
            self.draw(win)
            stage.draw_floor(win, self.prev_x, self.prev_y)
        # elif newpos == 4
        #     guy.attack
        else:
            print("It's a wall!")

    # def attack():
        
    def hurt(self, damage):
        self.health -= damage