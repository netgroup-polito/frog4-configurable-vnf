from dhcp.controller.dhcp_controller import DhcpController
from dhcp.controller.dhcp_server_controller import DhcpServerController
from common.controller.interface_controller import InterfaceController
from dhcp.parser.dhcp_server_parser import DhcpServerParser
from common.parser.interface_parser import InterfaceParser

import logging
import time
import json

class DoubleDeckerDhcpController():

    def __init__(self, message_bus, tenant_id, graph_id, vnf_id):

        self.messageBus = message_bus
        self.messageBus.set_controller(self)

        self.tenant_id = tenant_id
        self.graph_id = graph_id
        self.vnf_id = vnf_id

        self.dhcpController = DhcpController()

        self.interfaceController = InterfaceController()
        self.interfaceParser = InterfaceParser()

        self.dhcpServerController = DhcpServerController()
        self.dhcpServerParser = DhcpServerParser()



        ############# Parameters to monitor #############
        #################################################
        self.interfaces_old = []
        self.interfaces_to_export = []
        self.interfaces_removed = []

        self.dhcp_server_configuration_old = None
        self.dhcp_server_configuration_to_export = None

        self.dhcp_clients_old = []
        self.dhcp_clients_to_export = []
        self.dhcp_clients_removed = []
        ##################################################



    def start(self, initial_configuration):
        logging.debug("ddDhcpController started")

        self.interfaces_old = self.interfaceController.get_interfaces()
        self.dhcp_clients_old = self.dhcpServerController.get_clients()
        self.dhcp_server_configuration_old = self.dhcpServerController.get_dhcp_server_configuration()


        if initial_configuration is not None:
            logging.debug("Initial_configuration is not none, trying to set")
            self.dhcpController.set_configuration(initial_configuration)
            logging.debug("Configuration completed")

        while True:
            # Export the status every 3 seconds
            time.sleep(8)
            logging.debug("I'm: ddDhcpController")

            self._get_new_interfaces()
            self._get_new_dhcp_server_configuration()
            self._get_new_clients()

            if len(self.interfaces_to_export) > 0:
                self._publish_new_interfaces()
                self.interfaces_to_export = []

            if len(self.interfaces_removed) > 0:
                self._publish_interfaces_removed()
                self.interfaces_removed = []

            if self.dhcp_server_configuration_to_export is not None:
                self._publish_new_dhcp_server_configuration()
                self.dhcp_server_configuration_to_export = None

            if len(self.dhcp_clients_to_export) > 0:
                self._publish_new_clients()
                self.dhcp_clients_to_export = []

            if len(self.dhcp_clients_removed) > 0:
                self._publish_clients_removed()
                self.dhcp_clients_removed = []


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

            logging.debug("dhcp_server_config_old: ")
            logging.debug(self.dhcp_server_configuration_old.__str__())
            logging.debug("dhcp_server_config_to_export: ")
            logging.debug(self.dhcp_server_configuration_to_export.__str__())

            logging.debug("clients_old: ")
            for x in self.dhcp_clients_old:
                logging.debug(x.__str__())
            logging.debug("clients_to_export: ")
            for x in self.dhcp_clients_to_export:
                logging.debug(x.__str__())
            logging.debug("clients_to_remove: ")
            for x in self.dhcp_clients_removed:
                logging.debug(x.__str__())

        thread.join()


    def on_data_callback(self, src, msg):
        logging.debug("[ddDhcpController] From: " + src + " Msg: " + msg)



    def _get_new_interfaces(self):
        curr_interfaces = self.interfaceController.get_interfaces()
        for interface in curr_interfaces:
            if interface not in self.interfaces_old:
                self.interfaces_to_export.append(interface)
        for interface in self.interfaces_old:
            if interface not in curr_interfaces:
                self.interfaces_removed.append(interface)
        self.interfaces_old = curr_interfaces

    def _get_new_dhcp_server_configuration(self):
        curr_dhcp_server_configuration = self.dhcpServerController.get_dhcp_server_configuration()
        if not curr_dhcp_server_configuration.__eq__(self.dhcp_server_configuration_old):
            self.dhcp_server_configuration_to_export = curr_dhcp_server_configuration
            self.dhcp_server_configuration_old = curr_dhcp_server_configuration

    def _get_new_clients(self):
        curr_clients = self.dhcpServerController.get_clients()
        for client in curr_clients:
            if client not in self.dhcp_clients_old:
                self.dhcp_clients_to_export.append(client)
        for client in self.dhcp_clients_old:
            if client not in curr_clients:
                self.dhcp_clients_removed.append(client)
        self.dhcp_clients_old = curr_clients

    def _publish_new_interfaces(self):
        interfaces_dict = []
        for interface in self.interfaces_to_export:
            interfaces_dict.append(self.interfaceParser.get_interface_dict(interface))
        self.messageBus.publish_public_topic(self.tenant_id + "." +
                                             self.graph_id + "." +
                                             self.vnf_id + "." +
                                             "config-dhcp-server:interfaces/ifEntry_UPDATE",
                                             json.dumps(interfaces_dict, indent=4, sort_keys=True))

    def _publish_interfaces_removed(self):
        interfaces_dict = []
        for interface in self.interfaces_removed:
            interfaces_dict.append(self.interfaceParser.get_interface_dict(interface))
        self.messageBus.publish_public_topic(self.tenant_id + "." +
                                             self.graph_id + "." +
                                             self.vnf_id + "." +
                                             "config-dhcp-server:interfaces/ifEntry_DELETE",
                                             json.dumps(interfaces_dict, indent=4, sort_keys=True))

    def _publish_new_dhcp_server_configuration(self):
        dhcp_server_config_dict = self.dhcpServerParser.get_dhcp_server_configuration_dict(self.dhcp_server_configuration_to_export)
        self.messageBus.publish_public_topic(self.tenant_id + "." +
                                             self.graph_id + "." +
                                             self.vnf_id + "." +
                                             "config-dhcp-server:server/globalIpPool_UPDATE",
                                             json.dumps(dhcp_server_config_dict, indent=4, sort_keys=True))

    def _publish_new_clients(self):
        clients_dict = []
        for client in self.dhcp_clients_to_export:
            clients_dict.append(self.dhcpServerParser.get_client_dict(client))
        self.messageBus.publish_public_topic(self.tenant_id + "." +
                                             self.graph_id + "." +
                                             self.vnf_id + "." +
                                             "config-dhcp-server:server/clients_UPDATE",
                                             json.dumps(clients_dict, indent=4, sort_keys=True))

    def _publish_clients_removed(self):
        clients_dict = []
        for client in self.dhcp_clients_to_export:
            clients_dict.append(self.dhcpServerParser.get_client_dict(client))
        self.messageBus.publish_public_topic(self.tenant_id + "." +
                                             self.graph_id + "." +
                                             self.vnf_id + "." +
                                             "config-dhcp-server:server/clients_DELETE",
                                             json.dumps(clients_dict, indent=4, sort_keys=True))






