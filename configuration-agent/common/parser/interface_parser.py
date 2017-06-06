from common.model.interface import Interface, Ipv4Configuration

import logging

class InterfaceParser():

    # it receives the json block that describe the interfaces
    # and returns an array of interface objects
    def parse_interfaces(self, json_interfaces):
        interfaces = []
        for json_interface in json_interfaces:

            interface = self.parse_interface(json_interface)
            interfaces.append(interface)

        return interfaces

    def parse_interface(self, json_interface):
        name = json_interface['name']

        type = None
        if 'type' in json_interface:
            type = json_interface['type']

        management = None
        if 'management' in json_interface:
            management = json_interface['management']

        ipv4_configuration = None
        if 'ipv4_configuration' in json_interface:
            ipv4_configuration = self.parse_ipv4_configuration(json_interface['ipv4_configuration'])

        return Interface(name=name, type=type, management=management, ipv4_configuration=ipv4_configuration)

    def parse_ipv4_configuration(self, json_ipv4_configuration):
        configuration_type = None
        if 'configurationType' in json_ipv4_configuration:
            configuration_type = json_ipv4_configuration['configurationType']

        address = None
        if 'address' in json_ipv4_configuration:
            address = self.parse_address(json_ipv4_configuration)

        netmask = None
        if 'netmask' in json_ipv4_configuration:
            netmask = self.parse_netmask(json_ipv4_configuration)

        mac_address = None
        if 'mac_address' in json_ipv4_configuration:
            mac_address = self.parse_mac_address(json_ipv4_configuration)

        default_gw = None
        if 'default_gw' in json_ipv4_configuration:
            default_gw = self.parse_default_gw(json_ipv4_configuration)

        return Ipv4Configuration(configuration_type=configuration_type,
                                 address=address,
                                 netmask=netmask,
                                 mac_address=mac_address,
                                 default_gw=default_gw)

    def parse_address(self, json_ipv4_configuration):
        return json_ipv4_configuration['address']

    def parse_netmask(self, json_ipv4_configuration):
        return json_ipv4_configuration['netmask']

    def parse_mac_address(self, json_ipv4_configuration):
        return json_ipv4_configuration['mac_address']

    def parse_default_gw(self, json_ipv4_configuration):
        return json_ipv4_configuration['default_gw']


    # Give an interface it returns a dictionary
    def get_interface_dict(self, interface):
        interface_dict = {}

        interface_dict['name'] = interface.name

        interface_dict['type'] = "not_defined"
        if interface.type is not None:
            interface_dict['type'] = interface.type

        interface_dict['management'] = "not_defined"
        if interface.management is not None:
            interface_dict['management'] = interface.management

        if interface.ipv4_configuration is not None:
            interface_dict['ipv4_configuration'] = self.get_interface_ipv4Configuration(interface.ipv4_configuration)

        return interface_dict

    def get_interface_ipv4Configuration(self, ipv4_configuration):
        ipv4_configuration_dict = {}

        if ipv4_configuration.configuration_type is not None:
            ipv4_configuration_dict['configurationType'] = ipv4_configuration.configuration_type

        if ipv4_configuration.address is not None:
            ipv4_configuration_dict['address'] = ipv4_configuration.address

        if ipv4_configuration.netmask is not None:
            ipv4_configuration_dict['netmask'] = ipv4_configuration.netmask

        if ipv4_configuration.mac_address is not None:
            ipv4_configuration_dict['mac_address'] = ipv4_configuration.mac_address

        if ipv4_configuration.default_gw is not None:
            ipv4_configuration_dict['default_gw'] = ipv4_configuration.default_gw

        return ipv4_configuration_dict