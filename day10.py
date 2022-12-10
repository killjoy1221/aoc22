from typing import Iterator


class CPU:
    def __init__(self, code: Iterator[tuple[str, list[int]]]):
        self.code = iter(code)
        self.registers = {"X": 1}
        self.cycles = 1
        self.current_op = None
        self.rendered_rows = []
        self.current_render_row = ["."] * 40

    def tick(self):
        if not self.current_op:
            opcode, args = next(self.code)
            self.current_op = getattr(self, opcode)(*args)
        try:
            next(self.current_op)
        except StopIteration:
            self.current_op = None
        self.cycles += 1

    def addx(self, value: int):
        yield
        self.registers["X"] += value

    def noop(self):
        if False:
            yield

    @property
    def signal_strength(self):
        return self.cycles * self.registers["X"]

    def render_crt(self):
        beam_position = (self.cycles - 1) % 40
        if abs(beam_position - self.registers["X"]) <= 1:
            self.current_render_row[beam_position] = "#"

        if beam_position == 39:
            self.rendered_rows.append(self.current_render_row)
            self.current_render_row = ["."] * 40


def parse_opcodes(data: str):
    for line in data.splitlines():
        opcode, *args = line.split()
        args = [*map(int, args)]
        yield opcode, args


def main(data: str):
    cpu = CPU(parse_opcodes(data))
    signals = []
    while True:
        try:
            cpu.render_crt()
            cpu.tick()
        except StopIteration:
            break
        if cpu.cycles in (20, 60, 100, 140, 180, 220):
            signals.append(cpu.signal_strength)
            # print(cpu.cycles, cpu.registers["X"], cpu.signal_strength)

    print("Part 1:", sum(signals))

    print("Part 2:")
    print("\n".join("".join(row) for row in cpu.rendered_rows))
    # print(cpu.rendered_row)
