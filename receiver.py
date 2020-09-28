import os
import socket
from packet_builder import Packet, PacketType, bytes2hexstring
from packet_unwrapper import PacketUnwrapper
from file_manager import FileManager


class Receiver():
    def __init__(self, port, out_dir):
        self.port = port
        self.out_dir = out_dir
        self.socket = None
        self.filemanager = FileManager('./out/downloaded', 4)
        self.listen_socket()
        self.listen()

    def listen_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('', self.port))

    def listen(self):
        print("Listening incoming packages from " + str(self.port))
        seqnum = 0
        self.socket.settimeout(10)
        while True:
            try:
                payload, client_address = self.socket.recvfrom(2 << 16)
                packet = PacketUnwrapper(payload)
                # print("Incoming package: ", bytes2hexstring(packet.data))
                if packet.raw_type == 0x00 and packet.is_valid:
                    if packet.seqnum == seqnum:  # duplicate or initial
                        print("Echoing ACK package to " + str(client_address))
                        seqnum += 1
                        self.filemanager.add(packet.data)
                        # if random.random() < 0.05:
                        #     time.sleep(1.1)
                        self.socket.sendto(
                            Packet(PacketType.ACK, 1, packet.seqnum, b"\x00").buffer, client_address)
                        if seqnum % 5 == 0:
                            self.filemanager.write()
                    else:
                        pass
                elif packet.raw_type == 0x02:
                    self.filemanager.add(packet.data)
                    self.socket.sendto(
                        Packet(PacketType.FINACK, 1, packet.seqnum, b"\x00").buffer, client_address)
                    self.filemanager.write_end()
                    break
                else:
                    print("Corrupted data")
            except socket.timeout:
                print("Timed out")


if __name__ == "__main__":
    i1 = int(input())
    recv = Receiver(i1, '')
