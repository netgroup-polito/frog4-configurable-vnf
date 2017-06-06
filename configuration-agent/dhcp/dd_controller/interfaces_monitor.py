from common.controller.interface_controller import InterfaceController
from common.parser.interface_parser import InterfaceParser
from common.model.interface import Interface
from common.model.interface import Ipv4Configuration
from dhcp.dd_controller.element import Element

from common.constants import Constants
from common.config_instance import ConfigurationInstance
from threading import Thread

import logging
import time


class InterfacesMonitor():

    def __init__(self, dd_controller, curr_interfaces):

        self.EVENT_ADD = Constants.EVENT_ADD
        self.EVENT_UPDATE = Constants.EVENT_UPDATE
        self.EVENT_DELETE = Constants.EVENT_DELETE

        ######################### YANG CONSTANTS #########################
        self.SILENT = Constants.ADVERTISE_SILENT
        self.ON_CHANGE = Constants.ADVERTISE_ON_CHANGE
        self.PERIODIC = Constants.ADVERTISE_PERIODIC

        self.url_iface = "config-dhcp-server:interfaces/ifEntry"
        self.url_name = "/name"
        self.url_type = "/type"
        self.url_management = "/management"
        self.url_ipv4Config = "/ipv4_configuration"
        self.url_ipv4Config_address = self.url_ipv4Config + "/address"
        self.url_ipv4Config_netmask = self.url_ipv4Config + "/netmask"
        self.url_ipv4Config_macAddress = self.url_ipv4Config + "/mac_address"
        self.url_ipv4Config_defaultGW = self.url_ipv4Config + "/default_gw"

        self.elements = {}
        self.elements['interface'] = Element(advertise=self.SILENT)
        self.elements['name'] = Element(advertise=self.ON_CHANGE)
        self.elements['type'] = Element(advertise=self.ON_CHANGE)
        self.elements['management'] = Element(advertise=self.ON_CHANGE)
        self.elements['ipv4Configuration'] = Element(advertise=self.PERIODIC, period=5000)
        self.elements['address'] = Element(advertise=self.ON_CHANGE)
        self.elements['netmask'] = Element(advertise=self.ON_CHANGE)
        self.elements['macAddress'] = Element(advertise=self.SILENT)
        self.elements['defaultGW'] = Element(advertise=self.ON_CHANGE)
        ##################################################################

        self.periods = []
        for key, element in self.elements.items():
            if element.advertise == self.PERIODIC:
                element.period = element.period/1000
                if element.period not in self.periods:
                    self.periods.append(element.period)

        self.on_change_interval = ConfigurationInstance.get_on_change_interval(self)
        logging.debug("on_change_interval: " + str(self.on_change_interval))

        self.interfaces_old = curr_interfaces
        print("interfaces_old: " + str(len(self.interfaces_old)))
        self.interfaces_new = []
        self.interfaces_updated = []
        self.interfaces_removed = []

        self.ddController = dd_controller
        self.interfaceController = InterfaceController()
        self.interfaceParser = InterfaceParser()

    def start_monitoring(self):

        logging.debug("Interfaces monitoring started!")

        for period in self.periods:
            Thread(target=self._timer_periodic_callback, args=([period])).start()

        while True:

            self._get_new_interfaces()

            #print("interfaces_new: " + str(len(self.interfaces_new)))
            if len(self.interfaces_new) > 0:
                for interface in self.interfaces_new:
                    id = interface.name
                    self._publish_interface_leafs_on_change(id, interface, self.EVENT_ADD)
                self.interfaces_new = []

            #print("interfaces_removed: " + str(len(self.interfaces_removed)))
            if len(self.interfaces_removed) > 0:
                for interface in self.interfaces_removed:
                    id = interface.name
                    self._publish_interface_leafs_on_change(id, interface, self.EVENT_DELETE)
                self.interfaces_removed = []

            #print("interfaces_updated: " + str(len(self.interfaces_updated)))
            if len(self.interfaces_updated) > 0:
                for interface_map in self.interfaces_updated:
                    old_interface = interface_map['old']
                    new_interface = interface_map['new']
                    interface_diff = self._find_diff(old_interface, new_interface)
                    logging.debug(interface_diff.__str__())
                    id = new_interface.name
                    self._publish_interface_leafs_on_change(id, interface_diff, self.EVENT_UPDATE)
                self.interfaces_updated = []

            time.sleep(self.on_change_interval)

    def _get_new_interfaces(self):
        curr_interfaces = self.interfaceController.get_interfaces()
        interface_map = {}
        # Check new or modified interfaces
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
        # Check if an interface was removed
        for old_interface in self.interfaces_old:
            # get the old interface whose name is the same of the new interface
            interface = next((x for x in curr_interfaces if x.name == old_interface.name), None)
            if interface is None:
                self.interfaces_removed.append(old_interface)
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

    def _publish_interface_leafs_on_change(self, id, interface, method):

        if self.elements['interface'].advertise == self.ON_CHANGE:
            self._publish_interface(id, interface, method)

        if interface.name is not None:
            if self.elements['name'].advertise == self.ON_CHANGE:
                self._publish_interface_name(id, interface.name, method)

        if interface.type is not None:
            if self.elements['type'].advertise == self.ON_CHANGE:
                self._publish_interface_type(id, interface.type, method)

        if interface.management is not None:
            if self.elements['management'].advertise == self.ON_CHANGE:
                self._publish_interface_management(id, interface.management, method)

        if interface.ipv4_configuration is not None:
            if self.elements['ipv4Configuration'].advertise == self.ON_CHANGE:
                self._publish_interface_ipv4Config(id, interface.ipv4_configuration, method)

            if interface.ipv4_configuration.address is not None:
                if self.elements['address'].advertise == self.ON_CHANGE:
                    self._publish_interface_ipv4Config_address(id, interface.ipv4_configuration.address, method)

            if interface.ipv4_configuration.netmask is not None:
                if self.elements['netmask'].advertise == self.ON_CHANGE:
                    self._publish_interface_ipv4Config_netmask(id, interface.ipv4_configuration.netmask, method)

            if interface.ipv4_configuration.mac_address is not None:
                if self.elements['macAddress'].advertise == self.ON_CHANGE:
                    self._publish_interface_ipv4Config_macAddress(id, interface.ipv4_configuration.mac_address, method)

            if interface.ipv4_configuration.default_gw is not None:
                if self.elements['defaultGW'].advertise == self.ON_CHANGE:
                    self._publish_interface_ipv4Config_defaultGW(id, interface.ipv4_configuration.default_gw, method)

    def _publish_interface_leafs_periodic(self, interface, period):

        id = interface.name

        if self.elements['interface'].advertise == self.PERIODIC and self.elements['interface'].period == period:
            self._publish_interface(id, interface)

        if interface.name is not None:
            if self.elements['name'].advertise == self.PERIODIC and self.elements['name'].period == period:
                self._publish_interface_name(id, interface.name)

        if interface.type is not None:
            if self.elements['type'].advertise == self.PERIODIC and self.elements['type'].period == period:
                self._publish_interface_type(id, interface.type)

        if interface.management is not None:
            if self.elements['management'].advertise == self.PERIODIC and self.elements['management'].period == period:
                self._publish_interface_management(id, interface.management)

        if interface.ipv4_configuration is not None:
            if self.elements['ipv4Configuration'].advertise == self.PERIODIC and self.elements['ipv4Configuration'].period == period:
                self._publish_interface_ipv4Config(id, interface.ipv4_configuration)

            if interface.ipv4_configuration.address is not None:
                if self.elements['address'].advertise == self.PERIODIC and self.elements['address'].period == period:
                    self._publish_interface_ipv4Config_address(id, interface.ipv4_configuration.address)

            if interface.ipv4_configuration.netmask is not None:
                if self.elements['netmask'].advertise == self.PERIODIC and self.elements['netmask'].period == period:
                    self._publish_interface_ipv4Config_netmask(id, interface.ipv4_configuration.netmask)

            if interface.ipv4_configuration.mac_address is not None:
                if self.elements['macAddress'].advertise == self.PERIODIC and self.elements['macAddress'].period == period:
                    self._publish_interface_ipv4Config_macAddress(id, interface.ipv4_configuration.mac_address)

            if interface.ipv4_configuration.default_gw is not None:
                if self.elements['defaultGW'].advertise == self.PERIODIC and self.elements['defaultGW'].period == period:
                    self._publish_interface_ipv4Config_defaultGW(id, interface.ipv4_configuration.default_gw)

    def _timer_periodic_callback(self, period):

        while True:

            time.sleep(period)

            logging.debug("timer callback, period:" + str(period))
            curr_interfaces = self.interfaceController.get_interfaces()
            for interface in curr_interfaces:
                self._publish_interface_leafs_periodic(interface, period)


    ################### Private publish functions ###################
    def _publish_interface(self, id, data, method=None):
        interface_dict = self.interfaceParser.get_interface_dict(data)
        url = self.url_iface + "/" + id
        self.ddController.publish_on_bus(url, method, interface_dict)

    def _publish_interface_name(self, id, data, method=None):
        url = self.url_iface + "/" + id + self.url_name
        self.ddController.publish_on_bus(url, method, data)

    def _publish_interface_type(self, id, data, method=None):
        url = self.url_iface + "/" + id + self.url_type
        self.ddController.publish_on_bus(url, method, data)

    def _publish_interface_management(self, id, data, method=None):
        url = self.url_iface + "/" + id + self.url_management
        self.ddController.publish_on_bus(url, method, data)

    def _publish_interface_ipv4Config(self, id, data, method=None):
        ipv4Config_dict = self.interfaceParser.get_interface_ipv4Configuration(data)
        url = self.url_iface + "/" + id + self.url_ipv4Config
        self.ddController.publish_on_bus(url, method, ipv4Config_dict)

    def _publish_interface_ipv4Config_address(self, id, data, method=None):
        url = self.url_iface + "/" + id + self.url_ipv4Config_address
        self.ddController.publish_on_bus(url, method, data)

    def _publish_interface_ipv4Config_netmask(self, id, data, method=None):
        url = self.url_iface + "/" + id + self.url_ipv4Config_netmask
        self.ddController.publish_on_bus(url, method, data)

    def _publish_interface_ipv4Config_macAddress(self, id, data, method=None):
        url = self.url_iface + "/" + id + self.url_ipv4Config_macAddress
        self.ddController.publish_on_bus(url, method, data)

    def _publish_interface_ipv4Config_defaultGW(self, id, data, method=None):
        url = self.url_iface + "/" + id + self.url_ipv4Config_defaultGW
        self.ddController.publish_on_bus(url, method, data)

