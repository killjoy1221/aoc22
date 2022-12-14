from functools import cmp_to_key
from typing import Iterator, Protocol, TypeVar

Packet = list["Packet"] | int
PacketPair = tuple[Packet, Packet]

_T_contra = TypeVar("_T_contra", contravariant=True)


class SupportsCmp(Protocol[_T_contra]):
    def __gt__(self, __other: _T_contra) -> bool:
        ...

    def __lt__(self, __other: _T_contra) -> bool:
        ...


T_cmp = TypeVar("T_cmp", bound=SupportsCmp)


def cmp(a: T_cmp, b: T_cmp):
    return (a > b) - (a < b)


def packet_cmp(p1: Packet, p2: Packet):
    if isinstance(p1, int) and isinstance(p2, int):
        return cmp(p1, p2)
    if isinstance(p1, int):
        return packet_cmp([p1], p2)
    if isinstance(p2, int):
        return packet_cmp(p1, [p2])

    for pp1, pp2 in zip(p1, p2):
        if p_cmp := packet_cmp(pp1, pp2):
            return p_cmp

    return cmp(len(p1), len(p2))


def read_packets(data: str) -> Iterator[PacketPair]:
    for chunk in data.split("\n\n"):
        packets = chunk.split("\n", 1)
        p1, p2 = map(eval, packets)
        yield p1, p2


def compare_packets(packets: list[PacketPair]):
    for i, (p1, p2) in enumerate(packets, start=1):
        if packet_cmp(p1, p2) < 0:
            yield i


def sort_packets(packets: list[Packet]):
    return sorted(packets, key=cmp_to_key(packet_cmp))


def find_divider_indicies(packets: list[Packet], dividers: list[Packet]):
    return [i for i, p in enumerate(packets, start=1) if p in dividers]


def main(data: str):
    packets = list(read_packets(data))
    print("Part 1:", sum(compare_packets(packets)))

    divider_packets: list[Packet] = [
        [[2]],
        [[6]],
    ]

    all_packets = [x for y in packets for x in y]
    all_packets += divider_packets
    sorted_packets = sort_packets(all_packets)

    i1, i2 = find_divider_indicies(sorted_packets, divider_packets)
    print("Part 2:", i1 * i2)
