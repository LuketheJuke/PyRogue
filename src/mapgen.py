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
        self.all_cells_conn = False
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
    # srch_main modifies it to search for a point connected to the main cluster
    def search_conn_point(self, srch_main, room_x, room_y, x1, x2, y1, y2):
        best_dist = 20
        conn_point = (0,0)
        for x in range(0, self.stage_w - 1): 
            for y in range(0, self.stage_h - 1):
                # Check if we're in this room
                this_room = (x >= x1 and x <= x2) and (y >= y1 and y <= y2)
                # Initial distance check
                new_dist = abs(room_x - x) + abs(room_y - y)
                if (not(srch_main) and self.grid[y][x].walkable) or (srch_main and self.grid[y][x].main) and not(this_room) and new_dist < best_dist:
                    conn_point = (x,y)
                    best_dist = new_dist
        print(str(room_x)+", "+str(room_y))
        print(str(conn_point))
        return conn_point

    def create_hallways(self, srch_main):
        for r in self.rooms:
            # Check that room is not already connected
            if (not(srch_main) and not(r.connected)) or (srch_main and self.grid[r.y1][r.x1].main == False):
                # Find the closest room or hallway to connect to
                room_x = randint(r.x1, r.x2-1)
                room_y = randint(r.y1, r.y2-1)
                (conn_x, conn_y) = self.search_conn_point(srch_main, room_x, room_y, r.x1, r.x2, r.y1, r.y2)
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
                        self.grid[room_y][x].walkable = True
                if room_y != conn_y:
                    for y in y_range:
                        self.grid[y][conn_x].value = "&"
                        self.grid[y][conn_x].walkable = True

                if srch_main == True:
                    r.main = True
                    break # Only connect one room to main per cycle
                else:
                    r.connected = True

    def place_start_exit(self):
        # pick a random room to place the start in
        num_rooms = len(self.rooms)
        start_room_num = randint(0,num_rooms-1)
        # pick another random room to be the exit
        exit_room_num = randint(0,num_rooms-1)
        while exit_room_num == start_room_num: ### Just need to make sure they're not equal. Probably is a better way.
            exit_room_num = randint(0,num_rooms-1)
        
        startroom = self.rooms[start_room_num]
        exitroom = self.rooms[exit_room_num]

        print("Start Room: "+str(start_room_num)+", End Room: "+str(exit_room_num))

        self.startx = randint(startroom.x1+1, startroom.x2-1)
        self.starty = randint(startroom.y1+1, startroom.y2-1)
        self.exitx = randint(exitroom.x1+1, exitroom.x2-1)
        self.exity = randint(exitroom.y1+1, exitroom.y2-1)

        self.grid[self.starty][self.startx].value = "S"
        self.grid[self.exity][self.exitx].value = "E"

        print("Start: ("+str(self.startx)+","+str(self.starty)+")"+", End: "+"("+str(self.exitx)+","+str(self.exity)+")")

    # flood fill all "connected" cells to find outlier rooms
    def flood_fill(self, x, y):
        print("fill cell: " + str(x) + ", " + str(y))
        if self.grid[y][x].walkable == True and self.grid[y][x].main == False:
            self.grid[y][x].main = True
            if x < self.stage_w-2:
                self.flood_fill(x+1, y)
            if y < self.stage_h-2:
                self.flood_fill(x, y+1)
            if x > 0:
                self.flood_fill(x-1, y)
            if y > 0:
                self.flood_fill(x, y-1)
            if self.grid[y][x].value != "S" and self.grid[y][x].value != "E":
                self.grid[y][x].value = "="
        else:
            return

    def check_connected(self):
        for x in range(0, self.stage_w - 1):
            for y in range(0, self.stage_h - 1):
                if self.grid[y][x].walkable == True and self.grid[y][x].main == False:
                    self.all_cells_conn == False

    # Draw all the floors of the defined rooms
    def draw_rooms(self):
        # For each room, draw the floor
        for r in self.rooms:
            for i in range(r.x1,r.x2):
                for j in range(r.y1,r.y2):
                    self.grid[j][i].value = "&"
                    self.grid[j][i].walkable = True
    
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

    def write_output(self, name):
        outfile = open("levels/level" + name + "_gen.txt", "w")
        # Write to output file
        for j in range(0, self.stage_h - 1):
            map_line = ''
            for i in range(0,self.stage_w - 1):
                map_line += self.grid[j][i].value
            map_line += "\n"
            outfile.writelines(map_line)
        outfile.close()

# Test code, generate level to test if it's working
# Eventually, create a function that does all this with parameters
# that can be fed in from the top level. 
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
# Connect rooms to each other once
level1.create_hallways(srch_main = False)

# Write room file before fill shenanigans
level1.write_output("1")

level1.place_start_exit()
# Connect all rooms to main
# while level1.all_cells_conn == False:
level1.flood_fill(level1.startx, level1.starty)
level1.write_output("1_fill")
level1.create_hallways(srch_main = True)

# Write to output file
level1.write_output("1_hallways")

print("Done!") 