import os

import pygame
from pygame import surface

WIDTH, HEIGHT = (900, 500)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My gme")


world = set()
new_world = set()
potential = set()

from timeit import default_timer as timer

import random

random.seed(0)
for i in range(10000):

    world.add((random.randint(100, 200), random.randint(100, 200)))



def draw():
    WIN.fill((200, 200, 200))
    for point in world:
        WIN.set_at(point, (0, 0, 0))
    pygame.display.update()


def get_neigbours(point):
    return {(point[0] - 1, point[1] - 1),
            (point[0] + 0, point[1] - 1),
            (point[0] + 1, point[1] - 1),
            (point[0] - 1, point[1]),
            (point[0] + 1, point[1]),
            (point[0] - 1, point[1] + 1),
            (point[0] + 0, point[1] + 1),
            (point[0] + 1, point[1] + 1)}


def count_neighbours(neigh):
    return len(neigh.intersection(world))


def update_world():
    global world
    new_world = set()

    for point in world:
        potential = set()
        potential.add(point)
        nn = get_neigbours(point)

        potential = potential.union(nn)


    for point in potential:
        n = count_neighbours(point)
        if n == 3:
            new_world.add(point)
        elif point in world:
            if n == 2:
                new_world.add(point) # survived


    world = new_world


def move_view_left():
    global world
    new_world = set()
    for point in world:
        new_world.add((point[0]+1, point[1]))

    world = new_world


def move_view_right():
    global world
    new_world = set()
    for point in world:
        new_world.add((point[0] - 1, point[1]))

    world = new_world


def move_view(x, y):
    global world
    new_world = set()
    for point in world:
        new_world.add((point[0] - x, point[1] - y))

    world = new_world



def main():
    run = True

    mouse = False
    while run:
        start = timer()
        update_world() # 0.11838300000000013
        end = timer()
        print(end - start)
        draw() # 0.0008307000000007392
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = True
                pygame.mouse.get_rel()
            if event.type == pygame.MOUSEBUTTONUP:
                mouse = False
                pygame.mouse.get_rel()
            if mouse:
                x, y = pygame.mouse.get_rel()
                move_view(-x, -y)


    pygame.quit()


if __name__ == "__main__":
    main()
