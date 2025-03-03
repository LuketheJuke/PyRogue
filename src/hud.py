import pygame as pg
from render import print_to_HUD
import tcod

class hud():
    def __init__(self, grid, grid_w, grid_h, window):
        self.grid = grid
        self.grid_w = grid_w
        self.grid_h = grid_h
        screen_width = grid * grid_w
        screen_height = grid * grid_h
        self.window = window
        # Define top left corner
        self.x = 0*grid
        self.y = 32*grid
        # HUD should be drawn at the bottom of the screen, size based on screen size
        self.width = screen_width - self.x
        self.height = screen_height - self.y
        self.gameheight = (screen_height - self.height)//grid
        self.promptlist = []
        self.new_prompt = 0

    def update(self, player):
        hud_rect = (self.x, self.y, self.width, self.height)
        pg.draw.rect(self.window, (0,0,0), hud_rect)
        # Update player info
        self.update_player(player)
        # Display any prompts that were added to the list
        for i in range(0,len(self.promptlist)):
            print_to_HUD(self.promptlist[i], (self.grid_w/4)*2, 33+i)

    def update_player(self, player):
        # Display level # to HUD
        print_to_HUD("player Level: " + str(player.level), 2, 33)
        print_to_HUD("player Level: " + str(player.level), 2, 33)
        # Display health
        print_to_HUD("Health: " + str(player.health) + "/" + str(player.health_max), 2, 34)
        # Display weapon and attack value
        print_to_HUD("Weapon: " + player.weapon.name, 2, 36)
        print_to_HUD("Attack: " + str(player.weapon.attack), 2, 37)
        # Display armor and defense
        print_to_HUD("Armor: " + player.armor.name, 2, 38)
        print_to_HUD("Defense: " + str(player.armor.defense), 2, 39)
        # Display Inventory
        print_to_HUD("Inventory: ", (self.grid_w/4)*1, 33)
        print_to_HUD("1: " + player.inventory[0].name, (self.grid_w/4)*1, 34)
        print_to_HUD("2: " + player.inventory[1].name, (self.grid_w/4)*1, 35)
        print_to_HUD("3: " + player.inventory[2].name, (self.grid_w/4)*1, 36)
        print_to_HUD("4: " + player.inventory[3].name, (self.grid_w/4)*1, 37)

    def print_to_HUD(self, text, x, y):
        text_surf, rect = self.FONT.render(text, (255, 255, 255))
        self.window.blit(text_surf, (x*self.grid, y*self.grid))
    
    # Print something to the prompt queue for the player
    def to_prompt(self, prompt):
        self.promptlist.insert(0,prompt)
        if len(self.promptlist) == 7:
            self.promptlist.pop(6)