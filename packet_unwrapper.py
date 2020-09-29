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
        self.get_packet_data()
        self.get_packet_checksum()
        self.is_valid = self.verify_integrity()

    def get_packet_length(self):
        self.length = int(struct.unpack(">H", self.raw_length)[0])

    def get_packet_seqnum(self):
        self.seqnum = int(struct.unpack(">H", self.raw_seqnum)[0])

    def get_packet_checksum(self):
        self.checksum = int(struct.unpack(">H", self.raw_checksum)[0])

    def get_packet_data(self):
        self.data = struct.unpack("{}s".format(
            self.length), self.raw_buffer[7:])[0]

    def verify_integrity(self):
        print(bytes(self.raw_type))
        data = self.raw_type.to_bytes(
            1, byteorder="big") + self.raw_length + self.data
        sum = 0x00
        data_len = len(data)
        if (data_len % 2):
            data_len += 1
            data += struct.pack('!B', 0)

        sum = (data[0] << 8) + (data[1])
        for i in range(2, data_len, 2):
            w = (data[i] << 8) + (data[i+1])
            sum ^= w
        sum = sum & 0xFFFF
        sum = struct.pack('2s', sum.to_bytes(2, byteorder="big"))
        return True if sum == self.raw_checksum else False

    def print(self):
        print(self.raw_type)
        print(self.raw_length)
        print(self.raw_seqnum)
