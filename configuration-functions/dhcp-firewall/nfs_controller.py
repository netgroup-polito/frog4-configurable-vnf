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
        self.dhcp_rest_address = None
        self.dhcp_id = None
        self.dhcp_triple = None

        self.firewall_id = None
        self.firewall_rest_address = None
        self.url_policy = "/firewall/policies"

        self.vnf_hello_topic = "vnf_hello"
        self.dhcp_client_topic = None

        MessageBusController().set_handler(self)
        self.restClient = RestClient()
        logging.debug("Ho inizializzato l'NfsController")

    def set_nfs(self, json_nfs):
        dhcp_id = json_nfs['dhcp']
        firewall_id = json_nfs['firewall']
        self.set_dhcp_id(dhcp_id)
        self.set_firewall_id(firewall_id)

    def get_nfs(self):
        pass

    def get_dhcp_id(self):
        return self.dhcp_id
    def set_dhcp_id(self, dhcp_id):
        self.dhcp_id = dhcp_id
        logging.debug("set dhcp_id: " + dhcp_id)
        #self.dhcp_client_topic = self.dhcp_id + "/config-dhcp-server:server/clients"
        self.dhcp_client_topic = self.dhcp_triple + "/config-dhcp-server:server/clients"
        MessageBusController().subscribe(self.dhcp_client_topic)

    def get_firewall_id(self):
        return self.firewall_id
    def set_firewall_id(self, firewall_id):
        self.firewall_id = firewall_id
        logging.debug("set firewall_id: " + firewall_id)


    def handle_topic(self, src, topic, msg):
        #logging.debug("[handle_topic] src: " + src + " topic: " + topic + " msg: " + msg)

        if topic.__eq__(self.vnf_hello_topic):
            self._handle_vnf_hello(msg)

        elif topic[:len(self.dhcp_client_topic)].__eq__(self.dhcp_client_topic):
            self._handle_new_dhcp_client(msg)


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

        if self.dhcp_id is not None:
            if vnf_id == self.dhcp_id:
                self.dhcp_triple = tenant_id + "." + graph_id + "." + vnf_id
                if self.dhcp_rest_address is None:
                    self.dhcp_rest_address = rest_address
                    logging.debug("Saved dhcp rest_address: " + rest_address)
                elif self.dhcp_rest_address != rest_address:
                    self.dhcp_rest_address = rest_address
                    logging.debug("Replaced dhcp rest_address: " + rest_address)

        if self.firewall_id is not None:
            if vnf_id == self.firewall_id:
                if self.firewall_rest_address is None:
                    self.firewall_rest_address = rest_address
                    logging.debug("Saved firewall rest_address: " + rest_address)
                elif self.firewall_rest_address != rest_address:
                    self.firewall_rest_address = rest_address
                    logging.debug("Replaced firewall rest_address: " + rest_address)

    def _handle_new_dhcp_client(self, msg):

        json_data = json.loads(msg)
        data = json_data["data"]

        client_ip_address = data["ip_address"]

        policy_1_dict = {}
        policy_1_dict["action"] = "accept"
        policy_1_dict["protocol"] = "all"
        policy_1_dict["src-address"] = client_ip_address
        policy_1_dict["description"] = "Allow egress traffic"

        policy_2_dict = {}
        policy_2_dict["action"] = "accept"
        policy_2_dict["protocol"] = "all"
        policy_2_dict["dst-address"] = client_ip_address
        policy_2_dict["description"] = "Allow ingress traffic"

        url = self.firewall_rest_address + self.url_policy
        logging.debug("url to use for post: " + url)

        try:
            self.restClient.post(url, json.dumps(policy_1_dict))
            self.restClient.post(url, json.dumps(policy_2_dict))
        except HTTPError as err:
            logging.debug(err)
        except Exception as ex:
            logging.debug(ex)