from dhcp.service.dhcp_server_service import DhcpServerService
from config_instance import ConfigurationInstance

class DhcpServerController():

    def __init__(self):
        self.dhcpServerService = DhcpServerService()
        self.nf_type = ConfigurationInstance.get_nf_type(self)

    def configure_dhcp_server(self, dhcp_server):
        if self.nf_type == "docker" or self.nf_type == "vm":
            self.dhcpServerService.configure_dhcp_server(dhcp_server)

    def get_dhcp_server_configuration(self):
        if self.nf_type == "docker" or self.nf_type == "vm":
            return self.dhcpServerService.get_dhcp_server_configuration()

    def get_clients(self):
        if self.nf_type == "docker" or self.nf_type == "vm":
            return self.dhcpServerService.get_clients()