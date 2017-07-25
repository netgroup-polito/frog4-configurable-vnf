from components.common.traffic_shaper.traffic_shaper_controller import TrafficShaperController as TrafficShaperCoreController
from components.common.traffic_shaper.traffic_shaper_parser import TrafficShaperParser as TrafficShaperCoreParser
from components.common.interface.interface_controller import InterfaceController
from components.common.interface.interface_parser import InterfaceParser
from traffic_shaper.traffic_shaper_parser import TrafficShaperParser
import logging

# set log level
log_format = '%(asctime)s [%(levelname)s] %(filename)s:%(lineno)s %(message)s'
log_date_format = '[%d-%m-%Y %H:%M:%S]'
logging.basicConfig(level=logging.DEBUG, format=log_format, datefmt=log_date_format)


class TrafficShaperController():

    def __init__(self):
        self.trafficShaperParser = TrafficShaperParser()

        self.interfaceController = InterfaceController()
        self.interfaceParser = InterfaceParser

        self.trafficShaperCoreController = TrafficShaperCoreController()
        self.trafficShaperCoreParser = TrafficShaperCoreParser()

    def set_configuration(self, json_configuration):

        json_interfaces = self.trafficShaperParser.parse_interfaces(json_configuration)
        for json_iface in json_interfaces:
            self.configure_interface(json_iface)

        json_traffic_shaper = self.trafficShaperParser.parse_traffic_shaper_configuration(json_configuration)
        self.start_bandwitdh_shaping(json_traffic_shaper)

    def get_full_status(self):

        status = {}

        status["config-traffic-shaper:interfaces"] = self.get_interfaces_status()
        status["config-traffic-shaper:traffic_shaper"] = self.get_all_traffic_shapers()

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

    # Traffic Shaper
    def start_bandwitdh_shaping(self, json_traffic_shaper):
        logging.debug(json_traffic_shaper)
        traffic_shaper = self.trafficShaperCoreParser.parse_traffic_shaper_configuration(json_traffic_shaper)
        logging.debug(traffic_shaper.__str__())
        interface_id = self.trafficShaperCoreParser.parse_interface_to_control(json_traffic_shaper)
        interface = self.interfaceController.get_interface_by_id(interface_id)
        traffic_shaper.add_interface_name(interface.name)
        traffic_shaper.add_interface_address(interface.ipv4_configuration.address)
        self.trafficShaperCoreController.start_bandwitdh_shaping(traffic_shaper)

    def stop_bandwitdh_shaping(self, interface_name):
        if self.trafficShaperCoreController.traffic_shaper_exists(interface_name):
            self.trafficShaperCoreController.stop_bandwitdh_shaping(interface_name)
        else:
            raise ValueError("could not find traffic shaper for interface: " + interface_name)

    def update_bandwitdh_shaping_download_limit(self, interface_name, download_limit):
        if self.trafficShaperCoreController.traffic_shaper_exists(interface_name):
            self.trafficShaperCoreController.update_bandwidth_shaping_download_limit(interface_name, download_limit)
        else:
            raise ValueError("could not find traffic shaper for interface: " + interface_name)

    def update_bandwitdh_shaping_upload_limit(self, interface_name, upload_limit):
        if self.trafficShaperCoreController.traffic_shaper_exists(interface_name):
            self.trafficShaperCoreController.update_bandwidth_shaping_upload_limit(interface_name, upload_limit)
        else:
            raise ValueError("could not find traffic shaper for interface: " + interface_name)

    def get_all_traffic_shapers(self):
        traffic_shapers_dict = []
        traffic_shaper_list = self.trafficShaperCoreController.get_all_traffic_shapers()
        for traffic_shaper in traffic_shaper_list:
            traffic_shapers_dict.append(self.trafficShaperCoreParser.get_traffic_shaper_dict(traffic_shaper))
        return traffic_shapers_dict

    def get_traffic_shaper(self, interface_name):
        if interface_name is not None:
            if self.trafficShaperCoreController.traffic_shaper_exists(interface_name):
                traffic_shaper = self.trafficShaperCoreController.get_traffic_shaper(interface_name)
                return self.trafficShaperCoreParser.get_traffic_shaper_dict(traffic_shaper)
            else:
                raise ValueError("could not find traffic shaper for interface: " + interface_name)