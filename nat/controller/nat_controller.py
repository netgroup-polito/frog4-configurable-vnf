from common.controller.interface_controller import InterfaceController
from common.parser.interface_parser import InterfaceParser
from nat.service.nat_service import NatService
from nat.controller.floating_ip_controller import FloatingIpController
from nat.parser.floating_ip_parser import FloatingIpParser
from config_instance import ConfigurationInstance

import logging

class NatController():

    def __init__(self):
        self.interfaceController = InterfaceController()
        self.interfaceParser = InterfaceParser()

        self.natService = NatService()

        self.floatingIpController = FloatingIpController()
        self.floatingIpParser = FloatingIpParser()

        self.interfaces_to_export = []
        self.wan_interface_to_export = None
        self.floating_ip_to_export = []

        self.nf_type = ConfigurationInstance.get_nf_type(self)

    def set_configuration(self, json_configuration):

        conf_interfaces = json_configuration["config-nat:interfaces"]

        json_interfaces = conf_interfaces['ifEntry']
        for json_iface in json_interfaces:
            self.configure_interface(json_iface)

        conf_nat = json_configuration["config-nat:nat"]

        #self.set_ip_forward(conf_nat)

        json_floating_ip = conf_nat['staticBindings']['floatingIP']
        for curr_json_floating_ip in json_floating_ip:
            #self.configure_floating_ip(curr_json_floating_ip)
            pass


        logging.debug("interfaces_to_export: ")
        for x in self.interfaces_to_export:
            logging.debug(x.__str__())

        logging.debug("wan_interface_to_export: ")
        logging.debug(self.wan_interface_to_export)

        logging.debug("floating_ip_to_export: ")
        for x in self.floating_ip_to_export:
            logging.debug(x.__str__())


    def get_status(self):

        status = {}

        conf_interfaces = status["config-nat:interfaces"] = {}
        conf_interfaces["ifEntry"] = []
        conf_interfaces["ifEntry"].append(self.get_interfaces())

        conf_nat = status["config-nat:nat"] = {}
        conf_nat['wan-interface'] = self.get_wan_interface()
        conf_nat_static_bindings = conf_nat['staticBindings'] = {}
        conf_nat_static_bindings['floatingIP'] = []
        conf_nat_static_bindings['floatingIP'].append(self.get_floating_ip())

        return status


    # Interfaces
    def configure_interface(self, json_interface):
        interface = self.interfaceParser.parse_interface(json_interface)
        if interface.type != "transparent":
            iface_found = self.interfaceController.get_interface(interface.name)
            if iface_found is not None:
                if iface_found.__eq__(interface):
                    return
            self.interfaceController.configure_interface(interface)
            self.interfaces_to_export.append(interface)
            logging.debug("Configured interface: " + interface.__str__())

    def update_interface(self, name, json_interface):
        interface = self.interfaceParser.parse_interface(json_interface)
        if interface.type != "transparent":
            if self.interfaceController.interface_exists(name):
                self.interfaceController.configure_interface(interface)
                self.interfaces_to_export.append(interface)
                logging.debug("Updated interface: " + interface.__str__())
            else:
                raise ValueError("could not find interface: " + name)

    def update_interface_address(self, ifname, json_address):
        address = self.interfaceParser.parse_address(json_address)
        if self.interfaceController.interface_exists(ifname):
            self.interfaceController.configure_interface_address(ifname, address)
        else:
            raise ValueError("could not find interface: " + ifname)

    def update_interface_netmask(self, ifname, json_netmask):
        netmask = self.interfaceParser.parse_netmask(json_netmask)
        if self.interfaceController.interface_exists(ifname):
            self.interfaceController.configure_interface_netmask(ifname, netmask)
        else:
            raise ValueError("could not find interface: " + ifname)

    def update_interface_default_gw(self, ifname, json_default_gw):
        default_gw = self.interfaceParser.parse_default_gw(json_default_gw)
        if self.interfaceController.interface_exists(ifname):
            self.interfaceController.configure_interface_default_gw(ifname, default_gw)
        else:
            raise ValueError("could not find interface: " + ifname)

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

    def reset_interface(self, name):
        if not self.interfaceController.interface_exists(name):
            raise ValueError("could not find interface: " + name)
        self.interfaceController.reset_interface(name)


    # Nat
    def set_ip_forward(self, json_nat_configurations):
        wan_interface = json_nat_configurations['wan-interface']
        current_wan_iface = self.get_wan_interface()
        if current_wan_iface is None:
            if self.nf_type == "docker" or self.nf_type == "vm":
                self.natService.set_ip_forward(wan_interface)
            self.wan_interface_to_export = wan_interface
            logging.debug("Nat set on wan interface: " + wan_interface)

    def unset_ip_forward(self, json_nat_configurations):
        wan_interface = json_nat_configurations['wan-interface']
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


    # Floating ip
    def add_floating_ip(self, json_floating_ip):
        floating_ip = self.floatingIpParser.parse_floating_ip(json_floating_ip)
        floating_ip_list = self.floatingIpController.get_floating_ip()
        for curr_floating_ip in floating_ip_list:
            if curr_floating_ip.__eq__(floating_ip):
                return
        wan_interface = self.get_wan_interface()
        self.floatingIpController.configure_floating_ip(floating_ip, wan_interface)
        self.floating_ip_to_export.append(floating_ip)
        logging.debug("floating_ip set: private address " + floating_ip.private_address + " => public address" + floating_ip.public_address)

    def update_floating_ip(self, private_address, json_floating_ip):
        pass

    def update_floating_ip_private_address(self, private_address, json_private_address):
        pass

    def update_floating_ip_public_address(self, private_address, json_private_address):
        pass

    def delete_floating_ip(self, private_address):
        if self.floatingIpController.floating_ip_exists(private_address):
            self.floatingIpController.delete_floating_ip(private_address)
        else:
            raise ValueError("could not find a floating_ip with private address " + private_address)

    def get_all_floating_ip(self):
        floating_ip_list = self.floatingIpController.get_all_floating_ip()
        floating_ip_dict = []
        for floating_ip in floating_ip_list:
            floating_ip_dict.append(self.floatingIpParser.get_floating_ip_dict(floating_ip))
        return floating_ip_dict

    def get_floating_ip(self, private_address):
        floating_ip = self.floatingIpController.get_floating_ip(private_address)
        if floating_ip is None:
            raise ValueError("could not find a floating_ip with private address " + private_address)
        floating_ip_dict = self.floatingIpParser.get_floating_ip_dict(floating_ip)
        return floating_ip_dict

    def get_floating_ip_private_address(self, private_address):
        floating_ip_list = self.floatingIpController.get_all_floating_ip()
        for floating_ip in floating_ip_list:
            if floating_ip.private_address == private_address:
                return floating_ip.private_address
        raise ValueError("could not find a floating_ip with private address " + private_address)

    def get_floating_ip_public_address(self, private_address):
        floating_ip_list = self.floatingIpController.get_all_floating_ip()
        for floating_ip in floating_ip_list:
            if floating_ip.private_address == private_address:
                return floating_ip.public_address
        raise ValueError("could not find a floating_ip with private address " + private_address)
