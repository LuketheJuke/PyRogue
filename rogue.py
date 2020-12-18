import pygame as pg
import pygame.freetype
import stage
import people
import tileset
import items
import numpy as np

np.set_printoptions(threshold=np.inf)
pg.init()

# Return info for the PC screen
ScreenInfo = pg.display.Info()

grid_w = 60
grid_h = 40
# Set the size of the gameboard's grid based on current screen size
if ScreenInfo.current_h//grid_h >= 24 and ScreenInfo.current_w//grid_w >= 24:
    grid = 24
elif ScreenInfo.current_h//grid_h >= 16 and ScreenInfo.current_w//grid_w >= 16:
    grid = 16
else:
    grid = 8
screen_width = grid * grid_w
screen_height = grid * grid_h

class hud():
    def __init__(self, scr_width, scr_height):
        # Define top left corner
        self.x = 0*grid
        self.y = 32*grid
        # HUD should be drawn at the bottom of the screen, size based on screen size
        self.width = scr_width - self.x
        self.height = scr_height - self.y
        self.gameheight = (screen_height - self.height)//grid
        self.FONT = pg.freetype.Font("text/manaspc.ttf", grid)
        self.prompt = " "
        self.promptlist = []
        self.new_prompt = 0

    def update(self):
        hud_rect = (self.x, self.y, self.width, self.height)
        pygame.draw.rect(Rogue.win, (0,0,0), hud_rect)
        # Display level # to HUD
        self.print_to_HUD("Player Level: " + str(Rogue.guy.level), 2, 33)
        # Display health
        self.print_to_HUD("Health: " + str(Rogue.guy.health) + "/" + str(Rogue.guy.health_max), 2, 34)
        # Display weapon and attack value
        self.print_to_HUD("Weapon: " + Rogue.guy.weapon.name, 2, 36)
        self.print_to_HUD("Attack: " + str(Rogue.guy.weapon.attack), 2, 37)
        # Display armor and defense
        self.print_to_HUD("Armor: " + Rogue.guy.armor.name, 2, 38)
        self.print_to_HUD("Defense: " + str(Rogue.guy.armor.defense), 2, 39)
        # Display Inventory
        self.print_to_HUD("Inventory: ", (grid_w/4)*1, 33)
        self.print_to_HUD("1: " + Rogue.guy.inventory[0].name, (grid_w/4)*1, 34)
        self.print_to_HUD("2: " + Rogue.guy.inventory[1].name, (grid_w/4)*1, 35)
        self.print_to_HUD("3: " + Rogue.guy.inventory[2].name, (grid_w/4)*1, 36)
        self.print_to_HUD("4: " + Rogue.guy.inventory[3].name, (grid_w/4)*1, 37)
        #Check whether prompt has changed
        # Display Info to the player
        for i in range(0,len(self.promptlist)):
            self.print_to_HUD(self.promptlist[i], (grid_w/4)*2, 33+i)

    def print_to_HUD(self, text, x, y):
        text_surf, rect = self.FONT.render(text, (255, 255, 255))
        Rogue.win.blit(text_surf, (x*grid, y*grid))
    
    # Print something to the prompt queue for the player
    def to_prompt(self, text):
        self.prompt = text
        if len(self.promptlist) == 0:
            self.promptlist.insert(0,self.prompt)
        else:
            self.promptlist.insert(0,self.prompt)
            if len(self.promptlist) == 7:
                self.promptlist.pop(6)

