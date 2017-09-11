from common.dd_client import DDclient
from threading import Event, Thread
import time
import logging

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class MessageBusController(object, metaclass=Singleton):

    def __init__(self):

        self.VNF_HELLO_TIMER = 5

        self.tenant_id = None
        self.graph_id = None
        self.vnf_id = None
        self.rest_address = None

        self.is_registered_to_bus = False
        self.registered_to_bus = Event()
        self.is_registered_to_cs = False
        self.registered_to_cs = Event()

        logging.debug("Ho inizializzato il MessageBusController")

    def set_handler(self, handler):
        self.handler = handler

    def publish_public_on_bus(self, topic, data):
        logging.debug("(publish_public) Topic: " + topic + " Data: " + data)
        self.ddClient.publish_public_topic(topic, data)

    def publish_on_bus(self, topic, data):
        logging.debug("(publish) Topic: " + topic + " Data: " + data)
        self.ddClient.publish_topic(topic, data)

    def subscribe(self, topic):
        logging.debug("(subscribe) Topic: " + topic)
        self.ddClient.subscribe(topic, "noscope")

    def on_data_callback(self, src, msg):
        logging.debug("(on_data_callback) From: " + src + " Msg: " + msg)

        if "REGISTERED" in msg:
            if self.is_registered_to_cs is False:
                self.is_registered_to_cs = True
                self.registered_to_cs.set()

    def on_pub_callback(self, src, topic, msg):
        logging.debug("(on_pub_callback) Src: " + src + " Topic: " + topic + " Msg: " + msg)
        if self.handler is not None:
            self.handler.handle_topic(src, topic, msg)

    def on_reg_callback(self):
        #logging.debug("[MessageBusController] on_reg ack")
        self.is_registered_to_bus = True
        self.registered_to_bus.set()

    def register_to_bus(self, name, broker_url, customer, tenant_keys):
        self.ddClient = DDclient(self)
        self.registered_to_bus.clear()
        self.ddClient.register_to_bus(name, broker_url, customer, tenant_keys)
        while self.is_registered_to_bus is False:  # waiting for the agent to be registered to DD broker
            self.registered_to_bus.wait()

    def register_to_cs(self, tenant_id, graph_id, vnf_id, rest_address):
        self.tenant_id = tenant_id
        self.graph_id = graph_id
        self.vnf_id = vnf_id
        self.rest_address = rest_address

        self.registered_to_cs.clear()
        while self.is_registered_to_cs is False:  # waiting for the agent to be registered to the configuration service
            if not self.registered_to_cs.wait(5):
                if self.is_registered_to_cs is False:
                    self._send_vnf_hello()

    def schedule_hello_message(self):
        thread = Thread(target=self._periodic_vnf_hello)
        thread.start()

    def _periodic_vnf_hello(self):
        while True:
            #logging.debug("_periodic_vnf_hello!")
            self._send_vnf_hello()
            time.sleep(self.VNF_HELLO_TIMER)

    def _send_vnf_hello(self):
        msg = ""
        msg += "tenant-id " + self.tenant_id + "\n"
        msg += "graph-id " + self.graph_id + "\n"
        msg += "vnf-id " + self.vnf_id + "\n"
        msg += "rest-address " + self.rest_address
        self.publish_public_on_bus('vnf_hello', msg)