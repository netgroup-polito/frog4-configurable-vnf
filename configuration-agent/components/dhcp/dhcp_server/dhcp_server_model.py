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


class DhcpServer():
    def __init__(self,
                 default_lease_time=None,
                 max_lease_time=None,
                 subnet=None,
                 subnet_mask=None,
                 router=None,
                 dns_primary_server=None,
                 dns_secondary_server=None,
                 dns_domain_name=None,
                 sections=[]):

        self.default_lease_time = default_lease_time
        self.max_lease_time = max_lease_time
        self.subnet = subnet
        self.subnet_mask = subnet_mask
        self.router = router
        self.dns_primary_server = dns_primary_server
        self.dns_secondary_server = dns_secondary_server
        self.dns_domain_name = dns_domain_name
        self.sections = sections


    def __str__(self):
        str = "{"
        if self.default_lease_time is not None:
            str += "'default_lease_time': " + self.default_lease_time + ", "
        if self.max_lease_time is not None:
            str += "'max_lease_time': " + self.max_lease_time + ", "
        if self.router is not None:
            str += "'router': " + self.router+ ", "
        if self.dns_primary_server is not None:
            str += "'dns_primary_server': " + self.dns_primary_server + ", "
        if self.dns_secondary_server is not None:
            str += "'dns_secondary_server': " + self.dns_secondary_server + ", "
        if self.dns_domain_name is not None:
            str += "'dns_domain_name': " + self.dns_domain_name
        if self.subnet is not None:
            str += "'subnet': " + self.subnet + ", "
        if self.subnet_mask is not None:
            str += "'subnet_mask': " + self.subnet_mask + ", "
        if self.sections is not None:
            str += "'sections': {"
            for section in self.sections:
                str += section.__str__()
            str += "}, "
        str += "}"
        return str

    def __eq__(self, other):
        if self.default_lease_time != other.default_lease_time:
            return False
        if self.max_lease_time != other.max_lease_time:
            return False
        if self.subnet != other.subnet:
            return False
        if self.subnet_mask != other.subnet_mask:
            return False
        if self.router != other.router:
            return False
        if self.dns_primary_server != other.dns_primary_server:
            return False
        if self.dns_secondary_server != other.dns_secondary_server:
            return False
        if self.dns_domain_name != other.dns_domain_name:
            return False
        if not self.sections.__eq__(other.sections):
            return False
        return True
