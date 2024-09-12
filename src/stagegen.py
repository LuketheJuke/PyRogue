import pygame as pg
import numpy as np
import cell as cell
import room as room
import leaf as leaf
import tileset
from random import randint

# Set to 1 to include debug print statements
debug_mode = True
            
# Game Map Generation
# Organizes the leaves that the whole map is split into.
# Has settings to vary the level generation depending on dungeon level and 
# defined screen size. 
class MapGen():
    def __init__(self, width, height, dun_level):
        self.stage_w = width
        self.stage_h = height
        self.dun_level = dun_level
        self.rooms = []
        self.grid = []
        self.totalarea = 0
        for y in range(0, height - 1):
            row = []
            for x in range(0, width - 1):
                row.append(cell.Cell(x, y))
            self.grid.append(row)

    # BSP method
    # Create initial leaf, split GameMap in half vertically or horizontally to two leaves
    def init_leaf(self):
        Lin = leaf.Leaf(0, 0, self.stage_w, self.stage_h, 0)
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

    # Create rooms within the defined leaves
    def create_rooms(self):
        # Set a maximum and minimum number of rooms
        max_rooms = 12
        min_rooms = 7
        max_area = min_rooms * 60
        # Keep generating rooms until we hit the max_rooms value
        for L in self.Leaves:
            if not(L.has_room):
                gen_chance = randint(0,100)
                # Randomize room size, dependent on dimensions of leaf
                w = randint(3, L.w - 1)
                h = randint(3, L.h - 1)
                area = w * h
                # Generate x and y corner of room
                x = randint(L.x1, L.x2 - w) # give buffer of 1 to each edge to allow for wall generation around floors
                y = randint(L.y1, L.y2 - h)
                if gen_chance > 30 and len(self.rooms) < max_rooms and self.totalarea < max_area:
                    new_room = room.Room(x, y, w, h)
                    self.rooms.append(new_room)
                    self.totalarea += area
                    L.has_room = True
        
        # Run again if we didn't generate enough rooms
        if len(self.rooms) < min_rooms and self.totalarea < max_area:
            self.create_rooms()
    
    # Search the whole map for the closest connectable point
    def search_conn_point(self, conn_x, conn_y, x1, x2, y1, y2):
        best_dist = 20
        conn_point = (0,0)
        for x in range(0, self.stage_w - 1):
            for y in range(0, self.stage_h - 1):
                # Check if we're in this room
                this_room = (x >= x1 and x <= x2) and (y >= y1 and y <= y2)
                # Initial distance check
                new_dist = abs(conn_x - x) + abs(conn_y - y)
                if self.grid[y][x].value == "&" and not(this_room) and new_dist < best_dist:
                    conn_point = (x,y)
                    best_dist = new_dist                    
        return conn_point

    def create_hallways(self):
        for r in self.rooms:
            # Check that room is not already connected
            if not(r.connect):
                # Find the closest room or hallway to connect to
                room_x = randint(r.x1, r.x2)
                room_y = randint(r.y1, r.y2)
                (conn_x, conn_y) = self.search_conn_point(room_x, room_y, r.x1, r.x2, r.y1, r.y2)
                # Set the x range and y range
                if room_x < conn_x:
                    x_range = range(room_x, conn_x)
                else:
                    x_range = range(conn_x, room_x)
                
                if room_y < conn_y:
                    y_range = range(room_y, conn_y)
                else:
                    y_range = range(conn_y, room_y)

                # Draw a hallway connecting the room point with connect point
                if room_x != conn_x:
                    for x in x_range:
                        self.grid[room_y][x].value = "&"
                if room_y != conn_y:
                    for y in y_range:
                        self.grid[y][conn_x].value = "&"
                r.connect = True

    # Draw all the floors of the defined rooms
    def draw_rooms(self):
        # For each room, draw the floor
        for r in self.rooms:
            for i in range(r.x1,r.x2):
                for j in range(r.y1,r.y2):
                    self.grid[j][i].value = "&"
    
    # Draw the outline of the leaves
    def draw_leaf_borders(self):
            # Loop through x and y coorindates to draw outer edge of leaf
            for L in self.Leaves:
                for i in range(L.x1,L.x2+1):
                    self.grid[L.y1][i].value = "_"
                    self.grid[L.y2][i].value = "_"
                for i in range(L.y1,L.y2):
                    self.grid[i][L.x1].value = "_"
                    self.grid[i][L.x2].value = "_"
            
        
    # Print all leaves and their parameters - for debug
    def print_leaves(self):
        for i in level1.Leaves:
            print("x: " + str(i.x1) + "," + str(i.x2) + ", y: " + str(i.y1) + "," + str(i.y2) + ", width: " + str(i.w) + ", height: " + str(i.h) + ", depth: " + str(i.depth))

    def write_output(self):
        outfile = open("levels/level" + str(self.dun_level) + "_gen.txt", "w")
        # Write to output file
        for j in range(0, self.stage_h - 1):
            map_line = ''
            for i in range(0,self.stage_w - 1):
                map_line += self.grid[j][i].value
            map_line += "\n"
            outfile.writelines(map_line)
        outfile.close()

level1 = MapGen(60, 40, 1)
level1.init_leaf()

for i, val in enumerate(level1.Leaves):
    if val.depth < 2:
        level1.create_leaf(i)

for i, val in enumerate(level1.Leaves):
    if val.depth < 3:
        level1.create_leaf(i)

for i, val in enumerate(level1.Leaves):
    if val.depth < 4:
        level1.create_leaf(i)

level1.create_rooms()
# level1.draw_leaf_borders()
level1.draw_rooms()
level1.create_hallways()

# Write to output file
level1.write_output()

print("Done!") 