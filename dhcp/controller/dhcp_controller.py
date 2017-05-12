from common.controller.interface_controller import InterfaceController
from common.parser.interface_parser import InterfaceParser
from dhcp.controller.dhcp_server_controller import DhcpServerController
from dhcp.parser.dhcp_server_parser import DhcpServerParser

import logging
import json

class DhcpController():

    def __init__(self):
        self.interfaceController = InterfaceController()
        self.interfaceParser = InterfaceParser()

        self.dhcpServerController = DhcpServerController()
        self.dhcpServerParser = DhcpServerParser()

        self.interfaces_to_export = []
        self.dhcp_server_configuration_to_export = None
        self.dhcp_clients_to_export = []


    def set_configuration(self, json_configuration):

        conf_interfaces = json_configuration["config-dhcp-server:interfaces"]

        json_interfaces = conf_interfaces['ifEntry']
        for json_iface in json_interfaces:
            #self.configure_interface(json_iface)
            pass

        conf_dhcp_server = json_configuration["config-dhcp-server:server"]

        conf_global_ip_pool = conf_dhcp_server['globalIpPool']
        self.configure_dhcp_server(conf_global_ip_pool)

        logging.debug("interfaces_to_export: ")
        for x in self.interfaces_to_export:
            logging.debug(x.__str__())

        logging.debug("dhcp_configuration_to_export: ")
        logging.debug(self.dhcp_server_configuration_to_export.__str__())

        logging.debug("clients_to_export: ")
        for x in self.dhcp_clients_to_export:
            logging.debug(x.__str__())



    def get_status(self):

        status = {}

        conf_interfaces = status["config-firewall:interfaces"] = {}
        conf_interfaces["ifEntry"] = []
        conf_interfaces["ifEntry"].append(self.get_interfaces())

        conf_dhcp_server = status["config-dhcp-server:server"] = {}
        conf_dhcp_server['globalIpPool'] = {}
        conf_dhcp_server['globalIpPool'] = self.get_dhcp_server_configuration()
        conf_dhcp_server['clients'] = []
        conf_dhcp_server['clients'].append(self.get_clients())

        return status


    # Interfaces
    def configure_interface(self, json_interface):
        interface = self.interfaceParser.parse_interface(json_interface)
        if interface.type == "transparent":
            self.transparent_intefaces.append(interface)
            return
        else:
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
        interface_dict = self.interfaceParser.get_interface_dict(interface)
        return interface_dict

    def reset_interface(self, name):
        self.interfaceController.reset_interface(name)


    # Dhcp Server
    def configure_dhcp_server(self, json_dhcp_server_params):
        dhcp_server_configuration = self.dhcpServerParser.parse_dhcp_server(json_dhcp_server_params)
        if self.dhcpServerController.exists_configuration():
            current_dhcp_server_configuration = self.dhcpServerController.get_dhcp_server_configuration()
            if dhcp_server_configuration.__eq__(current_dhcp_server_configuration):
                return
        self.dhcpServerController.configure_dhcp_server(dhcp_server_configuration)
        self.dhcp_server_configuration_to_export = dhcp_server_configuration

    def update_gateway(self, json_gateway_params):
        gateway = self.dhcpServerParser.parse_gateway(json_gateway_params)
        if self.dhcpServerController.exists_configuration():
            dhcp_server_configuration = self.dhcpServerController.update_gateway(gateway)
            self.dhcp_server_configuration_to_export = dhcp_server_configuration
        return

    def update_gateway_address(self, json_address):
        address = self.dhcpServerParser.parse_gateway_address(json_address)
        if self.dhcpServerController.exists_configuration():
            dhcp_server_configuration = self.dhcpServerController.update_gateway_address(address)
            self.dhcp_server_configuration_to_export = dhcp_server_configuration
        return

    def update_gateway_netmask(self, json_netmask):
        netmask = self.dhcpServerParser.parse_gateway_netmask(json_netmask)
        if self.dhcpServerController.exists_configuration():
            dhcp_server_configuration = self.dhcpServerController.update_gateway_address(netmask)
            self.dhcp_server_configuration_to_export = dhcp_server_configuration
        return

    def update_ranges(self, json_range_params):
        ranges = self.dhcpServerParser.parse_range(json_range_params)
        if self.dhcpServerController.exists_configuration():
            dhcp_server_configuration = self.dhcpServerController.update_ranges(ranges)
            self.dhcp_server_configuration_to_export = dhcp_server_configuration
        return

    def update_default_lease_time(self, json_default_lease_time):
        default_lease_time = self.dhcpServerParser.parse_default_lease_time(json_default_lease_time)
        if self.dhcpServerController.exists_configuration():
            dhcp_server_configuration = self.dhcpServerController.update_default_lease_time(default_lease_time)
            self.dhcp_server_configuration_to_export = dhcp_server_configuration
        return

    def update_max_lease_time(self, json_max_lease_time):
        max_lease_time = self.dhcpServerParser.parse_max_lease_time(json_max_lease_time)
        if self.dhcpServerController.exists_configuration():
            dhcp_server_configuration = self.dhcpServerController.update_max_lease_time(max_lease_time)
            self.dhcp_server_configuration_to_export = dhcp_server_configuration
        return

    def update_dns(self, json_dns_params):
        dns = self.dhcpServerParser.parse_dns(json_dns_params)
        if self.dhcpServerController.exists_configuration():
            dhcp_server_configuration = self.dhcpServerController.update_dns(dns)
            self.dhcp_server_configuration_to_export = dhcp_server_configuration
        return

    def update_domain_name_server(self, json_domain_name_server):
        domain_name_server = self.dhcpServerParser.parse_domain_name_server(json_domain_name_server)
        if self.dhcpServerController.exists_configuration():
            dhcp_server_configuration = self.dhcpServerController.update_domain_name_server(domain_name_server)
            self.dhcp_server_configuration_to_export = dhcp_server_configuration
        return

    def update_domain_name(self, json_domain_name):
        domain_name = self.dhcpServerParser.parse_domain_name(json_domain_name)
        if self.dhcpServerController.exists_configuration():
            dhcp_server_configuration = self.dhcpServerController.update_domain_name(domain_name)
            self.dhcp_server_configuration_to_export = dhcp_server_configuration
        return

    def get_dhcp_server_configuration(self):
        dhcp_server_configuration = self.dhcpServerController.get_dhcp_server_configuration()
        return self.dhcpServerParser.get_dhcp_server_configuration_dict(dhcp_server_configuration)

    def get_clients(self):
        clients = self.dhcpServerController.get_clients()
        clients_dict = []
        for client in clients:
            clients_dict.append(self.dhcpServerParser.get_client_dict(client))
        return clients_dict

