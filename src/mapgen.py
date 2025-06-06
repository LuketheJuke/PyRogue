import pygame as pg
import numpy as np
import cell as cell
import room as room
import leaf as leaf
import tileset
from random import randint

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
        self.map = []
        self.totalarea = 0
        for y in range(height):
            row = []
            for x in range(width):
                row.append(cell.Cell(x, y))
            self.map.append(row)

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
        if self.Leaves[index].w > 5 and self.Leaves[index].h > 5:
            (L1, L2) = self.Leaves[index].split()
            # Store new leaves in the current index
            self.Leaves[index] = L1
            # Insert second new leaf in the next index
            self.Leaves.insert(index+1, L2)
        else:
            print("Leaf too small to split.")
            exit

    # Create rooms within the defined leaves
    def create_rooms(self):
        # Set a maximum and minimum number of rooms
        max_rooms = 12
        min_rooms = 7
        max_area = min_rooms * 60
        self.rooms = []
        # Keep generating rooms until we hit the max_rooms value 
        for L in self.Leaves:
            if not(L.has_room):
                gen_chance = randint(0,100)
                # Generate rooms randomly, as long as we haven't reached max
                if gen_chance > 30 and len(self.rooms) < max_rooms and self.totalarea < max_area:
                    # print("Creating new room.")
                    # Randomize room size, dependent on dimensions of leaf
                    if L.w == 5:
                        w = 3
                    else:
                        w = randint(2, L.w - 2)
                    if L.h == 5:
                        h = 3
                    else:
                        h = randint(2, L.h - 2)
                    area = w * h
                    # Generate x and y corner of room
                    if L.x1+1 == L.x2-w-1:
                        x = L.x1+1
                    else:
                        x = randint(L.x1+1, (L.x2-w)-1)
                    if L.y1+1 == (L.y2-h)-1:
                        y = L.y1+1
                    else:
                        y = randint(L.y1+1, (L.y2-h)-1)
                    new_room = room.Room(x, y, w, h)
                    self.draw_room(new_room)
                    if len(self.rooms) > 0: # Check if other rooms exist before drawing hallway
                        self.create_hallway(new_room)
                    self.rooms.append(new_room)
                    rooms_empty = 1
                    self.totalarea += area
                    L.has_room = True
        
        # Run again if we didn't generate enough rooms
        if len(self.rooms) < min_rooms and self.totalarea < max_area:
            self.create_rooms()
    
    # Draw the floor of a room
    def draw_room(self, room):
        # For each room, draw the floor
        for i in range(room.x1,room.x2):
            for j in range(room.y1,room.y2):
                self.map[j][i].value = "*"
                self.map[j][i].walkable = True
                self.map[j][i].room = True

    # Create a hallway connecting new room to the rest of the level, to the nearest connecting point
    def create_hallway(self, room):
        # Find the closest room or hallway to connect to
        room_x = randint(room.x1, room.x2-1)
        room_y = randint(room.y1, room.y2-1)
        (conn_x, conn_y) = self.search_conn_point(room_x, room_y, room.x1, room.x2, room.y1, room.y2)
        # Set the x range and y range
        if room_x < conn_x:
            x_range = range(room_x, conn_x+1)
        else:
            x_range = range(conn_x, room_x+1)
        if room_y < conn_y:
            y_range = range(room_y, conn_y+1)
        else:
            y_range = range(conn_y, room_y+1)
        # Draw a hallway connecting the room point with connect point
        if room_x != conn_x:
            for x in x_range:
                self.map[room_y][x].value = "*"
                self.map[room_y][x].walkable = True
        if room_y != conn_y:
            for y in y_range:
                self.map[y][conn_x].value = "*"
                self.map[y][conn_x].walkable = True

    def draw_walls(self):
        for x in range(0, self.stage_w): 
            for y in range(0, self.stage_h):
                if self.map[y][x].walkable == True: # Generate walls around walkable terrain
                    outer_cells = [self.map[y+1][x], self.map[y][x+1], self.map[y-1][x], self.map[y][x-1],
                                   self.map[y+1][x+1], self.map[y-1][x+1], self.map[y-1][x-1], self.map[y+1][x-1]]
                    for c in outer_cells:
                        if c.walkable == False:
                            c.value = "="
                            c.wall = True
                            # Determine which side of the floor this is on to set the type of wall (east, west, etc).

    # Search the whole map for the closest connectable point
    # srch_main modifies it to search for a point connected to the main cluster
    def search_conn_point(self, room_x, room_y, x1, x2, y1, y2):
        best_dist = 50
        conn_point = ()
        for x in range(0, self.stage_w): 
            for y in range(0, self.stage_h):
                # Check if we're in this room
                this_room = (x >= x1 and x <= x2) and (y >= y1 and y <= y2)
                # Initial distance check
                new_dist = abs(room_x - x) + abs(room_y - y)
                if self.map[y][x].walkable and not(this_room) and new_dist < best_dist:
                    conn_point = (x,y)
                    best_dist = new_dist
        # print(str(room_x)+", "+str(room_y))
        if conn_point == ():
            print("Couldn't find connect point.")
            exit
        else:
            # print(str(conn_point))
            return conn_point

    def place_start_exit(self):
        # pick a random room to place the start in
        num_rooms = len(self.rooms)
        start_room_num = randint(0,num_rooms-1)
        # pick another random room to be the exit
        exit_room_num = randint(0,num_rooms-1)
        while exit_room_num == start_room_num: ### Just need to make sure they're not equal. Probably is a better way.
            exit_room_num = randint(0,num_rooms-1)
        
        # Label start and exit rooms
        startroom = self.rooms[start_room_num]
        exitroom = self.rooms[exit_room_num]

        # Place start and exit in a random location in their room
        self.startx = randint(startroom.x1+1, startroom.x2-1)
        self.starty = randint(startroom.y1+1, startroom.y2-1)
        self.exitx = randint(exitroom.x1+1, exitroom.x2-1)
        self.exity = randint(exitroom.y1+1, exitroom.y2-1)

        # Label rooms and cells as start/exit
        startroom.start = True
        exitroom.exit = True
        self.map[self.starty][self.startx].start = True
        self.map[self.exity][self.exitx].exit = True

        # Debug statements
        # print("Start Room: "+str(start_room_num)+", End Room: "+str(exit_room_num))
        # print("Start: ("+str(self.startx)+","+str(self.starty)+")"+", End: "+"("+str(self.exitx)+","+str(self.exity)+")")

    # Populate level with items and enemies
    def populate_level(self, item_min, item_max, enemy_min, enemy_max):
        item_total = 0
        # Cycle through rooms, place items until we hit max value
        # while item_total < item_min:
        while item_total < item_max:
            for r in self.rooms:
                item_chance = randint(0,1) # 50% chance to place item
                if item_chance == 1:
                    [item_id, item_x, item_y] = r.place_item()
                    item_total += 1
                    self.map[item_y][item_x].item_id = item_id
        # # Place enemies, with enemies more likely in rooms with items
        # while enemy_total < enemy_min:
        #     for r in self.rooms:
        #         if enemy_total < enemy_max:
        #             enemy_num = r.place_enemies
        #             enemy_total += enemy_num
        #         else:
        #             exit


    # flood fill all "connected" cells to find outlier rooms
    def flood_fill(self, x, y):
        # print("fill cell: " + str(x) + ", " + str(y))
        if self.map[y][x].walkable == True and self.map[y][x].main == False:
            self.map[y][x].main = True
            if x < self.stage_w-2:
                self.flood_fill(x+1, y)
            if y < self.stage_h-2:
                self.flood_fill(x, y+1)
            if x > 0:
                self.flood_fill(x-1, y)
            if y > 0:
                self.flood_fill(x, y-1)
            if self.map[y][x].value != "p" and self.map[y][x].value != "f":
                self.map[y][x].value = "="
        else:
            return
    
    # Draw the outline of the leaves
    def draw_leaf_borders(self):
            # Loop through x and y coorindates to draw outer edge of leaf
            for L in self.Leaves:
                # print("L.x1 = "+str(L.x1))
                # print("L.x2 = "+str(L.x2))
                # print("L.y1 = "+str(L.y1))
                # print("L.y2 = "+str(L.y2))
                for i in range(L.x1,L.x2):
                    # print(i)
                    self.map[L.y1][i].value = "_"
                    self.map[L.y2-1][i].value = "_"
                for i in range(L.y1,L.y2):
                    # print(i)
                    self.map[i][L.x1].value = "_"
                    self.map[i][L.x2-1].value = "_"
        
    def write_output(self, name):
        outfile = open("levels/level" + name + "_gen.txt", "w")
        # Write to output file
        for j in range(0, self.stage_h):
            map_line = ''
            for i in range(0,self.stage_w):
                map_line += self.map[j][i].value
            map_line += "\n"
            outfile.writelines(map_line)
        outfile.close()

def gen_level(width, height, dun_level):
        # Generate a map
        level = MapGen(width, height, dun_level)
        level.init_leaf()

        # Cycle through leaves and split until we reach a certain amount of splits
        # Modify this to be dependent on level size in the future
        for i, val in enumerate(level.Leaves):
            if val.depth < 2:
                level.create_leaf(i)
        for i, val in enumerate(level.Leaves):
            if val.depth < 3:
                level.create_leaf(i)
        for i, val in enumerate(level.Leaves):
            if val.depth < 4:
                level.create_leaf(i)

        # Create rooms within leaves, draw walls, place start/exit
        level.create_rooms()
        level.draw_walls()
        # level1.draw_leaf_borders()
        level.place_start_exit()

        # Place items and enemies
        level.populate_level(item_min = 4, item_max = 8, enemy_min = 4, enemy_max = 8)

        # Write to output file
        level.write_output(str(dun_level))
        return [level.map, level.startx, level.starty]

gen_level(60, 32, 1)