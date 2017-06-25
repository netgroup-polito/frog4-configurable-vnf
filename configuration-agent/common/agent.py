#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import logging
import os
import shutil
import sys
from subprocess import call
from threading import Event
from threading import Thread

from common.config_instance import ConfigurationInstance
from common.dd_client import DDclient
from common.utils import Bash
from common.db.db_manager import dbManager

from common.vnf_template_library.exception import TemplateValidationError
from common.vnf_template_library.template import Template
from common.vnf_template_library.validator import ValidateTemplate

# set log level
log_format = '%(asctime)s [%(levelname)s] %(filename)s:%(lineno)s %(message)s'
log_date_format = '[%d-%m-%Y %H:%M:%S]'
logging.basicConfig(filename="logging_agent.log", level=logging.DEBUG, format=log_format, datefmt=log_date_format)

class ConfigurationAgent():

    def __init__(self, vnf_name, nf_type, datadisk_path, on_change_interval=None):

        self.messageBus = DDclient(self)
        self.dd_controller = None

        ConfigurationInstance.set_vnf(self, vnf_name)
        ConfigurationInstance.set_nf_type(self, nf_type)
        ConfigurationInstance.set_datadisk_path(self, datadisk_path)
        if on_change_interval is not None:
            ConfigurationInstance.set_on_change_interval(self, int(on_change_interval)/1000)
        else:
            ConfigurationInstance.set_on_change_interval(self, 1)

        self.vnf = ConfigurationInstance.get_vnf(self)
        self.nf_type = ConfigurationInstance.get_nf_type(self)
        self.datadisk_path = ConfigurationInstance.get_datadisk_path(self)

        logging.debug("nf_type: " + self.nf_type)
        logging.debug("datadisk_path: " + self.datadisk_path)
        logging.debug("on_change_interval: " + str(ConfigurationInstance.get_on_change_interval(self)))

        dbManager().clear_db()

        ###################################################################
        self.tenant_id = None
        self.graph_id = None
        self.vnf_id = None
        self.broker_url = None
        self.configuration_interface = None
        '''
        is_registered_to_bus is a flag notifying if the agent is already registered to the message broker
        Only after such a registration the agent can ask for the configuration service registration
        registered_to_bus is a condition variable which awakes when the registration with the broker is successfull
        '''
        self.is_registered_to_bus = False
        self.registered_to_bus = Event()
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
        self.metadata_file = self.datadisk_path + "/metadata.json"
        self.initial_configuration_path = self.datadisk_path + "/initial_configuration.json"
        assert os.path.exists(self.tenant_keys_file) is True, "Error, tenant-keys.json file not found in datadisk"
        assert os.path.exists(self.template), "Error, template.json file not found in datadisk"
        assert os.path.exists(self.metadata_file) is True, "Error, metadata.json file not found in datadisk"
        self._read_metadata_file(self.metadata_file)
        if os.path.isdir("/etc/doubledecker") is False:
            os.makedirs("/etc/doubledecker")
        if os.path.exists("/etc/doubledecker/" + self.tenant_id + "-keys.json") is False:
            shutil.copy(self.tenant_keys_file, "/etc/doubledecker/" + self.tenant_id + "-keys.json")

        self.configuration_interface = self._get_iface_from_template()
        logging.debug("configuration interface: " + self.configuration_interface)
        ConfigurationInstance.set_iface_management(self, self.configuration_interface)

        # Add rule in the routing table to contact the broker
        self._add_broker_rule(self.broker_url, self.configuration_interface)

        self.initial_configuration = None
        if os.path.exists(self.initial_configuration_path):
            with open(self.initial_configuration_path) as configuration:
                json_data = configuration.read()
                self.initial_configuration = json.loads(json_data)


    def create_dd_controller(self, ddSpecificController):
        self.dd_controller = ddSpecificController(self.tenant_id, self.graph_id, self.vnf_id)

    def set_initial_configuration(self):
        self.dd_controller.set_initial_configuration(self.initial_configuration)
        self.rest_address = self.dd_controller.get_address_of_configuration_interface(self.configuration_interface)

    def register_agent(self):
        """
        Agent core method. It manages the registration both to the message broker and to the configuration service
        :return:
        """
        self.registered_to_bus.clear()
        self.registered_to_cs.clear()

        logging.debug("Trying to register to the message broker...")
        dd_name = self.tenant_id+'.'+self.graph_id+'.'+self.vnf_id
        self.messageBus.register_to_bus(name=dd_name,
                                       dealer_url=self.broker_url,
                                       customer=self.tenant_id,
                                       keyfile="/etc/doubledecker/" + self.tenant_id + "-keys.json")
        while self.is_registered_to_bus is False:  # waiting for the agent to be registered to DD broker
            self.registered_to_bus.wait()
        logging.debug("Trying to register to the message broker...done!")
        while self.is_registered_to_cs is False:  # waiting for the agent to be registered to the configuration service
            logging.debug("Trying to register to the configuration service...")
            if not self.registered_to_cs.wait(5):
                if self.is_registered_to_cs is False:
                    self._vnf_registration()
        logging.debug("Trying to register to the configuration service...done!")

    def start_dd_controller(self):
        thread = Thread(target=self.dd_controller.start, args=[self.messageBus])
        thread.start()
        logging.info("DoubleDecker Successfully started")

    def start_rest_controller(self, rest_app):
        rest_port = "9000"
        if self.is_registered_to_bus is True:
            topic = self.tenant_id + "." + self.graph_id + "." + self.vnf_id + "/restServer"
            data = self.rest_address + ":" + rest_port
            self.messageBus.publish_public_topic(topic, data)
        logging.info("Rest Server started on: " + self.rest_address + ':' + rest_port)
        call("gunicorn -b " + self.rest_address + ':' + rest_port + " -t 500 " + rest_app + ":app", shell=True)

    def on_reg_callback(self):
        self.is_registered_to_bus = True
        self.registered_to_bus.set()
        self._vnf_registration()

    def on_data_callback(self, src, msg):
        logging.debug("[agent] From: " + src + " Msg: " + msg)

        if msg.__eq__("REGISTERED"):
            self.is_registered_to_cs = True
            self.registered_to_cs.set()


    def _read_metadata_file(self, metadata_path):
        """
        It reads the volume attached to the VNF (datadisk) and looks for the information the VNF needs
        It excpects to find a metadata file describing the VNF's name, ID and tenant ID
        :param ds_metadata:
        :return:
        """
        try:
            with open(metadata_path) as metadata_file:

                json_data = metadata_file.read()
                metadata = json.loads(json_data)

                assert 'tenant-id' in metadata, "tenant-id key not found in metadata file"
                assert 'graph-id' in metadata, "graph-id key not found in metadata file"
                assert 'vnf-id' in metadata, "vnf-id key not found in metadata file"
                assert 'broker-url' in metadata, "broker-url key not found in metadata file"

                self.tenant_id = metadata['tenant-id']
                self.graph_id = metadata['graph-id']
                self.vnf_id = metadata['vnf-id']
                ConfigurationInstance.set_triple(self, self.tenant_id+'.'+self.graph_id+'.'+self.vnf_id)
                self.broker_url = metadata['broker-url']

        except Exception as e:
            logging.debug("Error during metadata reading.\n" + str(e))
            sys.exit(1)

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

    def _vnf_registration(self):
        msg = ""
        msg += "tenant-id:" + self.tenant_id + "\n"
        msg += "graph-id:" + self.graph_id + "\n"
        msg += "vnf-id:" + self.vnf_id
        self.messageBus.publish_public_topic('vnf_registration', msg)
