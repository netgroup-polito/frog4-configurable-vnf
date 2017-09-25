from cf_core.config import Configuration
from cf_core.config_instance import ConfigurationInstance
from components.interface.interface_controller import InterfaceController
from components.interface.interface_parser import InterfaceParser
import logging

conf = Configuration()
# Set log level
log_format = '%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)s] %(message)s'
log_date_format = '[%d-%m-%Y %H:%M:%S]'

if conf.LOG_LEVEL == "INFO":
    log_level = logging.INFO
elif conf.LOG_LEVEL == "WARNING":
    log_level = logging.WARNING
else:
    log_level = logging.DEBUG

if conf.LOG_FILE is not None:
    logging.basicConfig(filename=conf.LOG_FILE, level=log_level, format=log_format, datefmt=log_date_format)
else:
    logging.basicConfig(level=log_level, format=log_format, datefmt=log_date_format)


class ManagementInterfaceController():

    def __init__(self):
        self.interfaceController = InterfaceController()
        self.interfaceParser = InterfaceParser()

    # Management Interface
    def get_interface(self, name):
        logging.debug("get_interface: " + name)
        interface = self.interfaceController.get_interface_by_name(name)
        if interface is None:
            raise ValueError("could not find interface: " + name)
        interface_dict = self.interfaceParser.get_interface_dict(interface)
        return interface_dict

    def get_name_management_interface(self):
        return ConfigurationInstance().get_name_management_interface()

    def configure_management_interface(self, json_interface):
        interface = self.interfaceParser.parse_interface(json_interface)
        iface_found = self.interfaceController.get_interface_by_name(interface.name)
        if iface_found is not None:
            if iface_found.__eq__(interface):
                return
        self.interfaceController.configure_interface(interface)
        logging.debug("Configured interface: " + interface.__str__())
        ConfigurationInstance().save_name_management_interface(interface.name)

    def update_interface(self, name, json_interface):
        interface = self.interfaceParser.parse_interface(json_interface)
        if self.interfaceController.interface_exists(name):
            self.interfaceController.configure_interface(interface)
            logging.debug("Updated interface: " + interface.__str__())
        else:
            raise ValueError("could not find interface: " + name)

    def reset_interface(self, name):
        if not self.interfaceController.interface_exists(name):
            raise ValueError("could not find interface: " + name)
        self.interfaceController.reset_interface(name)

    def get_interface_ipv4Configuration(self, name):
        if not self.interfaceController.interface_exists(name):
            raise ValueError("could not find interface: " + name)
        interface = self.interfaceController.get_interface_by_name(name)
        ipv4_configuration_dict = self.interfaceParser.get_interface_ipv4Configuration(interface.ipv4_configuration)
        return ipv4_configuration_dict

    def get_interface_ipv4Configuration_address(self, name):
        if not self.interfaceController.interface_exists(name):
            raise ValueError("could not find interface: " + name)
        interface = self.interfaceController.get_interface_by_name(name)
        return interface.ipv4_configuration.address

    def get_interface_ipv4Configuration_netmask(self, name):
        if not self.interfaceController.interface_exists(name):
            raise ValueError("could not find interface: " + name)
        interface = self.interfaceController.get_interface_by_name(name)
        return interface.ipv4_configuration.netmask

    def get_interface_ipv4Configuration_default_gw(self, name):
        if not self.interfaceController.interface_exists(name):
            raise ValueError("could not find interface: " + name)
        interface = self.interfaceController.get_interface_by_name(name)
        return interface.ipv4_configuration.default_gw

    def get_interface_ipv4Configuration_mac_address(self, name):
        if not self.interfaceController.interface_exists(name):
            raise ValueError("could not find interface: " + name)
        interface = self.interfaceController.get_interface_by_name(name)
        return interface.ipv4_configuration.mac_address

    def update_interface_ipv4Configuration(self, ifname, json_ipv4Configuration):
        ipv4Configuration = self.interfaceParser.parse_ipv4_configuration(json_ipv4Configuration)
        if self.interfaceController.interface_exists(ifname):
            self.interfaceController.configure_interface_ipv4Configuration(ifname, ipv4Configuration)
        else:
            raise ValueError("could not find interface: " + ifname)

    def update_interface_ipv4Configuration_address(self, ifname, address):
        if self.interfaceController.interface_exists(ifname):
            self.interfaceController.configure_interface_ipv4Configuration_address(ifname, address)
        else:
            raise ValueError("could not find interface: " + ifname)

    def update_interface_ipv4Configuration_netmask(self, ifname, netmask):
        if self.interfaceController.interface_exists(ifname):
            self.interfaceController.configure_interface_ipv4Configuration_netmask(ifname, netmask)
        else:
            raise ValueError("could not find interface: " + ifname)

    def update_interface_ipv4Configuration_default_gw(self, ifname, default_gw):
        if self.interfaceController.interface_exists(ifname):
            self.interfaceController.configure_interface_ipv4Configuration_default_gw(ifname, default_gw)
        else:
            raise ValueError("could not find interface: " + ifname)