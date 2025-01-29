import pygame as pg
import numpy as np
from random import randint

# Each cell stores certain parameters to be easily checkable
class Cell():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.occupied = False
        self.has_item = False
        self.walkable = False
        self.room = False
        self.value = "."