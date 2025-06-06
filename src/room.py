from random import randint
import item
import mob

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
        self.items = [] # list of items
        self.enemies = [] # list of enemies
        self.start = False
        self.exit = False
    
    def center(self):
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

    def place_enemy(self):
        # Check how many enemies we have, return True if we can place another
        if self.enemies < self.enemy_max:
            # place an enemy
            self.enemies += 1
        # Once we hit the max, return "full"
        # Determine enemy x and y, return value to mapgen to place into position
        # Create "mob" object. The mobs are only initialized here, but mob info should be 
        # maintained in the "mob" objects. 
        enemy_x = randint(self.x1,self.x2)
        enemy_y = randint(self.y1,self.y2)
        enemy_type = randint(0,4) # Pick a random enemy from the list

        enemy = mob(enemy_x, enemy_y, enemy_type)
    
    def place_item(self):
        # Place item in a random spot in the room
        item_x = randint(self.x1,self.x2)
        item_y = randint(self.y1,self.y2)
        # grab an item from item_list
        item_id = randint(0,len(item.item_ids))
        self.items.append([item_id, item_x, item_y]) # use item_type for this, for now just use the health potion index
        return [item_id, item_x, item_y]
    
    def count_enemies(self):
        len(enemies)

    def count_items(self):
        # count list of items
        len(items)

    # def get_item_location(self):

    # Function ideas:
    # place_enemy_group
    # - calls place_enemy multiple times to place a few enemies in a room of a thematic type
    # get_enemy_info
    # - Can be called by mapgen or any other function to return the type and location of enemies in a room
    #   