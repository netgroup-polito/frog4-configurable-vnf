class IperfClient:

    def __init__(self,
                 server_address=None,
                 server_port=None,
                 protocol="tcp",
                 duration=10,
                 bidirectional=False):

        self.server_address = server_address
        self.server_port = server_port
        self.protocol = protocol
        self.duration = duration
        self.bidirectional = bidirectional

    def __str__(self):
        string = "{"
        if self.server_address is not None:
            string += "'server_address': " + self.server_address + ", "
        if self.server_port is not None:
            string += "'server_port': " + self.server_port + ", "
        if self.protocol is not None:
            string += "'protocol': " + self.protocol + ", "
        if self.duration is not None:
            string += "'duration': " + str(self.duration) + ", "
        if self.bidirectional is not None:
            string += "'bidirectional': %s" % self.bidirectional
        string += "}"
        return string
