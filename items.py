from dice import roll

# weapon attributes:
# name, [attackmin, attackmax]
weapons = [["Dagger", [1,4]], 
        ["Short Sword", [2,4]], 
        ["Long Sword", [2,6]], 
        ["Battle Axe", [1,12]], 
        ["Claymore", [3,6]]]

# potions:
# healing potion - heals
# armor potion - raises armor for a few turns
# strength potion - raises attack for a few turns
# sight potion - reveals the whole map

class mod_potion():
    def __init__(self, name):
        self.name = name

    def healing(self, health, grade):
        heal = roll(grade,4)
        health += heal
        print("Healed  by " + str(heal))
    
    def sight(self)

# armor types
# name, armor value
armor = [["Shirt", 0], 
        ["Leather", 1], 
        ["Chain", 2], 
        ["Plate", 3], 
        ["Dragon", 4]]