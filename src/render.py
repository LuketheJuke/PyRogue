import pygame as pg
import tileset

def setup(grid):
    # Using global variables for now - should probably find a better way to do this later
    global stage_tiles
    global item_tiles
    global monster_tiles
    global FONT
    # Define font
    FONT = pg.freetype.Font("text/manaspc.ttf", grid)
    # Create tilesets
    stage_tiles = tileset.make_tileset("sprites/BitsyDungeonTilesby_enui/DungeonTiles.png", grid)
    item_tiles = tileset.make_tileset("sprites/BitsyDungeonTilesby_enui/ItemTiles.png", grid)
    monster_tiles = tileset.make_tileset("sprites/BitsyDungeonTilesby_enui/MonsterTiles.png", grid)

# Print text to HUD
def print_to_HUD(grid, window, text, x, y):
    text_surf, rect = FONT.render(text, (255, 255, 255))
    window.blit(text_surf, (x*grid, y*grid))

# Draw all entities, player, enemies, etc
def draw_entity(grid, window, spritenum, entity):
    # Pull the correct sprites for this entity
    spritelist = monster_tiles[entity.sprites[0][0], entity.sprites[0][1]], monster_tiles[entity.sprites[1][0], entity.sprites[1][1]]
    # How to pull correct sprites without "mob" module knowing the sprite tile detals?
    window.blit(spritelist[spritenum], (entity.x*grid, entity.y*grid))

# Draw the stage
def draw_stage(grid, window, map, playerx, playery, sight):
    # wall = 2
    # floor = (1, 3, 4, 5, 6, 7, 8, 9, 10, 11) #tile types that are treated as a floor
    # Cycle through the gameboard and draw the corresponding tile
    for y in range(playery-sight, playery+sight):
        for x in range(playerx-sight, playerx+sight):
            if y >= len(map) or x >= len(map[0]):
                pass
            elif (abs(playerx-x) + abs(playery-y)) < sight:
                if map[y][x].occupied:
                    pass
                elif map[y][x].has_item:
                    if map[y][x].exit: # down staircase
                        window.blit(stage_tiles[4][3], (x*grid, y*grid))
                    elif map[y][x].item == "Long Sword": # long sword
                        window.blit(item_tiles[1][2], (x*grid, y*grid))
                    elif map[y][x].item == "Health Potion": # Health potion
                        window.blit(item_tiles[1][0], (x*grid, y*grid))
                    elif map[y][x].item == "Leather Armor": # Leather armor
                        window.blit(item_tiles[1][5], (x*grid, y*grid))
                    elif map[y][x].item == "Battle Axe": # Battle axe
                        window.blit(item_tiles[0][3], (x*grid, y*grid))
                    elif map[y][x].item == "Plate Armor": # Plate armor
                        window.blit(item_tiles[1][6], (x*grid, y*grid))
                elif map[y][x].walkable: # floor
                    window.blit(stage_tiles[0][0], (x*grid, y*grid))
                elif map[y][x].wall: # Walls
                    north = map[y-1][x] 
                    south = map[y+1][x] 
                    west = map[y][x-1] 
                    east = map[y][x+1]
                    # Check were walls are (2) and floor is (1), and draw the appropriate wall
                    if north.wall and south.wall:
                        if west.walkable:
                            window.blit(stage_tiles[4][1], (x*grid, y*grid))
                        elif east.walkable:
                            window.blit(stage_tiles[0][2], (x*grid, y*grid))
                        else:
                            pass
                    elif east.wall:
                        if west.wall:
                            if south.walkable:
                                window.blit(stage_tiles[3][0], (x*grid, y*grid))
                            elif north.walkable:
                                window.blit(pg.transform.flip(stage_tiles[3][0],0,1), (x*grid, y*grid))
                        elif south.wall:
                            if west.walkable and north.walkable:
                                window.blit(stage_tiles[0][1], (x*grid, y*grid))
                            else:
                                window.blit(stage_tiles[1][2], (x*grid, y*grid))
                        elif north.wall:
                            if south.walkable and west.walkable:
                                window.blit(stage_tiles[2][1], (x*grid, y*grid))
                            else:
                                window.blit(pg.transform.flip(stage_tiles[1][2],0,1), (x*grid, y*grid))
                    elif west.wall:
                        if south.wall:
                            if east.walkable and north.walkable:
                                window.blit(stage_tiles[1][1], (x*grid, y*grid))
                            else:
                                window.blit(stage_tiles[4][2], (x*grid, y*grid))
                        elif north.wall:
                            if south.walkable:
                                window.blit(stage_tiles[3][1], (x*grid, y*grid))
                            else:
                                window.blit(pg.transform.flip(stage_tiles[4][2],0,1), (x*grid, y*grid))
                else: # Draw a blank space
                    # Eventually, draw a greyed out version of the previous tile.
                    window.blit(stage_tiles[1][4], (x*grid, y*grid))