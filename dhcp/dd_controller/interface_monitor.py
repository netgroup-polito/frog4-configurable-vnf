from common.controller.interface_controller import InterfaceController
from common.model.interface import Interface
from common.model.interface import Ipv4Configuration

class InterfaceMonitor():

    def __init__(self, dd_controller, curr_interfaces):
        self.url_iface = "config-dhcp-server:interfaces/ifEntry"
        self.url_iface_name = self.url_iface + "/name"
        self.url_iface_type = self.url_iface + "/type"
        self.url_iface_management = self.url_iface + "/management"
        self.url_iface_ipv4Config = self.url_iface + "/ipv4_configuration"
        self.url_iface_ipv4Config_address = self.url_iface_ipv4Config + "/address"
        self.url_iface_ipv4Config_netmask = self.url_iface_ipv4Config + "/netmask"
        self.url_iface_ipv4Config_macAddress = self.url_iface_ipv4Config + "/mac_address"
        self.url_iface_ipv4Config_defaultGW = self.url_iface_ipv4Config + "/default_gw"

        self.interfaces_old = curr_interfaces
        self.interfaces_new = []
        self.interfaces_updated = []
        self.interfaces_removed = []

        self.ddController = dd_controller
        self.interfaceController = InterfaceController()

    def monitor(self):

        self._get_new_interfaces()

        if len(self.interfaces_new) > 0:
            for interface in self.interfaces_new:
                self._publish_interface(interface, "add")
            self.interfaces_new = []

        if len(self.interfaces_removed) > 0:
            for interface in self.interfaces_removed:
                self._publish_interface(interface, "delete")
            self.interfaces_removed = []

        if len(self.interfaces_updated) > 0:
            for interface_map in self.interfaces_updated:
                old_interface = interface_map['old']
                new_interface = interface_map['new']
                interface_diff = self._find_diff(old_interface, new_interface)
                self._publish_interface(interface_diff, "update")
            self.interfaces_updated = []


    def _get_new_interfaces(self):
        curr_interfaces = self.interfaceController.get_interfaces()
        interface_map = {}
        # Check interfaces new or modified
        for interface in curr_interfaces:
            # get the old interface whose name is the same of the new interface
            old_interface = next((x for x in self.interfaces_old if x.name == interface.name), None)
            if old_interface is None:
                self.interfaces_new.append(interface)
            else:
                if not interface.__eq__(old_interface):
                    interface_map['old'] = old_interface
                    interface_map['new'] = interface
                    self.interfaces_updated.append(interface_map)
        # Check if an interfaces was removed
        for old_interface in self.interfaces_old:
            # get the old interface whose name is the same of the new interface
            interface = next((x for x in curr_interfaces if x.name == old_interface.name), None)
            if interface is None:
                self.interfaces_removed.append(interface)
        self.interfaces_old = curr_interfaces

    def _find_diff(self, old_interface, new_interface):

        type = None
        if not old_interface.type.__eq__(new_interface.type):
            type = new_interface.type

        management = None
        if not old_interface.management.__eq__(new_interface.management):
            management = new_interface.management

        old_ipv4Config = old_interface.ipv4_configuration
        new_ipv4Config = new_interface.ipv4_configuration

        configuration_type = None
        if not old_ipv4Config.configuration_type.__eq__(new_ipv4Config.configuration_type):
            configuration_type = new_ipv4Config.configuration_type

        address = None
        if not old_ipv4Config.address.__eq__(new_ipv4Config.address):
            address = new_ipv4Config.address

        netmask = None
        if not old_ipv4Config.netmask.__eq__(new_ipv4Config.netmask):
            netmask = new_ipv4Config.netmask

        mac_address = None
        if not old_ipv4Config.mac_address.__eq__(new_ipv4Config.mac_address):
            mac_address = new_ipv4Config.mac_address

        default_gw = None
        if not old_ipv4Config.default_gw.__eq__(new_ipv4Config.default_gw):
            default_gw = new_ipv4Config.default_gw

        ipv4_configuration = Ipv4Configuration(configuration_type=configuration_type,
                                               address=address,
                                               netmask=netmask,
                                               mac_address=mac_address,
                                               default_gw=default_gw)
        interface = Interface(name=None,
                              type=type,
                              management=management,
                              ipv4_configuration=ipv4_configuration)

        return interface

    def _publish_interface(self, interface, method):

        if interface.name is not None:
            self._publish_interface_name(interface.name, method)

        if interface.type is not None:
            self._publish_interface_type(interface.type, method)

        if interface.management is not None:
            self._publish_interface_management(interface.management, method)

        if interface.ipv4_configuration.address is not None:
            self._publish_interface_ipv4Config_address(interface.ipv4_configuration.address, method)

        if interface.ipv4_configuration.netmask is not None:
            self._publish_interface_ipv4Config_netmask(interface.ipv4_configuration.netmask, method)

        if interface.ipv4_configuration.mac_address is not None:
            self._publish_interface_ipv4Config_macAddress(interface.ipv4_configuration.mac_address, method)

        if interface.ipv4_configuration.default_gw is not None:
            self._publish_interface_ipv4Config_defaultGW(interface.ipv4_configuration.default_gw, method)

    def _publish_interface_name(self, data, method):
        self.ddController.publish_on_bus(self.url_iface_name, method, data)

    def _publish_interface_type(self, data, method):
        self.ddController.publish_on_bus(self.url_iface_type, method, data)

    def _publish_interface_management(self, data, method):
        self.ddController.publish_on_bus(self.url_iface_management, method, data)

    def _publish_interface_ipv4Config_address(self, data, method):
        self.ddController.publish_on_bus(self.url_iface_ipv4Config_address, method, data)

    def _publish_interface_ipv4Config_netmask(self, data, method):
        self.ddController.publish_on_bus(self.url_iface_ipv4Config_netmask, method, data)

    def _publish_interface_ipv4Config_macAddress(self, data, method):
        self.ddController.publish_on_bus(self.url_iface_ipv4Config_macAddress, method, data)

    def _publish_interface_ipv4Config_defaultGW(self, data, method):
        self.ddController.publish_on_bus(self.url_iface_ipv4Config_defaultGW, method, data)

