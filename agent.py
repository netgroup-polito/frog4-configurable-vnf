#!/usr/bin/python3
# -*- coding: utf-8 -*-

#from dhcp.dhcp_agent import Dhcp
#from firewall.firewall_agent import Firewall
from config_parser import ConfigParser
from config_instance import ConfigurationInstance
from firewall.controller.firewall_controller import FirewallController
from nat.controller.nat_controller import NatController
from dhcp.controller.dhcp_controller import DhcpController
#from nat.nat_agent import Nat

from doubledecker import clientSafe

import sys
import logging
import json

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%H:%M:%S')

class ConfigurationAgent(clientSafe.ClientSafe):

    def __init__(self, nf_type, datadisk_path):

        self.configParser = ConfigParser()

        ConfigurationInstance.set_vnf(self, self.configParser.get("settings", "vnf"))
        ConfigurationInstance.set_nf_type(self, nf_type)
        ConfigurationInstance.set_datadisk_path(self, datadisk_path)

        self.vnf = ConfigurationInstance.get_vnf(self)
        self.nf_type = ConfigurationInstance.get_nf_type(self)
        self.datadisk_path = ConfigurationInstance.get_datadisk_path(self)

        logging.debug(self.vnf + " agent started...")
        logging.debug("nf_type: " + self.nf_type)
        logging.debug("datadisk_path: " + self.datadisk_path)

        #self.vnf_agent = None
        #vnf_agent_class = getattr(sys.modules[__name__], self.vnf)
        #self.vnf_agent = vnf_agent_class()

        self.firewallController = FirewallController()
        self.natController = NatController()
        self.dhcpController = DhcpController()

        #json_data = open("tmp/FW_initial_configuration.json").read()
        #json_data = open("tmp/NAT_initial_configuration.json").read()
        #json_data = open("tmp/DHCP_initial_configuration.json").read()
        #data = json.loads(json_data)
        #self.firewallController.set_configuration(data)
        #self.natController.set_configuration(data)
        #self.dhcpController.set_configuration(data)

        #status = self.firewallController.get_status()
        #status = self.natController.get_status()
        status = self.dhcpController.get_status()
        print(json.dumps(status, indent=4, sort_keys=True))

    def start_agent(self):
        pass

    def on_data(self):
        pass

    def on_discon(self):
        pass

    def on_error(self):
        pass

    def on_pub(self):
        pass

    def on_reg(self):
        pass




if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Error to start: usage agent.py <nf_type> <datadisk_path>")
    else:
        ConfigurationAgent(sys.argv[1], sys.argv[2])