from dataclasses import dataclass
from enum import Enum, auto
from typing import NamedTuple
import numpy as np
import string


def get_height(s: str):
    match s:
        case "S":
            return get_height("a")
        case "E":
            return get_height("z")
        case _:
            return string.ascii_lowercase.index(s)


class Status(Enum):
    START = auto()
    GOAL = auto()
    BLOCKED = auto()
    VALID = auto()
    INVALID = auto()
    UNKNOWN = auto()


class Direction(Enum):
    NORTH = (0, -1)
    SOUTH = (0, +1)
    EAST = (+1, 0)
    WEST = (-1, 0)


all_dirs = Direction.__members__


class Position(NamedTuple):
    x: int
    y: int

    def add(self, dir: Direction):
        x, y = dir.value
        return Position(self.x + x, self.y + y)


@dataclass(frozen=True)
class Location:
    pos: Position
    path: list[Direction]
    status: Status = Status.UNKNOWN


@dataclass
class PathFinder:
    grid: np.ndarray
    start_pos: Position
    targets: list[Position]
    reverse: bool
    visited: set[Position]

    def get_height(self, pos: Position):
        return self.grid[pos.y, pos.x]

    def find_shortest_path(self):
        location = Location(self.start_pos, [], Status.START)

        queue = [location]

        while queue:
            current_location = queue.pop(0)
            for d in Direction.__members__.values():
                new_location = self.explore_in_direction(current_location, d)
                if new_location.status is Status.GOAL:
                    return new_location.path
                if new_location.status is Status.VALID:
                    queue.append(new_location)

        return None

    def location_status(self, old_pos: Position, new_pos: Position):
        if (
            new_pos.x < 0
            or new_pos.x >= self.grid.shape[1]
            or new_pos.y < 0
            or new_pos.y >= self.grid.shape[0]
        ):
            return Status.INVALID

        old_height = self.get_height(old_pos)
        new_height = self.get_height(new_pos)
        if new_pos in self.visited or (
            new_height - old_height < -1
            if self.reverse
            else new_height - old_height > 1
        ):
            return Status.BLOCKED

        if new_pos in self.targets:
            return Status.GOAL

        return Status.VALID

    def explore_in_direction(
        self,
        current_location: Location,
        direction: Direction,
    ):
        new_path = list(current_location.path)
        new_path.append(direction)

        pos = current_location.pos

        new_pos = pos.add(direction)
        status = self.location_status(pos, new_pos)
        new_location = Location(new_pos, new_path, status)
        if new_location.status is Status.VALID:
            self.visited.add(new_pos)

        return new_location


class HeightMap:
    def __init__(self, data: str):
        self.grid = np.array(
            [[get_height(c) for c in line] for line in data.splitlines()]
        )
        self.visited: set[Position] = set()
        line_length = data.index("\n") + 1

        start_pos = data.index("S")
        start_x = start_pos % line_length
        start_y = start_pos // line_length
        self.start_pos = Position(start_x, start_y)

        end_pos = data.index("E")
        end_x = end_pos % line_length
        end_y = end_pos // line_length
        self.end_pos = Position(end_x, end_y)

    def find_all_positions_of(self, height: int) -> list[Position]:
        return [Position(x, y) for y, x in np.argwhere(self.grid == height)]

    def find_shortest_path(
        self,
        start_pos: Position | None = None,
        targets: list[Position] | None = None,
        *,
        reverse: bool = False,
    ):
        if start_pos is None:
            start_pos = self.start_pos
        if targets is None:
            targets = [self.end_pos]

        pf = PathFinder(self.grid, start_pos, targets, reverse, set())
        return pf.find_shortest_path()

    def part_1(self):
        path = self.find_shortest_path()
        if path is None:
            return "No path found"
        else:
            return len(path)

    def part_2(self):
        targets = self.find_all_positions_of(0)
        start_pos = self.end_pos
        path = self.find_shortest_path(start_pos, targets, reverse=True)
        if path is None:
            return "No path found"
        else:
            return len(path)


def main(data: str):
    hm = HeightMap(data)
    print("Part 1:", hm.part_1())
    print("Part 2:", hm.part_2())
