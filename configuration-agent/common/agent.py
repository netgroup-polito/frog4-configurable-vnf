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
from common.message_bus_controller import MessageBusController
from common.dd_client import DDclient
from common.utils import Bash
from common.db.db_manager import dbManager

from vnf_template_library.exception import TemplateValidationError
from vnf_template_library.template import Template
from vnf_template_library.validator import ValidateTemplate

# set log level
log_format = '%(asctime)s [%(levelname)s] %(filename)s:%(lineno)s %(message)s'
log_date_format = '[%d-%m-%Y %H:%M:%S]'
logging.basicConfig(filename="logging_agent.log", level=logging.DEBUG, format=log_format, datefmt=log_date_format)

class ConfigurationAgent():

    def __init__(self, vnf_name, nf_type, datadisk_path, on_change_interval=None):

        self.monitor = None
        self.rest_port = "9010"

        ConfigurationInstance().clear_db()
        ConfigurationInstance().save_vnf_name(vnf_name)
        ConfigurationInstance().save_nf_type(nf_type)
        ConfigurationInstance().save_datadisk_path(datadisk_path)
        if on_change_interval is not None:
            on_change_interval = int(on_change_interval)/1000
        else:
            on_change_interval = 1
        ConfigurationInstance().save_on_change_interval(on_change_interval)

        self.vnf = ConfigurationInstance().get_vnf_name()
        self.nf_type = ConfigurationInstance().get_nf_type()
        self.datadisk_path = ConfigurationInstance().get_datadisk_path()

        logging.debug("nf_type: " + self.nf_type)
        logging.debug("datadisk_path: " + self.datadisk_path)
        logging.debug("on_change_interval: " + str(ConfigurationInstance().get_on_change_interval()))

        dbManager().clear_db()

        ###################################################################
        self.tenant_id = None
        self.graph_id = None
        self.vnf_id = None
        self.broker_url = None
        self.configuration_interface = None
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
        tenant_keys_path = "/etc/doubledecker/" + self.tenant_id + "-keys.json"
        if os.path.exists(tenant_keys_path) is False:
            shutil.copy(self.tenant_keys_file, tenant_keys_path)

        self.configuration_interface = self._get_iface_from_template()
        logging.debug("configuration interface: " + self.configuration_interface)
        ConfigurationInstance().save_iface_management(self.configuration_interface)

        # Add rule in the routing table to contact the broker
        #self._add_broker_rule(self.broker_url, self.configuration_interface)

        self.initial_configuration = None
        if os.path.exists(self.initial_configuration_path):
            with open(self.initial_configuration_path) as configuration:
                json_data = configuration.read()
                self.initial_configuration = json.loads(json_data)

    def start_monitoring(self, monitor_class):

        # Configure the vnf with the initial configuration
        # in order to obtain the ip address of the management interface
        self.monitor = monitor_class(self.tenant_id, self.graph_id, self.vnf_id)
        self.monitor.set_initial_configuration(self.initial_configuration)
        self.address_iface_management = self.monitor.get_address_of_configuration_interface(self.configuration_interface)
        self.rest_address = "http://" + self.address_iface_management + ":" + self.rest_port

        # Register vnf to the bus
        dd_name = self.tenant_id + '.' + self.graph_id + '.' + self.vnf_id
        tenant_keys = "/etc/doubledecker/" + self.tenant_id + "-keys.json"
        MessageBusController().register_to_bus(dd_name, self.broker_url, self.tenant_id, tenant_keys)
        logging.info("DoubleDecker Successfully started")

        # Register vnf to the configuration-orchestrator
        logging.debug("Trying to register to the configuration service...")
        MessageBusController().register_to_cs(self.tenant_id, self.graph_id, self.vnf_id, self.rest_address)
        logging.debug("Trying to register to the configuration service...done!")

        # Start monitoring
        thread = Thread(target=self.monitor.start)
        thread.start()

        # Start periodic sending of hello_message
        MessageBusController().schedule_hello_message()

    def start_rest_controller(self, rest_app):
        logging.info("Rest Server started on: " + self.rest_address)
        call("gunicorn -b " + self.address_iface_management + ':' + self.rest_port + " -t 500 " + rest_app + ":app", shell=True)

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
                triple = self.tenant_id+'.'+self.graph_id+'.'+self.vnf_id
                ConfigurationInstance().save_triple(triple)
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
