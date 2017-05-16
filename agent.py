#!/usr/bin/python3
# -*- coding: utf-8 -*-
from config_parser import ConfigParser
from config_instance import ConfigurationInstance
from threading import Event
from threading import Thread
from utils import Bash
from message_bus import MessageBus

from vnf_template_library.exception import TemplateValidationError
from vnf_template_library.template import Template
from vnf_template_library.validator import ValidateTemplate

from dhcp.controller.dd_dhcp_controller import DoubleDeckerDhcpController
#from firewall.controller.dd_firewall_controller import DoubleDeckerFirewallController
#from nat.controller.dd_nat_controller import DoubleDeckerNatController

import sys
import logging
import os
import shutil
import json

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%H:%M:%S')

class ConfigurationAgent():

    def __init__(self, nf_type, datadisk_path):

        self.configParser = ConfigParser()
        self.messageBus = MessageBus(self)

        self.vnf = self.configParser.get("settings", "vnf")
        assert self.vnf=="dhcp" or \
               self.vnf =="firewall" or \
               self.vnf=="nat", \
               "Error, found an invalid vnf name in the config file"

        ConfigurationInstance.set_vnf(self, self.configParser.get("settings", "vnf"))
        ConfigurationInstance.set_nf_type(self, nf_type)
        ConfigurationInstance.set_datadisk_path(self, datadisk_path)

        self.vnf = ConfigurationInstance.get_vnf(self)
        self.nf_type = ConfigurationInstance.get_nf_type(self)
        self.datadisk_path = ConfigurationInstance.get_datadisk_path(self)

        logging.debug(self.vnf + " agent started...")
        logging.debug("nf_type: " + self.nf_type)
        logging.debug("datadisk_path: " + self.datadisk_path)

        ###################################################################
        self.tenant_id = None
        self.graph_id = None
        self.vnf_id = None
        self.broker_url = None
        self.configuration_interface = None
        '''
        is_registered_to_dd is a flag notifying if the agent is already registered to the message broker
        Only after such a registration the agent can ask for the configuration service registration
        registered_to_dd is a condition variable which awakes when the registration with the broker is successfull
        '''
        self.is_registered_to_dd = False
        self.registered_to_dd = Event()
        '''
        is_registered_to_cs is a flag notifying if the agent is already registered to the configuration service
        Only after such a registration the agent can start exporting its status
        Registered_to_cs is a condition variable which awakes when the registration with the cs is successfull
        '''
        self.is_registered_to_cs = False
        self.registered_to_cs = Event()
        '''
        datadisk_path contains the path where an external volume is attached to the VNF.
        Inside such a module you can find a metadata file containing some information about the VNF
        The datadisk contains:
        - tenant keys
        - template of the VNF
        - a metadata file
        - an initial configuration the VNF has tu use at bootstrap (optional)
        '''
        assert os.path.isdir(self.datadisk_path) is True, "datadisk not mounted onto the VNF"
        self.tenant_keys_file = self.datadisk_path + "/tenant-keys.json"
        self.template = self.datadisk_path + "/template.json"
        self.metadata_file = self.datadisk_path + "/metadata"
        self.initial_configuration_path = self.datadisk_path + "/initial_configuration.json"
        assert os.path.exists(self.tenant_keys_file) is True, "tenant-keys.json file not found in datadisk"
        assert os.path.exists(self.template), "Error, VNF template not found in datadisk"
        assert os.path.exists(self.metadata_file) is True, "metadata file not found in datadisk"
        self._read_metadata_file(self.metadata_file)
        if os.path.isdir("/etc/doubledecker") is False:
            os.makedirs("/etc/doubledecker")
        if os.path.exists("/etc/doubledecker/" + self.tenant_id + "-keys.json") is False:
            shutil.copy(self.tenant_keys_file, "/etc/doubledecker/" + self.tenant_id + "-keys.json")

        self.configuration_interface = self._get_iface_from_template()
        logging.debug("configuration interface: " + self.configuration_interface)

        # Add rule in the routing table to contact the broker
        #self._add_broker_rule(self.broker_url, self.configuration_interface)

        self.start_agent()


        ###################################################################

        #self.vnf_agent = None
        #vnf_agent_class = getattr(sys.modules[__name__], self.vnf)
        #self.vnf_agent = vnf_agent_class()

        #self.firewallController = FirewallController()
        #self.natController = NatController()
        #self.dhcpController = DhcpController()

        #json_data = open("tmp/FW_initial_configuration.json").read()
        #json_data = open("tmp/NAT_initial_configuration.json").read()
        #json_data = open("tmp/DHCP_initial_configuration.json").read()

        #data = json.loads(json_data)

        #self.firewallController.set_configuration(data)
        #self.natController.set_configuration(data)
        #self.dhcpController.set_configuration(data)


        #status = self.firewallController.get_status()
        #status = self.natController.get_status()
        #status = self.dhcpController.get_status()

        #print(json.dumps(status, indent=4, sort_keys=True))



    def start_agent(self):
        """
        Agent core method. It manages the registration both to the message broker and to the configuration service
        :return:
        """
        self.registered_to_dd.clear()
        self.registered_to_cs.clear()

        logging.debug("Trying to register to the message broker...")
        self.messageBus.register_to_dd(name=self.vnf,
                                       dealer_url=self.broker_url,
                                       customer=self.tenant_id,
                                       keyfile="/etc/doubledecker/" + self.tenant_id + "-keys.json")
        while self.is_registered_to_dd is False:  # waiting for the agent to be registered to DD broker
            self.registered_to_dd.wait()
        logging.debug("Trying to register to the message broker...done!")
        while self.is_registered_to_cs is False:  # waiting for the agent to be registered to the configuration service
            logging.debug("Trying to register to the configuration service...")
            if not self.registered_to_cs.wait(5):
                if self.is_registered_to_cs is False:
                    self._vnf_registration()
        logging.debug("Trying to register to the configuration service...done!")

        controller = self._select_controller()
        controller.start()

        logging.debug("End program")

    def on_reg_callback(self):
        self.is_registered_to_dd = True
        self.registered_to_dd.set()
        self._vnf_registration()

    def on_data_callback(self, src, msg):
        logging.debug("[agent] From: " + src + " Msg: " + msg)

        if msg == "REGISTERED " + self.tenant_id + '.' + self.vnf_id:
            self.is_registered_to_cs = True
            self.registered_to_cs.set()
            return

    def _select_controller(self):
        controller = None
        if self.vnf == "dhcp":
            return DoubleDeckerDhcpController(self.messageBus)
        elif self.vnf == "firewall":
            pass
            #return DoubleDeckerFirewallController(self.messageBus)
        elif self.vnf == "nat":
            pass
            #return DoubleDeckerNatController(self.messageBus)

    def _read_metadata_file(self, metadata_path):
        """
        It reads the volume attached to the VNF (datadisk) and looks for the information the VNF needs
        It excpects to find a metadata file describing the VNF's name, ID and tenant ID
        :param ds_metadata:
        :return:
        """
        try:
            metadata = open(metadata_path, "r")
            for line in metadata.readlines():
                words = "".join(line.split()).split('=')
                if words[0] == "tenant-id":
                    self.tenant_id = words[1]
                elif words[0] == "graph-id":
                    self.graph_id = words[1]
                elif words[0] == "vnf-id":
                    self.vnf_id = words[1]
                elif words[0] == "broker-url":
                    self.broker_url = words[1]
                else:
                    logging.debug("unknown keyword in metadata: " + words[0])
        except Exception as e:
            logging.debug("Error during metadata reading.\n" + str(e))
            sys.exit(1)
        finally:
            if metadata is not None:
                metadata.close()

        assert self.tenant_id is not None, "tenant-id key not found in metadata file"
        assert self.graph_id is not None, "graph-id key not found in metadata file"
        assert self.vnf_id is not None, "vnf-id key not found in metadata file"
        assert self.broker_url is not None, "broker-url key not found in metadata file"

    def _get_iface_from_template(self):
        with open(self.template) as template_data:
            tmpl = json.load(template_data)

        template = Template()
        try:
            validator = ValidateTemplate()
            validator.validate(tmpl)
            template.parseDict(tmpl)
        except TemplateValidationError as e:
            logging.debug("template parsing failed")
            exit(1)

        for port in template.ports:
            if port.label == "management":
                iface = port.name + port.position.split('-')[0]
        assert iface is not None, "Error, the template does not contain a management interface"

        return iface

    def _add_broker_rule(self, broker_url, management_iface):
        """
        This method add a route in the routing table that allow the vnf to contact the broker
        :param broker_url: read by the metadata file format: tcp://address:url
        :return:
        """
        broker_address = (broker_url.split(':')[1])[2:]
        logging.debug('route add ' + broker_address + ' dev ' + management_iface)
        Bash('route add ' + broker_address + ' dev ' + management_iface)

    def _register_to_dd(self, name, dealer_url, customer, keyfile):
        super().__init__(name=name.encode('utf8'),
                         dealerurl=dealer_url,
                         customer=customer.encode('utf8'),
                         keyfile=keyfile)
        thread = Thread(target=self.start)
        thread.start()
        return thread

    def _vnf_registration(self):
        msg = ""
        msg += "tenant-id:" + self.tenant_id + "\n"
        msg += "graph-id:" + self.graph_id + "\n"
        msg += "vnf-id:" + self.vnf_id
        logging.debug('Registering to the configuration service: ' + msg)
        self.messageBus.publish_public_topic('public.vnf_registration', msg)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Error to start: usage agent.py <nf_type> <datadisk_path>")
    else:
        if sys.argv[1] != "docker" and sys.argv[1] != "vm" and sys.argv[1] != "native":
            print("Error to start: <nf_type> can be 'docker' or 'native' or 'vm'")
        else:
            ConfigurationAgent(sys.argv[1], sys.argv[2])