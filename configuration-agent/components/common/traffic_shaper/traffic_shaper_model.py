class TrafficShaper:

    def __init__(self,
                 interface=None,
                 download_limit=None,
                 upload_limit=None):

        self.interface_name = None
        self.interface_address = None
        if interface is not None:
            self.interface_name = interface.name
            self.interface_address = interface.address
        self.download_limit = download_limit
        self.upload_limit = upload_limit

    def add_interface_name(self, interface_name):
        self.interface_name = interface_name

    def add_interface_address(self, interface_address):
        self.interface_address = interface_address

    def __str__(self):
        string = "{"
        if self.interface_name is not None:
            string += "'interface_name': " + self.interface_name + ", "
        if self.interface_address is not None:
            string += "'interface_address': " + self.interface_address + ", "
        if self.download_limit is not None:
            string += "'download_limit': " + str(self.download_limit) + ", "
        if self.upload_limit is not None:
            string += "'upload_limit': " + str(self.upload_limit)
        string += "}"
        return string