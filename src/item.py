import csv
import player
from dice import roll

# Load csv file with item info
with open('src/data/item_data.csv', newline='') as csvfile:
    item_data = []
    index = 0
    itemreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in itemreader:
        item_data.append(row)

# Load csv file with weapon info
# with open('src/data/weapon_data.csv', newline='') as csvfile:
#     weapon_data = []
#     index = 0
#     weaponreader = csv.reader(csvfile, delimiter=',', quotechar='|')
#     for row in weaponreader:
#         weapon_data.append(row)

# Put all item_ids into a list
item_ids = []
for data in item_data[1:]:
    item_ids.append(data[0])

print(item_ids)

class item():
    def __init__(self, item_id):
        # Search item_data for item_id
        for data in item_data:
            if data[0] == item_id:
                print("Item " + data[0] + " found!")
                self.name = data[1]
                self.target = data[2]
                self.effect = data[3]
                self.dice = data[4]
                self.sides = data[5]
                self.modifier = data[6]
                self.duration = data[7]
                self.description = data[8]
                found = True
        if not(found):
            print("Item not found.")
            exit

    def use(self, target):
        if self.effect == heal:
            target.health += roll(self.dice, self.sides) + self.modifier
            if target.health > target.health_max:
                target.health = target.health_max

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
