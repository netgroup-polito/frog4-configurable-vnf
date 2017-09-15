from components.common.interface.interface_controller import InterfaceController
from components.common.interface.interface_monitor import InterfacesMonitor
from ids.ids_controller import IdsController
from common.message_bus_controller import MessageBusController

from threading import Thread
from datetime import datetime
import logging
import json

class IdsMonitor():

    def __init__(self, tenant_id, graph_id, vnf_id):

        self.idsController = IdsController()
        self.interfaceController = InterfaceController()

        self.tenant_id = tenant_id
        self.graph_id = graph_id
        self.vnf_id = vnf_id

        self.configuration_interface = None

        self.interfacesMonitor = None

    def set_initial_configuration(self, initial_configuration):

        curr_interfaces = self.interfaceController.get_interfaces()
        self.interfacesMonitor = InterfacesMonitor(self, curr_interfaces)

        logging.debug("Setting initial configuration...")
        self.idsController.set_configuration(initial_configuration)
        logging.debug("Setting initial configuration...done!")

    def get_address_of_configuration_interface(self, configuration_interface):
        self.configuration_interface = configuration_interface
        return self.idsController.get_interface_ipv4Configuration_address(configuration_interface)

    def start(self):

        threads = []
        threads.append(Thread(target=self.interfacesMonitor.start_monitoring, args=()))

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
        MessageBusController().publish_on_bus(msg, json.dumps(body, indent=4, sort_keys=True))