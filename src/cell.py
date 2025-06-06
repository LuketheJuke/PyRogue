import pygame as pg
import numpy as np
from random import randint

# Each cell stores certain parameters to be easily checkable
class Cell():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.occupied = False
        self.hostile = False
        self.item_id = ""
        self.walkable = False
        self.wall = False
        self.value = "."
        self.start = False
        self.exit = False

# Edit this to keep track of what's in the cell:
# Structure: floor, wall, door, stair
# Item: weapon, potion, armor, chest
# NPC: enemy, ally