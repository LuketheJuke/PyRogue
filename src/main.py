import pygame as pg

from rogue import Game

def main():
    pg.init()
    pg.display.set_caption("Rogue")
    pg.key.set_repeat(250,100)
    
    # Find a better way to scale the window. 
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

    # Start the game
    Rogue = Game(grid_w, grid_h, grid)
    Rogue.Start()

    while Rogue.playing == True:
        Rogue.run()

    pg.quit()

if __name__ == "__main__":
    main()