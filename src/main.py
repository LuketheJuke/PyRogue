import pygame as pg
import rogue

def main():
    pg.init()
    pg.display.set_caption("Rogue")
    pg.key.set_repeat(250,100)

    # Start the game
    Game = rogue.Rogue()
    Game.Start()

    while Game.playing == True:
        Game.run()

    pg.quit()

if __name__ == "__main__":
    main()