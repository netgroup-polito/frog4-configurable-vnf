class Ipv4Configuration:
    def __init__(self, configuration_type=None, address=None, netmask=None, mac_address=None, default_gw=None):
        self.configuration_type = configuration_type
        self.address = address
        self.netmask = netmask
        self.mac_address = mac_address
        self.default_gw = default_gw

    def __str__(self):
        str = "{"
        if self.configuration_type is not None:
            str += "'configuration_type': " + self.configuration_type + ", "
        if self.address is not None:
            str += "'address': " + self.address + ", "
        if self.netmask is not None:
            str += "'netmask': " + self.netmask + ", "
        if self.mac_address is not None:
            str += "'mac_address': " + self.mac_address + ", "
        if self.default_gw is not None:
            str += "'default_gw': " + self.default_gw
        str += "}"
        return str

    def __eq__(self, other):
        if self.address != other.address:
            return False
        if self.netmask != other.netmask:
            return False
        if self.mac_address != other.mac_address:
            return False
        if self.default_gw != other.default_gw:
            return False
        return True

class Interface:
    def __init__(self, name=None, type=None, management=None, ipv4_configuration=None):
        self.name = name
        self.type = type
        self.management = management
        self.ipv4_configuration = ipv4_configuration

    def __str__(self):
        str = "{"
        if self.name is not None:
            str += "'name': " + self.name + ", "
        if self.type is not None:
            str += "'type': " + self.type + ", "
        if self.management is not None:
            str += "'management': %s" % self.management + ", "
        if self.ipv4_configuration is not None:
            str += "'ipv4_configuration': " + self.ipv4_configuration.__str__()
        str += "}"
        return str

    def __eq__(self, other):
        if self.name != other.name:
            return False
        if not self.ipv4_configuration.__eq__(other.ipv4_configuration):
            return False
        return True

