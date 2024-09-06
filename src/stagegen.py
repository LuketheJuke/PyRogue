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

class Leaf():
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.x2 = x + w
        self.y1 = y
        self.y2 = y + h
        self.center_x = int((self.x1 + self.x2) / 2)
        self.center_y = int((self.y1 + self.y2) / 2)

    # Determine x and y coordinates to split the leaf and return child leaves
    def split(self):
        split_scale = .2 # Vary split location by 20%

        # If the section is very wide or very tall, split it along the longer side
        if self.w > 2 * self.h:
            split_dir = 1 # Split vertically
        elif self.h > 2 * self.w:
            split_dir = 0 # Split horizontally
        else:
            split_dir = randint(0,1)

        if split_dir == 1: # Split vertically
            split_x = randint((self.w/2)-round(self.w*split_scale), (self.w/2)+round(self.w*split_scale))
            split_y = self.center_y
            print("Split vertically along x coord " + str(split_x))
        else: #Split horizontally
            split_y = randint((self.h/2)-round(self.h*split_scale), (self.h/2)+round(self.h*split_scale))
            split_x = self.center_x
            print("Split horizontally along y coord " + str(split_y))

        # Create child leaves, return them as part of this function
        c1 = Leaf(self.x, self.y, w1, h1)
        c2 = Leaf(split_x, split_y, w2, h2)
        # Will returning these work the way I want? How will this be handled at the map_gen level?
        return(c1,c2)

class GameMap():
    def __init__(self, width, height, dun_level):
        self.stage_w = width
        self.stage_h = height
        self.dun_level = dun_level

    # BSP method
    # Create initial leaf, split GameMap in half vertically or horizontally to two leaves
    def init_leaf(self, width, height):
        Lin = Leaf(0, 0, self.width, self.height)
        (L1, L2) = Lin.split()
        self.Leaves = []
        self.Leaves.append(L1)
        self.Leaves.append(L2)
        
    # Used for any further splitting of leaves
    # Manage list of leaves
    def create_leaf(self, index):
        # Need to figure out how to put these into a list, in a specific order. 
        # Then when I split them, they should stay in that particular order. 
        # So initial split: (L1, L2), then if I split L1: (L1a, L1b, L2)
        # Use list.insert(i,x) with i being the location. In the above example, I'd use this I think:
        # list.remove(L1) - easier way to do this without actually removing it?
        # list.insert(0, L1a)
        # list.insert(1, L1b)
        (C1, C2) = self.Leaves(index).split()
        self.Leaves[index] = C1
        self.Leaves.insert(index+1, C2)

    

    # Random rectangle method: 
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
            # Randomize room size
            w = randint(4, 12)
            h = randint(4, 10)
            # Generate x and y corner of room
            x = randint(1, self.stage_w - w - 1) # give buffer of 1 to each edge to allow for wall generation around floors
            y = randint(1, self.stage_h - h - 1)
            print("Width: " + str(w) + ", Height: " + str(h))
            new_room = Room(x, y, w, h)
            print("Room x1, x2: " + str(new_room.x1) + ", " + str(new_room.x2))
            print("Room y1, y2: " + str(new_room.y1) + ", " + str(new_room.y2))
            if r == 0:
                valid_room = 1
            else:
                for i in self.rooms: #check if new room intersects with other rooms
                    print("Room " + str(r) + ", check for intersect.")
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
                    self.map[j][i] = "*"
        
        # Write to output file
        for j in range(0, self.stage_h):
            map_line = ''.join(level1.map[j]) + "\n"
            print(map_line)
            outfile.writelines(map_line)

        outfile.close()

    # def draw_hallways(self):
        

level1 = GameMap(60, 40, 1)
level1.create_rooms()
level1.draw_rooms()
print("Done!") 