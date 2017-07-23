class IperfServer:
    def __init__(self,
                 address=None,
                 port=None):

        self.address = address
        self.port = port

    def __str__(self):
        str = "{"
        if self.address is not None:
            str += "'address': " + self.address + ", "
        if self.port is not None:
            str += "'port': " + self.port
        str += "}"
        return str