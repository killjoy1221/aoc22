from typing import Iterator


class CPU:
    def __init__(self, code: Iterator[tuple[str, list[int]]]):
        self.code = iter(code)
        self.registers = {"X": 1}
        self.cycles = 0
        self.rendered_rows = []
        self.current_render_row = ["."] * 40

    def operations(self):
        for opcode, args in self.code:
            yield from getattr(self, opcode)(*args)

    def tick(self):
        self.cycles += 1

    def _delay(self, cycles: int):
        for _ in range(cycles):
            yield

    def addx(self, value: int):
        yield from self._delay(2)
        self.registers["X"] += value

    def noop(self):
        yield from self._delay(1)

    @property
    def signal_strength(self):
        return self.cycles * self.registers["X"]

    def render_tick(self):
        beam_position = self.cycles % 40
        if abs(beam_position - self.registers["X"]) <= 1:
            self.current_render_row[beam_position] = "#"

        if beam_position == 39:
            self.rendered_rows.append(self.current_render_row)
            self.current_render_row = ["."] * 40

    def render_crt(self):
        return "\n".join("".join(row) for row in self.rendered_rows)


def parse_opcodes(data: str):
    for line in data.splitlines():
        opcode, *args = line.split()
        args = [*map(int, args)]
        yield opcode, args


def main(data: str):
    cpu = CPU(parse_opcodes(data))
    signals = []
    for _ in cpu.operations():
        cpu.render_tick()
        cpu.tick()

        if cpu.cycles in (20, 60, 100, 140, 180, 220):
            signals.append(cpu.signal_strength)
            # print(cpu.cycles, cpu.registers["X"], cpu.signal_strength)

    print("Part 1:", sum(signals))

    print("Part 2:")
    print(cpu.render_crt())
    # print(cpu.rendered_row)
