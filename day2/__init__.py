from enum import Enum
from typing import Iterable, Literal


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


class MatchResult(Enum):
    LOSE = "X"
    DRAW = "Y"
    WIN = "Z"

    @property
    def score(self):
        return MatchResult._member_names_.index(self.name) * 3


def get_winner(p1: Move, p2: Move):
    """Gets the winner of a rock paper scissors contest.

    Returns -1 for player 1, 1 for player 2, 0 or tie
    """
    if p1.loses_to is p2:
        return 1
    if p2.loses_to is p1:
        return -1

    return 0


def get_next_move(move: Move, win_or_lose: MatchResult):
    if win_or_lose is MatchResult.DRAW:
        return move
    if win_or_lose is MatchResult.WIN:
        return move.loses_to
    if win_or_lose is MatchResult.LOSE:
        return move.wins_against


class Game:
    def __init__(self):
        self.score = 0

    def play_round(self, opponent: Move, own: Move) -> MatchResult:
        if opponent.loses_to is own:
            return MatchResult.WIN
        if own.loses_to is opponent:
            return MatchResult.LOSE

        return MatchResult.DRAW

    def play(self, moves: Iterable[tuple[Move, Move]]):
        for opponent, own in moves:
            self.score += own.score + self.play_round(opponent, own).score


ABC = Literal["A", "B", "C"]
XYZ = Literal["X", "Y", "Z"]
MoveData = list[tuple[ABC, XYZ]]


def parse_data(data: str) -> MoveData:
    return [tuple(line.split()) for line in data.splitlines()]  # type: ignore


def main(data: str):
    movedata = parse_data(data)
    print("Part 1:", part1(movedata))
    print("Part 2:", part2(movedata))


def part1(data: MoveData):
    move_map = {"X": "A", "Y": "B", "Z": "C"}

    def map_data(line: tuple[ABC, XYZ]):
        a, b = line
        return Move(a), Move(move_map[b])

    game = Game()
    game.play(map(map_data, data))
    return game.score


def part2(data: MoveData):
    def map_data(line: tuple[ABC, XYZ]):
        a, b = line
        move = Move(a)
        result = MatchResult(b)
        return move, get_next_move(move, result)

    game = Game()
    game.play(map(map_data, data))
    return game.score
