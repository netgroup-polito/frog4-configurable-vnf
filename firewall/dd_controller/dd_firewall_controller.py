from firewall.controller.firewall_controller import FirewallController
from firewall.controller.policy_controller import PolicyController
from firewall.controller.blacklist_controller import BlacklistController
from firewall.controller.whitelist_controller import WhitelistController
from common.controller.interface_controller import InterfaceController

#from firewall.dd_controller.interface_monitor import InterfacesMonitor
from firewall.dd_controller.policies_monitor import PoliciesMonitor
from firewall.dd_controller.blacklist_monitor import BlacklistMonitor
from firewall.dd_controller.whitelist_monitor import WhitelistMonitor

from threading import Thread
from datetime import datetime

import logging
import json

class DoubleDeckerFirewallController():

    def __init__(self, message_bus, tenant_id, graph_id, vnf_id):

        self.messageBus = message_bus
        self.messageBus.set_controller(self)

        self.firewallController = FirewallController()
        self.interfaceController = InterfaceController()
        self.policyController = PolicyController()
        self.blacklistController = BlacklistController()
        self.whitelistController = WhitelistController()

        self.tenant_id = tenant_id
        self.graph_id = graph_id
        self.vnf_id = vnf_id

        self.configuration_interface = None

        self.interfacesMonitor = None
        self.policiesMonitor = None
        self.blacklistMonitor = None
        self.whitelistMonitor = None

    def set_initial_configuration(self, initial_configuration):

        #curr_interfaces = self.interfaceController.get_interfaces()
        #self.interfacesMonitor = InterfacesMonitor(self, curr_interfaces)

        curr_policies = self.firewallController.get_policies()
        self.policiesMonitor = PoliciesMonitor(self, curr_policies)

        curr_blacklist = self.blacklistController.get_blacklist()
        self.blacklistMonitor = BlacklistMonitor(self, curr_blacklist)

        curr_whitelist = self.whitelistController.get_whitelist()
        self.whitelistMonitor = WhitelistMonitor(self, curr_whitelist)


        logging.debug("Setting initial configuration...")
        self.firewallController.set_configuration(initial_configuration)
        logging.debug("Setting initial configuration...done!")

    def get_address_of_configuration_interface(self, configuration_interface):
        self.configuration_interface = configuration_interface
        return self.firewallController.get_interface_ipv4Configuration_address(configuration_interface)

    def start(self):

        threads = []
        #threads.append(Thread(target=self.interfacesMonitor.start_monitoring, args=()))
        threads.append(Thread(target=self.policiesMonitor.start_monitoring, args=()))
        threads.append(Thread(target=self.blacklistMonitor.start_monitoring, args=()))
        threads.append(Thread(target=self.whitelistMonitor.start_monitoring, args=()))

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
        logging.debug("[ddFirewallController] From: " + src + " Msg: " + msg)