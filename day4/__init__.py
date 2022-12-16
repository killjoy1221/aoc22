def parse_sections(s: str):
    start, end = map(int, s.split("-"))
    return set(range(start, end + 1))


def main(data: str):
    redudnant_count = 0
    overlapping_count = 0
    for line in data.splitlines():
        # e - elf
        e1, e2 = map(parse_sections, line.split(","))
        if e1.issubset(e2) or e1.issuperset(e2):
            redudnant_count += 1
        if e1.intersection(e2):
            overlapping_count += 1
    print("Part 1:", redudnant_count)
    print("Part 2:", overlapping_count)
