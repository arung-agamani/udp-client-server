import os
import socket
from packet_builder import Packet, PacketType, bytes2hexstring
from packet_unwrapper import PacketUnwrapper
from file_manager import FileManager
import time


class Receiver():
    def __init__(self, port, out_dir):
        self.port = port
        self.out_dir = out_dir
        self.socket = None
        self.filemanager = FileManager('./out/downloaded', 1)
        self.listen_socket()
        self.listen()

    def listen_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('', self.port))

    def listen(self):
        # set current seqnum
        seqnum = 0
        client_adr = None
        while True:
            startTime = time.time()
            request, client_address = self.socket.recvfrom(32774)
            client_adr = client_address
            packet = PacketUnwrapper(request)
            if packet.raw_type == 0x00:  # DATA packet
                print("Received DATA")
                if packet.seqnum == seqnum:  # In order
                    print("In order packet, seqnum: ", seqnum)
                    if packet.is_valid:  # validate
                        print("Data valid! Processing")
                        self.filemanager.add(packet.data)
                        self.socket.sendto(
                            Packet(PacketType.ACK, 1, seqnum, b"\x69").buffer, client_address)
                        seqnum += 1
                        stopTime = time.time()
                        print("Delay between valid packets: {} seconds".format(
                            stopTime - startTime))
                    else:
                        print("Packet with seqnum {} is corrupted.".format(seqnum))
                else:
                    print("Packet out of order")
                    if packet.seqnum == seqnum - 1:
                        print(
                            "Duplicate packet [{}]. Resending ACK".format(seqnum - 1))
                        self.socket.sendto(
                            Packet(PacketType.ACK, 1, seqnum - 1, b"\x69").buffer, client_address)
                    else:
                        print("What packet order is this. Expect [{}] Got [{}]".format(
                            seqnum, packet.seqnum))

            elif packet.raw_type == 0x02:  # FIN packet. TODO: Handle if FIN-ACK is lost
                print("Received FIN")
                if packet.seqnum == seqnum:  # in order
                    print("In order FIN")
                    if packet.is_valid:  # data validated
                        print("Data valid! Ending")
                        self.socket.sendto(
                            Packet(PacketType.FINACK, 1, seqnum, b"\x70").buffer, client_address)
                        self.filemanager.add(packet.data)
                        self.filemanager.write_end()
                        break
                    else:
                        print("FIN Data corrupted")
                else:
                    print("Out of order FIN")
            else:
                print("Unknown packet")
        for i in range(10):
            self.socket.sendto(
                Packet(PacketType.FINACK, 1, seqnum, b"\x70").buffer, client_adr)
            time.sleep(min(i+1, 3))


if __name__ == "__main__":
    i1 = int(input())
    recv = Receiver(i1, '')
