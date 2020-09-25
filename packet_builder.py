import struct

class PacketType():
    DATA = 0x0
    ACK = 0x1
    FIN = 0x2
    FINACK = 0x3

class Packet():
    def set_type(self, type):
        self.type = type

    def set_data(self, data):
        self.data = data

    def set_length(self, data):
        self.length = len(self.data)

    def set_checksum(self, checksum):
        self.checksum = checksum
    
    def calc_checksum(self, data):
        pass

    def build(self):
        pass
