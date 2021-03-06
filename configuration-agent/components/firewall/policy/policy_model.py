class Policy:
    def __init__(self,
                 id=None,
                 description=None,
                 action=None,
                 protocol=None,
                 in_interface=None,
                 out_interface=None,
                 src_address=None,
                 dst_address=None,
                 src_port=None,
                 dst_port=None
                 ):

        self.id = id
        self.description = description
        self.action = action
        self.protocol = protocol
        self.in_interface = in_interface
        self.out_interface = out_interface
        self.src_address = src_address
        self.dst_address = dst_address
        self.src_port = src_port
        self.dst_port = dst_port


    def __str__(self):
        string = "{"
        if self.id is not None:
            string += "'id': " + str(self.id) + ", "
        if self.description is not None:
            string += "'description': " + self.description + ", "
        if self.action is not None:
            string += "'action': " + self.action + ", "
        if self.protocol is not None:
            string += "'protocol': " + self.protocol + ", "
        if self.in_interface is not None:
            string += "'in_interface': " + self.in_interface + ", "
        if self.out_interface is not None:
            string += "'out_interface': " + self.out_interface + ", "
        if self.src_address is not None:
            string += "'src_address': " + self.src_address + ", "
        if self.dst_address is not None:
            string += "'dst_address': " + self.dst_address + ", "
        if self.src_port is not None:
            string += "'src_port': " + self.src_port + ", "
        if self.dst_port is not None:
            string += "'dst_port': " + self.dst_port
            string += "}"
        return string

    def __eq__(self, other):
        if self.action.lower() != other.action.lower():
            return False
        if self.protocol.lower() != other.protocol.lower():
            return False
        if self.in_interface != other.in_interface:
            return False
        if self.out_interface != other.out_interface:
            return False
        if self.src_address != other.src_address:
            return False
        if self.dst_address != other.dst_address:
            return False
        if self.src_port != other.src_port:
            return False
        if self.dst_port != other.dst_port:
            return False
        return True

    def __hash__(self):
        return hash((self.action,
                     self.protocol,
                     self.in_interface,
                     self.out_interface,
                     self.src_address,
                     self.dst_address,
                     self.src_port,
                     self.dst_port))