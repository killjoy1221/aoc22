import re
from typing import NamedTuple, Iterable

move_pattern = re.compile(r"^move (\d+) from (\d+) to (\d+)$")


def parse_board(data: str):
    lines = data.splitlines()[::-1]
    board = {int(stack): [] for stack in lines[0].split()}
    for layer in lines[1:]:
        for i in range(len(board)):
            crate = layer[(i * 4) + 1]
            if crate != " ":
                board[i + 1].append(crate)

    return board


class Move(NamedTuple):
    count: int
    frm: int
    to: int


def parse_moves(data: str):
    for line in data.splitlines():
        move = move_pattern.match(line)
        if move:
            yield Move(*map(int, move.groups()))


def main(data: str):
    board, moves = data.split("\n\n")
    for func in part_1, part_2:
        func(parse_board(board), parse_moves(moves))


def part_1(board: dict[int, list[str]], moves: Iterable[Move]):
    for m in moves:
        for _ in range(m.count):
            board[m.to].append(board[m.frm].pop())

    print("Part 1:", "".join(b[-1] for b in board.values()))


def part_2(board: dict[int, list[str]], moves: Iterable[Move]):
    for m in moves:
        crates = board[m.frm][-m.count:]
        board[m.frm][-m.count:] = []
        board[m.to].extend(crates)

    print("Part 2:", "".join(b[-1] for b in board.values()))
