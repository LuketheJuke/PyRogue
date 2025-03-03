import pygame as pg

FONT = pg.freetype.Font("text/manaspc.ttf", grid)

window = pg.display.set_mode((self.screen_width, self.screen_height))
window.fill((0,0,0))

def print_to_HUD(text, x, y):
    text_surf, rect = FONT.render(text, (255, 255, 255))
    window.blit(text_surf, (x*self.grid, y*self.grid))

def print_entity(spritenum, x, y):
    window.blit(self.spritelist[spritenum], (self.x*grid, self.y*grid))