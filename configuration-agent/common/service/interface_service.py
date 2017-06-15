from common.model.interface import Interface, Ipv4Configuration
from common.utils import Bash
from common.config_instance import ConfigurationInstance
from common.db.db_manager import dbManager

import netifaces

class InterfaceService():

    # configure an interface
    def configure_interface(self, interface):
            ifname = interface.name
            dbManager().write_interface_id(interface.id, ifname)
            ipv4Configuration = interface.ipv4_configuration
            self.configure_interface_ipv4Configuration(ifname, ipv4Configuration)

    def configure_interface_ipv4Configuration(self, ifname, ipv4_configuration):
        #print("interface configured... fake! ahah")
        #pass
        if ipv4_configuration.configuration_type == "static" or ipv4_configuration.configuration_type == "not_defined":
            self.configure_interface_ipv4Configuration_address(ifname, ipv4_configuration.address)
            if ipv4_configuration.netmask is not None:
                self.configure_interface_ipv4Configuration_netmask(ifname, ipv4_configuration.netmask)
            if ipv4_configuration.default_gw is not None:
                self.configure_interface_ipv4Configuration_default_gw(ifname, ipv4_configuration.default_gw)
        elif ipv4_configuration.configuration_type == "dhcp":
            if ipv4_configuration.default_gw is not None:
                Bash('route del default gw ' + ipv4_configuration.default_gw)
            Bash('ifconfig ' + ifname + ' 0')
            Bash('if [ ! -e "/usr/sbin/dhclient" ]; then cp /sbin/dhclient /usr/sbin/dhclient; fi')
            Bash('/usr/sbin/dhclient ' + ifname + ' -v')

    def configure_interface_ipv4Configuration_address(self, ifname, address):
        Bash('ifconfig ' + ifname + ' ' + address)

    def configure_interface_ipv4Configuration_netmask(self, ifname, netmask):
        Bash('ifconfig ' + ifname + ' netmask ' + netmask)

    def configure_interface_ipv4Configuration_default_gw(self, ifname, default_gw):
        Bash('route add default gw ' + default_gw + ' ' + ifname)


    # return all current configured interfaces
    def get_interfaces(self):
        iface_management = ConfigurationInstance.get_iface_management(self)
        interfaces = []
        net_ifaces = netifaces.interfaces()
        for net_iface in net_ifaces:

            if net_iface.__eq__("lo"):
                continue

            name = net_iface

            id = dbManager().read_interface_id(name)
            if id == None:
                id = "not_defined"

            type = "not_defined"

            if name == iface_management:
                management = True
            else:
                management = False

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

            interface = Interface(id=id, name=name, type=type, management=management, ipv4_configuration=ipv4_configuration)
            interfaces.append(interface)

        return interfaces

    # return a specific configured interface
    def get_interface_by_name(self, name):
        interfaces = self.get_interfaces()
        for interface in interfaces:
            if interface.name == name:
                return interface
        return None

        # return a specific configured interface

    def get_interface_by_id(self, id):
        interfaces = self.get_interfaces()
        for interface in interfaces:
            if (interface.id).__eq__(id):
                return interface
        return None


    def reset_interface(self, name):
        Bash('ifconfig ' + name + ' 0.0.0.0')