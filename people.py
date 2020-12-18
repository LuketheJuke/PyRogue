import pygame as pg
import stage
from dice import roll

# Use the same class for player and enemies
class p1():
    def __init__(self, health, attack, x, y, spritelist):
        self.health = health
        self.health_max = health
        self.attack = attack
        self.prev_x = x
        self.x = x
        self.prev_y = y
        self.y = y
        self.location = (x, y)
        self.spritelist = spritelist
        self.frame = 0
        self.alive = 1
        self.cleared = 0
        self.xp = 0
        self.sight = 8

    # Draw sprite for the person
    def draw(self, win, spritenum, grid):
        win.blit(self.spritelist[spritenum], (self.x*grid, self.y*grid))

    # Used for movement as the player
    def move_player(self, cx, cy, gameboard, win, grid):
        self.prev_x = self.x
        self.prev_y = self.y
        nx = self.x + cx
        ny = self.y + cy
        hit_enemy = 0
        next_level = 0

        newpos = gameboard[ny][nx]
        if newpos == 1 or newpos == 5:
            self.x = nx
            self.y = ny
            gameboard[self.y][self.x] = '3'
            gameboard[self.prev_y][self.prev_x] = '1'
            stage.draw_floor(win, self.prev_x, self.prev_y, grid)
        elif newpos == 4:
            hit_enemy = 1
        elif newpos == 5:
            next_level = 1
        else:
            pass
        # Return hit enemy and it's position
        return [hit_enemy, nx, ny]

    def hit(self, enemy):
        enemy.hurt(roll(1,self.attack))
        if enemy.health <= 0:
            self.xp += enemy.xpval
    
    def hurt(self, damage):
        self.health -= damage
        # print(self.health)
        if self.health <= 0:
            self.alive = 0

    def get_stats(self):
        return [self.health, self.health_max, self.attack]

    # Clear player from the gameboard
    def clear_player(self, gameboard, win, grid):
        gameboard[self.y][self.x] = '1'
        stage.draw_floor(win, self.x, self.y, grid)
        self.cleared = 1


# Class defining mob behavior
class mob():
    def __init__(self, x, y, name, health, attack, xpval, spritelist):
        self.name = name
        self.health = health
        self.attack = attack
        self.xpval = xpval
        self.prev_x = x
        self.x = x
        self.prev_y = y
        self.y = y
        self.location = (x, y)
        self.spritelist = spritelist
        self.frame = 0
        self.alive = 1
        self.cleared = 0

    # Only draw on the map if the player is within a certain radius
    def draw(self, win, spritenum, playerx, playery, sight, grid):
        if (abs(playerx-self.x) + abs(playery-self.y)) < sight:
            win.blit(self.spritelist[spritenum], (self.x*grid, self.y*grid))
            
        # Used for movement as a mob
    def move_mob(self, gameboard, win, player_x, player_y):
        self.prev_x = self.x
        self.prev_y = self.y
        x_diff = self.x - player_x
        y_diff = self.y - player_y
        hit_player = 0

        # move towards the player
        if (abs(x_diff)+abs(y_diff)) < 7:
            if abs(x_diff) > abs(y_diff):
                cy = 0
                if x_diff > 0:
                    cx = -1
                else:
                    cx = 1
            elif abs(y_diff) > abs(x_diff):
                cx = 0
                if y_diff > 0:
                    cy = -1
                else:
                    cy = 1
            elif x_diff > 0: 
                cx = -1
                cy = 0
            elif y_diff > 0: 
                cx = 0
                cy = -1
            elif x_diff < 0: 
                cx = 1
                cy = 0
            elif y_diff < 0: 
                cx = 0
                cy = 1
            else: 
                cx = 0
                cy = 0
        else:
            cx = 0
            cy = 0

        nx = self.x + cx
        ny = self.y + cy
        newpos = gameboard[ny][nx]

        if newpos == 1 or newpos == 5:
            self.x = nx
            self.y = ny
            gameboard[self.y][self.x] = '4'
            gameboard[self.prev_y][self.prev_x] = '1'
        elif newpos == 3:
            hit_player = 1
        elif newpos == 2:
            pass
        return hit_player

    def hit(self, enemy):
        enemy.hurt(roll(1,self.attack))

    # Take damage
    def hurt(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.alive = 0 # poor guy :(
    
    # Clear mob from the gameboard
    def clear_mob(self, gameboard, win, grid):
        gameboard[self.y][self.x] = '1'
        stage.draw_floor(win, self.x, self.y, grid)
        self.cleared = 1
