import numpy as np


class Trees:
    def __init__(self, data: str):
        trees = [list(row) for row in data.splitlines()]
        self.trees = np.array(trees, dtype="byte")

    def get_tree(self, x: int, y: int):
        return self.trees[y][x]

    def get_row(self, y: int):
        return self.trees[y]

    def get_column(self, x: int):
        return self.trees[:, x]

    def is_tree_visible(self, x: int, y: int):
        row = self.get_row(y)
        col = self.get_column(x)
        row_left = row[:x]
        row_right = row[x + 1:]
        col_top = col[:y]
        col_bottom = col[y + 1:]
        t = self.get_tree(x, y)
        # print(row_left, t, row_right)
        return (
            np.amax(row_left) >= t
            and np.amax(row_right) >= t
            and np.amax(col_top) >= t
            and np.amax(col_bottom) >= t
        )

    def visibility_map(self):
        # the edges get an automatic fail
        yield from [0] * self.trees.shape[0]
        for y in range(1, self.trees.shape[0] - 1):
            yield 0
            for x in range(1, self.trees.shape[1] - 1):
                yield self.is_tree_visible(x, y)
            yield 0
        yield from [0] * self.trees.shape[0]

    def score_view(self, x: int, y: int):
        t = self.get_tree(x, y)
        left_score = 0
        for x2 in range(x - 1, -1, -1):
            left_score += 1
            if self.get_tree(x2, y) >= t:
                break
        right_score = 0
        for x2 in range(x + 1, self.trees.shape[1]):
            right_score += 1
            if self.get_tree(x2, y) >= t:
                break
        top_score = 0
        for y2 in range(y - 1, -1, -1):
            top_score += 1
            if self.get_tree(x, y2) >= t:
                break
        bottom_score = 0
        for y2 in range(y + 1, self.trees.shape[0]):
            bottom_score += 1
            if self.get_tree(x, y2) >= t:
                break
        return left_score * right_score * top_score * bottom_score

    def viewability_map(self):
        for y in range(self.trees.shape[0]):
            for x in range(self.trees.shape[1]):
                yield self.score_view(x, y)

    def map_array(self, func):
        return np.array([*func()]).reshape(self.trees.shape)

    def __str__(self):
        return str(self.trees)


def main(data: str):
    trees = Trees(data)
    # print(trees)
    visible = trees.map_array(trees.visibility_map)
    # print((3, 1), trees.is_tree_visible(3, 1))
    # print(visible)
    # print(visible.reshape(trees.trees.shape))
    print("Part 1:", np.count_nonzero(visible == 0))

    trees_view = trees.map_array(trees.viewability_map)
    # print(trees.score_view(2, 3))
    # print(trees_view)
    print("Part 2:", np.amax(trees_view))
