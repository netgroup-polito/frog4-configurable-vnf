from components.common.interface.interface_controller import InterfaceController
from components.common.interface.interface_parser import InterfaceParser
from components.common.bridge.bridge_controller import BridgeController
from components.common.bridge.bridge_model import Bridge
from components.ids.ids_controller import IdsController as IdsCoreController
from components.ids.ids_parser import IdsParser as IdsCoreParser
from ids.ids_parser import IdsParser
import logging

class IdsController():

    def __init__(self):
        self.interfaceController = InterfaceController()
        self.interfaceParser = InterfaceParser()

        self.bridgeController = BridgeController()

        self.idsCoreController = IdsCoreController()
        self.idsCoreParser = IdsCoreParser()

        self.idsParser = IdsParser()

        self.transparent_intefaces = []

    def set_configuration(self, json_configuration):
        json_interfaces = self.idsParser.parse_interfaces(json_configuration)
        for json_iface in json_interfaces:
            self.configure_interface(json_iface)

        assert len(self.transparent_intefaces) == 2, "Error: transparent interfaces have to be 2"
        logging.debug("Found " + str(len(self.transparent_intefaces)) + " transparent interfaces, now create a bridge between them")
        bridge = Bridge("br0", self.transparent_intefaces[0].name, self.transparent_intefaces[1].name)
        logging.debug("Bridge to create: " + bridge.__str__())
        self.create_bridge(bridge)

        # Configure IDS
        if 'config-ids:ids' in json_configuration:
            logging.debug("Found and Ids Configuration, try to set it...")
            ids_configuration = self.idsParser.parse_ids_configuration(json_configuration)
            self.set_ids_configuration(ids_configuration)
            logging.debug("Found and Ids Configuration, try to set it...done!")
            logging.debug("Starting snort as a daemon...")
            self.idsCoreController.start_ids()
            logging.debug("Starting snort as a daemon...done!")

    def get_full_status(self):
        pass

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
        if interface.type == "transparent":
            self.transparent_intefaces.append(interface)
            logging.debug("Found a transparent interface: " + interface.__str__())
            return
        else:
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


    # Bridge
    def create_bridge(self, bridge):
        br_found = self.interfaceController.get_interface_by_name(bridge.name)
        if br_found is None:
            self.bridgeController.create_bridge(bridge)
            logging.debug("Bridge created")
        else:
            logging.debug("Bridge already existent")

    # Ids
    def set_ids_configuration(self, json_ids_configuration):
        idsConfiguration = self.idsCoreParser.parse_ids_configuration(json_ids_configuration)
        self.idsCoreController.set_configuration(idsConfiguration)

    def add_attackToMonitor(self, attack):
        try:
            self.idsCoreController.add_attackToMonitor(attack)
        except ValueError as ve:
            raise ve
