from packet_builder import Packet, PacketType

p1 = Packet(PacketType.FINACK, 8, 256, b"\x64\x64\x90\x90")

p1.print()

# file piece manage

# baca file, pecah jadi beberapa parts,
# setiap partsnya ditampung dalam packet yang akan dikirim
def split(file, data_size): 
    packets = []
    partnum = 0
    input = open(file, 'rb') # use binary mode
    while True:  # eof=empty string from read
        chunk = input.read(data_size)
        if not chunk:
            break
        partnum += 1
        if partnum == 1:
            packet = Packet(PacketType.DATA, data_size, partnum, chunk)
        elif partnum == 2:
            packet = Packet(PacketType.ACK, data_size, partnum, chunk)
        elif partnum == 2:
            packet = Packet(PacketType.FIN, data_size, partnum, chunk)
        else:
            packet = Packet(PacketType.FINACK, data_size, partnum, chunk)
        packets.append(packet)
    input.close()
    return packets
            

# setiap packet yang didapat, apabila urutannya 
# udah sesuai dan ga ada error, maka langsung append) ke sebuah file
def get_packet(packet, prev_packet, to_file_dir):
    if not check_packet_error(packet, prev_packet):
        file = open(to_file_dir, 'wb')
        file.write(packet.data)
        file.close()
    pass

def check_packet_error(packet, prev_packet):
    pass