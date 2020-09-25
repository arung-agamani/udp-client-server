from packet_builder import Packet, PacketType

p1 = Packet(PacketType.FINACK, 8, 256, b"\x64\x64\x90\x90")

p1.print()
