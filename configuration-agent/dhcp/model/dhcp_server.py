class Gateway():
    def __init__(self, gateway_address=None, gateway_netmask=None):
        self.address = gateway_address
        self.netmask = gateway_netmask

    def __str__(self):
        str = "{"
        if self.address is not None:
            str += "'address': " + self.address + ", "
        if self.netmask is not None:
            str += "'netmask': " + self.netmask
        str += "}"
        return str

    def __eq__(self, other):
        if self.address != other.address:
            return False
        if self.netmask != other.netmask:
            return False
        return True

class Section():
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
    def __init__(self, primary_server=None, secondary_server=None, domain_name=None):
        self.primary_server = primary_server
        self.secondary_server = secondary_server
        self.domain_name = domain_name

    def __str__(self):
        str = "{"
        if self.primary_server is not None:
            str += "'primary_server': " + self.primary_server + ", "
        if self.secondary_server is not None:
            str += "'secondary_server': " + self.secondary_server + ", "
        if self.domain_name is not None:
            str += "'domain_name': " + self.domain_name
        str += "}"
        return str

    def __eq__(self, other):
        if self.primary_server != other.primary_server:
            return False
        if self.secondary_server != other.secondary_server:
            return False
        if self.domain_name != other.domain_name:
            return False
        return True

class DhcpServer():
    def __init__(self,
                 gateway=None,
                 sections=[],
                 default_lease_time=None,
                 max_lease_time=None,
                 dns=None):

        self.gateway = gateway
        self.sections = sections
        self.default_lease_time = default_lease_time
        self.max_lease_time = max_lease_time
        self.dns = dns


    def __str__(self):
        str = "{"
        if self.gateway is not None:
            str += "'gateway': " + self.gateway.__str__() + ", "
        if self.sections is not None:
            str += "'sections': {"
            for section in self.sections:
                str += section.__str__()
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
        if not self.sections.__eq__(other.sections):
            return False
        if self.default_lease_time != other.default_lease_time:
            return False
        if self.max_lease_time != other.max_lease_time:
            return False
        if not self.dns.__eq__(other.dns):
            return False
        return True