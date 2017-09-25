from components.interface.interface_service import InterfaceService

class InterfaceController():

    def __init__(self):
        self.interfaceService = InterfaceService()

    def configure_interface(self, interface):
        self.interfaceService.configure_interface(interface)

    def configure_interface_ipv4Configuration(self, ifname, ipv4Configuration):
        self.interfaceService.configure_interface_ipv4Configuration(ifname, ipv4Configuration)

    def configure_interface_ipv4Configuration_address(self, ifname, address):
        self.interfaceService.configure_interface_ipv4Configuration_address(ifname, address)

    def configure_interface_ipv4Configuration_netmask(self, ifname, netmask):
        self.interfaceService.configure_interface_ipv4Configuration_netmask(ifname, netmask)

    def configure_interface_ipv4Configuration_default_gw(self, ifname, default_gw):
        self.interfaceService.configure_interface_ipv4Configuration_default_gw(ifname, default_gw)

    def get_interfaces(self):
        return self.interfaceService.get_interfaces()

    def get_interface_by_name(self, name):
        return self.interfaceService.get_interface_by_name(name)

    def interface_exists(self, name):
        if self.get_interface_by_name(name) is None:
            return False
        else:
            return True

    def reset_interface(self, name):
        return self.interfaceService.reset_interface(name)
