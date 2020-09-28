import socket
import time
import threading
import file_manager
from packet_builder import Packet, PacketType, bytes2hexstring
from packet_unwrapper import PacketUnwrapper
import sys

class Sender():
    def __init__(self, filename, host, port):
        self.host = host
        self.port = port
        self.filename = filename
        self.packets_queue = []
        self.create_socket()
        self.create_file_queue()

    def create_file_queue(self):
        self.packets_queue = file_manager.split(self.filename, 32727)
        print("File splitted")

    def create_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('127.0.0.1', 5000))
        print("Socket created")

    def send_packet(self, packet: Packet):
        message = packet.buffer
        self.socket.sendto(message, (self.host, self.port))
        pass

    def send_file(self):
        # this is where things start to escalate real quickly
        # implement using Stop-and-Wait protocol
        seqnum = 0
        self.socket.settimeout(1)
        while seqnum != len(self.packets_queue):
            # send a packet
            if seqnum != len(self.packets_queue) - 1:
                # print("Sending packet with seqnum : ", seqnum, bytes2hexstring(self.packets_queue[seqnum].data))
                self.send_packet(self.packets_queue[seqnum])
                # start timeout
                # if packet arrives, increment seqnum
                try:
                    response, server_address = self.socket.recvfrom(2 << 16)
                    received_packet = PacketUnwrapper(response)
                    print("Received seqnum: ", received_packet.seqnum)
                    if received_packet.raw_type == 0x01: #ACK Package
                        if received_packet.seqnum == seqnum:
                            print("ACK packet received, sending next package, if any")
                            seqnum += 1
                except socket.timeout:
                    print("Timeout on sending packet seqnum:", seqnum)
                    print("Re-attempting...")
                except ConnectionResetError:
                    print("Connection reset. Peer is probably not open.")
                # if timeout arrives, do nothing, let the loop goes as to send same packet
            else: # Send FIN package
                try:
                    print("Sending FIN package")
                    # print("Sending packet with seqnum : ", seqnum, bytes2hexstring(self.packets_queue[seqnum].data))
                    self.send_packet(self.packets_queue[seqnum])
                    response, server_address = self.socket.recvfrom(2 << 16)
                    received_packet = PacketUnwrapper(response)
                    print("Received seqnum: ", received_packet.seqnum)
                    if received_packet.raw_type == 0x03:
                        if received_packet.seqnum == seqnum:
                            print("FIN-ACK packet received. Ending the current transmission")
                            seqnum += 1
                except socket.timeout:
                    print("Timeout on sending packet seqnum:", seqnum)
                    print("Re-attempting...")
                except ConnectionResetError:
                    print("Connection reset. Peer is probably not open.")
                # if timeout arrives, do nothing, let the loop goes as to send same packet

# get input dari run_sender.h
# return input yg berisi address, port, dan path file
def get_input():
    inputs = [] # 3 input untuk sender
    for line in sys.stdin:
        sys.stdout.write(line)
        line = (line.replace("-e","")).replace("\n","")
        inputs.append(line)
    return inputs

if __name__ == "__main__":
    sender = Sender('./2mb-test.svg','127.0.0.1', 9999)
    sender.send_file()
    # test
    inputs = get_input()
    sender2 = Sender(inputs[2],inputs[0], inputs[1])
    sender2.send_file()