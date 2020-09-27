from packet_builder import Packet, PacketType, bytes2hexstring
import os
import queue

# file piece manage

# baca file, pecah jadi beberapa parts,
# setiap partsnya ditampung dalam packet yang akan dikirim
def split(file, data_size: int): 
    packets = []
    partnum = 0
    input = open(file, 'rb') # use binary mode
    last_chunk = None
    while True:  # eof=empty string from read
        chunk = input.read(data_size)
        if not chunk:
            break        
        else:
            last_chunk = chunk
            packets.append(Packet(PacketType.DATA, data_size, partnum, chunk))
        partnum += 1
    input.close()
    packets[len(packets) - 1] = Packet(PacketType.FIN, len(last_chunk), partnum - 1, last_chunk)
    return packets
            

# setiap packet yang didapat, apabila urutannya 
# udah sesuai dan ga ada error, maka langsung append) ke sebuah file
def get_packet(packet, prev_packet, to_file_dir):
    if not check_packet_error(packet, prev_packet):
        file = open(to_file_dir, 'wb')
        file.write(packet.data)
        file.close()
    pass

class FileManager():
    def __init__(self, filepath, throttling_num):
        self.filepath = filepath
        self.throttling_num = throttling_num
        self.queue = []
        self.file_IO = open(filepath, 'ab+')
        print("File manager for ", filepath, "created!")

    def add(self, data):
        # print(data)
        self.queue.append(data)

    def write(self):
        data = b''
        for i in range(0, len(self.queue) - 1):
            if i < self.throttling_num:
                data += self.queue[i]
            else:
                break
        self.file_IO.write(data)
        self.queue = self.queue[self.throttling_num:]

    def write_end(self):
        print("End-game file called")
        data = b''
        for i in range(0, len(self.queue)):
            data += self.queue[i]
            # print(self.queue[i], data, i, bytes2hexstring(self.queue[i]))
        # print(data)
        self.file_IO.write(data)
        self.file_IO.close()
        
