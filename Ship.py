from Position import *
import pygame
from colors import *
import math
import random
import matplotlib.path as mplPath
import numpy as np
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

class Ship:

    def __init__(self, screen):
        self.position = Position(400, 300)
        self.size = 5
        self.screen = screen
        self.angle = math.pi / 2
        self.offset = Position(2 * self.size, 2 * self.size)
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0
        self.step = 0
        self.score = 0
        self.obstacles = []
        self.enable = True
        random.seed()
        self.polygon = self.draw()
        self.genome = [0, 45, 90]

    def draw(self):
        polygon = pygame.draw.polygon(self.screen, BLUE, self.rotate([
            [self.position.x - self.offset.x, self.position.y - self.offset.y],
            [self.position.x - self.offset.x, self.position.y - self.offset.y + 4 * self.size],
            [self.position.x - self.offset.x + 4 * self.size, self.position.y - self.offset.y + 2 * self.size]
        ]))
        self.polygon = polygon
        return polygon

    def setSpeed(self, speed, angle):
        self.angle = angle
        self.vx = speed * math.cos(math.radians(angle))
        self.vy = speed * math.sin(math.radians(angle))

    def move(self):
        x = self.position.x
        y = self.position.y
        if not self.is_inside(x, y) or self.is_colliding():
            self.enable = False
        if self.enable:
            self.step += 1
            self.vx += self.ax/5
            self.vy += self.ay/5
            self.position.x += self.vx
            self.position.y += self.vy

    def rotate(self, points):
        vx = self.vx
        vy = self.vy
        angle = 0
        if (vx, vy) != (0, 0):
            vx, vy = vy/(math.sqrt(vx**2+vy**2)), vx/(math.sqrt(vx**2+vy**2))
            if vy>=0: angle = - math.acos(vx) + math.pi/2
            else: angle = math.acos(vx) + math.pi/2

        ox, oy = self.position.x, self.position.y

        result = []
        for point in points:
            px, py = point[0], point[1]

            qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
            qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
            result.append([qx, qy])

        return result

    def is_inside(self, x, y):
        if 0 <= x <= 1000 and 0 <= y <= 800:
            return True
        return False

    def is_colliding(self):
        point = Point(self.position.x, self.position.y)
        for obstacle in self.obstacles:
            polygon = Polygon(obstacle.points)
            if polygon.contains(point):
                return True
        return False

    def scoring(self, target):
        distance = math.sqrt((target.position.x - self.position.x)**2 + (target.position.y - self.position.y)**2)
        if distance != 0:
            s = 1./distance
        else:
            s = 10000
        if not self.enable:
            s *= 0.85
        self.score = s


    def init_position(self):
        self.enable = True
        self.score = 0
        self.position.x = 400
        self.position.y = 300

    def setObstacles(self, obstacles):
        self.obstacles = obstacles

    def copy(self, ship):
        self.position = Position(ship.position.x, ship.position.y)
        self.size = ship.size
        self.screen = ship.screen
        self.angle = ship.angle
        self.offset = ship.offset
        self.vx = ship.vx
        self.vy = ship.vy
        self.ax = ship.ax
        self.ay = ship.ay
        self.step = ship.step
        self.score = ship.score
        self.obstacles = ship.obstacles
        self.enable = ship.enable
        self.polygon = ship.polygon
        self.genome = ship.genome

