from common.controller.interface_controller import InterfaceController
from common.parser.interface_parser import InterfaceParser
from nat.service.nat_service import NatService
from nat.parser.nat_table_parser import NatTableParser
from nat.controller.floating_ip_controller import FloatingIpController
from nat.parser.floating_ip_parser import FloatingIpParser
from config_instance import ConfigurationInstance

import logging

class NatController():

    def __init__(self):
        self.interfaceController = InterfaceController()
        self.interfaceParser = InterfaceParser()

        self.natService = NatService()
        self.natTableParser = NatTableParser()

        self.floatingIpController = FloatingIpController()
        self.floatingIpParser = FloatingIpParser()

        self.nf_type = ConfigurationInstance.get_nf_type(self)

    def set_configuration(self, json_configuration):

        conf_interfaces = json_configuration["config-nat:interfaces"]

        json_interfaces = conf_interfaces['ifEntry']
        for json_iface in json_interfaces:
            self.configure_interface(json_iface)

        conf_nat = json_configuration["config-nat:nat"]

        #self.set_ip_forward(conf_nat['wan-interface'])

        json_floating_ip = conf_nat['staticBindings']['floatingIP']
        for curr_json_floating_ip in json_floating_ip:
            #self.configure_floating_ip(curr_json_floating_ip)
            pass


    def get_full_status(self):

        status = {}

        status["config-nat:interfaces"] = self.get_interfaces_status()
        status["config-nat:nat"] = self.get_nat_status()

        return status


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
        interface = self.interfaceController.get_interface(name)
        if interface is None:
            raise ValueError("could not find interface: " + name)
        interface_dict = self.interfaceParser.get_interface_dict(interface)
        return interface_dict

    def configure_interface(self, json_interface):
        interface = self.interfaceParser.parse_interface(json_interface)
        if interface.type != "transparent":
            iface_found = self.interfaceController.get_interface(interface.name)
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

    def get_interface_ipv4Configuration(self, name):
        if not self.interfaceController.interface_exists(name):
            raise ValueError("could not find interface: " + name)
        interface = self.interfaceController.get_interface(name)
        ipv4_configuration_dict = self.interfaceParser.get_interface_ipv4Configuration(interface.ipv4_configuration)
        return ipv4_configuration_dict

    def get_interface_ipv4Configuration_address(self, name):
        if not self.interfaceController.interface_exists(name):
            raise ValueError("could not find interface: " + name)
        interface = self.interfaceController.get_interface(name)
        return interface.ipv4_configuration.address

    def get_interface_ipv4Configuration_netmask(self, name):
        if not self.interfaceController.interface_exists(name):
            raise ValueError("could not find interface: " + name)
        interface = self.interfaceController.get_interface(name)
        return interface.ipv4_configuration.netmask

    def get_interface_ipv4Configuration_default_gw(self, name):
        if not self.interfaceController.interface_exists(name):
            raise ValueError("could not find interface: " + name)
        interface = self.interfaceController.get_interface(name)
        return interface.ipv4_configuration.default_gw

    def get_interface_ipv4Configuration_mac_address(self, name):
        if not self.interfaceController.interface_exists(name):
            raise ValueError("could not find interface: " + name)
        interface = self.interfaceController.get_interface(name)
        return interface.ipv4_configuration.mac_address


    # Nat
    def get_nat_status(self):
        nat = {}
        nat['wan-interface'] = self.get_wan_interface()
        nat['floatingIP'] = self.get_all_floating_ip()
        return nat

    # Nat/Wan-interface
    def set_ip_forward(self, wan_interface):
        current_wan_iface = self.get_wan_interface()
        if current_wan_iface is None:
            if self.nf_type == "docker" or self.nf_type == "vm":
                self.natService.set_ip_forward(wan_interface)
            logging.debug("Nat set on wan interface: " + wan_interface)

    def unset_ip_forward(self, wan_interface):
        current_wan_iface = self.get_wan_interface()
        if current_wan_iface is not None:
            if self.nf_type == "docker" or self.nf_type == "vm":
                self.natService.unset_ip_forward(wan_interface)
            logging.debug("Nat unset")

    def get_wan_interface(self):
        if self.nf_type == "docker" or self.nf_type == "vm":
            try:
                return self.natService.get_wan_interface()
            except Exception as e:
                logging.debug("Exception: " + str(e))
                return None

    # Nat/nat-table
    def get_nat_table(self):
        if self.nf_type == "docker" or self.nf_type == "vm":
            nat_table = self.natService.get_nat_table()
        else:
            raise Exception("There is no implementation for nf_type different to docker and vm")
        nat_table_dict = []
        for nat_session in nat_table:
            nat_table_dict.append(self.natTableParser.get_nat_session_dict(nat_session))
        return nat_table_dict

    # Nat/StaticBindings
    def add_floating_ip(self, json_floating_ip):
        floating_ip = self.floatingIpParser.parse_floating_ip(json_floating_ip)
        floating_ip_list = self.floatingIpController.get_floating_ip()
        for curr_floating_ip in floating_ip_list:
            if curr_floating_ip.__eq__(floating_ip):
                return
        wan_interface = self.get_wan_interface()
        self.floatingIpController.configure_floating_ip(floating_ip, wan_interface)
        logging.debug("floating_ip set: private address " + floating_ip.private_address + " => public address" + floating_ip.public_address)

    def update_floating_ip(self, public_address, json_floating_ip):
        pass

    def update_floating_ip_private_address(self, public_address, private_address):
        pass

    def update_floating_ip_public_address(self, public_address, private_address):
        pass

    def delete_floating_ip(self, public_address):
        if self.floatingIpController.floating_ip_exists(public_address):
            self.floatingIpController.delete_floating_ip(public_address)
        else:
            raise ValueError("could not find a floating_ip with public address " + public_address)

    def get_all_floating_ip(self):
        floating_ip_list = self.floatingIpController.get_all_floating_ip()
        floating_ip_dict = []
        for floating_ip in floating_ip_list:
            floating_ip_dict.append(self.floatingIpParser.get_floating_ip_dict(floating_ip))
        return floating_ip_dict

    def get_floating_ip(self, public_address):
        floating_ip = self.floatingIpController.get_floating_ip(public_address)
        if floating_ip is None:
            raise ValueError("could not find a floating_ip with public address " + public_address)
        floating_ip_dict = self.floatingIpParser.get_floating_ip_dict(floating_ip)
        return floating_ip_dict

    def get_floating_ip_private_address(self, public_address):
        floating_ip_list = self.floatingIpController.get_all_floating_ip()
        for floating_ip in floating_ip_list:
            if floating_ip.public_address == public_address:
                return floating_ip.private_address
        raise ValueError("could not find a floating_ip with public address " + public_address)

    def get_floating_ip_public_address(self, public_address):
        floating_ip_list = self.floatingIpController.get_all_floating_ip()
        for floating_ip in floating_ip_list:
            if floating_ip.public_address == public_address:
                return floating_ip.public_address
        raise ValueError("could not find a floating_ip with public address " + public_address)
