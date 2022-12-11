from math import prod
from operator import add, mul

import numpy as np


class Operation:
    def __init__(self, data: str) -> None:
        *_, op, val = data.split()
        self.op = mul if op == "*" else add
        self.value = "old" if val == "old" else int(val)

    def __call__(self, old: int) -> int:
        value = self.value
        if value == "old":
            value = old
        return self.op(old, value)

    def __repr__(self) -> str:
        return f"new = old {self.op} {self.value}"


class Tests:
    def __init__(self, name: str, if_true: str, if_false: str) -> None:
        self.test_value = int(name.split()[-1])
        self.if_true = int(if_true.split()[-1])
        self.if_false = int(if_false.split()[-1])

    def __call__(self, value: int) -> int:
        if value % self.test_value == 0:
            return self.if_true
        return self.if_false


class Monkey:
    def __init__(
        self, starting_items: list[int], operation: Operation, tests: Tests
    ) -> None:
        self.starting_items = starting_items
        self.operation = operation
        self.tests = tests
        self.reset()

    def reset(self):
        self.items = np.array(self.starting_items, "uint64")
        self.inspected = 0

    def inspect_items(self, relief: int | None = None):
        while len(self.items):
            self.inspected += 1
            item = self.items[0]
            self.items = np.delete(self.items, 0)
            item = self.operation(item)
            if relief is None:
                item //= 3
            else:
                item %= relief
            next_monkey = self.tests(item)
            yield next_monkey, item


def keep_away_round(monkeys: list[Monkey], *, relief: int | None = None):
    for m in monkeys:
        for next_monkey, item in m.inspect_items(relief):
            items = monkeys[next_monkey].items
            items = np.append(items, np.array([item]))
            monkeys[next_monkey].items = items


def keep_away(monkeys: list[Monkey]):
    # part 1
    for _ in range(20):
        keep_away_round(monkeys)

    two_most_active_monkeys = sorted(m.inspected for m in monkeys)[-2:]
    monkey_business_level = prod(two_most_active_monkeys)

    print("Part 1:", monkey_business_level)

    for m in monkeys:
        m.reset()

    # part 2

    relief = prod(m.tests.test_value for m in monkeys)
    for _ in range(1, 10_001):
        keep_away_round(monkeys, relief=relief)
        print(f"\r{f'{_/10000:.2%}':>7}", end="")
        if _ in (1, 20, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000):
            print(f"{_:6}", np.array([m.inspected for m in monkeys]))

    two_most_active_monkeys = sorted(m.inspected for m in monkeys)[-2:]
    monkey_business_level = prod(two_most_active_monkeys)
    print("Part 2:", monkey_business_level)


def main(data: str):
    monkeys = []
    lines = iter(data.splitlines())
    while True:
        # Monkey 0:
        next(lines)
        #   Starting items: x, y
        starting_items = next(lines).split(": ")[1]
        #   Operation: new = old <op> old|<num>
        operation = next(lines).split(": ")[1]
        #   Test: divisible by <num>
        test_name = next(lines).split(": ")[1]
        #     If true: throw to monkey x
        if_true = next(lines).split(": ")[1]
        #     If false: throw to monkey y
        if_false = next(lines).split(": ")[1]

        monkeys.append(
            Monkey(
                list(map(int, starting_items.split(", "))),
                Operation(operation),
                Tests(test_name, if_true, if_false),
            ),
        )
        try:
            next(lines)  # empty line
        except StopIteration:
            break

    # print("\n".join(f"{i}: {m.items}" for i, m in enumerate(monkeys)))
    keep_away(monkeys)
