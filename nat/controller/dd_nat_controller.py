from nat.controller.nat_controller import NatController
from common.controller.interface_controller import InterfaceController
from common.parser.interface_parser import InterfaceParser

import logging
import time
import json

class DoubleDeckerNatController():

    def __init__(self, message_bus, tenant_id, graph_id, vnf_id):

        self.messageBus = message_bus
        self.messageBus.set_controller(self)

        self.tenant_id = tenant_id
        self.graph_id = graph_id
        self.vnf_id = vnf_id

        self.natController = NatController()

        self.interfaceController = InterfaceController()
        self.interfaceParser = InterfaceParser()

        ############# Parameters to monitor #############
        #################################################
        self.interfaces_old = []
        self.interfaces_to_export = []
        self.interfaces_removed = []
        ##################################################



    def start(self, initial_configuration):
        logging.debug("ddNatController started")

        self.interfaces_old = self.natController.get_interfaces()

        if initial_configuration is not None:
            logging.debug("Initial_configuration is not none, trying to set")
            self.natController.set_configuration(initial_configuration)
            logging.debug("Configuration completed")

        while True:
            # Export the status every 3 seconds
            time.sleep(8)
            logging.debug("I'm: ddNatController")

            self._get_new_interfaces()
            self._get_new_nat_server_configuration()
            self._get_new_clients()

            if len(self.interfaces_to_export) > 0:
                self._publish_new_interfaces()
                self.interfaces_to_export = []

            if len(self.interfaces_removed) > 0:
                self._publish_interfaces_removed()
                self.interfaces_removed = []

            if self.nat_server_configuration_to_export is not None:
                self._publish_new_nat_server_configuration()
                self.nat_server_configuration_to_export = None

            if len(self.nat_clients_to_export) > 0:
                self._publish_new_clients()
                self.nat_clients_to_export = []

            if len(self.nat_clients_removed) > 0:
                self._publish_clients_removed()
                self.nat_clients_removed = []


            """
            logging.debug("interfaces_old: ")
            for x in self.interfaces_old:
                logging.debug(x.__str__())
            logging.debug("interfaces_to_export: ")
            for x in self.interfaces_to_export:
                logging.debug(x.__str__())
            logging.debug("interfaces_to_remove: ")
            for x in self.interfaces_removed:
                logging.debug(x.__str__())
            """

        thread.join()


    def on_data_callback(self, src, msg):
        logging.debug("[ddNatController] From: " + src + " Msg: " + msg)


    def _get_new_interfaces(self):
        curr_interfaces = self.InterfaceController.get_interfaces()
        for interface in curr_interfaces:
            if interface not in self.interfaces_old:
                self.interfaces_to_export.append(interface)
        for interface in self.interfaces_old:
            if interface not in curr_interfaces:
                self.interfaces_removed.append(interface)
        self.interfaces_old = curr_interfaces


    def _publish_new_interfaces(self):
        interfaces_dict = []
        for interface in self.interfaces_to_export:
            interfaces_dict.append(self.interfaceParser.get_interface_dict(interface))
        self.messageBus.publish_public_topic(self.tenant_id + "." +
                                             self.graph_id + "." +
                                             self.vnf_id + "." +
                                             "config-nat:interfaces/ifEntry_UPDATE",
                                             json.dumps(interfaces_dict, indent=4, sort_keys=True))

    def _publish_interfaces_removed(self):
        interfaces_dict = []
        for interface in self.interfaces_removed:
            interfaces_dict.append(self.interfaceParser.get_interface_dict(interface))
        self.messageBus.publish_public_topic(self.tenant_id + "." +
                                             self.graph_id + "." +
                                             self.vnf_id + "." +
                                             "config-nat:interfaces/ifEntry_DELETE",
                                             json.dumps(interfaces_dict, indent=4, sort_keys=True))

