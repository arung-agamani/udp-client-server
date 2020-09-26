from packet_builder import Packet, PacketType
from file_manager import split
import os

p1 = Packet(PacketType.FINACK, 4, 256, b"\x64\x65\x65\x64")

# p1.print()

packets = split("./test.txt", 4)
for packet in packets:
    packet.print()