from cf_core.dd_client import DDclient
from cf_core.config_instance import ConfigurationInstance
from threading import Event
import json
import logging
import sys

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class MessageBusController(object, metaclass=Singleton):

    def __init__(self):
        self.handler = None

        self.tenant_keys = None
        self.broker_url = None
        self.triple = None

        self.is_registered_to_bus = False
        self.registered_to_bus = Event()

        logging.debug("Ho inizializzato il MessageBusController")

    def set_handler(self, handler):
        self.handler = handler

    def publish_on_bus(self, topic, data):
        logging.debug("(publish) Topic: " + topic + " Data: " + data)
        self.ddClient.publish_topic(topic, json.dumps(data))

    def subscribe(self, topic):
        logging.debug("(subscribe) Topic: " + topic)
        self.ddClient.subscribe(topic, "noscope")

    def on_data_callback(self, src, msg):
        logging.debug("(on_data_callback) From: " + src + " Msg: " + msg)

    def on_pub_callback(self, src, topic, msg):
        logging.debug("(on_pub_callback) Src: " + src + " Topic: " + topic + " Msg: " + msg)
        if self.handler is not None:
            self.handler.handle_topic(src, topic, msg)

    def on_reg_callback(self):
        self.is_registered_to_bus = True
        self.registered_to_bus.set()

    def register_to_bus(self):
        datadisk_path = ConfigurationInstance().get_datadisk_path()
        self._read_datadisk(datadisk_path)
        self.ddClient = DDclient(self)
        self.registered_to_bus.clear()
        self.ddClient.register_to_bus("configFunctions", self.broker_url, self.tenant_keys)
        while self.is_registered_to_bus is False:  # waiting for the agent to be registered to DD broker
            self.registered_to_bus.wait()
        logging.info("DoubleDecker Successfully started")

    def _read_datadisk(self, datadisk_path):
        self.tenant_keys = datadisk_path + "/tenant-keys.json"
        metadata_path = datadisk_path + "/metadata.json"
        self._read_metadata_file(metadata_path)

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

                tenant_id = metadata['tenant-id']
                graph_id = metadata['graph-id']
                vnf_id = metadata['vnf-id']
                self.triple = tenant_id+'.'+graph_id+'.'+vnf_id
                #ConfigurationInstance.set_triple(self, self.tenant_id+'.'+self.graph_id+'.'+self.vnf_id)
                self.broker_url = metadata['broker-url']

        except Exception as e:
            logging.debug("Error during metadata reading.\n" + str(e))
            sys.exit(1)