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
        self.packets_queue = file_manager.split(self.filename, (32767))
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
        # HANDLE THESE STUFF
        # REORDERING, DUPLICATES, CORRUPTS, LOST

        # set initial timeout
        timeout = 1  # 3 seconds
        self.socket.settimeout(timeout)
        # set number of retries
        # consecutiveRetryCount = 0  # will be incremented for every timeout
        # sequence number
        seqNum = 0
        while seqNum < len(self.packets_queue):
            # handle initial data sending
            self.socket.sendto(
                self.packets_queue[seqNum].buffer, (self.host, self.port))
            # try except
            try:
                response, server_address = self.socket.recvfrom(8)
                packet = PacketUnwrapper(response)
                if packet.raw_type == 0x01:  # ack package
                    print("Received ACK")
                    if packet.seqnum == seqNum:
                        print("ACK in order!")
                        if packet.is_valid:
                            print("[{}] was sent succesfully!".format(seqNum))
                            seqNum += 1
                        else:
                            print("ACK packet seqnum {} is corrupted".format(seqNum))
                    else:
                        print(
                            "ACK received but not in order. Seqnum recv: ", packet.seqnum)
                elif packet.raw_type == 0x03:  # finack
                    print("Received FIN-ACK")
                    if packet.seqnum == seqNum:
                        print("FIN-ACK in order!")
                        if packet.is_valid:
                            print("Last packet was sent succesfully!")
                            break
                        else:
                            print("FINACK packet seqnum is corrupted")
                    else:
                        print("FIN-ACK received but not in order. This is weird")
            except socket.timeout:
                print("Socket timeout on waiting for [{}] ACK".format(seqNum))
                # increase timeout
                timeout = min(2*timeout, 5)
                print("Setting socket timeout to", timeout)
                self.socket.settimeout(timeout)


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
    targetList = inputs[0].split(',')
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        for target in targetList:
            executor.submit(Sender, inputs[2], target, int(inputs[1]))
    # sender2 = Sender(inputs[2], inputs[0], int(inputs[1]))
    # sender2.send_file()
