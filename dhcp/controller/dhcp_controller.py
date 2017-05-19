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


    def get_full_status(self):

        status = {}

        status["config-firewall:interfaces"] = self.get_interfaces_status()
        status["config-dhcp-server:server"] = self.get_dhcp_status()

        return status


    # Interfaces
    def get_interfaces_status(self):
        conf_interfaces = {}
        conf_interfaces["ifEntry"] = self.get_interfaces_ifEntry()
        return conf_interfaces

    # Interfaces/ifEntry
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

    def get_interfaces_ifEntry(self):
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


    # Dhcp Server
    def get_dhcp_status(self):
        conf_dhcp_server = {}
        conf_dhcp_server['globalIpPool'] = self.get_dhcp_server_configuration()
        conf_dhcp_server['clients'] = self.get_clients()
        return conf_dhcp_server

    # Dhcp Server/Configuration
    def configure_dhcp_server(self, json_dhcp_server_params):
        dhcp_server_configuration = self.dhcpServerParser.parse_dhcp_server(json_dhcp_server_params)
        if self.dhcpServerController.configuration_exists():
            current_dhcp_server_configuration = self.dhcpServerController.get_dhcp_server_configuration()
            if dhcp_server_configuration.__eq__(current_dhcp_server_configuration):
                return
        self.dhcpServerController.configure_dhcp_server(dhcp_server_configuration)
        self.dhcp_server_configuration_to_export = dhcp_server_configuration

    def update_gateway(self, json_gateway_params):
        gateway = self.dhcpServerParser.parse_gateway(json_gateway_params)
        if self.dhcpServerController.configuration_exists():
            dhcp_server_configuration = self.dhcpServerController.update_gateway(gateway)
            self.dhcp_server_configuration_to_export = dhcp_server_configuration
        return

    def update_gateway_address(self, json_address):
        address = self.dhcpServerParser.parse_gateway_address(json_address)
        if self.dhcpServerController.configuration_exists():
            dhcp_server_configuration = self.dhcpServerController.update_gateway_address(address)
            self.dhcp_server_configuration_to_export = dhcp_server_configuration
        return

    def update_gateway_netmask(self, json_netmask):
        netmask = self.dhcpServerParser.parse_gateway_netmask(json_netmask)
        if self.dhcpServerController.configuration_exists():
            dhcp_server_configuration = self.dhcpServerController.update_gateway_address(netmask)
            self.dhcp_server_configuration_to_export = dhcp_server_configuration
        return

    def add_section(self, json_section):
        section = self.dhcpServerParser.parse_section(json_section)
        if self.dhcpServerController.configuration_exists():
            dhcp_server_configuration = self.dhcpServerController.add_section(section)
            self.dhcp_server_configuration_to_export = dhcp_server_configuration
        return

    def update_section(self, section_start_ip, json_section):
        section = self.dhcpServerParser.parse_section(json_section)
        if self.dhcpServerController.configuration_exists():
            dhcp_server_configuration = self.dhcpServerController.update_section(section_start_ip, section)
            self.dhcp_server_configuration_to_export = dhcp_server_configuration
        return

    def update_section_start_ip(self, section_start_ip, json_start_ip):
        start_ip = self.dhcpServerParser.parse_start_ip(json_start_ip)
        if self.dhcpServerController.configuration_exists():
            dhcp_server_configuration = self.dhcpServerController.add_section_start_ip(section_start_ip, start_ip)
            self.dhcp_server_configuration_to_export = dhcp_server_configuration
        return

    def update_section_end_ip(self, section_start_ip, json_end_ip):
        end_ip = self.dhcpServerParser.parse_end_ip(json_end_ip)
        if self.dhcpServerController.configuration_exists():
            dhcp_server_configuration = self.dhcpServerController.add_section_end_ip(section_start_ip, end_ip)
            self.dhcp_server_configuration_to_export = dhcp_server_configuration
        return

    def update_default_lease_time(self, json_default_lease_time):
        default_lease_time = self.dhcpServerParser.parse_default_lease_time(json_default_lease_time)
        if self.dhcpServerController.configuration_exists():
            dhcp_server_configuration = self.dhcpServerController.update_default_lease_time(default_lease_time)
            self.dhcp_server_configuration_to_export = dhcp_server_configuration
        return

    def update_max_lease_time(self, json_max_lease_time):
        max_lease_time = self.dhcpServerParser.parse_max_lease_time(json_max_lease_time)
        if self.dhcpServerController.configuration_exists():
            dhcp_server_configuration = self.dhcpServerController.update_max_lease_time(max_lease_time)
            self.dhcp_server_configuration_to_export = dhcp_server_configuration
        return

    def update_dns(self, json_dns_params):
        dns = self.dhcpServerParser.parse_dns(json_dns_params)
        if self.dhcpServerController.configuration_exists():
            dhcp_server_configuration = self.dhcpServerController.update_dns(dns)
            self.dhcp_server_configuration_to_export = dhcp_server_configuration
        return

    def update_dns_primary_server(self, json_primary_server):
        primary_server = self.dhcpServerParser.parse_primary_server(json_primary_server)
        if self.dhcpServerController.configuration_exists():
            dhcp_server_configuration = self.dhcpServerController.update_dns_primary_server(primary_server)
            self.dhcp_server_configuration_to_export = dhcp_server_configuration
        return

    def update_dns_secondary_server(self, json_secondary_server):
        secondary_server = self.dhcpServerParser.parse_secondary_server(json_secondary_server)
        if self.dhcpServerController.configuration_exists():
            dhcp_server_configuration = self.dhcpServerController.update_dns_secondary_server(secondary_server)
            self.dhcp_server_configuration_to_export = dhcp_server_configuration
        return

    def update_domain_name(self, json_domain_name):
        domain_name = self.dhcpServerParser.parse_domain_name(json_domain_name)
        if self.dhcpServerController.configuration_exists():
            dhcp_server_configuration = self.dhcpServerController.update_domain_name(domain_name)
            self.dhcp_server_configuration_to_export = dhcp_server_configuration
        return

    def get_dhcp_server_configuration(self):
        if not self.dhcpServerController.configuration_exists():
            raise ValueError("could not find a dhcp server configuration")
        dhcp_server_configuration = self.dhcpServerController.get_dhcp_server_configuration()
        return self.dhcpServerParser.get_dhcp_server_configuration_dict(dhcp_server_configuration)

    def get_dhcp_server_configuration_gateway(self):
        if not self.dhcpServerController.configuration_exists():
            raise ValueError("could not find a dhcp server configuration")
        dhcp_server_configuration = self.dhcpServerController.get_dhcp_server_configuration()
        return self.dhcpServerParser.get_dhcp_server_configuration_gateway_dict(dhcp_server_configuration.gateway)

    def get_dhcp_server_configuration_gateway_address(self):
        if not self.dhcpServerController.configuration_exists():
            raise ValueError("could not find a dhcp server configuration")
        dhcp_server_configuration = self.dhcpServerController.get_dhcp_server_configuration()
        return dhcp_server_configuration.gateway.address

    def get_dhcp_server_configuration_netmask(self):
        if not self.dhcpServerController.configuration_exists():
            raise ValueError("could not find a dhcp server configuration")
        dhcp_server_configuration = self.dhcpServerController.get_dhcp_server_configuration()
        return dhcp_server_configuration.gateway.netmask

    def get_dhcp_server_configuration_sections(self):
        if not self.dhcpServerController.configuration_exists():
            raise ValueError("could not find a dhcp server configuration")
        dhcp_server_configuration = self.dhcpServerController.get_dhcp_server_configuration()
        sections = dhcp_server_configuration.sections
        sections_dict = []
        for section in sections:
            section_dict = self.dhcpServerParser.get_dhcp_server_configuration_section_dict(section)
            sections_dict.append(section_dict)
        return sections_dict

    def get_dhcp_server_configuration_section(self, section_start_ip):
        if not self.dhcpServerController.configuration_exists():
            raise ValueError("could not find a dhcp server configuration")
        dhcp_server_configuration = self.dhcpServerController.get_dhcp_server_configuration()
        sections = dhcp_server_configuration.sections
        section_found = None
        for section in sections:
            if section.start_ip == section_start_ip:
                section_found = section
                break
        if section_found is not None:
            return self.dhcpServerParser.parse_section(section_found)
        else:
            raise ValueError("could not find section with start_ip: " + section_start_ip)

    def get_dhcp_server_configuration_section_start_ip(self, section_start_ip):
        if not self.dhcpServerController.configuration_exists():
            raise ValueError("could not find a dhcp server configuration")
        dhcp_server_configuration = self.dhcpServerController.get_dhcp_server_configuration()
        sections = dhcp_server_configuration.sections
        for section in sections:
            if section.start_ip == section_start_ip:
                return section.start_ip
        raise ValueError("could not find section with start_ip: " + section_start_ip)

    def get_dhcp_server_configuration_section_end_ip(self, section_start_ip):
        if not self.dhcpServerController.configuration_exists():
            raise ValueError("could not find a dhcp server configuration")
        dhcp_server_configuration = self.dhcpServerController.get_dhcp_server_configuration()
        sections = dhcp_server_configuration.sections
        for section in sections:
            if section.start_ip == section_start_ip:
                return section.end_ip
        raise ValueError("could not find section with start_ip: " + section_start_ip)

    def get_dhcp_server_configuration_default_lease_time(self):
        if not self.dhcpServerController.configuration_exists():
            raise ValueError("could not find a dhcp server configuration")
        dhcp_server_configuration = self.dhcpServerController.get_dhcp_server_configuration()
        return self.dhcp_server_configuration.default_lease_time

    def get_dhcp_server_configuration_max_lease_time(self):
        if not self.dhcpServerController.configuration_exists():
            raise ValueError("could not find a dhcp server configuration")
        dhcp_server_configuration = self.dhcpServerController.get_dhcp_server_configuration()
        return dhcp_server_configuration.max_lease_time

    def get_dhcp_server_configuration_dns(self):
        if not self.dhcpServerController.configuration_exists():
            raise ValueError("could not find a dhcp server configuration")
        dhcp_server_configuration = self.dhcpServerController.get_dhcp_server_configuration()
        return self.dhcpServerParser.parse_dns(dhcp_server_configuration.dns)

    def get_dhcp_server_configuration_primary_dns(self):
        if not self.dhcpServerController.configuration_exists():
            raise ValueError("could not find a dhcp server configuration")
        dhcp_server_configuration = self.dhcpServerController.get_dhcp_server_configuration()
        return dhcp_server_configuration.dns.primary_server

    def get_dhcp_server_configuration_secondary_dns(self):
        if not self.dhcpServerController.configuration_exists():
            raise ValueError("could not find a dhcp server configuration")
        dhcp_server_configuration = self.dhcpServerController.get_dhcp_server_configuration()
        return dhcp_server_configuration.dns.secondary_server

    def get_dhcp_server_configuration_domain_name(self):
        if not self.dhcpServerController.configuration_exists():
            raise ValueError("could not find a dhcp server configuration")
        dhcp_server_configuration = self.dhcpServerController.get_dhcp_server_configuration()
        return dhcp_server_configuration.dns.domain_name

    # Dhcp Server/Clients
    def get_clients(self):
        clients = self.dhcpServerController.get_clients()
        clients_dict = []
        for client in clients:
            clients_dict.append(self.dhcpServerParser.get_client_dict(client))
        return clients_dict

    def get_client(self, mac_address):
        client = self.dhcpServerController.get_client(mac_address)
        if client is None:
            raise ValueError("could not find client: " + mac_address)
        client_dict = self.dhcpServerParser.get_client_dict(client)
        return client_dict

    def get_client_ip_address(self, mac_address):
        client = self.dhcpServerController.get_client(mac_address)
        if client is None:
            raise ValueError("could not find client: " + mac_address)
        return client.ip_address

    def get_client_hostname(self, mac_address):
        client = self.dhcpServerController.get_client(mac_address)
        if client is None:
            raise ValueError("could not find client: " + mac_address)
        return client.hostaname

    def get_client_valid_until(self, mac_address):
        client = self.dhcpServerController.get_client(mac_address)
        if client is None:
            raise ValueError("could not find client: " + mac_address)
        return client.valid_until

