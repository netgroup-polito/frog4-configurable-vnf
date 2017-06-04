from nat.controller.nat_controller import NatController
from nat.controller.floating_ip_controller import FloatingIpController
from common.controller.interface_controller import InterfaceController

#from nat.dd_controller.nat_table_monitor import NatTableMonitor
#from nat.dd_controller.floating_ip_monitor import FloatingIpMonitor
#from nat.dd_controller.interface_monitor import InterfaceMonitor

from threading import Thread
from datetime import datetime

import logging
import json

class DoubleDeckerNatController():

    def __init__(self, message_bus, tenant_id, graph_id, vnf_id):

        self.messageBus = message_bus
        self.messageBus.set_controller(self)

        self.natController = NatController()
        self.interfaceController = InterfaceController()
        #self.floatingIpController = FloatingIpController()

        self.tenant_id = tenant_id
        self.graph_id = graph_id
        self.vnf_id = vnf_id

        self.configuration_interface = None

        self.interfacesMonitor = None
        self.natTableMonitor = None
        #self.floatingIpMonitor = None

    def set_initial_configuration(self, initial_configuration):

        #curr_interfaces = self.interfaceController.get_interfaces()
        #self.interfacesMonitor = InterfacesMonitor(self, curr_interfaces)

        #curr_natTable = self.natController.get_nat_table()
        #self.natTableMonitor = NatTableMonitor(self, curr_natTable)

        #curr_floating_ips = self.floatingIpController.get_all_floating_ip()
        #self.floatingIpMonitor = FloatingIpMonitor(self, curr_floating_ips)

        logging.debug("Setting initial configuration...")
        self.natController.set_configuration(initial_configuration)
        logging.debug("Setting initial configuration...done!")

    def get_address_of_configuration_interface(self, configuration_interface):
        self.configuration_interface = configuration_interface
        return self.natController.get_interface_ipv4Configuration_address(configuration_interface)

    def start(self):

        threads = []
        #threads.append(Thread(target=self.interfacesMonitor.start_monitoring, args=()))
        #threads.append(Thread(target=self.natTableMonitor.start_monitoring, args=()))
        #threads.append(Thread(target=self.floatingIpMonitor.start_monitoring, args=()))

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
        logging.debug("[ddNatController] From: " + src + " Msg: " + msg)