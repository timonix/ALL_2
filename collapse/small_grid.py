# rules
# tile 0 can be next to tile 0
# tile 1 can be next to nothing

class Tile:
    def __init__(self, tile_type):
        self.type = tile_type
        self.valid_neighbour = {}

    def add_valid_neighbour(self, n, dir):
        if dir in self.valid_neighbour:
            self.valid_neighbour[dir].add(n)
        else:
            self.valid_neighbour[dir] = {n}


tile_0 = Tile("Tile 0")
tile_1 = Tile("tile_1")
tile_0.add_valid_neighbour(tile_0, "north")
tile_0.add_valid_neighbour(tile_0, "south")
tile_0.add_valid_neighbour(tile_1, "east")

tile_1.add_valid_neighbour(tile_0, "west")
tile_1.add_valid_neighbour(tile_1, "north")
tile_1.add_valid_neighbour(tile_1, "south")
all_tiles = {tile_0, tile_1}


class MetaTile:
    directions = {"north", "west", "south", "east"}

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

    def neighbouring_tiles(self):
        n = {}
        if (self.location[0] - 1, self.location[1]) in self.world:
            n["west"] = self.world[self.location[0] - 1, self.location[1]]
        if (self.location[0] + 1, self.location[1]) in self.world:
            n["east"] = self.world[self.location[0] + 1, self.location[1]]
        if (self.location[0], self.location[1] - 1) in self.world:
            n["north"] = self.world[self.location[0], self.location[1] - 1]
        if (self.location[0], self.location[1] + 1) in self.world:
            n["south"] = self.world[self.location[0], self.location[1] + 1]
        return n

    def collapse(self):
        neighbouring_tiles = self.neighbouring_tiles()
        for direction in MetaTile.directions:
            if direction in neighbouring_tiles:
                intersect = self.valid_neighbours[direction].intersection(neighbouring_tiles[direction].valid_tiles)
                if neighbouring_tiles[direction].valid_tiles != intersect:
                    neighbouring_tiles[direction].valid_tiles = intersect
                    neighbouring_tiles[direction].collapse()



grid = {}
for x in range(2):
    for y in range(2):
        grid[(x, y)] = (MetaTile((x, y), grid))

for mt in grid.values():
    print(mt.valid_tiles)


for mt in grid.values():
    mt.collapse()

for mt in grid.values():
    print(mt.valid_tiles)
print()

print()
for mt in grid.values():
    print(mt.valid_tiles)

print(grid[(0, 0)].valid_neighbours)
