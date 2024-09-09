import pygame as pg
import numpy as np
import tileset
from random import randint

# Set to 1 to include debug print statements
debug_mode = True

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
    def __init__(self, x, y, w, h, depth):
        self.x1 = x
        self.x2 = x + w - 1
        self.y1 = y
        self.y2 = y + h - 1
        self.w = w
        self.h = h
        self.center_x = int((self.x1 + self.x2) / 2)
        self.center_y = int((self.y1 + self.y2) / 2)
        self.depth = depth # Number of splits on this leaf

    # Determine x and y coordinates to split the leaf and return child leaves
    def split(self):
        split_scale = .1 # Vary split location by 10%

        # If the section is very wide or very tall, split it along the longer side
        if self.w > 2.2 * self.h or self.h < 6:
            split_dir = 1 # Split vertically
        elif self.h > 1.6 * self.w or self.w < 8:
            split_dir = 0 # Split horizontally
        else:
            split_dir = randint(0,1)

        if split_dir == 1: # Split vertically
            split_x = randint(round((self.w/2)-self.w*split_scale), round((self.w/2)+self.w*split_scale))
            # print("Split vertically along x coord " + str(split_x))
            w1 = split_x
            w2 = self.w - split_x
            h1 = self.h
            h2 = self.h
            new_x = self.x1 + split_x
            new_y = self.y1
        else: #Split horizontally
            split_y = randint(round((self.h/2)-self.h*split_scale), round((self.h/2)+self.h*split_scale))
            # print("Split horizontally along y coord " + str(split_y))
            w1 = self.w
            w2 = self.w
            h1 = split_y
            h2 = self.h - split_y
            new_x = self.x1
            new_y = self.y1 + split_y

        # Increment depth to indicate there's been an additional split
        depth = self.depth+1

        # Create child leaves, return them as part of this function
        C1 = Leaf(self.x1, self.y1, w1, h1, depth)
        C2 = Leaf(new_x, new_y, w2, h2, depth)
        return(C1,C2)
            


class GameMap():
    def __init__(self, width, height, dun_level):
        self.stage_w = width
        self.stage_h = height
        self.dun_level = dun_level

    # BSP method
    # Create initial leaf, split GameMap in half vertically or horizontally to two leaves
    def init_leaf(self):
        Lin = Leaf(0, 0, self.stage_w, self.stage_h, 0)
        (L1, L2) = Lin.split()
        self.Leaves = []
        self.Leaves.append(L1)
        self.Leaves.append(L2)
        
    # Used for any further splitting of leaves
    def create_leaf(self, index):
        (L1, L2) = self.Leaves[index].split()
        
        # Store new leaves in the current index
        self.Leaves[index] = L1
        # Insert second new leaf in the next index
        self.Leaves.insert(index+1, L2)

    # Print all leaves and their parameters - for debug
    def print_leaves(self):
        for i in level1.Leaves:
            print("x: " + str(i.x1) + "," + str(i.x2) + ", y: " + str(i.y1) + "," + str(i.y2) + ", width: " + str(i.w) + ", height: " + str(i.h) + ", depth: " + str(i.depth))
    
    # Draw the outline of the leaves
    def draw_leaf_borders(self):
            self.map = [["."] * self.stage_w for i in range(self.stage_h)]
            outfile = open("levels/level" + str(self.dun_level) + "_gen.txt", "w")
            
            for leaf in self.Leaves:
                for i in range(leaf.x1,leaf.x2+1):
                    print("Drawing x: " + str(i) + ", y: " + str(leaf.y1))
                    self.map[leaf.y1][i] = "_"
                    print("Drawing x: " + str(i) + ", y: " + str(leaf.y2))
                    self.map[leaf.y2][i] = "_"
                for i in range(leaf.y1,leaf.y2):
                    print("Drawing x: " + str(leaf.x1) + ", y: " + str(i))
                    self.map[i][leaf.x1] = "_"
                    print("Drawing x: " + str(leaf.x2) + ", y: " + str(i))
                    self.map[i][leaf.x2] = "_"

            # Write to output file
            for j in range(0, self.stage_h):
                map_line = ''.join(level1.map[j]) + "\n"
                print(map_line)
                outfile.writelines(map_line)
            
            outfile.close()
                    

    # Random rectangle method: 
    def create_rooms(self):
        # Create rooms in each leaf, or random chance to be an empty spot
        self.rooms = []

        # Set a maximum and minimum number of rooms
        # Dependent on how the leaves are generated?
        # max_rooms = 
        # min_rooms =

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
level1.init_leaf()

if debug_mode:
    print("First Split")
    level1.print_leaves()

for i, val in enumerate(level1.Leaves):
    if val.depth < 2:
        level1.create_leaf(i)

if debug_mode:
    print("Second Split")
    level1.print_leaves()

for i, val in enumerate(level1.Leaves):
    if val.depth < 3:
        level1.create_leaf(i)

if debug_mode:
    print("Third Split")
    level1.print_leaves()

for i, val in enumerate(level1.Leaves):
    if val.depth < 4:
        level1.create_leaf(i)

if debug_mode:
    print("Fourth Split")
    level1.print_leaves()

level1.draw_leaf_borders()

# level1.draw_rooms()
print("Done!") 