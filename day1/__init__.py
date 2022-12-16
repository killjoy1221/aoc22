def main(data: str):
    elves = [sect.splitlines() for sect in data.split("\n\n")]
    calories = [sum(map(int, elf)) for elf in elves]

    # part 1
    print(max(calories))
    # part 2
    print(sum(sorted(calories)[-3:]))
