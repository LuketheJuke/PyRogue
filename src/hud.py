import pygame as pg
from render import print_to_HUD

class hud():
    def __init__(self, stage_w, stage_h):
        self.stage_w = stage_w
        self.stage_h = stage_h
        self.promptlist = []
        self.new_prompt = 0
        # Height of the hud in "blocks"
        self.hud_size = 8

    def update(self, grid, window, player):
        font_size = grid*(3/4)
        # Update player info
        self.update_player(grid, window, player)
        # Display all prompts
        for i in range(0,len(self.promptlist)):
            print_to_HUD(grid, font_size, window, self.promptlist[i], (self.stage_w/4)*2, 33+i)

    def update_player(self, grid, window, player):
        font_size = grid
        # Display level # to HUD
        print_to_HUD(grid, font_size, window, "Player Level: " + str(player.level), 2, 33)
        # Display health
        print_to_HUD(grid, font_size, window, "Health: " + str(player.health) + "/" + str(player.health_max), 2, 34)
        # Display weapon and attack value
        print_to_HUD(grid, font_size, window, "Weapon: " + player.weapon.name, 2, 36)
        print_to_HUD(grid, font_size, window, "Attack: " + str(player.weapon.attack), 2, 37)
        # Display armor and defense
        print_to_HUD(grid, font_size, window, "Armor: " + player.armor.name, 2, 38)
        print_to_HUD(grid, font_size, window, "Defense: " + str(player.armor.defense), 2, 39)
        # Display Inventory
        print_to_HUD(grid, font_size, window, "Inventory: ", (self.stage_w/4)*1, 33)
        print_to_HUD(grid, font_size, window, "1: " + player.inventory[0].name, (self.stage_w/4)*1, 34)
        print_to_HUD(grid, font_size, window, "2: " + player.inventory[1].name, (self.stage_w/4)*1, 35)
        print_to_HUD(grid, font_size, window, "3: " + player.inventory[2].name, (self.stage_w/4)*1, 36)
        print_to_HUD(grid, font_size, window, "4: " + player.inventory[3].name, (self.stage_w/4)*1, 37)
    
    # Print something to the prompt queue for the player
    def to_prompt(self, prompt):
        self.promptlist.insert(0,prompt)
        if len(self.promptlist) == 7:
            self.promptlist.pop(6)