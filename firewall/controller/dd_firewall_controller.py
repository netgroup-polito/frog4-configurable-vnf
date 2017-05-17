from firewall.controller.firewall_controller import FirewallController
from firewall.controller.policy_controller import PolicyController
from firewall.controller.blacklist_controller import BlacklistController
from firewall.controller.whitelist_controller import WhitelistController
from common.controller.interface_controller import InterfaceController
from firewall.parser.policy_parser import PolicyParser
from firewall.parser.blacklist_parser import BlacklistParser
from firewall.parser.whitelist_parser import WhitelistParser
from common.parser.interface_parser import InterfaceParser

import logging
import time
import json


class DoubleDeckerFirewallController():
    def __init__(self, message_bus, tenant_id, graph_id, vnf_id):

        self.messageBus = message_bus
        self.messageBus.set_controller(self)

        self.tenant_id = tenant_id
        self.graph_id = graph_id
        self.vnf_id = vnf_id

        self.firewallController = FirewallController()

        self.interfaceController = InterfaceController()
        self.interfaceParser = InterfaceParser()

        self.policyController = PolicyController()
        self.policyParser = PolicyParser()

        self.blacklistController = BlacklistController()
        self.blacklistParser = BlacklistParser()

        self.whitelistController = WhitelistController()
        self.whitelistParser = WhitelistParser()

        ############# Parameters to monitor #############
        #################################################
        self.interfaces_old = []
        self.interfaces_to_export = []
        self.interfaces_removed = []

        self.policies_old = []
        self.policies_to_export = []
        self.policies_removed = []

        self.blacklist_old = []
        self.blacklist_to_export = []
        self.blacklist_removed = []

        self.whitelist_old = []
        self.whitelist_to_export = []
        self.whitelist_removed = []
        ##################################################

    def start(self, initial_configuration):
        logging.debug("ddFirewallController started")

        self.interfaces_old = self.firewallController.get_interfaces()
        self.policies_old = self.firewallController.get_policies()
        self.blacklist_old = self.firewallController.get_blacklist()
        self.whitelist_old = self.firewallController.get_whitelist()

        if initial_configuration is not None:
            logging.debug("Initial_configuration is not none, trying to set")
            self.firewallController.set_configuration(initial_configuration)
            logging.debug("Configuration completed")

        while True:
            # Export the status every 3 seconds
            time.sleep(8)
            logging.debug("I'm: ddFirewallController")

            self._get_new_interfaces()
            self._get_new_policies()
            self._get_new_blacklist()
            self._get_new_whitelist()

            if len(self.interfaces_to_export) > 0:
                self._publish_new_interfaces()
                self.interfaces_to_export = []

            if len(self.interfaces_removed) > 0:
                self._publish_interfaces_removed()
                self.interfaces_removed = []

            if len(self.policies_to_export) > 0:
                self._publish_new_clients()
                self.policies_to_export = []

            if len(self.policies_removed) > 0:
                self._publish_clients_removed()
                self.policies_removed = []

            if len(self.blacklist_to_export) > 0:
                self._publish_new_blacklist()
                self.blacklist_to_export = []

            if len(self.blacklist_removed) > 0:
                self._publish_blacklist_removed()
                self.blacklist_removed = []

            if len(self.whitelist_to_export) > 0:
                self._publish_new_whitelist()
                self.whitelist_to_export = []

            if len(self.whitelist_removed) > 0:
                self._publish_whitelist_removed()
                self.whitelist_removed = []

            """
            logging.debug("interfaces_old: ")
            for x in self.interfaces_old:
                logging.debug(x.__str__())
            logging.debug("interfaces_to_export: ")
            for x in self.interfaces_to_export:
                logging.debug(x.__str__())
            logging.debug("interfaces_to_remove: ")
            for x in self.interfaces_removed:
                logging.debug(x.__str__())
            

            logging.debug("clients_old: ")
            for x in self.policies_old:
                logging.debug(x.__str__())
            logging.debug("clients_to_export: ")
            for x in self.policies_to_export:
                logging.debug(x.__str__())
            logging.debug("clients_to_remove: ")
            for x in self.policies_removed:
                logging.debug(x.__str__())
            """

        thread.join()

    def on_data_callback(self, src, msg):
        logging.debug("[ddFirewallController] From: " + src + " Msg: " + msg)


    def _get_new_interfaces(self):
        curr_interfaces = self.interfaceController.get_interfaces()
        for interface in curr_interfaces:
            if interface not in self.interfaces_old:
                self.interfaces_to_export.append(interface)
        for interface in self.interfaces_old:
            if interface not in curr_interfaces:
                self.interfaces_removed.append(interface)
        self.interfaces_old = curr_interfaces

    def _get_new_policies(self):
        curr_policies = self.policyController.get_policies()
        for policy in curr_policies:
            if policy not in self.policies_old:
                self.policies_to_export.append(policy)
        for policy in self.policies_old:
            if policy not in curr_policies:
                self.policies_removed.append(policy)
        self.policies_old = curr_policies

    def _get_new_blacklist(self):
        curr_blacklist = self.blacklistController.get_blacklist()
        for url in curr_blacklist:
            if url not in self.blacklist_old:
                self.blacklist_to_export.append(url)
        for url in self.blacklist_old:
            if url not in curr_blacklist:
                self.blacklist_removed.append(url)
        self.blacklist_old = curr_blacklist

    def _get_new_whitelist(self):
        curr_whitelist = self.blacklistController.get_blacklist()
        for url in curr_whitelist:
            if url not in self.whitelist_old:
                self.whitelist_to_export.append(url)
        for url in self.whitelist_old:
            if url not in curr_whitelist:
                self.whitelist_removed.append(url)
        self.whitelist_old = curr_whitelist


    def _publish_new_interfaces(self):
        interfaces_dict = []
        for interface in self.interfaces_to_export:
            interfaces_dict.append(self.interfaceParser.get_interface_dict(interface))
        self.messageBus.publish_public_topic(self.tenant_id + "." +
                                             self.graph_id + "." +
                                             self.vnf_id + "." +
                                             "config-firewall:interfaces/ifEntry_UPDATE",
                                             json.dumps(interfaces_dict, indent=4, sort_keys=True))

    def _publish_interfaces_removed(self):
        interfaces_dict = []
        for interface in self.interfaces_removed:
            interfaces_dict.append(self.interfaceParser.get_interface_dict(interface))
        self.messageBus.publish_public_topic(self.tenant_id + "." +
                                             self.graph_id + "." +
                                             self.vnf_id + "." +
                                             "config-firewall:interfaces/ifEntry_DELETE",
                                             json.dumps(interfaces_dict, indent=4, sort_keys=True))

    def _publish_new_policies(self):
        policies_dict = []
        for policy in self.policies_to_export:
            policies_dict.append(self.policyParser.get_policy_dict(policy))
        self.messageBus.publish_public_topic(self.tenant_id + "." +
                                             self.graph_id + "." +
                                             self.vnf_id + "." +
                                             "config-firewall:server/policies_UPDATE",
                                             json.dumps(policies_dict, indent=4, sort_keys=True))

    def _publish_policies_removed(self):
        policies_dict = []
        for policy in self.policies_removed:
            policies_dict.append(self.policyParser.get_policy_dict(policy))
        self.messageBus.publish_public_topic(self.tenant_id + "." +
                                             self.graph_id + "." +
                                             self.vnf_id + "." +
                                             "config-firewall:server/policies_DELETE",
                                             json.dumps(policies_dict, indent=4, sort_keys=True))

    def _publish_new_blacklist(self):
        blacklist_dict = []
        for url in self.blacklist_to_export:
            blacklist_dict.append(self.blacklistParser.get_url_dict(url))
        self.messageBus.publish_public_topic(self.tenant_id + "." +
                                             self.graph_id + "." +
                                             self.vnf_id + "." +
                                             "config-firewall:server/blacklist_UPDATE",
                                             json.dumps(blacklist_dict, indent=4, sort_keys=True))

    def _publish_blacklist_removed(self):
        blacklist_dict = []
        for url in self.blacklist_to_export:
            blacklist_dict.append(self.blacklistParser.get_url_dict(url))
        self.messageBus.publish_public_topic(self.tenant_id + "." +
                                             self.graph_id + "." +
                                             self.vnf_id + "." +
                                             "config-firewall:server/blacklist_DELETE",
                                             json.dumps(blacklist_dict, indent=4, sort_keys=True))

    def _publish_new_whitelist(self):
        whitelist_dict = []
        for url in self.whitelist_to_export:
            whitelist_dict.append(self.whitelistParser.get_url_dict(url))
        self.messageBus.publish_public_topic(self.tenant_id + "." +
                                             self.graph_id + "." +
                                             self.vnf_id + "." +
                                             "config-firewall:server/whitelist_UPDATE",
                                             json.dumps(whitelist_dict, indent=4, sort_keys=True))

    def _publish_whitelist_removed(self):
        whitelist_dict = []
        for url in self.whitelist_to_export:
            whitelist_dict.append(self.whitelistParser.get_url_dict(url))
        self.messageBus.publish_public_topic(self.tenant_id + "." +
                                             self.graph_id + "." +
                                             self.vnf_id + "." +
                                             "config-firewall:server/whitelist_DELETE",
                                             json.dumps(whitelist_dict, indent=4, sort_keys=True))





