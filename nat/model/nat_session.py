class NatSession():

    def __init__(self,
                 id=None,
                 protocol=None,
                 src_address=None,
                 src_port=None,
                 dst_address=None,
                 dst_port=None,
                 translated_address=None,
                 translated_port=None,
                 tcp_state=None
                 ):

        self.id = id
        self.protocol = self._get_protocol_name(protocol)
        self.src_address = str(src_address)
        self.src_port = str(src_port)
        self.dst_address = str(dst_address)
        self.dst_port = str(dst_port)
        self.translated_address = str(translated_address)
        self.translated_port = str(translated_port)
        self.tcp_state = self._get_tcp_state(tcp_state)


    def __str__(self):
        string = "{"
        if self.id is not None:
            string += "'id': " + self.id + ", "
        if self.protocol is not None:
            string += "'protocol': " + str(self.protocol) + ", "
        if self.src_address is not None:
            string += "'src_address': " + str(self.src_address) + ", "
        if self.src_port is not None:
            string += "'src_port': " + str(self.src_port) + ", "
        if self.dst_address is not None:
            string += "'dst_address': " + str(self.dst_address) + ", "
        if self.dst_port is not None:
            string += "'dst_port': " + str(self.dst_port) + ", "
        if self.translated_address is not None:
            string += "'translated_address': " + str(self.translated_address) + ", "
        if self.translated_port is not None:
            string += "'translated_port': " + str(self.translated_port) + ", "
        if self.tcp_state is not None:
            string += "'tcp_state: '" + str(self.tcp_state)
        string += "}"
        return string

    def __eq__(self, other):
        if self.id != other.id:
            return False
        if self.protocol != other.protocol:
            return False
        if self.src_address != other.src_address:
            return False
        if self.src_port != other.src_port:
            return False
        if self.dst_address != other.dst_address:
            return False
        if self.dst_port != other.dst_port:
            return False
        if self.translated_address != other.translated_address:
            return False
        if self.translated_port != other.translated_port:
            return False
        if self.tcp_state != other.tcp_state:
            return False

    def __hash__(self):
        return hash((self.protocol,
                     self.src_address,
                     self.src_port,
                     self.dst_address,
                     self.dst_port,
                     self.translated_address,
                     self.translated_port,
                     self.tcp_state))

    def _get_protocol_name(self, protocol):
        if protocol == 1:
            return "ICMP"
        elif protocol == 2:
            return "IGMP"
        elif protocol == 6:
            return "TCP"
        elif protocol == 8:
            return "EGP"
        elif protocol == 17:
            return "UDP"
        elif protocol == 41:
            return "IPv6"
        elif protocol == 47:
            return "GRE"
        elif protocol == 50:
            return "ESP"
        elif protocol == 51:
            return "AH"
        elif protocol == 58:
            return "ICMPv6"
        elif protocol == 255:
            return "RAW"

    def _get_tcp_state(self, tcp_state):
        if tcp_state == 0:
            return "NONE"
        elif tcp_state == 1:
            return "SYN_SENT"
        elif tcp_state == 2:
            return "SYN_RECV"
        elif tcp_state == 3:
            return "ESTABLISHED"
        elif tcp_state == 4:
            return "FIN_WAIT"
        elif tcp_state == 5:
            return "CLOSE_WAIT"
        elif tcp_state == 6:
            return "LAST_ACK"
        elif tcp_state == 7:
            return "TIME_WAIT"
        elif tcp_state == 8:
            return "CLOSE"
        elif tcp_state == 9:
            return "LISTEN"
