import pygame as pg
import tcod

class hud():
    def __init__(self, player, window, screen_width, screen_height, grid, grid_w, grid_h):
        self.player = player
        self.win = window
        # Define top left corner
        self.x = 0*grid
        self.y = 32*grid
        # HUD should be drawn at the bottom of the screen, size based on screen size
        self.width = screen_width - self.x
        self.height = screen_height - self.y
        self.gameheight = (screen_height - self.height)//grid
        self.FONT = pg.freetype.Font("text/manaspc.ttf", grid)
        self.prompt = " "
        self.promptlist = []
        self.new_prompt = 0

    def update(self, guy):
        hud_rect = (self.x, self.y, self.width, self.height)
        pg.draw.rect(self.win, (0,0,0), hud_rect)
        # Display level # to HUD
        self.print_to_HUD("player Level: " + str(self.player.level), 2, 33)
        self.print_to_HUD("player Level: " + str(self.player.level), 2, 33)
        # Display health
        self.print_to_HUD("Health: " + str(self.player.health) + "/" + str(self.player.health_max), 2, 34)
        # Display weapon and attack value
        self.print_to_HUD("Weapon: " + self.player.weapon.name, 2, 36)
        self.print_to_HUD("Attack: " + str(self.player.weapon.attack), 2, 37)
        # Display armor and defense
        self.print_to_HUD("Armor: " + self.player.armor.name, 2, 38)
        self.print_to_HUD("Defense: " + str(self.player.armor.defense), 2, 39)
        # Display Inventory
        self.print_to_HUD("Inventory: ", (grid_w/4)*1, 33)
        self.print_to_HUD("1: " + self.player.inventory[0].name, (grid_w/4)*1, 34)
        self.print_to_HUD("2: " + self.player.inventory[1].name, (grid_w/4)*1, 35)
        self.print_to_HUD("3: " + self.player.inventory[2].name, (grid_w/4)*1, 36)
        self.print_to_HUD("4: " + self.player.inventory[3].name, (grid_w/4)*1, 37)
        #Check whether prompt has changed
        # Display Info to the self.player
        for i in range(0,len(self.promptlist)):
            self.print_to_HUD(self.promptlist[i], (grid_w/4)*2, 33+i)

    def print_to_HUD(self, text, x, y):
        text_surf, rect = self.FONT.render(text, (255, 255, 255))
        self.win.blit(text_surf, (x*grid, y*grid))
    
    # Print something to the prompt queue for the player
    def to_prompt(self, text):
        self.prompt = text
        if len(self.promptlist) == 0:
            self.promptlist.insert(0,self.prompt)
        else:
            self.promptlist.insert(0,self.prompt)
            if len(self.promptlist) == 7:
                self.promptlist.pop(6)