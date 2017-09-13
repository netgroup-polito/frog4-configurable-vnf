from components.dhcp.dhcp_client.dhcp_client_service import DhcpClientService
from common.config_instance import ConfigurationInstance

class DhcpClientController():

    def __init__(self):
        self.dhcpClientService = DhcpClientService()
        self.nf_type = ConfigurationInstance().get_nf_type()

    def client_exists(self, mac_address):
        client = self.get_client(mac_address)
        if client is not None:
            return True
        else:
            return False

    def get_clients(self):
        if self.nf_type == "docker" or self.nf_type == "vm":
            return self.dhcpClientService.get_clients()

    def get_client(self, mac_address):
        if self.nf_type == "docker" or self.nf_type == "vm":
            return self.dhcpClientService.get_client(mac_address)

    def get_client_ip_address(self, mac_address):
        client = self.get_client(mac_address)
        return client.ip_address

    def get_client_hostname(self, mac_address):
        client = self.get_client(mac_address)
        return client.hostname

    def get_client_valid_until(self, mac_address):
        client = self.get_client(mac_address)
        return client.valid_until