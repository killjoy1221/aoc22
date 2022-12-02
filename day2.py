from enum import Enum
from typing import Literal


class Move(Enum):
    ROCK = "A"
    PAPER = "B"
    SCISSORS = "C"

    @property
    def score(self):
        return Move._member_names_.index(self.name) + 1

    def _get_next(self, direction: int):
        index = (Move._member_names_.index(self.name) + direction) % 3
        name = Move._member_names_[index]
        return Move[name]

    @property
    def wins_against(self):
        return self._get_next(-1)

    @property
    def loses_to(self):
        return self._get_next(1)


class ShouldWinOrLose(Enum):
    LOSE = "X"
    DRAW = "Y"
    WIN = "Z"


def get_winner(p1: Move, p2: Move):
    """Gets the winner of a rock paper scissors contest.

    Returns -1 for player 1, 1 for player 2, 0 or tie
    """
    if p1.loses_to is p2:
        return 1
    if p2.loses_to is p1:
        return -1

    return 0


def get_next_move(move: Move, win_or_lose: ShouldWinOrLose):
    if win_or_lose is ShouldWinOrLose.DRAW:
        return move
    if win_or_lose is ShouldWinOrLose.WIN:
        return move.loses_to
    if win_or_lose is ShouldWinOrLose.LOSE:
        return move.wins_against


class Game:
    def __init__(self):
        self.p1_score = 0
        self.p2_score = 0

    def move(self, p1: Move, p2: Move):

        self.p1_score += p1.score
        self.p2_score += p2.score

        winner = get_winner(p1, p2)
        if winner == -1:
            # player 1 won
            self.p1_score += 6
        elif winner == 0:
            # it's a draw
            self.p1_score += 3
            self.p2_score += 3
        elif winner == 1:
            # player 2 won
            self.p2_score += 6


ABC = Literal["A", "B", "C"]
XYZ = Literal["X", "Y", "Z"]
MoveData = list[tuple[ABC, XYZ]]


def parse_data(data: str) -> MoveData:
    return [tuple(line.split()) for line in data.splitlines()]  # type: ignore


def main(data: str):
    movedata = parse_data(data)
    part1(movedata)
    part2(movedata)


def part1(data: MoveData):
    move_map = {"X": "A", "Y": "B", "Z": "C"}

    game = Game()
    for p1_move, p2_move in data:
        p2_move = move_map.get(p2_move)
        p1 = Move(p1_move)
        p2 = Move(p2_move)
        game.move(p1, p2)

    print("Part 1:", game.p2_score)


def part2(data: MoveData):
    game = Game()
    for a, b in data:
        move = Move(a)
        winorlose = ShouldWinOrLose(b)
        next_move = get_next_move(move, winorlose)
        game.move(move, next_move)

    print("Part 2:", game.p2_score)
