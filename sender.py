import socket
import errno
import time
import threading
import file_manager
import concurrent.futures
from packet_builder import Packet, PacketType, bytes2hexstring
from packet_unwrapper import PacketUnwrapper
import sys


class Sender():
    def __init__(self, filename, host, port):
        self.host = host
        self.port = port
        self.filename = filename
        self.packets_queue = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.create_socket(5000)
        self.create_file_queue()
        self.send_file()
        self.socket.close()

    def create_file_queue(self):
        self.packets_queue = file_manager.split(self.filename, (2 << 10))
        print("File splitted")

    def create_socket(self, _port):
        try:
            self.socket.bind(('', _port))
            print("Socket created")
        except socket.error as err:
            if err.errno == errno.EADDRINUSE:
                print("This address {} already in use, trying {}".format(
                    _port, _port + 1))
                self.create_socket(_port+1)
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
        totalConsecutiveRetry = 0
        self.socket.settimeout(initialTimeout)
        while seqnum != len(self.packets_queue):
            # send a packet
            if totalConsecutiveRetry > 6:
                break
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
                            totalConsecutiveRetry = 0
                except socket.timeout:
                    print("Timeout on sending packet seqnum:",
                          seqnum, file=sys.stderr)
                    print(
                        "Re-attempting with time window {} seconds".format(2*initialTimeout))
                    if seqnum != 0:
                        self.socket.settimeout(min(10, 2 * initialTimeout))
                        initialTimeout = min(10, 2 * initialTimeout)
                        totalConsecutiveRetry += 1
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
                            totalConsecutiveRetry = 0
                except socket.timeout:
                    print(
                        "Re-attempting with time window {} seconds".format(2*initialTimeout))
                    if seqnum != 0:
                        self.socket.settimeout(min(10, 2 * initialTimeout))
                        initialTimeout = min(10, 2 * initialTimeout)
                        totalConsecutiveRetry += 1
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
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        for target in targetList:
            executor.submit(Sender, inputs[2], target, int(inputs[1]))
    # sender2 = Sender(inputs[2], inputs[0], int(inputs[1]))
    # sender2.send_file()
