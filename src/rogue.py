import pygame as pg
import numpy as np
import tileset
import mapgen
import render
import mob
import player
import items
from hud import hud

np.set_printoptions(threshold=np.inf)

# Define window size. This should be more dynamic in the future. Also, hud size
# and gamemap size shouldn't be correlated at all. 
grid_w = 60
grid_h = 40

# Main game class
class Rogue:
    def __init__(self):
        # Initialize variables
        self.grid_w = 60
        self.grid_h = 40
        self.grid = self.setup_screen()
        self.screen_width = self.grid * grid_w
        self.screen_height = self.grid * grid_h
        # Setup screen
        self.win = pg.display.set_mode((self.screen_width, self.screen_height))
        self.win.fill((0,0,0))
        # create clock variable and key repeat rate
        self.clock = pg.time.Clock()
        self.frame = 0
        self.playing = True
        # define starting level
        self.level = 1
        # import GRAPHICS
        render.setup(self.grid)
        self.spritenum = 0

    def setup_screen(self):
        # Return info for the PC screen
        ScreenInfo = pg.display.Info()
        # Set the size of the map's grid based on current screen size
        if ScreenInfo.current_h//grid_h >= 24 and ScreenInfo.current_w//grid_w >= 24:
            grid = 24
        elif ScreenInfo.current_h//grid_h >= 16 and ScreenInfo.current_w//grid_w >= 16:
            grid = 16
        else:
            grid = 8
        # print("Grid value = " + str(grid))
        return grid

    def Start(self):
        self.game_end = 0
        # Setup HUD
        self.hud = hud(self.grid_w, self.grid_h)
        self.hud.to_prompt("Number keys to use items")
        self.hud.to_prompt("Arrow keys to move/attack")
        self.hud.to_prompt("Good luck!")
        # Convert hud_size to "real" value based on grid size
        self.map_height = self.grid_h - self.hud.hud_size
        print("Screen size: " + str(self.map_height))
        self.level = 1
        self.stage_gen()
        self.player_gen(1)
        self.mob_gen()

    def next_stage(self):
        # self.win.fill((0,0,0))
        self.stage_gen()
        self.player_gen(0)
        self.mob_gen()
        self.hud.to_prompt("Welcome to level " + str(self.level))

    def stage_gen(self):
        # import GRAPHICS
        # Generate and draw the map based on level
        # Check that the width and height are correct
        [self.map, self.xinit, self.yinit] = mapgen.gen_level(self.grid_w, self.map_height, self.level)

    def player_gen(self, init):
        if init == 1: 
            # First time player generation
            self.guy = player.p1(15, items.dagger, items.shirt, self.xinit, self.yinit)
        else:
            # Generate player at start of new map
            self.guy.x = self.xinit
            self.guy.y = self.yinit 

    # Generate mobs
    def mob_gen(self):
        self.mobs = []
        self.dragon_spawn = 0
        for y in range(0,(len(self.map))):
            for x in range(0,len(self.map[0])):
                if self.map.enemy[y][x]:
                    enemynum = np.random.randint(0, 4) # 5 different enemy types, make this smarter sometime later
                    self.mobs.append(mob.mob(x, y, enemynum))
                if self.map.dragon[y][x]:
                    self.dragon = mob.dragon(x, y)
                    self.dragon_spawn = 1

    # Handle inputs and modify game objects
    def events(self):
        num_keys = [pg.K_1, pg.K_2, pg.K_3, pg.K_4]
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
            elif event.type == pg.KEYDOWN:
                # On directional inputs
                if event.key == pg.K_LEFT:
                    self.player_turn(-1, 0)
                elif event.key == pg.K_RIGHT:
                    self.player_turn(1, 0)
                elif event.key == pg.K_UP:
                    self.player_turn(0, -1)
                elif event.key == pg.K_DOWN:
                    self.player_turn(0, 1)
                elif event.key in num_keys:
                    if event.key == pg.K_1:
                        self.guy.use_item(0)
                    elif event.key == pg.K_2:
                        self.guy.use_item(1)
                    elif event.key == pg.K_3:
                        self.guy.use_item(2)
                    elif event.key == pg.K_4:
                        self.guy.use_item(3)
                # If player dies or dragon is killed, game is over, prompt to restart the game. 
                elif (self.guy.alive == 0 or self.game_end == 1) and (event.key == pg.K_y):
                    self.Start()
                elif (self.guy.alive == 0 or self.game_end == 1) and (event.key == pg.K_n):
                    self.playing = False
                else:
                    self.player_turn(0, 0)
    # Player turn
    # Need to modify this to be simpler. Most or all of this functionality can likely be handled elsewhere. 
    def player_turn(self, dx, dy):
        if self.guy.alive == 1:
            dest_cell = self.map[self.guy.y+dy][self.guy.x+dx]
            [hit_enemy, hit_dragon, enemy_x, enemy_y, next_level] = self.guy.move_player(dx, dy, dest_cell)
            if next_level == 1:
                self.level += 1
                # print(self.level)
                self.next_stage()
            elif hit_enemy == 1:
                for i in self.mobs:
                    if (i.x == enemy_x and i.y == enemy_y):
                        damage, level_up = self.guy.hit(i)
                        self.hud.to_prompt("YOU hit " + i.name + " for " + str(damage) + " damage")
                        if level_up:
                            self.hud.to_prompt("LEVEL UP!")
            elif hit_dragon == 1:
                damage, level_up = self.guy.hit(self.dragon)
                self.hud.to_prompt("YOU hit " + self.dragon.name + " for " + str(damage) + " damage")
                if level_up:
                    self.hud.to_prompt("LEVEL UP!")
        self.mob_turn()

    # mobs movement and attack
    def mob_turn(self):
        for i in self.mobs:
            # Check if mob is alive, or hasn't been cleared yet
            if i.alive == 1:
                hit_player = i.move_mob(self.gameboard, self.win, self.guy.x, self.guy.y)
                # Check to see if we hit the player
                if hit_player == 1:
                    damage = i.hit(self.guy)
                    self.hud.to_prompt(i.name + " hit YOU for " + str(damage) + " damage")
            elif i.cleared == 0:
                i.clear_mob(self.gameboard, self.win, self.grid)
                self.hud.to_prompt(i.name + " was slain!")
        if self.dragon_spawn == 1:
            if self.dragon.alive == 1:
                dragon_hit = self.dragon.move(self.gameboard, self.win, self.guy.x, self.guy.y)
                if dragon_hit == 1:
                    damage = self.dragon.hit(self.guy)
                    self.hud.to_prompt(self.dragon.name + " hit YOU for " + str(damage) + " damage")
            elif self.dragon.cleared == 0:
                self.game_end = 1
                self.hud.to_prompt("YOU WIN! Do you want to play again (Y/N)?")
                self.dragon.clear_dragon(self.gameboard, self.win, self.grid)

    # Update game state
    # def update(self):
        # Draw player and mobs each loop
        # if self.guy.alive == 1:
        #     self.guy.draw(self.win, self.spritenum, self.grid)
        # elif self.guy.cleared == 0:
        #     self.guy.clear_player(self.gameboard, self.win, self.grid)
        #     self.hud.to_prompt("YOU DIED! Do you want to play again (Y/N)?")
        # for i in self.mobs:
        #     if i.alive == 1:
        #         i.draw(self.win, self.spritenum, self.guy.x, self.guy.y, self.guy.sight, self.grid)
        # if self.dragon_spawn == 1:
        #     if self.dragon.alive == 1:
        #         self.dragon.draw(self.win, self.spritenum, self.guy.x, self.guy.y, self.guy.sight, self.grid)
        #draw the map, hud, entities, after updating all positions
        # self.render_graphics()
        # pg.display.update()

    # render GRAPHICS to screen
    def render_graphics(self):
        # Cycle frames at a specific rate to slow down animations
        # Only change sprites every 500 loops to slow down animation
        if self.frame == 0:
            self.frame = 100
            if spritenum == 0:
                spritenum = 1
            else:
                spritenum = 0
        else:
            self.frame -= 1
        # Draw the stage
        render.draw_stage(self.grid, self.win, self.map, self.guy.x, self.guy.y, self.guy.sight, self.grid)
        # Update the hud
        self.hud.update(self.grid, self.win, spritenum, self.guy)
        # Draw the player
        render.draw_entity(self.guy)
        # Draw the npcs and enemies
        for i in self.mobs:
            render.draw_entity(self.grid, self.win, spritenum, i)
        pg.display.update()
        
    def run(self):
        # Game Loop
        while self.playing:
            self.events()
            self.render_graphics()

