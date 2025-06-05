from random import randint

# Object used for rooms
class Room():
    # Draw a rectangle to create a room
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.x2 = x + w
        self.y1 = y
        self.y2 = y + h
        self.connected = False
        self.main = False
        self.enemies = 0
        self.items = 0
        self.start = False
        self.exit = False
    
    def center(self):
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

    def place_enemies(self):
        self.enemy_max = 3
        # Check how many enemies we have, return True if we can place another
        # Place similar enemies together, like goblins
        if self.enemies < self.enemy_max:
            # place an enemy
            self.enemies += 1
        # Once we hit the max, return "full"
        # Determine enemy x and y, return value to mapgen to place into position
    
    def place_items(self, item_num):
        # Place items in random rooms
        self.items += item_num
        
        return self.itemnum
    
    def count_items(self):
        for i in range(self.x1, self.x2):
            for j in range(self.y1, self.y2):
                