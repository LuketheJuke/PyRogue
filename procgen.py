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
    def __init__(self, width, height, dun_level):
        self.stage_w = width
        self.stage_h = height

    def create_rooms(self):
        #Create a certain number of rooms in randomized positions, check for intersections, keep track of each place
        rooms = []
        num_rooms = randint(4, 6) #for now use raw numbers, eventually, generate based on the level
        r = 0

        # Keep generating rooms until we hit the num_rooms value
        while r < num_rooms:
            valid_room = 0
            w = randint(4, 8)
            h = randint(4, 8)
            x = randint(1, self.stage_l - w - 1) #give buffer of 1 to each edge to allow for wall generation around floors
            y = randint(1, self.stage_w - h - 1)
            new_room = Room(x, y, w, h)
            for i in rooms: #check if new room intersects with other rooms
                if Room.intersect(i):
                    break
                else:
                    valid_room = 1
            
            if valid_room == 1:
                rooms.append(new_room)
                r += 1
            else:
                continue

    # def create_halls(self)
    #     #Connect rooms with hallways

    # def draw_rooms(self, rooms):
    #     #For each room, draw the floor