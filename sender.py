import socket
import errno
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
        self.create_socket(5000)
        self.create_file_queue()
        self.send_file()

    def create_file_queue(self):
        self.packets_queue = file_manager.split(self.filename, 1472)
        print("File splitted")

    def create_socket(self, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self.socket.bind(('', port))
            print("Socket created")
        except socket.error as err:
            if err.errno == errno.EADDRINUSE:
                print("This address {} already in use, trying {}".format(
                    port, port + 1))
                self.create_socket(port+1)
            else:
                print("Unknown error")
                print(err)

    def send_packet(self, packet: Packet):
        message = packet.buffer
        self.socket.sendto(message, (self.host, self.port))
        pass

    def send_file(self):
        # this is where things start to escalate real quickly
        # implement using Stop-and-Wait protocol
        seqnum = 0
        initialTimeout = 3
        self.socket.settimeout(initialTimeout)
        while seqnum != len(self.packets_queue):
            # send a packet
            if seqnum != len(self.packets_queue) - 1:
                # print("Sending packet with seqnum : ", seqnum, bytes2hexstring(self.packets_queue[seqnum].data))
                self.send_packet(self.packets_queue[seqnum])
                # start timeout
                startTime = time.time()
                # if packet arrives, increment seqnum
                try:
                    response, server_address = self.socket.recvfrom(2 << 16)
                    received_packet = PacketUnwrapper(response)
                    print("Received seqnum: ", received_packet.seqnum)
                    if received_packet.raw_type == 0x01:  # ACK Package
                        if received_packet.seqnum == seqnum:
                            print(
                                "ACK packet received, sending next package, if any")
                            stopTime = time.time()
                            deltaTime = stopTime - startTime
                            initialTimeout = 2 * deltaTime
                            self.socket.settimeout(2 * deltaTime)
                            print("Timeout now at : ", initialTimeout)
                            seqnum += 1
                except socket.timeout:
                    print("Timeout on sending packet seqnum:", seqnum)
                    print(
                        "Re-attempting with time window {} seconds".format(2*initialTimeout))
                    self.socket.settimeout(2 * initialTimeout)
                    initialTimeout *= 2
                except ConnectionResetError:
                    print("Connection reset. Peer is probably not open.")
                # if timeout arrives, do nothing, let the loop goes as to send same packet
            else:  # Send FIN package
                try:
                    print("Sending FIN package")
                    # print("Sending packet with seqnum : ", seqnum, bytes2hexstring(self.packets_queue[seqnum].data))
                    self.send_packet(self.packets_queue[seqnum])
                    response, server_address = self.socket.recvfrom(2 << 16)
                    received_packet = PacketUnwrapper(response)
                    print("Received seqnum: ", received_packet.seqnum)
                    if received_packet.raw_type == 0x03:
                        if received_packet.seqnum == seqnum:
                            print(
                                "FIN-ACK packet received. Ending the current transmission")
                            seqnum += 1
                except socket.timeout:
                    print(
                        "Re-attempting with time window {} seconds".format(2*initialTimeout))
                    self.socket.settimeout(2 * initialTimeout)
                    initialTimeout *= 2
                except ConnectionResetError:
                    print("Connection reset. Peer is probably not open.")
                # if timeout arrives, do nothing, let the loop goes as to send same packet

# get input dari run_sender.h
# return input yg berisi address, port, dan path file


def get_input():
    inputs = []  # 3 input untuk sender
    for line in sys.stdin:
        line = ((line.replace("-e", "")).replace("\n", "")).replace(" ", "")
        inputs.append(line)
    return inputs


if __name__ == "__main__":
    # sender = Sender('./2mb-test.svg', '127.0.0.2', 9999)
    # sender.send_file()
    # test

    inputs = get_input()
    print(inputs)
    targetList = inputs[0].split(',')
    print(targetList)
    senderTask = []
    for target in targetList:
        senderTask.append(Sender(inputs[2], target, int(inputs[1])))
    # sender2 = Sender(inputs[2], inputs[0], int(inputs[1]))
    # sender2.send_file()
