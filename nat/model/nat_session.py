class NatSession():

    def __init__(self,
                 id=None,
                 protocol=None,
                 src_address=None,
                 src_port=None,
                 dst_address=None,
                 dst_port=None,
                 translated_address=None,
                 translated_port=None
                 ):

        self.id = id
        self.protocol = protocol
        self.src_address = src_address
        self.src_port = src_port
        self.dst_address = dst_address
        self.dst_port = dst_port
        self.translated_address = translated_address
        self.translated_port = translated_port


    def __str__(self):
        str = "{"
        if self.id is not None:
            str += "'id': " + self.id + ", "
        if self.protocol is not None:
            str += "'protocol': " + self.protocol + ", "
        if self.src_address is not None:
            str += "'src_address': " + self.src_address + ", "
        if self.src_port is not None:
            str += "'src_port': " + self.src_port + ", "
        if self.dst_address is not None:
            str += "'dst_address': " + self.dst_address + ", "
        if self.dst_port is not None:
            str += "'dst_port': " + self.dst_port + ", "
        if self.translated_address is not None:
            str += "'translated_address': " + self.translated_address + ", "
        if self.translated_port is not None:
            str += "'translated_port': " + self.translated_port
        str += "}"
        return str

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

    def __hash__(self):
        return hash((self.protocol,
                     self.src_address,
                     self.src_port,
                     self.dst_address,
                     self.dst_port,
                     self.translated_address,
                     self.translated_port))