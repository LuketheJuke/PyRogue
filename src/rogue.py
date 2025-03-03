import pygame as pg
import numpy as np
import pygame.freetype

import stage
import mob
import player
import tileset
import items
from hud import hud

np.set_printoptions(threshold=np.inf)

# Main game class
class Game:
    def __init__(self, grid_w, grid_h, grid):
        # width of grid is 24 pixels
        # Initialize variables
        self.grid_w = grid_w
        self.grid_h = grid_h
        self.grid = grid
        self.screen_width = grid * grid_w
        self.screen_height = grid * grid_h
        # initialize gameboard array - defines each location in the grid
        self.gameboard = np.zeros((grid_h, grid_w))
        self.win = pg.display.set_mode((self.screen_width, self.screen_height))
        self.win.fill((0,0,0))
        # Set up HUD
        self.hud = hud(grid_w, grid_h, grid, self.win)
        # create clock variable and key repeat rate
        self.clock = pg.time.Clock()
        self.frame = 0
        self.playing = True
        # define starting level
        self.level = 1
        # import GRAPHICS
        self.spritenum = 0
        self.monsters = tileset.make_tileset("sprites/BitsyDungeonTilesby_enui/MonsterTiles.png", grid)

    def Start(self):
        self.game_end = 0
        window = pg.display.set_mode((self.screen_width, self.screen_height))
        self.win = window

        self.hud = hud(self.grid_w, self.grid_h, self.grid, window)
        self.win.fill((0,0,0))
        # Start game - also used to restart the game
        self.hud.to_prompt("Number keys to use items")
        self.hud.to_prompt("Arrow keys to move/attack")
        self.hud.to_prompt("Good luck!")
        self.level = 1
        self.stage_gen()
        self.player_gen(1)
        self.mob_gen()

    def next_stage(self):
        self.win.fill((0,0,0))
        self.stage_gen()
        self.player_gen(0)
        self.mob_gen()
        self.hud.to_prompt("Welcome to level " + str(self.level))

    def stage_gen(self):
        # import GRAPHICS
        stage.get_tiles("sprites/BitsyDungeonTilesby_enui/DungeonTiles.png", self.grid)
        # Generate and draw the stage based on level
        (self.xinit, self.yinit) = stage.generate(self.win, self.gameboard, self.hud.gameheight, self.grid_w, self.level, self.grid)

    def player_gen(self, init):
        if init == 1: 
            # First time player generation
            self.guy = player.p1(15, items.dagger, items.shirt, self.xinit, self.yinit, [self.monsters[0][4], self.monsters[1][4]])
        else:
            # Generate player at start of new stage
            self.guy.x = self.xinit
            self.guy.y = self.yinit 

    # Generate mobs
    def mob_gen(self):
        self.mobs = []
        self.dragon_spawn = 0
        # name, health, attack, xpval
        enemylist = [['BAT', 3, 1, 2, [self.monsters[0][17], self.monsters[1][17]]], 
                    ['GHOST', 5, 2, 4, [self.monsters[0][8], self.monsters[1][8]]], 
                    ['GOBLIN', 6, 3, 5, [self.monsters[0][6], self.monsters[1][6]]], 
                    ['SKELETON', 8, 3, 6, [self.monsters[0][5], self.monsters[1][5]]], 
                    ['WEREWOLF', 10, 5, 12, [self.monsters[0][15], self.monsters[1][15]]]]
        dragon =    ['DRAGON', 60, 12, 100, [self.monsters[1][14], self.monsters[0][14],  # A 3 dimensional array with x, y, spritenum as the parameters 
                                            self.monsters[1][13], self.monsters[0][13],  
                                            self.monsters[1][12], self.monsters[0][12], 
                                            self.monsters[1][11], self.monsters[0][11]]]
        for y in range(0,(len(self.gameboard))):
            for x in range(0,len(self.gameboard[0])):
                if self.gameboard[y][x] == 4:
                    r = np.random.randint(0, len(enemylist))
                    self.mobs.append(mob.mob(x, y, enemylist[r][0], enemylist[r][1], enemylist[r][2], enemylist[r][3], enemylist[r][4]))
                if self.gameboard[y][x] == 9:
                    self.dragon = mob.dragon(x, y, dragon[0], dragon[1], dragon[2], dragon[3], dragon[4])
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
    def player_turn(self, cx, cy):
        if self.guy.alive == 1:
            [hit_enemy, hit_dragon, enemy_x, enemy_y, next_level] = self.guy.move_player(cx, cy, self.gameboard, self.win, self.grid)
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
    def update(self):
        # Only change sprites every 500 loops to slow down animation
        if self.frame == 0:
            self.frame = 100
            if self.spritenum == 0:
                self.spritenum = 1
            else:
                self.spritenum = 0
        else:
            self.frame -= 1
        # Draw player and mobs each loop
        if self.guy.alive == 1:
            self.guy.draw(self.win, self.spritenum, self.grid)
        elif self.guy.cleared == 0:
            self.guy.clear_player(self.gameboard, self.win, self.grid)
            self.hud.to_prompt("YOU DIED! Do you want to play again (Y/N)?")
        for i in self.mobs:
            if i.alive == 1:
                i.draw(self.win, self.spritenum, self.guy.x, self.guy.y, self.guy.sight, self.grid)
        if self.dragon_spawn == 1:
            if self.dragon.alive == 1:
                self.dragon.draw(self.win, self.spritenum, self.guy.x, self.guy.y, self.guy.sight, self.grid)
        #draw some of the stage based on player location
        stage.draw_stage(self.win, self.gameboard, self.guy.x, self.guy.y, self.guy.sight, self.grid)
        pg.display.update()

    def render(self):
        stage.draw_stage(self.win, self.gameboard, self.guy.x, self.guy.y, self.guy.sight, self.grid)
        pg.display.update()
        
    def run(self):
        # Game Loop
        while self.playing:
            self.events()
            self.update()
            self.hud.update(self.guy)
