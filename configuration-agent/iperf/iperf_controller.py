from components.common.iperf.iperf_controller import IperfController as IperfCoreController
from components.common.iperf.iperf_parser import IperfParser as IperfCoreParser
from components.common.interface.interface_controller import InterfaceController
from components.common.interface.interface_parser import InterfaceParser
from iperf.iperf_parser import IperfParser
import logging

# set log level
log_format = '%(asctime)s [%(levelname)s] %(filename)s:%(lineno)s %(message)s'
log_date_format = '[%d-%m-%Y %H:%M:%S]'
logging.basicConfig(level=logging.DEBUG, format=log_format, datefmt=log_date_format)


class IperfController():

    def __init__(self):
        self.iperfParser = IperfParser()

        self.interfaceController = InterfaceController()
        self.interfaceParser = InterfaceParser

        self.iperfCoreController = IperfCoreController()
        self.iperfCoreParser = IperfCoreParser()

    def set_configuration(self, json_configuration):

        json_interfaces = self.iperfParser.parse_interfaces(json_configuration)
        for json_iface in json_interfaces:
            self.configure_interface(json_iface)

        json_conf_iperf = self.iperfParser.parse_iperf_configuration(json_configuration)

        if 'server' in json_conf_iperf:
            json_server_params = self.iperfCoreParser.parse_server(json_conf_iperf)
            self.start_iperf_server(json_server_params)

        if 'client' in json_conf_iperf:
            json_client_params = self.iperfCoreParser.parse_client(json_conf_iperf)
            self.start_iperf_client(json_client_params)

    # Interfaces
    def get_interfaces_status(self):
        conf_interfaces = {}
        conf_interfaces["ifEntry"] = self.get_interfaces()
        return conf_interfaces

    # Interfaces/ifEntry
    def get_interfaces(self):
        interfaces = self.interfaceController.get_interfaces()
        interfaces_dict = []
        for interface in interfaces:
            interfaces_dict.append(self.interfaceParser.get_interface_dict(interface))
        return interfaces_dict

    def get_interface(self, name):
        interface = self.interfaceController.get_interface_by_name(name)
        if interface is None:
            raise ValueError("could not find interface: " + name)
        interface_dict = self.interfaceParser.get_interface_dict(interface)
        return interface_dict

    def configure_interface(self, json_interface):
        interface = self.interfaceParser.parse_interface(json_interface)
        if interface.type != "transparent":
            iface_found = self.interfaceController.get_interface_by_name(interface.name)
            if iface_found is not None:
                if iface_found.__eq__(interface):
                    return
            self.interfaceController.configure_interface(interface)
            logging.debug("Configured interface: " + interface.__str__())

    def update_interface(self, name, json_interface):
        interface = self.interfaceParser.parse_interface(json_interface)
        if interface.type != "transparent":
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
        print(ipv4Configuration)
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

    # Iperf
    def start_iperf_client(self, json_iperf_client):
        iperf_client = self.iperfCoreParser.parse_client_configuration(json_iperf_client)
        return self.iperfCoreController.start_iperf_client(iperf_client)

    def start_iperf_server(self, json_iperf_server):
        iperf_server = self.iperfCoreParser.parse_server_configuration(json_iperf_server)
        return self.iperfCoreController.start_iperf_server(iperf_server)
