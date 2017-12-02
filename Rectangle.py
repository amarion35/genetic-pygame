import pygame
from colors import *
from Position import Position
import math

class Rectangle:

    def __init__(self, surface, xpos, ypos, width, height, angle):
        self.position = Position(xpos, ypos)
        self.width = width
        self.height = height
        self.surface = surface
        self.angle = angle
        self.offset = Position(width / 2., height / 2.)
        self.points = []
        self.draw()

    def draw(self):
        self.points = self.rotate([
            [self.position.x - self.offset.x, self.position.y + self.offset.y],
            [self.position.x + self.offset.x, self.position.y + self.offset.y],
            [self.position.x + self.offset.x, self.position.y - self.offset.y],
            [self.position.x - self.offset.x, self.position.y - self.offset.y],
        ])
        self.rectangle = pygame.draw.polygon(self.surface, BLACK, self.points)


    def rotate(self, points):
        ox, oy = self.position.x, self.position.y

        result = []

        for point in points:
            px, py = point[0], point[1]

            qx = ox + math.cos(self.angle) * (px - ox) - math.sin(self.angle) * (py - oy)
            qy = oy + math.sin(self.angle) * (px - ox) + math.cos(self.angle) * (py - oy)
            result.append([qx, qy])
        return result
