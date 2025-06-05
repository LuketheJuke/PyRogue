from dice import roll

# Import item stats from a spreadsheet?
# What info would there need to be?
#   name
#   attack if equipped
#   defense if equipped
#   use effects
#   

class item():
    def __init__(self, item_id):
        self.name = item_id.name
        self.item_type = item_id.item_type
        self.description = item_id.description

    def use():
        pass
    
    def hit():
        pass

# Making classes for weapons and armor
# Right now they're simple but they'll be useful if I add more weapon stats like durability
class weapon():
    def __init__(self, name, attacknum, attack):
        self.name = name
        self.attacknum = attacknum # number of times to roll the attack damage
        self.attack = attack

    def use():
        pass

dagger = weapon("Dagger", 1, 4)
long_sword = weapon("Long Sword", 1, 8)
battle_axe = weapon("Battle Axe", 1, 12)


class armor():
    def __init__(self, name, defense):
        self.name = name
        self.defense = defense

shirt = armor("Plain Shirt", 0)
leather_armor = armor("Leather Armor", 1)
chain_mail = armor("Chain Mail", 2)
plate_mail = armor("Plate Mail", 3)


# potions:
# healing potion - heals
class potion():
    def __init__(self, name, level):
        self.name = name = name
        self.level = level

    # Heal the player
    def use(self):
        heal = roll(self.level, 4) # heal for 2d4
        return heal

empty = potion(" ", 0) # empty object
healing_potion = potion("Healing Potion", 2)
# greater_healing_potion = potion("Greater Healing Potion", 4)