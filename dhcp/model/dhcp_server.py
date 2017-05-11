class Gateway():
    def __init__(self, gateway_address=None, gateway_netmask=None):
        self.gateway_address = gateway_address
        self.gateway_netmask = gateway_netmask

    def __str__(self):
        str = "{"
        if self.gateway_address is not None:
            str += "'address': " + self.gateway_address + ", "
        if self.gateway_netmask is not None:
            str += "'netmask': " + self.gateway_netmask
        str += "}"
        return str

    def __eq__(self, other):
        if self.gateway_address != other.gateway_address:
            return False
        if self.gateway_netmask != other.gateway_netmask:
            return False
        return True

class Range():
    def __init__(self, start_ip=None, end_ip=None):
        self.start_ip = start_ip
        self.end_ip = end_ip

    def __str__(self):
        str = "{"
        if self.start_ip is not None:
            str += "'start_ip': " + self.start_ip + ", "
        if self.end_ip is not None:
            str += "'end_ip': " + self.end_ip
        str += "}"
        return str

    def __eq__(self, other):
        if self.start_ip != other.start_ip:
            return False
        if self.end_ip != other.end_ip:
            return False
        return True

class Dns():
    def __init__(self, domain_name_server=None, domain_name=None):
        self.domain_name_server = domain_name_server
        self.domain_name = domain_name

    def __str__(self):
        str = "{"
        if self.domain_name_server is not None:
            str += "'domain_name_server': " + self.domain_name_server + ", "
        if self.domain_name is not None:
            str += "'domain_name': " + self.domain_name
        str += "}"
        return str

    def __eq__(self, other):
        if self.domain_name_server != other.domain_name_server:
            return False
        if self.domain_name != other.domain_name:
            return False
        return True

class DhcpServer():
    def __init__(self,
                 gateway=None,
                 ranges=[],
                 default_lease_time=None,
                 max_lease_time=None,
                 dns=None):

        self.gateway = gateway
        self.ranges = ranges
        self.default_lease_time = default_lease_time
        self.max_lease_time = max_lease_time
        self.dns = dns


    def __str__(self):
        str = "{"
        if self.gateway is not None:
            str += "'gateway': " + self.gateway.__str__() + ", "
        if self.ranges is not None:
            str += "'ranges': {"
            for range in self.ranges:
                str += range.__str__()
            str += "}, "
        if self.default_lease_time is not None:
            str += "'default_lease_time': " + self.default_lease_time + ", "
        if self.max_lease_time is not None:
            str += "'max_lease_time': " + self.max_lease_time + ", "
        if self.dns is not None:
            str += "'dns': " + self.dns.__str__()
        str += "}"
        return str

    def __eq__(self, other):
        if not self.gateway.__eq__(other.gateway):
            return False
        for range in self.ranges:
            if not range.__eq__(other.range):
                return False
        if self.default_lease_time != other.default_lease_time:
            return False
        if self.max_lease_time != other.max_lease_time:
            return False
        if not self.dns.__eq__(other.dns):
            return False
        return True