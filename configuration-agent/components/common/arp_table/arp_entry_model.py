class ArpEntry:
    def __init__(self, ip_address=None, mac_address=None):
        self.ip_address = ip_address
        self.mac_address = mac_address

    def __str__(self):
        str = "{"
        if self.ip_address is not None:
            str += "'ip_address': " + self.ip_address + ", "
        if self.mac_address is not None:
            str += "'mac_address': " + self.mac_address
        str += "}"
        return str

    def __eq__(self, other):
        if self.ip_address != other.ip_address:
            return False
        if self.mac_address != other.mac_address:
            return False
        return True