import pygame as pg
import numpy as np
import tileset
from random import randint

class Room():
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
            print("Intersect detected!")
            return True
        else:
            return False

class GameMap():
    def __init__(self, width, height, dun_level):
        self.stage_w = width
        self.stage_h = height
        self.dun_level = dun_level

    def create_rooms(self):
        #Create a certain number of rooms in randomized positions, check for intersections, keep track of each place
        self.rooms = []
        num_rooms = randint(8, 10) #for now use raw numbers, eventually, generate based on the level
        print("Number of rooms: " + str(num_rooms))
        r = 0

        # Keep generating rooms until we hit the num_rooms value
        while r < num_rooms:
            print("Generating room " + str(r))
            valid_room = 0
            w = randint(4, 12)
            h = randint(4, 10)
            x_lim = randint(1, self.stage_w - w - 1) #give buffer of 1 to each edge to allow for wall generation around floors
            y_lim = randint(1, self.stage_h - h - 1)
            print("Width: " + str(w) + ", Height: " + str(h))
            new_room = Room(x_lim, y_lim, w, h)
            print("Room x1, x2: " + str(new_room.x1) + ", " + str(new_room.x2))
            print("Room y1, y2: " + str(new_room.y1) + ", " + str(new_room.y2))
            if r == 0:
                valid_room = 1
            else:
                for i in self.rooms: #check if new room intersects with other rooms
                    print("Room i, check for intersect.")
                    if Room.intersect(new_room, i):
                        valid_room = 0
                        break
                    else:
                        valid_room = 1
            
            if valid_room == 1:
                print("Room is valid.")
                self.rooms.append(new_room)
                r += 1
            else:
                print("Room not valid, continue loop.")
                continue

    # def create_halls(self)
    #     #Connect rooms with hallways

    def draw_rooms(self):
        self.map = [["."] * self.stage_w for i in range(self.stage_h)]
        outfile = open("levels/level" + str(self.dun_level) + "_gen.txt", "w")

        # For each room, draw the floor
        for r in self.rooms:
            print("Drawing room " + str(r))
            print(range(r.x1,r.x2))
            print(range(r.y1,r.y2))
            for i in range(r.x1,r.x2):
                for j in range(r.y1,r.y2):
                    print("Writing to " + str(i) + ", " + str(j))
                    self.map[j][i] = "*"
        
        # Write to output file
        for j in range(0, self.stage_h):
            print("Writing line " + str(j))
            map_line = ''.join(level1.map[j]) + "\n"
            print(map_line)
            outfile.writelines(map_line)

        outfile.close()

level1 = GameMap(60, 40, 1)
level1.create_rooms()
level1.draw_rooms()
print("Done!")