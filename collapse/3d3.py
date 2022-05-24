# rules
# tile 0 can be next to tile 0
# tile 1 can be next to nothing

import copy
import random


class Tile:
    def __init__(self, tile_type):
        self.type = tile_type
        self.valid_neighbour = {}

    def add_valid_neighbour(self, n, dir):

        if dir in self.valid_neighbour:
            self.valid_neighbour[dir].add(n)
        else:
            self.valid_neighbour[dir] = {n}

directions = {"north": +1, "south": -1, "east": +2, "west": -2, "down": -3, "up": +3}



air = Tile("air")
water = Tile("water")
ground = Tile("ground")
building = Tile("building")

air.add_valid_neighbour(building, "north")
air.add_valid_neighbour(building, "south")
air.add_valid_neighbour(building, "east")
air.add_valid_neighbour(building, "west")

air.add_valid_neighbour(air, "north")
air.add_valid_neighbour(air, "south")
air.add_valid_neighbour(air, "east")
air.add_valid_neighbour(air, "west")

building.add_valid_neighbour(air, "north")
building.add_valid_neighbour(air, "south")
building.add_valid_neighbour(air, "east")
building.add_valid_neighbour(air, "west")

##############
ground.add_valid_neighbour(ground, "north")
ground.add_valid_neighbour(ground, "south")
ground.add_valid_neighbour(ground, "east")
ground.add_valid_neighbour(ground, "west")

ground.add_valid_neighbour(water, "north")
ground.add_valid_neighbour(water, "south")
ground.add_valid_neighbour(water, "east")
ground.add_valid_neighbour(water, "west")

water.add_valid_neighbour(ground, "north")
water.add_valid_neighbour(ground, "south")
water.add_valid_neighbour(ground, "east")
water.add_valid_neighbour(ground, "west")

water.add_valid_neighbour(water, "north")
water.add_valid_neighbour(water, "south")
water.add_valid_neighbour(water, "east")
water.add_valid_neighbour(water, "west")
##############

air.add_valid_neighbour(water, "down")
air.add_valid_neighbour(ground, "down")
air.add_valid_neighbour(building, "down")
air.add_valid_neighbour(air, "down")
air.add_valid_neighbour(air, "up")

ground.add_valid_neighbour(air, "up")
ground.add_valid_neighbour(building, "up")

building.add_valid_neighbour(air, "up")
building.add_valid_neighbour(building, "up")
building.add_valid_neighbour(ground, "down")

water.add_valid_neighbour(air, "up")

all_tiles = {air, ground, building, water}


class MetaTile:
    def __init__(self, location, world):
        self.world = world
        self.location = location
        self.valid_tiles = all_tiles

        self.valid_neighbours = dict()

        for direction in MetaTile.directions:
            self.valid_neighbours[direction] = set()

        for tile in self.valid_tiles:
            for direction in MetaTile.directions:
                if direction in tile.valid_neighbour:
                    for t in tile.valid_neighbour[direction]:
                        self.valid_neighbours[direction].add(t)

    @staticmethod
    def axis_change(coordinate, axis, change):
        c = list(coordinate)
        c[axis] += change
        return tuple(c)

    def remove_valid_tiles(self, t):
        self.valid_tiles = self.valid_tiles.difference(t)

        new_valid_neighbours = dict()
        for direction in MetaTile.directions:
            new_valid_neighbours[direction] = set()

        for tt in self.valid_tiles:
            for direction in MetaTile.directions:
                if direction in tt.valid_neighbour:
                    for t in tt.valid_neighbour[direction]:
                        new_valid_neighbours[direction].add(t)

        for direction, set_of_valid in new_valid_neighbours.items():
            self.valid_neighbours[direction] = self.valid_neighbours[direction].intersection(set_of_valid)

        self.collapse()

    def remove_random_tile(self):
        tile = [random.choice(list(self.valid_tiles))]
        self.remove_valid_tiles(tile)

    def neighbouring_tiles(self):
        n = {}
        for dir, axis in MetaTile.directions.items():
            new_coord = self.axis_change(self.location, abs(axis) - 1, int(axis / abs(axis)))
            if new_coord in self.world:
                n[dir] = self.world[new_coord]
        return n

    def collapse(self):
        neighbouring_tiles = self.neighbouring_tiles()
        for direction in MetaTile.directions:
            if direction in neighbouring_tiles:
                intersect = self.valid_neighbours[direction].intersection(neighbouring_tiles[direction].valid_tiles)
                if neighbouring_tiles[direction].valid_tiles != intersect:
                    neighbouring_tiles[direction].valid_tiles = intersect
                    neighbouring_tiles[direction].collapse()

GRID_SHAPE = (10,10,2)

def generate_new_grid(shape):
    g = {}
    for x in range(shape[0]):
        for y in range(shape[1]):
            for z in range(shape[2]):
                g[(x, y, z)] = (MetaTile((x, y, z), g))
    for mt in g.values():
        mt.collapse()
    return g


grid = generate_new_grid(GRID_SHAPE)

valid = 0
while (True):
    valid = 0
    for mt in grid.values():
        if len(mt.valid_tiles) == 0:
            valid = -1
            break
        valid = len(mt.valid_tiles) + valid

    if valid == 27:
        break
    if valid == -1:
        # create new grid
        print("new grid")
        grid = generate_new_grid(GRID_SHAPE)

    else:
        rt = random.choice(list(grid.values()))
        if len(rt.valid_tiles) > 1:
            rt.remove_random_tile()

for mt in grid.items():
    print(mt[0], end=" -> ")
    for tile in mt[1].valid_tiles:
        print(tile.type, end="::")
    print()
