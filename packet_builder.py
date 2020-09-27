import struct

def bytes2hexstring(byte_obj):
    return ''.join('{:02x}'.format(x) for x in byte_obj)

class PacketType():
    DATA = b"\x00"
    ACK = b"\x01"
    FIN = b"\x02"
    FINACK = b"\x03"

class Packet():
    '''Packet Builder
        4 arguments
        - type which needs to be using PacketType for shorthand
        - length : 1-byte integer
        - seq_num : 2-bytes integer
        - data : <length>-bytes array of bytes

        Convert data into byte string or raw array of bytes first
    '''
    def __init__(self, type, length, seq_num, data):
        self.set_type(type)
        self.data_length = length
        self.set_data(data)
        self.set_length(length)
        self.set_seq_num(seq_num)
        self.set_checksum()
        self.buffer = self.build()

    def set_type(self, _type):
        self.type = struct.pack('c', _type)

    def set_length(self, length: int):
        self.length = struct.pack('2s', length.to_bytes(2, byteorder="big"))

    def set_seq_num(self, seq_num: int):
        self.seq_num = struct.pack('2s', seq_num.to_bytes(2, byteorder="big"))

    def set_checksum(self):        
        checksum = self.calc_checksum(self.data)
        self.checksum = struct.pack('2s', checksum.to_bytes(2, byteorder="big"))
    def set_data(self, data):
        if (len(data) > self.data_length):
            print('Data segmentation is too big')
        else:
            self.data = struct.pack('{}s'.format(self.data_length), data)

    def calc_checksum(self, data):
        sum = 0x00
        data_len = len(data)
        if (data_len % 2):
            data_len += 1
            data += struct.pack( '!B' , 0)

        sum = (data[0] << 8) + (data[1])
        for i in range(2, data_len, 2):
            w = (data[i] << 8) + (data[i+1])
            sum ^= w
        return sum & 0xFFFF

    def build(self):
        return struct.pack('c2s2s2s{}s'.format(self.data_length), self.type, self.length, self.seq_num, self.checksum, self.data)

    def print(self):
        print(self.bytes2hexstring(self.type))
        print(self.bytes2hexstring(self.length))
        print(self.bytes2hexstring(self.seq_num))
        print(self.bytes2hexstring(self.checksum))
        print(self.bytes2hexstring(self.data))
