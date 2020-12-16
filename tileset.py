import pygame

# Load an image
def load_image(image):
    image = pygame.image.load(image).convert()
    image_width, image_height = image.get_size()
    return image, image_width, image_height

# Slice image into usable tiles and return array of tiles
def slice_image(image, tile_width, tile_height):
    image_width, image_height = image.get_size()
    tile_table = []
    for i in range(0, image_width//tile_width):
        tile_line = []
        tile_table.append(tile_line)
        for j in range(0, image_height//tile_height):
            rect = (i*tile_width, j*tile_height, tile_width, tile_height)
            tile_line.append(image.subsurface(rect))
    return tile_table

def make_tileset(image):
    # Load sprite tileset
    [map, map_w, map_h] = load_image(image)
    map_scaled = pygame.transform.scale(map, (map_w*3, map_h*3))
    # image_width, image_height = map_scaled.get_size()
    tiles = slice_image(map_scaled, 24, 24)
    return tiles