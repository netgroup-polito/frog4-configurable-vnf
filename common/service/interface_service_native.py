from common.model.interface import Interface, Ipv4Configuration
from utils import Bash

import netifaces

import logging

class InterfaceServiceNative():

    # configure an interface
    def configure_interface(self, interface):
        if interface.ipv4_configuration is not None:
            ipv4_configuration = interface.ipv4_configuration
            if ipv4_configuration.configuration_type == "static" or ipv4_configuration.configuration_type == "not_defined":
                self.configure_interface_address(interface.name, ipv4_configuration.address)
                if ipv4_configuration.netmask is not None:
                    self.configure_interface_netmask(interface.name, ipv4_configuration.netmask)
                if ipv4_configuration.default_gw is not None:
                    self.configure_interface_default_gw(interface.name, ipv4_configuration.default_gw)
            elif ipv4_configuration.configuration_type == "dhcp":
                # if ipv4_configuration.default_gw is not None:
                # Bash('route del default gw ' + ipv4_configuration.default_gw)
                self.configure_interface_dhcp(interface.name)
            else:
                raise Exception("configuration_type invalid!")
        else:
            raise Exception("Interface is not configurable! It must contain the ipv4_configuration")

    def configure_interface_address(ifname, address):
        Bash('ifconfig ' + ifname + ' ' + address)

    def configure_interface_netmask(ifname, netmask):
        Bash('ifconfig ' + ifname + ' netmask ' + netmask)

    def configure_interface_default_gw(ifname, default_gw):
        Bash('route add default gw ' + default_gw + ' ' + ifname)


    # return all current configured interfaces
    def get_interfaces(self):
        interfaces = []
        net_ifaces = netifaces.interfaces()
        for net_iface in net_ifaces:

            name = net_iface
            management = None

            configuration_type = "not_defined"
            ipv4_address = None
            netmask = None
            mac_address = None
            default_gw = None

            # get ipv4_address and netmask
            if 2 in netifaces.ifaddresses(net_iface):
                interface_af_inet_info = netifaces.ifaddresses(net_iface)[2]
                ipv4_address = interface_af_inet_info[0]['addr']
                netmask = interface_af_inet_info[0]['netmask']

            # get mac_addres
            mac_address = netifaces.ifaddresses(net_iface)[netifaces.AF_LINK][0]['addr']

            # get default_gw
            gws = netifaces.gateways()
            if gws['default'] != {} and gws['default'][netifaces.AF_INET][1] == net_iface:
                default_gw = gws['default'][netifaces.AF_INET][0]

            ipv4_configuration = Ipv4Configuration(configuration_type=configuration_type,
                                                   address=ipv4_address,
                                                   netmask=netmask,
                                                   mac_address=mac_address,
                                                   default_gw=default_gw)

            interface = Interface(name=name, management=management, ipv4_configuration=ipv4_configuration)
            interfaces.append(interface)

        return interfaces

    # return a specific configured interface
    def get_interface(self, name):
        interfaces = self.get_interfaces()
        for interface in interfaces:
            if interface.name == name:
                return interface
        return None

