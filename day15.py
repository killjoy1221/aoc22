from __future__ import annotations
import re
from typing import NamedTuple
import numpy as np

intp = r"(-?\d+)"

sensor_data_pattern = re.compile(
    f"^Sensor at x={intp}, y={intp}: closest beacon is at x={intp}, y={intp}$"
)


class Vec2i(NamedTuple):
    x: int
    y: int


def calc_range(sensor: Vec2i, beacon: Vec2i):
    return abs(sensor.x - beacon.x) + abs(sensor.y - beacon.y)


def main(data: str):
    sensors: list[tuple[Vec2i, Vec2i]] = []
    for line in data.splitlines():
        m = sensor_data_pattern.match(line)
        assert m is not None
        at_x, at_y, to_x, to_y = map(int, m.groups())
        sensors.append((Vec2i(at_x, at_y), Vec2i(to_x, to_y)))

    largest = max(s.y for s, _ in sensors)
    y = 10 if largest <= 20 else 2_000_000
    m = y * 2

    covered_squares = set()
    for (s, b) in sensors:
        sensor_range = calc_range(s, b)
        ty = s.y + sensor_range
        by = s.y - sensor_range
        if s.y > y and by > y or s.y < y and ty < y:
            continue
        dst = sensor_range - abs(y - s.y)
        start_x = s.x - dst
        end_x = s.x + dst
        covered = range(start_x, end_x)
        covered_squares.update(covered)

    print("Part 1:", len(covered_squares))

    # Part 2 is hard
