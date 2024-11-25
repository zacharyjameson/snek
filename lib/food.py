# food.py
import pygame
import random


class Food:
    def __init__(self, block_size, bounds):
        self.block_size = block_size
        self.bounds = bounds
        self.respawn()

    def respawn(self):
        self.x = random.randint(
            0, self.bounds[0] - self.block_size) // self.block_size * self.block_size
        self.y = random.randint(
            0, self.bounds[1] - self.block_size) // self.block_size * self.block_size

    def draw(self, game, window):
        game.draw.rect(window, (0, 255, 0), (self.x, self.y,
                                             self.block_size, self.block_size))
