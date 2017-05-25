from common.service.interface_service import InterfaceService
from common.service.interface_service_native import InterfaceServiceNative
from config_instance import ConfigurationInstance

class InterfaceController():

    def __init__(self):
        self.interfaceService = InterfaceService()
        self.interfaceServiceNative = InterfaceServiceNative()
        self.nf_type = ConfigurationInstance.get_nf_type(self)

    def configure_interface(self, interface):
        if self.nf_type=="docker" or self.nf_type=="vm":
            self.interfaceService.configure_interface(interface)
        if self.nf_type=="native":
            self.interfaceServiceNative.configure_interface(interface)

    def configure_interface_ipv4Configuration(self, ifname, ipv4Configuration):
        if self.nf_type=="docker" or self.nf_type=="vm":
            self.interfaceService.configure_interface_ipv4Configuration(ifname, ipv4Configuration)

    def configure_interface_ipv4Configuration_address(self, ifname, address):
        if self.nf_type=="docker" or self.nf_type=="vm":
            self.interfaceService.configure_interface_ipv4Configuration_address(ifname, address)
        if self.nf_type=="native":
            self.interfaceServiceNative.configure_interface_address(ifname, address)

    def configure_interface_ipv4Configuration_netmask(self, ifname, netmask):
        if self.nf_type == "docker" or self.nf_type == "vm":
            self.interfaceService.configure_interface_ipv4Configuration_netmask(ifname, netmask)
        if self.nf_type == "native":
            self.interfaceServiceNative.configure_interface_netmask(ifname, netmask)

    def configure_interface_ipv4Configuration_default_gw(self, ifname, default_gw):
        if self.nf_type == "docker" or self.nf_type == "vm":
            self.interfaceService.configure_interface_ipv4Configuration_default_gw(ifname, default_gw)
        if self.nf_type == "native":
            self.interfaceServiceNative.configure_interface_default_gw(ifname, default_gw)

    def get_interfaces(self):
        if self.nf_type == "docker" or self.nf_type == "vm":
            return self.interfaceService.get_interfaces()
        if self.nf_type == "native":
            return self.interfaceServiceNative.get_interfaces()

    def get_interface(self, name):
        if self.nf_type == "docker" or self.nf_type == "vm":
            return self.interfaceService.get_interface(name)
        if self.nf_type == "native":
            return self.interfaceServiceNative.get_interface(name)

    def interface_exists(self, name):
        if self.get_interface(name) is None:
            return False
        else:
            return True

    def reset_interface(self, name):
        if self.nf_type == "docker" or self.nf_type == "vm":
            return self.interfaceService.reset_interface(name)
        if self.nf_type == "native":
            #return self.interfaceServiceNative.reset_interface(name)
            pass

