class Client():
    def __init__(self,
                 mac_address=None,
                 ip_address=None,
                 hostname=None,
                 valid_until=None):

        self.mac_address = mac_address
        self.ip_address = ip_address
        self.hostname = hostname
        self.valid_until = valid_until

    def __str__(self):
        str = "{"
        if self.mac_address is not None:
            str += "'mac_address': " + self.mac_address + ", "
        if self.ip_address is not None:
            str += "'ip_address': " + self.ip_address + ", "
        if self.hostname is not None:
            str += "'hostname': " + self.hostname + ", "
        if self.valid_until is not None:
            str += "'valid_until': " + self.valid_until
        str += "}"
        return str

    def __eq__(self, other):
        if self.mac_address != other.mac_address:
            return False
        if self.ip_address != other.ip_address:
            return False
        if self.hostname != other.hostname:
            return False
        if self.valid_until != other.valid_until:
            return False
        return True