from components.common.traffic_shaper.traffic_shaper_controller import TrafficShaperController as TrafficShaperCoreController
from components.common.traffic_shaper.traffic_shaper_parser import TrafficShaperParser as TrafficShaperCoreParser
#from components.common.interface.interface_controller import InterfaceController
#from components.common.interface.interface_parser import InterfaceParser

class TrafficShaperController():

    def __init__(self):
        #self.interfaceController = InterfaceController()
        #self.interfaceParser = InterfaceParser
        self.trafficShaperCoreController = TrafficShaperCoreController()
        self.trafficShaperCoreParser = TrafficShaperCoreParser()

    """
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
    """

    # Traffic Shaper
    def start_bandwitdh_shaping(self, json_traffic_shaper):
        traffic_shaper = self.trafficShaperCoreParser.parse_traffic_shaper_configuration(json_traffic_shaper)
        interface_id = self.trafficShaperCoreParser.parse_interface_to_control(json_traffic_shaper)
        interface = self.interfaceController.get_interface_by_id(interface_id)
        traffic_shaper.add_interface_name(interface.name)
        traffic_shaper.add_interface_address(interface.ipv4_configuration.address)
        self.trafficShaperCoreController.start_bandwitdh_shaping(traffic_shaper)

    def stop_bandwitdh_shaping(self):
        self.trafficShaperCoreController.start_bandwitdh_shaping(interface_name)

    def get_status(self):
        self.trafficShaperCoreController.get_status(interface_name)
