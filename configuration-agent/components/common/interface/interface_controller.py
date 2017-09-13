from components.common.interface.interface_service import InterfaceService
from common.config_instance import ConfigurationInstance

class InterfaceController():

    def __init__(self):
        self.interfaceService = InterfaceService()
        self.nf_type = ConfigurationInstance().get_nf_type()

    def configure_interface(self, interface):
        if self.nf_type == "docker" or self.nf_type == "vm":
            self.interfaceService.configure_interface(interface)

    def configure_interface_ipv4Configuration(self, ifname, ipv4Configuration):
        if self.nf_type == "docker" or self.nf_type == "vm":
            self.interfaceService.configure_interface_ipv4Configuration(ifname, ipv4Configuration)

    def configure_interface_ipv4Configuration_address(self, ifname, address):
        if self.nf_type == "docker" or self.nf_type == "vm":
            self.interfaceService.configure_interface_ipv4Configuration_address(ifname, address)

    def configure_interface_ipv4Configuration_netmask(self, ifname, netmask):
        if self.nf_type == "docker" or self.nf_type == "vm":
            self.interfaceService.configure_interface_ipv4Configuration_netmask(ifname, netmask)

    def configure_interface_ipv4Configuration_default_gw(self, ifname, default_gw):
        if self.nf_type == "docker" or self.nf_type == "vm":
            self.interfaceService.configure_interface_ipv4Configuration_default_gw(ifname, default_gw)

    def get_interfaces(self):
        if self.nf_type == "docker" or self.nf_type == "vm":
            return self.interfaceService.get_interfaces()

    def get_interface_by_id(self, id):
        if self.nf_type == "docker" or self.nf_type == "vm":
            return self.interfaceService.get_interface_by_id(id)

    def get_interface_by_name(self, name):
        if self.nf_type == "docker" or self.nf_type == "vm":
            return self.interfaceService.get_interface_by_name(name)

    def interface_exists(self, name):
        if self.get_interface_by_name(name) is None:
            return False
        else:
            return True

    def reset_interface(self, name):
        if self.nf_type == "docker" or self.nf_type == "vm":
            return self.interfaceService.reset_interface(name)