# Main game class
class Game:
    def __init__(self):
        # width of grid is 24 pixels
        # self.grid = 24
        # # set window size and label
        # screen_width = self.grid*50
        # screen_height = self.grid*40
        pg.display.set_caption("Rogue")
        # initialize gameboard array - defines each location in the grid
        self.gameboard = np.zeros((grid_h, grid_w))
        self.win = pg.display.set_mode((screen_width, screen_height))
        self.win.fill((0,0,0))
        # create clock variable and key repeat rate
        self.clock = pg.time.Clock()
        pg.key.set_repeat(250,100)
        self.frame = 0
        self.playing = True
        # define starting level
        self.level = 1
        # import GRAPHICS
        self.spritenum = 0
        self.monsters = tileset.make_tileset("sprites/BitsyDungeonTilesby_enui/MonsterTiles.png", grid)

    def Start(self):
        self.win.fill((0,0,0))
        # Start game - also used to restart the game
        RogueHUD.to_prompt("Number keys to use items")
        RogueHUD.to_prompt("Arrow keys to move/attack")
        RogueHUD.to_prompt("Good luck!")
        self.level = 1
        self.stage_gen()
        self.player_gen(1)
        self.mob_gen()

    def next_stage(self):
        self.win.fill((0,0,0))
        self.stage_gen()
        self.player_gen(0)
        self.mob_gen()
        RogueHUD.to_prompt("Welcome to level " + str(self.level))

    def stage_gen(self):
        # import GRAPHICS
        stage.get_tiles("sprites/BitsyDungeonTilesby_enui/DungeonTiles.png", grid)
        # Generate and draw the stage based on level
        (self.xinit, self.yinit) = stage.generate(self.win, self.gameboard, RogueHUD.gameheight, grid_w, self.level, grid)

    def player_gen(self, init):
        if init == 1: 
            # First time player generation
            self.guy = people.p1(15, items.dagger, items.shirt, self.xinit, self.yinit, [self.monsters[0][4], self.monsters[1][4]])
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
                    self.mobs.append(people.mob(x, y, enemylist[r][0], enemylist[r][1], enemylist[r][2], enemylist[r][3], enemylist[r][4]))
                if self.gameboard[y][x] == 9:
                    self.dragon = people.dragon(x, y, dragon[0], dragon[1], dragon[2], dragon[3], dragon[4])
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
                elif (self.guy.alive == 0) and (event.key == pg.K_y):
                    self.Start()
                elif (self.guy.alive == 0) and (event.key == pg.K_n):
                    self.playing = False
                else:
                    self.player_turn(0, 0)
    # Player turn
    def player_turn(self, cx, cy):
        if self.guy.alive == 1:
            [hit_enemy, hit_dragon, enemy_x, enemy_y, next_level] = self.guy.move_player(cx, cy, self.gameboard, self.win, grid)
            if next_level == 1:
                self.level += 1
                # print(self.level)
                self.next_stage()
            elif hit_enemy == 1:
                for i in self.mobs:
                    if (i.x == enemy_x and i.y == enemy_y):
                        damage, level_up = self.guy.hit(i)
                        RogueHUD.to_prompt("YOU hit " + i.name + " for " + str(damage) + " damage")
                        if level_up:
                            RogueHUD.to_prompt("LEVEL UP!")
            elif hit_dragon == 1:
                damage, level_up = self.guy.hit(self.dragon)
                RogueHUD.to_prompt("YOU hit " + self.dragon.name + " for " + str(damage) + " damage")
                if level_up:
                    RogueHUD.to_prompt("LEVEL UP!")
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
                    RogueHUD.to_prompt(i.name + " hit YOU for " + str(damage) + " damage")
            elif i.cleared == 0:
                i.clear_mob(self.gameboard, self.win, grid)
                RogueHUD.to_prompt(i.name + " was slain!")
        if self.dragon_spawn == 1:
            if self.dragon.alive == 1:
                dragon_hit = self.dragon.move(self.gameboard, self.win, self.guy.x, self.guy.y)
                if dragon_hit == 1:
                    damage = self.dragon.hit(self.guy)
                    RogueHUD.to_prompt(self.dragon.name + " hit YOU for " + str(damage) + " damage")
            elif self.dragon.cleared == 0:
                RogueHUD.to_prompt("YOU WIN! Do you want to play again (Y/N)?")
                self.dragon.clear_dragon(self.gameboard, self.win, grid)

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
            self.guy.draw(self.win, self.spritenum, grid)
        elif self.guy.cleared == 0:
            self.guy.clear_player(self.gameboard, self.win, grid)
            RogueHUD.to_prompt("YOU DIED! Do you want to play again (Y/N)?")
        for i in self.mobs:
            if i.alive == 1:
                i.draw(self.win, self.spritenum, self.guy.x, self.guy.y, self.guy.sight, grid)
        if self.dragon_spawn == 1:
            if self.dragon.alive == 1:
                self.dragon.draw(self.win, self.spritenum, self.guy.x, self.guy.y, self.guy.sight, grid)                
        #draw some of the stage based on player location
        stage.draw_stage(self.win, self.gameboard, self.guy.x, self.guy.y, self.guy.sight, grid)
        pg.display.update()
        
    def run(self):
        # Game Loop
        while self.playing:
            self.events()
            self.update()
            RogueHUD.update()


Rogue = Game()
RogueHUD = hud(screen_width, screen_height)

while Rogue.playing == True:
    Rogue.Start()
    Rogue.run()

pg.quit()