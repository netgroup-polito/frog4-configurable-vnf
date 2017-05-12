from dhcp.service.dhcp_server_service import DhcpServerService
from config_instance import ConfigurationInstance

class DhcpServerController():

    def __init__(self):
        self.dhcpServerService = DhcpServerService()
        self.nf_type = ConfigurationInstance.get_nf_type(self)

    def configure_dhcp_server(self, dhcp_server):
        if self.nf_type == "docker" or self.nf_type == "vm":
            self.dhcpServerService.configure_dhcp_server(dhcp_server)

    def update_gateway(self, gateway):
        current_dhcp_server_configuration = self.get_dhcp_server_configuration()
        current_dhcp_server_configuration.gateway = gateway
        self.configure_dhcp_server(current_dhcp_server_configuration)
        return current_dhcp_server_configuration

    def update_gateway_address(self, address):
        current_dhcp_server_configuration = self.get_dhcp_server_configuration()
        current_dhcp_server_configuration.gateway.address = address
        self.configure_dhcp_server(current_dhcp_server_configuration)
        return current_dhcp_server_configuration

    def update_gateway_netmask(self, netmask):
        current_dhcp_server_configuration = self.get_dhcp_server_configuration()
        current_dhcp_server_configuration.gateway.netmask = netmask
        self.configure_dhcp_server(current_dhcp_server_configuration)
        return current_dhcp_server_configuration

    def update_ranges(self, range_params):
        current_dhcp_server_configuration = self.get_dhcp_server_configuration()
        current_dhcp_server_configuration.ranges = range_params
        self.configure_dhcp_server(current_dhcp_server_configuration)
        return current_dhcp_server_configuration

    def update_default_lease_time(self, default_lease_time):
        current_dhcp_server_configuration = self.get_dhcp_server_configuration()
        current_dhcp_server_configuration.default_lease_time = default_lease_time
        self.configure_dhcp_server(current_dhcp_server_configuration)
        return current_dhcp_server_configuration

    def update_max_lease_time(self, max_lease_time):
        current_dhcp_server_configuration = self.get_dhcp_server_configuration()
        current_dhcp_server_configuration.max_lease_time = max_lease_time
        self.configure_dhcp_server(current_dhcp_server_configuration)
        return current_dhcp_server_configuration

    def update_dns(self, dns_params):
        current_dhcp_server_configuration = self.get_dhcp_server_configuration()
        current_dhcp_server_configuration.dns = dns_params
        self.configure_dhcp_server(current_dhcp_server_configuration)
        return current_dhcp_server_configuration

    def update_domain_name_server(self, domain_name_server):
        current_dhcp_server_configuration = self.get_dhcp_server_configuration()
        current_dhcp_server_configuration.dns.domain_name_server = domain_name_server
        self.configure_dhcp_server(current_dhcp_server_configuration)
        return current_dhcp_server_configuration

    def update_domain_name(self, domain_name):
        current_dhcp_server_configuration = self.get_dhcp_server_configuration()
        current_dhcp_server_configuration.dns.domain_name = domain_name
        self.configure_dhcp_server(current_dhcp_server_configuration)
        return current_dhcp_server_configuration

    def exists_configuration(self):
        if self.nf_type == "docker" or self.nf_type == "vm":
            try:
                self.dhcpServerService.get_dhcp_server_configuration()
                return True
            except Exception as e:
                return False

    def get_dhcp_server_configuration(self):
        if self.nf_type == "docker" or self.nf_type == "vm":
            return self.dhcpServerService.get_dhcp_server_configuration()

    def get_clients(self):
        if self.nf_type == "docker" or self.nf_type == "vm":
            return self.dhcpServerService.get_clients()