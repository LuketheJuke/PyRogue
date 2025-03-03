import pygame as pg
import stage
import items
from dice import roll

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
        damage = roll(1,self.attack)
        enemy.hurt(damage)
        return damage

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

# Modified version of mob class
class dragon():
    def __init__(self, x, y, name, health, attack, xpval, spritelist):
        self.name = name
        self.health = health
        self.attack = attack
        self.xpval = xpval
        self.prev_x = x
        self.x = [x, x-1]
        self.prev_y = y
        self.y = [y, y-1]
        self.location = (x, y) #defined as the top left corner of the dragon
        self.spritelist = spritelist
        self.frame = 0
        self.alive = 1
        self.cleared = 0

    # Only draw on the map if the player is within a certain radius
    def draw(self, win, spritenum, playerx, playery, sight, grid):
        for x in range(0,2):
            for y in range(0,2):
                if (abs(playerx-self.x[x]) + abs(playery-self.y[y])) < sight:
                    sprite = spritenum*4 + y*2 + x*1
                    win.blit(self.spritelist[sprite], (self.x[x]*grid, self.y[y]*grid))
            
        # Used for dragon movement
    def move(self, gameboard, win, player_x, player_y):
        self.prev_x = self.x
        self.prev_y = self.y
        x_diff = self.x[0] - player_x
        y_diff = self.y[0] - player_y
        hit_player = 0
        nx = []
        ny = []
        newpos = []
        move_good = 1

        # move towards the player
        if (abs(x_diff)+abs(y_diff)) < 9:
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

        moveable = (1, 5, 9)
        for x in self.x:
            nx.append(x + cx)
        for y in self.y: 
            ny.append(y + cy)
        for x in nx:
            for y in ny:
                newpos.append(gameboard[y][x])
                if gameboard[y][x] in moveable:
                    move_good == 0
        # print(move_good)

        if 3 in newpos:
            hit_player = 1
            # print("RAR")
        elif 2 in newpos:
            pass
        elif move_good == 1:
            # print("MOVE")
            self.x = nx
            self.y = ny
            for x in range(0,2):
                for y in range(0,2):
                    gameboard[self.y[y]][self.x[x]] = '9'
                    gameboard[self.prev_y[y]-cy][self.prev_x[x]-cx] = '1'
        
        return hit_player

    def hit(self, enemy):
        damage = roll(1,self.attack)
        enemy.hurt(damage)
        return damage

    # Take damage
    def hurt(self, damage):
        self.health -= damage
        if self.health <= 0:
            dragon_killed = 1
            self.alive = 0 # poor guy :(
    
    # Clear mob from the gameboard
    def clear_dragon(self, gameboard, win, grid):
        for x in range(0,2):
            for y in range(0,2):
                gameboard[self.y[y]][self.x[x]] = '1'
                stage.draw_floor(win, self.x[x], self.y[y], grid)
                self.cleared = 1