from message_bus import MessageBus
from dhcp.controller.dhcp_controller import DhcpController
from dhcp.controller.dhcp_server_controller import DhcpServerController

import logging
import time

class DoubleDeckerDhcpController():

    def __init__(self, message_bus):

        self.messageBus = message_bus
        self.messageBus.set_controller(self)
        self.dhcpController = DhcpController()
        self.dhcpServerController = DhcpController()

        self.interfaces_old = []
        self.interfaces_to_export = []
        self.interfaces_removed = []

        self.dhcp_server_configuration_old = None
        self.dhcp_server_configuration_to_export = None

        self.dhcp_clients_old = []
        self.dhcp_clients_to_export = []
        self.dhcp_clients_removed = []




    def start(self, initial_configuration):
        logging.debug("ddDhcpController started")

        self.dhcp_clients_old = self.dhcpServerController.get_clients()
        self.dhcp_server_configuration_old = self.dhcpServerController.get_dhcp_server_configuration()
        self.interfaces_old = self.dhcpServerController.get_interfaces()

        if initial_configuration is not None:
            logging.debug("Initial_configuration is not none, trying to set")
            self.dhcpController.set_configuration(initial_configuration)
            logging.debug("Configuration completed")

        while True:
            # Export the status every 3 seconds
            time.sleep(8)
            logging.debug("I'm: ddDhcpController")

            self.get_new_clients()
            self.get_new_interfaces()
            self.get_new_dhcp_server_configuration()

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



    def get_new_interfaces(self):
        curr_interfaces = self.dhcpServerController.get_interfaces()
        for interface in curr_interfaces:
            if interface not in self.interfaces_old:
                self.interfaces_to_export.append(interface)
        for interface in self.interfaces_old:
            if interface not in curr_interfaces:
                self.interfaces_removed.append(interface)
        self.interfaces_old = curr_interfaces

    def get_new_dhcp_server_configuration(self):
        curr_dhcp_server_configuration = self.dhcpServerController.get_dhcp_server_configuration()
        if not curr_dhcp_server_configuration.__eq__(self.dhcp_server_configuration_old):
            self.dhcp_server_configuration_to_export = curr_dhcp_server_configuration
            self.dhcp_server_configuration_old = curr_dhcp_server_configuration

    def get_new_clients(self):
        curr_clients = self.dhcpServerController.get_clients()
        for client in curr_clients:
            if client not in self.dhcp_clients_old:
                self.dhcp_clients_to_export.append(client)
        for client in self.dhcp_clients_old:
            if client not in curr_clients:
                self.dhcp_clients_removed.append(client)
        self.dhcp_clients_old = curr_clients






