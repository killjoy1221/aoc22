from itertools import pairwise
from typing import NamedTuple
from enum import Enum, auto


class Position(NamedTuple):
    x: int
    y: int

    def add(self, x: int, y: int):
        return Position(self.x + x, self.y + y)


class Tile(Enum):
    ROCK = auto()
    SAND = auto()


class FloorDict(dict[Position, Tile]):
    def __init__(self, d: dict[Position, Tile], floor_y):
        super().__init__(d)
        self.floor_y = floor_y

    def __getitem__(self, __key: Position) -> Tile:
        if __key.y == self.floor_y:
            return Tile.ROCK
        return super().__getitem__(__key)

    def __contains__(self, __o: Position) -> bool:
        if __o.y == self.floor_y:
            return True
        return super().__contains__(__o)


class Grid:
    sand_entry_position = Position(500, 0)

    def __init__(self, rocks: list[list[Position]]):
        grid = {}

        for line in rocks:
            for step1, step2 in pairwise(line):
                if step1.x == step2.x:
                    for y in nrange(step1.y, step2.y):
                        grid[Position(step1.x, y)] = Tile.ROCK
                if step1.y == step2.y:
                    for x in nrange(step1.x, step2.x):
                        grid[Position(x, step1.y)] = Tile.ROCK

        floor_y = max(p.y for p in grid) + 2
        self.grid = FloorDict(grid, floor_y)

    def get_tiles(self, tile: Tile):
        return [k for k, v in self.grid.items() if v is tile]

    def is_in_bottomless_pit(self, pos: Position):
        same_x = [p.y for p in self.grid.keys() if p.x == pos.x]
        return not bool(same_x) or max(same_x) < pos.y

    def drop_sand(self, *, until_blocked=False):
        sand_pos = self.sand_entry_position

        if self.sand_entry_position in self.grid:
            return False

        while True:
            for x in 0, -1, 1:
                pos = sand_pos.add(x, 1)
                if pos not in self.grid and pos.add(0, -1):
                    if not until_blocked and self.is_in_bottomless_pit(pos):
                        return False
                    sand_pos = pos
                    break
            else:
                break

        self.grid[sand_pos] = Tile.SAND
        return True

    def render(self, x1: int, y1: int, x2: int, y2: int):
        for y in range(y1, y2 + 1):
            print(f"{y:3}", end=" ")
            for x in range(x1, x2 + 1):
                pos = Position(x, y)
                if pos == self.sand_entry_position:
                    c = "+"
                elif pos not in self.grid:
                    c = "."
                elif self.grid[pos] == Tile.ROCK:
                    c = "#"
                else:
                    c = "o"
                print(c, end="")
            print()
        print()


def parse_rocks(data: str):
    return [
        [Position(*map(int, step.split(","))) for step in line.split(" -> ")]
        for line in data.splitlines()
    ]


def nrange(a: int, b: int):
    """A range that iterates min to max"""
    mx = max(a, b)
    mn = min(a, b)
    yield from range(mn, mx + 1)


def main(data: str):
    grid = Grid(parse_rocks(data))

    while grid.drop_sand():
        pass

    sands = grid.get_tiles(Tile.SAND)
    print("Part 1:", len(sands))

    while grid.drop_sand(until_blocked=True):
        pass

    # rocks = grid.get_tiles(Tile.ROCK)
    # xs = {r.x for r in rocks}
    # ys = {r.y for r in rocks}
    # mxy = max(ys) + 2
    # mnx = min(xs) - mxy
    # mxx = max(xs) + mxy
    # grid.render(mnx, 0, mxx, mxy)

    sands = grid.get_tiles(Tile.SAND)
    print("Part 2:", len(sands))
