import pygame as pg
import tileset
from random import randint

class Room:
    # Draw a rectangle to create a room
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.x2 = x + w
        self.y1 = y
        self.y2 = y + h
    
    def center(self):
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
    
    def intersect(self, other):
        #returns true if this rectangle intersects with another
        if self.x1 <= other.x2 and self.x2 >= other.x1 and self.y1 <= other.y2 and self.y2 >= other.y1:
            return True
        else:
            return False


class GameMap:
    def create_rooms(self):
        rooms = []
        num_rooms = randint(4, 6) #for now use raw numbers, eventually, generate based on the level
        r = 0

        while r < num_rooms:
            w = randint(4,8)
            h = randint(4,8)





