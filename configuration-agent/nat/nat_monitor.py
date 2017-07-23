from components.common.interface.interface_controller import InterfaceController
from components.common.interface.interface_monitor import InterfacesMonitor
from components.nat.nat_table.nat_table_controller import NatTableController
from components.nat.nat_table.nat_table_monitor import NatTableMonitor
from nat.nat_controller import NatController

from threading import Thread
from datetime import datetime
import logging
import json

class NatMonitor():

    def __init__(self, tenant_id, graph_id, vnf_id):

        self.messageBus = None

        self.natController = NatController()
        self.interfaceController = InterfaceController()
        self.natTableController = NatTableController()

        self.tenant_id = tenant_id
        self.graph_id = graph_id
        self.vnf_id = vnf_id

        self.configuration_interface = None

        self.interfacesMonitor = None
        self.natTableMonitor = None

    def set_initial_configuration(self, initial_configuration):

        curr_interfaces = self.interfaceController.get_interfaces()
        self.interfacesMonitor = InterfacesMonitor(self, curr_interfaces)

        curr_natTable = self.natController.get_nat_table()
        self.natTableMonitor = NatTableMonitor(self, curr_natTable)

        logging.debug("Setting initial configuration...")
        self.natController.set_configuration(initial_configuration)
        logging.debug("Setting initial configuration...done!")

    def get_address_of_configuration_interface(self, configuration_interface):
        self.configuration_interface = configuration_interface
        return self.natController.get_interface_ipv4Configuration_address(configuration_interface)

    def start(self, message_bus):

        self.messageBus = message_bus
        self.messageBus.set_controller(self)

        threads = []
        threads.append(Thread(target=self.interfacesMonitor.start_monitoring, args=()))
        threads.append(Thread(target=self.natTableMonitor.start_monitoring, args=()))

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
        logging.debug("[FirewallMonitor] From: " + src + " Msg: " + msg)