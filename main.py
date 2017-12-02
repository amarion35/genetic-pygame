import pygame
from Ship import Ship
from Target import Target
from Rectangle import Rectangle
from colors import *
import random
import math
import time

pygame.init()


screen = pygame.display.set_mode([800, 600])
done = False
clock = pygame.time.Clock()
random.seed()

speed_simulation = 2

instance = 100
duration = 5. / speed_simulation
genome_size = 4
size_pop = 100
size_surviving_pop = size_pop // 3

state = 0
target = Target(screen, 700, 500)
rect1 = Rectangle(screen, 550, 350, 200, 20, -45)
rect2 = Rectangle(screen, 350, 350, 200, 20, 45)
rect3 = Rectangle(screen, 650, 450, 200, 20, -45)
obstacles = [rect1, rect2]
ships = []
speed = 6

max_score_all_time = 0


def gen_ships():
    for k in range(0, size_pop):
        ship = Ship(screen)
        ship.genome = [(random.randrange(2*speed_simulation, 8*speed_simulation),
                        random.randrange(-180, 180))] +\
                      [(random.randrange(2*speed_simulation, 8*speed_simulation),
                        random.randrange(-160, 160))
                       for i in range(genome_size-1)]
        ship.setSpeed(ship.genome[0][0], ship.genome[0][1])
        ship.setObstacles(obstacles)
        ships.append(ship)
    return ships


def select_ships():
    ships.sort(key=lambda s: s.score, reverse=True)
    return ships[:size_surviving_pop]


def mutations():
    for i, ship in enumerate(ships):
        ships[i].genome = [(g[0] + ((j+1*genome_size)/(2*genome_size))*(random.randrange(0, 100)/100. - 0.5)/speed_simulation*(1+ships[i].score**2+ships[i].score**3),
                            g[1] + ((j+1*genome_size)/(2*genome_size))*(random.randrange(-10, 10))/(0.5+ships[i].score**2+ships[i].score**3))
                           for j, g in enumerate(ships[i].genome)]
    return ships


def duplicate():
    for k in range(size_pop - size_surviving_pop):
        ship = Ship(screen)
        ship.copy(ships[k % size_surviving_pop])
        ships.append(ship)
    return ships


def reinit():
    for ship in ships:
        ship.init_position()
    return ships


def draw():
    for ship in ships:
        ship.draw()


def setSpeed(state):
    for ship in ships:
        ship.setSpeed(ship.genome[min(state, len(ship.genome)-1)][0], ship.genome[min(state, len(ship.genome)-1)][1])


def move():
    for ship in ships:
        ship.move()


def score(max_score_all_time):
    for ship in ships:
        ship.scoring(target)
    max_score = max(ship.score for ship in ships)
    if max_score > max_score_all_time:
        max_score_all_time = max_score
    for ship in ships:
        ship.score /= max_score
    return max_score_all_time


def all_ships_out():
    all_out = True
    for ship in ships:
        if ship.vx != 0 or ship.vy != 0:
            all_out = False
    return all_out


ships = gen_ships()
t = time.clock()
while not done:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    screen.fill(WHITE)
    for obst in obstacles:
        obst.draw()
    target.draw()
    draw()
    move()
    pygame.display.flip()
    if (time.clock() -t > state*duration/(genome_size+1)):
        setSpeed(state)
        state += 1

    if (all_ships_out() or time.clock() - t > duration) and instance > 0:
        instance -= 1
        state = 0
        max_score_all_time = score(max_score_all_time)
        ships = select_ships()
        ships = duplicate()
        ships = mutations()
        ships = reinit()
        setSpeed(0)
        t = time.clock()
        # ships = gen_ships()


