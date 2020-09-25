class PacketErrors():
    '''
        Normally there should be 4 errors
        1. Packet sent but no ACK response
        2. Last packet sent but no FIN-ACK response
        3. Packet out of order
        4. Another not yet identified errors
    '''
    def construct_no_ACK_error(self):
        pass

    def construct_no_FINACK_error(self):
        pass

    def construct_out_of_order_error(self):
        pass