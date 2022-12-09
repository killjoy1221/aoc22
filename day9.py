import numpy as np
from itertools import pairwise

UP = "U"
DOWN = "D"
LEFT = "L"
RIGHT = "R"

directions = {
    UP: np.array([0, 1]),
    DOWN: np.array([0, -1]),
    LEFT: np.array([-1, 0]),
    RIGHT: np.array([1, 0]),
}


class Rope:
    def __init__(
        self,
        length: int = 2,
        *,
        debug: bool = False,
        debug_size: tuple[int, int] | None = None,
        debug_steps: bool = False,
    ):
        self.rope_length = length
        self.debug = debug
        self.debug_size = debug_size
        self.debug_steps = debug_steps

        self.knots = np.array([[0, 0]] * length)

        self.tail_visited = set()
        self.tail_visited.add(tuple(self.knots[-1]))

    def step(self, d: str, m: int):
        direction = directions[d]
        if self.debug:
            print("==", d, m, "==")
            print()
        for _ in range(m):
            # increment the head
            self.knots[0] += direction
            # componesate for each following segment
            for k1, k2 in pairwise(self.knots):
                # calculate the delta length to the next knot
                dx = k1[0] - k2[0]
                dy = k1[1] - k2[1]
                if abs(dx) > 1 or abs(dy) > 1:
                    k2[:] = k2 + np.sign(np.array([dx, dy]))
            if self.debug_steps:
                self.print_stage()

            # add the tail to the visited set
            self.tail_visited.add(tuple(self.knots[-1]))
        if self.debug and not self.debug_steps:
            self.print_stage()

    def run(self, data: str):
        self.print_stage()
        for line in data.splitlines():
            # direction, magnitude
            d, m = line.split()
            m = int(m)
            self.step(d, m)

        print(len(self.tail_visited))

    def print_stage(self):
        if self.debug_size is None:
            return

        start_x, start_y = 0, 0
        width, height = self.debug_size
        if width > 6:
            start_x = -width // 2
        if height > 5:
            start_y = -height // 2
        for y in range(height + start_y, start_y - 1, -1):
            for x in range(start_x, width - start_x):
                for i, k in enumerate(self.knots):
                    if tuple(k) == (x, y):
                        break
                else:
                    i = "s" if (x, y) == (0, 0) else "."
                if i == 0:
                    i = "H"
                if i == 1 and self.rope_length == 2:
                    i = "T"
                print(i, end="")
            print()
        print()


def main(data: str):
    dataset = data.split("\n\n")
    # example data has 2 versions for each part, split by an empty line
    if len(dataset) == 1:
        dataset = dataset * 2
    data1, data2 = dataset

    # part 1, 2 knots
    Rope().run(data1)
    # part 2, 10 knots
    Rope(10).run(data2)
