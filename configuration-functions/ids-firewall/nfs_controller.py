from requests.exceptions import HTTPError
from cf_core.message_bus_controller import MessageBusController
from cf_core.rest_client import RestClient
import logging
import json

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class NfsController(object, metaclass=Singleton):

    def __init__(self):
        self.ids_rest_address = None
        self.ids_id = None
        self.ids_triple = None

        self.firewall_id = None
        self.firewall_rest_address = None
        self.url_policy = "/firewall/policies"

        self.vnf_hello_topic = "vnf_hello"
        self.ids_topic = None

        MessageBusController().set_handler(self)
        self.restClient = RestClient()
        logging.debug("Ho inizializzato l'NfsController")

    def set_nfs(self, json_nfs):
        ids_id = json_nfs['ids']
        firewall_id = json_nfs['firewall']
        self.set_ids_id(ids_id)
        self.set_firewall_id(firewall_id)

    def get_nfs(self):
        pass

    def get_ids_id(self):
        return self.ids_id
    def set_ids_id(self, ids_id):
        self.ids_id = ids_id
        logging.debug("set ids_id: " + ids_id)
        #self.ids_topic = self.ids_id + "/config-ids:ids/attack_detected"
        self.ids_topic = self.ids_triple + "/config-ids:ids/attack_detected"
        MessageBusController().subscribe(self.ids_topic)

    def get_firewall_id(self):
        return self.firewall_id
    def set_firewall_id(self, firewall_id):
        self.firewall_id = firewall_id
        logging.debug("set firewall_id: " + firewall_id)


    def handle_topic(self, src, topic, msg):
        #logging.debug("[handle_topic] src: " + src + " topic: " + topic + " msg: " + msg)

        if topic.__eq__(self.vnf_hello_topic):
            self._handle_vnf_hello(msg)

        elif topic.__eq__(self.ids_topic):
            self._handle_attack(msg)


    def _handle_vnf_hello(self, msg):

        tenant_id = None
        graph_id = None
        vnf_id = None
        rest_address = None

        data = json.loads(msg)
        tenant_id = data['tenant-id']
        graph_id = data['graph-id']
        vnf_id = data['vnf-id']
        rest_address = data['rest-address']

        if self.ids_id is not None:
            if vnf_id == self.ids_id:
                self.ids_triple = tenant_id + "." + graph_id + "." + vnf_id
                if self.ids_rest_address is None:
                    self.ids_rest_address = rest_address
                    logging.debug("Saved ids rest_address: " + rest_address)
                elif self.ids_rest_address != rest_address:
                    self.ids_rest_address = rest_address
                    logging.debug("Replaced ids rest_address: " + rest_address)

        if self.firewall_id is not None:
            if vnf_id == self.firewall_id:
                if self.firewall_rest_address is None:
                    self.firewall_rest_address = rest_address
                    logging.debug("Saved firewall rest_address: " + rest_address)
                elif self.firewall_rest_address != rest_address:
                    self.firewall_rest_address = rest_address
                    logging.debug("Replaced firewall rest_address: " + rest_address)

    def _handle_attack(self, msg):

        json_data = json.loads(msg)
        data = json_data["data"]

        attack_name = data["attack_name"]
        logging.debug("Attack received: " + attack_name)
        if attack_name.__eq__("port_scan"):
            protocol = "tcp"
        elif attack_name.__eq__("ping_flood"):
            protocol = "icmp"
        else:
            logging.info("Attack: " + attack_name + " unknown.")
            logging.info("I can't configure the firewall")
            return

        src_ip = data["src_address"]
        dst_ip = data["dst_address"]

        policy_dict = {}
        policy_dict["action"] = "drop"
        policy_dict["protocol"] = protocol
        policy_dict["src-address"] = src_ip
        policy_dict["dst-address"] = dst_ip
        policy_dict["description"] = "Block " + protocol + " traffic"

        url = self.firewall_rest_address + self.url_policy
        logging.debug("url to use for post: " + url)

        try:
            self.restClient.post(url, json.dumps(policy_dict))
        except HTTPError as err:
            logging.debug(err)
        except Exception as ex:
            logging.debug(ex)
