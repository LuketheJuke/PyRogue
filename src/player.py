import pygame as pg
import stage
import items
from dice import roll

# Use the same class for player and enemies
class p1():
    def __init__(self, health, weapon, armor, x, y, spritelist):
        self.health = health
        self.health_max = health
        self.weapon = weapon
        self.armor = armor
        self.prev_x = x
        self.x = x
        self.prev_y = y
        self.y = y
        self.location = (x, y)
        self.spritelist = spritelist
        self.frame = 0
        self.alive = 1
        self.cleared = 0
        self.level = 1
        self.base_attack = 0
        self.xp = 0
        self.sight = 8
        self.inventory = [items.empty, items.empty, items.empty, items.empty]

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
        hit_dragon = 0
        next_level = 0
        newpos = gameboard[ny][nx]
        # Change behavior based on what's in the new position
        if newpos == 1:
            self.x = nx
            self.y = ny
            gameboard[self.y][self.x] = '3'
            gameboard[self.prev_y][self.prev_x] = '1'
            stage.draw_floor(win, self.prev_x, self.prev_y, grid)
        elif newpos == 4:
            hit_enemy = 1
        elif newpos == 5:
            next_level = 1
        elif newpos == 6:
            self.weapon = items.long_sword
            self.x = nx
            self.y = ny
            gameboard[self.y][self.x] = '3'
            gameboard[self.prev_y][self.prev_x] = '1'
            stage.draw_floor(win, self.prev_x, self.prev_y, grid)
        elif newpos == 7:
            self.x = nx
            self.y = ny
            gameboard[self.y][self.x] = '3'
            gameboard[self.prev_y][self.prev_x] = '1'
            stage.draw_floor(win, self.prev_x, self.prev_y, grid)
            self.add_item(items.healing_potion)
        elif newpos == 8:
            self.x = nx
            self.y = ny
            gameboard[self.y][self.x] = '3'
            gameboard[self.prev_y][self.prev_x] = '1'
            stage.draw_floor(win, self.prev_x, self.prev_y, grid)
            self.armor = items.leather_armor
        elif newpos == 9:
            hit_dragon = 1
        elif newpos == 10:
            self.x = nx
            self.y = ny
            gameboard[self.y][self.x] = '3'
            gameboard[self.prev_y][self.prev_x] = '1'
            stage.draw_floor(win, self.prev_x, self.prev_y, grid)
            self.weapon = items.battle_axe
        elif newpos == 11:
            self.x = nx
            self.y = ny
            gameboard[self.y][self.x] = '3'
            gameboard[self.prev_y][self.prev_x] = '1'
            stage.draw_floor(win, self.prev_x, self.prev_y, grid)
            self.armor = items.plate_mail
        else:
            pass
        # Return hit enemy and it's position
        return [hit_enemy, hit_dragon, nx, ny, next_level]

    def hit(self, enemy):
        damage = roll(self.weapon.attacknum, self.weapon.attack + self.base_attack)
        enemy.hurt(damage)
        level_up = False
        if enemy.health <= 0:
            self.xp += enemy.xpval
            level_up = self.check_level_up()
        return damage, level_up
    
    def hurt(self, damage):
        damage_reduced = damage - self.armor.defense
        if damage_reduced < 0:
            pass
        else:
            self.health -= damage_reduced
        # print(self.health)
        if self.health <= 0:
            self.alive = 0

    # Clear player from the gameboard
    def clear_player(self, gameboard, win, grid):
        gameboard[self.y][self.x] = '1'
        stage.draw_floor(win, self.x, self.y, grid)
        self.cleared = 1
    
    def check_level_up(self):
        xp_needed = self.level * 10
        if self.xp >= xp_needed:
            level_up = True
            self.level += 1
            self.health += 2*self.level
            self.health_max += 2*self.level
            self.base_attack += 1
            self.xp = self.xp - xp_needed
        else: 
            level_up = False
        return level_up

    def add_item(self, item):
        self.inventory.insert(0, item) 
        self.inventory.pop(4) 

    def use_item(self, num):
        heal = self.inventory[num].use()
        self.health += heal
        if self.health > self.health_max:
            self.health = self.health_max
        self.inventory[num] = items.empty
