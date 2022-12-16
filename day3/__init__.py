import string


def split_evently(lst: list, count: int):
    for i in range(0, len(lst), count):
        end_index = i + count
        yield lst[i:end_index]


def get_priority(c: str):
    return string.ascii_letters.index(c) + 1


class Rucksack:
    def __init__(self, contents: str):
        self.contents = contents

    @property
    def compartments(self):
        count = len(self.contents) // 2
        return self.contents[:count], self.contents[count:]

    @property
    def shared_item(self):
        return set.intersection(*map(set, self.compartments)).pop()


class Group:
    def __init__(self, rucksacks: list[Rucksack]):
        self.rucksacks = rucksacks

    @property
    def badge(self):
        contents = [set(rs.contents) for rs in self.rucksacks]
        return set.intersection(*contents).pop()


def main(data: str):
    rucksacks = [*map(Rucksack, data.splitlines())]
    print("Part 1:", sum(get_priority(c.shared_item) for c in rucksacks))

    groups = [Group(rs) for rs in split_evently(rucksacks, 3)]
    print("Part 2:", sum(get_priority(g.badge) for g in groups))
