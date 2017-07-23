from components.common.interface.interface_controller import InterfaceController
from components.common.interface.interface_monitor import InterfacesMonitor
from components.dhcp.dhcp_server.dhcp_server_controller import DhcpServerController
from components.dhcp.dhcp_server.dhcp_server_monitor import DhcpServerMonitor
from components.dhcp.dhcp_client.dhcp_client_controller import DhcpClientController
from components.dhcp.dhcp_client.dhcp_client_monitor import DhcpClientsMonitor
from dhcp.dhcp_controller import DhcpController

from threading import Thread
from datetime import datetime
import logging
import json

class DhcpMonitor():

    def __init__(self, tenant_id, graph_id, vnf_id):

        self.messageBus = None

        self.dhcpController = DhcpController()
        self.interfaceController = InterfaceController()
        self.dhcpServerController = DhcpServerController()
        self.dhcpClientController = DhcpClientController()

        self.tenant_id = tenant_id
        self.graph_id = graph_id
        self.vnf_id = vnf_id

        self.configuration_interface = None

        self.interfacesMonitor = None
        self.dhcpServerMonitor = None
        self.dhcpClientsMonitor = None

    def set_initial_configuration(self, initial_configuration):

        curr_interfaces = self.interfaceController.get_interfaces()
        self.interfacesMonitor = InterfacesMonitor(self, curr_interfaces)

        curr_dhcp_server_configuration = self.dhcpServerController.get_dhcp_server_configuration()
        self.dhcpServerMonitor = DhcpServerMonitor(self, curr_dhcp_server_configuration)

        curr_dhcp_clients = self.dhcpClientController.get_clients()
        self.dhcpClientsMonitor = DhcpClientsMonitor(self, curr_dhcp_clients)

        logging.debug("Setting initial configuration...")
        self.dhcpController.set_configuration(initial_configuration)
        logging.debug("Setting initial configuration...done!")

    def get_address_of_configuration_interface(self, configuration_interface):
        self.configuration_interface = configuration_interface
        return self.dhcpController.get_interface_ipv4Configuration_address(configuration_interface)

    def start(self, message_bus):

        self.messageBus = message_bus
        self.messageBus.set_controller(self)

        threads = []
        threads.append(Thread(target=self.interfacesMonitor.start_monitoring, args=()))
        threads.append(Thread(target=self.dhcpServerMonitor.start_monitoring, args=()))
        threads.append(Thread(target=self.dhcpClientsMonitor.start_monitoring, args=()))

        # Start all threads
        for t in threads:
            t.start()

        # Wait for all of them to finish
        for t in threads:
            t.join()

    def publish_on_bus(self, url, method, data):
        msg = self.tenant_id + "." + self.graph_id + "." + self.vnf_id + "." + url
        body = {}
        if method is not None:
            body['event'] = method.upper()
        else:
            body['event'] = "PERIODIC"
        body['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        body['data'] = data
        self.messageBus.publish_topic(msg , json.dumps(body, indent=4, sort_keys=True))

    def on_data_callback(self, src, msg):
        logging.debug("[DhcpMonitor] From: " + src + " Msg: " + msg)






