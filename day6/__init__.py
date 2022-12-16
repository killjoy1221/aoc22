def main(data: str):
    for line in data.splitlines():
        part = 1
        c = 4
        for i in range(len(line)):
            end = i + c
            signal = line[i:end]
            if len(set(signal)) == len(signal):
                print(f"Part {part}: {end}", end=", ")
                if part == 2:
                    break
                part = 2
                c = 14
        print()
