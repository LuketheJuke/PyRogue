import pygame as pg
import numpy as np
from random import randint

# Class used to define the leaves that the map is split into
# Has functions to split into smaller leaves
class Leaf():
    def __init__(self, x, y, w, h, depth):
        self.x1 = x
        self.x2 = x + w - 1
        self.y1 = y
        self.y2 = y + h - 1
        self.w = w
        self.h = h
        self.center_x = int((self.x1 + self.x2) / 2)
        self.center_y = int((self.y1 + self.y2) / 2)
        self.depth = depth # Number of splits on this leaf
        self.has_room = False

    # Determine x and y coordinates to split the leaf and return child leaves
    def split(self):
        split_scale = .1 # Vary split location by 10%

        # If the section is very wide or very tall, split it along the longer side
        if self.w > 2.2 * self.h or self.h < 7:
            split_dir = 1 # Split vertically
        elif self.h > 1.6 * self.w or self.w < 9:
            split_dir = 0 # Split horizontally
        else:
            split_dir = randint(0,1)

        if split_dir == 1: # Split vertically
            split_x = randint(round((self.w/2)-self.w*split_scale), round((self.w/2)+self.w*split_scale))
            # print("Split vertically along x coord " + str(split_x))
            w1 = split_x
            w2 = self.w - split_x
            h1 = self.h
            h2 = self.h
            new_x = self.x1 + split_x
            new_y = self.y1
        else: #Split horizontally
            split_y = randint(round((self.h/2) - self.h * split_scale), round((self.h/2) + self.h * split_scale))
            # print("Split horizontally along y coord " + str(split_y))
            w1 = self.w
            w2 = self.w
            h1 = split_y
            h2 = self.h - split_y
            new_x = self.x1
            new_y = self.y1 + split_y

        # Increment depth to indicate there's been an additional split
        depth = self.depth+1

        # Create child leaves, return them as part of this function
        C1 = Leaf(self.x1, self.y1, w1, h1, depth)
        C2 = Leaf(new_x, new_y, w2, h2, depth)
        return(C1,C2)