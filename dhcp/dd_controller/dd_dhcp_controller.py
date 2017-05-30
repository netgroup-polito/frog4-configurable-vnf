from dhcp.controller.dhcp_controller import DhcpController
from dhcp.controller.dhcp_server_controller import DhcpServerController
from common.controller.interface_controller import InterfaceController

from dhcp.dd_controller.interface_monitor import InterfaceMonitor
from dhcp.dd_controller.dhcp_server_monitor import DhcpServerMonitor

from threading import Thread

import logging
import time
import json

class DoubleDeckerDhcpController():

    def __init__(self, message_bus, tenant_id, graph_id, vnf_id):

        self.messageBus = message_bus
        self.messageBus.set_controller(self)

        self.dhcpController = DhcpController()
        self.interfaceController = InterfaceController()
        self.dhcpServerController = DhcpServerController()

        self.tenant_id = tenant_id
        self.graph_id = graph_id
        self.vnf_id = vnf_id

        self.configuration_interface = None

        self.interfaceMonitor = None
        self.dhcpServerMonitor = None
        self.dhcpClientsMonitor = None


    def set_initial_configuration(self, initial_configuration):

        curr_interfaces = self.interfaceController.get_interfaces()
        self.interfaceMonitor = InterfaceMonitor(self, curr_interfaces)

        curr_dhcp_server_configuration = self.dhcpServerController.get_dhcp_server_configuration()
        self.dhcpServerMonitor = DhcpServerMonitor(self, curr_dhcp_server_configuration)

        curr_dhcp_clients = self.dhcpServerController.get_clients()
        #self.dhcpClientsMonitor = DhcpClientsMonitor(self, curr_dhcp_server_configuration)

        logging.debug("Setting initial configuration...")
        self.dhcpController.set_configuration(initial_configuration)
        logging.debug("Setting initial configuration...done!")

    def get_address_of_configuration_interface(self, configuration_interface):
        self.configuration_interface = configuration_interface
        return self.dhcpController.get_interface_ipv4Configuration_address(configuration_interface)

    def start(self):

        threads = []
        threads.append(Thread(target=self.interfaceMonitor.start_monitoring, args=()))
        threads.append(Thread(target=self.dhcpServerMonitor.start_monitoring, args=()))
        #threads.append(Thread(target=self.dhcpClientsMonitor.start_monitoring, args=()))

        # Start all threads
        for t in threads:
            t.start()

        # Wait for all of them to finish
        for t in threads:
            t.join()



    def publish_on_bus(self, url, method, data):
        if method is not None:
            msg = self.tenant_id + "." + self.graph_id + "." + self.vnf_id + "." + url + '_' + method.upper()
        else:
            msg = self.tenant_id + "." + self.graph_id + "." + self.vnf_id + "." + url
        self.messageBus.publish_topic(msg , json.dumps(data, indent=4, sort_keys=True))

    def on_data_callback(self, src, msg):
        logging.debug("[ddDhcpController] From: " + src + " Msg: " + msg)




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





