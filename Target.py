from Position import *
import pygame
from colors import *


class Target:

    def __init__(self, screen, x ,y):
        self.position = Position(x, y)
        self.size = 5
        self.screen = screen
        self.offset = Position(2 * self.size, 2 * self.size)

    def draw(self):
        pygame.draw.circle(self.screen, RED,
                           [self.position.x,
                            self.position.y],
                           self.size)

