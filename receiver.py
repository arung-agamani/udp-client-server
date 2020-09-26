import os
import socket
from packet_builder import Packet, PacketType
from packet_unwrapper import PacketUnwrapper

class Receiver():
    def __init__(self, port, out_dir):
        self.port = port
        self.out_dir = out_dir
        self.socket = None
        self.listen_socket()
        self.listen()
    
    def listen_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('127.0.0.1', self.port))

    def listen(self):
        print("Listening incoming packages from " + str(self.port))
        seqnum = 0
        while True:
            payload, client_address = self.socket.recvfrom(2 << 16)
            print("Incoming package : ", str(payload))
            
            packet = PacketUnwrapper(payload)
            if packet.raw_type == 0x00:
                if packet.seqnum == seqnum: #duplicate or initial
                    print("Echoing ACK package to " + str(client_address))
                    seqnum += 1
                    sent = self.socket.sendto(Packet(PacketType.ACK, 1, packet.seqnum, b"\x00").buffer, client_address)
                else:
                    pass
            elif packet.raw_type == 0x02:
                sent = self.socket.sendto(Packet(PacketType.FINACK, 1, packet.seqnum, b"\x00").buffer, client_address)
                break

if __name__ == "__main__":
    recv = Receiver(9999, './outDir')