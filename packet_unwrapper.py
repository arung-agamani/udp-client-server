import struct

class PacketUnwrapper():
    def __init__(self, payload: str):
        self.raw_buffer = payload
        self.raw_type = payload[0]
        self.raw_length = payload[1:3]
        self.raw_seqnum = payload[3:5]
        self.raw_checksum = payload[5:7]
        self.get_packet_length()
        self.get_packet_seqnum()
        self.get_packet_checksum()
        self.get_packet_data()
    
    def get_packet_length(self):
        self.length = int(struct.unpack(">H", self.raw_length)[0])
    
    def get_packet_seqnum(self):
        self.seqnum = int(struct.unpack(">H", self.raw_seqnum)[0])

    def get_packet_checksum(self):
        self.checksum = int(struct.unpack(">H", self.raw_checksum)[0])

    def get_packet_data(self):
        self.data = struct.unpack("{}s".format(self.length), self.raw_buffer[7:])[0]

    def print(self):
        print(self.raw_type)
        print(self.raw_length)
        print(self.raw_seqnum)