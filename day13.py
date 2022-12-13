from dataclasses import dataclass


PacketType = list["PacketType"] | int


@dataclass
class Packet:
    p: PacketType

    def __lt__(self, other: "Packet"):
        p1 = self.p
        p2 = other.p
        if isinstance(p1, int) and isinstance(p2, int):
            return p1 < p2
        if isinstance(p1, int):
            return Packet([p1]) < other
        if isinstance(p2, int):
            return self < Packet([p2])

        for pp1, pp2 in zip(p1, p2):
            if Packet(pp1) < Packet(pp2):
                return True
            if Packet(pp2) < Packet(pp1):
                return False

        return len(p1) < len(p2)


@dataclass
class PacketPair:
    p1: Packet
    p2: Packet

    def compare(self) -> int:
        if self.p1 < self.p2:
            return -1
        if self.p2 < self.p1:
            return 1
        return 0


def read_packets(data: str):
    for chunk in data.split("\n\n"):
        packets = chunk.split("\n", 1)
        p1, p2 = map(Packet, map(eval, packets))
        yield PacketPair(p1, p2)


def compare_packets(packets: list[PacketPair]):
    for i, pair in enumerate(packets, start=1):
        if pair.compare() < 0:
            yield i


def sort_packets(packets: list[Packet]):
    return sorted(packets)


def find_divider_indicies(packets: list[Packet], dividers: list[Packet]):
    return [i for i, p in enumerate(packets, start=1) if p in dividers]


def main(data: str):
    packets = list(read_packets(data))
    print("Part 1:", sum(compare_packets(packets)))

    divider_packets = [
        Packet([[2]]),
        Packet([[6]]),
    ]

    all_packets = [x for y in packets for x in [y.p1, y.p2]]
    all_packets += divider_packets
    sorted_packets = sort_packets(all_packets)

    i1, i2 = find_divider_indicies(sorted_packets, divider_packets)
    print("Part 2:", i1 * i2)
