from firewall.dd_controller.element import Element
from firewall.controller.policy_controller import PolicyController
from firewall.parser.policy_parser import PolicyParser
from firewall.model.policy import Policy

from common.constants import Constants
from config_instance import ConfigurationInstance
from threading import Thread

import logging
import time

class PoliciesMonitor():

    def __init__(self, dd_controller, curr_policies):
        self.EVENT_ADD = Constants.EVENT_ADD
        self.EVENT_UPDATE = Constants.EVENT_UPDATE
        self.EVENT_DELETE = Constants.EVENT_DELETE

        ######################### YANG CONSTANTS #########################
        self.SILENT = Constants.ADVERTISE_SILENT
        self.ON_CHANGE = Constants.ADVERTISE_ON_CHANGE
        self.PERIODIC = Constants.ADVERTISE_PERIODIC

        self.url_policy = "config-firewall:firewall/policies"
        self.url_description = "/description"
        self.url_action = "/action"
        self.url_protocol = "/protocol"
        self.url_inInterface = "/in-interface"
        self.url_outInterface = "/out-interface"
        self.url_srcAddress = "/src-address"
        self.url_dstAddress = "/dst-address"
        self.url_srcPort = "/src-port"
        self.url_dstPort = "/dst-port"

        self.elements = {}
        self.elements['policy'] = Element(advertise=self.ON_CHANGE)
        self.elements['description'] = Element(advertise=self.ON_CHANGE)
        self.elements['action'] = Element(advertise=self.ON_CHANGE)
        self.elements['protocol'] = Element(advertise=self.ON_CHANGE)
        self.elements['inInterface'] = Element(advertise=self.ON_CHANGE)
        self.elements['outInterface'] = Element(advertise=self.ON_CHANGE)
        self.elements['srcAddress'] = Element(advertise=self.ON_CHANGE)
        self.elements['dstAddress'] = Element(advertise=self.ON_CHANGE)
        self.elements['srcPort'] = Element(advertise=self.ON_CHANGE)
        self.elements['dstPort'] = Element(advertise=self.ON_CHANGE)
        ##################################################################

        self.periods = []
        for key, element in self.elements.items():
            if element.advertise == self.PERIODIC:
                element.period = element.period / 1000
                if element.period not in self.periods:
                    self.periods.append(element.period)

        self.on_change_interval = ConfigurationInstance.get_on_change_interval(self)
        logging.debug("on_change_interval: " + str(self.on_change_interval))

        self.policies_old = curr_policies
        print("policies_old: " + str(len(self.policies_old)))
        self.policies_new = []
        self.policies_updated = []
        self.policies_removed = []

        self.ddController = dd_controller
        self.policyController = PolicyController()
        self.policyParser = PolicyParser()

    def start_monitoring(self):
        logging.debug("Policies monitoring started!")

        for period in self.periods:
            Thread(target=self._timer_periodic_callback, args=([period])).start()

        while True:

            self._get_new_policies()

            # print("policies_new: " + str(len(self.policies_new)))
            if len(self.policies_new) > 0:
                for policy in self.policies_new:
                    id = policy.id
                    self._publish_policy_leafs_on_change(id, policy, self.EVENT_ADD)
                self.policies_new = []

            # print("policies_removed: " + str(len(self.policies_removed)))
            if len(self.policies_removed) > 0:
                for policy in self.policies_removed:
                    id = policy.id
                    self._publish_policy_leafs_on_change(id, policy, self.EVENT_DELETE)
                self.policies_removed = []

            # print("policies_updated: " + str(len(self.policies_updated)))
            if len(self.policies_updated) > 0:
                for policy_map in self.policies_updated:
                    old_policy = policy_map['old']
                    new_policy = policy_map['new']
                    policy_diff = self._find_diff(old_policy, new_policy)
                    logging.debug(policy_diff.__str__())
                    id = new_policy.id
                    self._publish_policy_leafs_on_change(id, policy_diff, self.EVENT_UPDATE)
                self.policies_updated = []

            time.sleep(self.on_change_interval)

    def _get_new_policies(self):
        curr_policies = self.policyController.get_policies()
        policy_map = {}
        # Check new or modified policies
        for policy in curr_policies:
            # get the old policy whose id is the same of the new policy
            old_policy = next((x for x in self.interfaces_old if x.id == policy.id), None)
            if old_policy is None:
                self.policies_new.append(policy)
            else:
                if not policy.__eq__(old_policy):
                    policy_map['old'] = old_policy
                    policy_map['new'] = policy
                    self.interfaces_updated.append(policy_map)
        # Check if a policy was removed
        for old_policy in self.interfaces_old:
            # get the old policy whose id is the same of the new policy
            policy = next((x for x in curr_policies if x.id == old_policy.id), None)
            if policy is None:
                self.policies_removed.append(old_policy)
        self.policies_old = curr_policies

    def _find_diff(self, old_policy, new_policy):

        description = None
        if not old_policy.description.__eq__(new_policy.description):
            description = new_policy.description

        action = None
        if not old_policy.action.__eq__(new_policy.action):
            action = new_policy.action

        protocol = None
        if not old_policy.protocol.__eq__(new_policy.protocol):
            protocol = new_policy.protocol

        in_interface = None
        if not old_policy.in_interface.__eq__(new_policy.in_interface):
            in_interface = new_policy.in_interface

        out_interface = None
        if not old_policy.out_interface.__eq__(new_policy.out_interface):
            out_interface = new_policy.out_interface

        src_address = None
        if not old_policy.src_address.__eq__(new_policy.src_address):
            src_address = new_policy.src_address

        dst_address = None
        if not old_policy.dst_address.__eq__(new_policy.dst_address):
            dst_address = new_policy.dst_address

        src_port = None
        if not old_policy.src_port.__eq__(new_policy.src_port):
            src_port = new_policy.src_port

        dst_port = None
        if not old_policy.dst_port.__eq__(new_policy.dst_port):
            dst_port = new_policy.dst_port

        policy = Policy(id=None,
                        description=description,
                        action=action,
                        protocol=protocol,
                        in_interface=in_interface,
                        out_interface=out_interface,
                        src_address=src_address,
                        dst_address=dst_address,
                        src_port=src_port,
                        dst_port=dst_port)

        return policy

    def _publish_policy_leafs_on_change(self, id, policy, method):

        if self.elements['policy'].advertise == self.ON_CHANGE:
            self._publish_policy(id, policy, method)

        if policy.description is not None:
            if self.elements['description'].advertise == self.ON_CHANGE:
                self._publish_policy_description(id, policy.description, method)

        if policy.action is not None:
            if self.elements['action'].advertise == self.ON_CHANGE:
                self._publish_policy_action(id, policy.action, method)

        if policy.protocol is not None:
            if self.elements['protocol'].advertise == self.ON_CHANGE:
                self._publish_policy_protocol(id, policy.protocol, method)

        if policy.in_interface is not None:
            if self.elements['inInterface'].advertise == self.ON_CHANGE:
                self._publish_policy_inInterface(id, policy.in_interface, method)

        if policy.out_interface is not None:
            if self.elements['outInterface'].advertise == self.ON_CHANGE:
                self._publish_policy_outInterface(id, policy.out_interface, method)

        if policy.src_address is not None:
            if self.elements['srcAddress'].advertise == self.ON_CHANGE:
                self._publish_policy_srcAddress(id, policy.src_address, method)

        if policy.dst_address is not None:
            if self.elements['dstAddress'].advertise == self.ON_CHANGE:
                self._publish_policy_dstAddress(id, policy.dst_address, method)

        if policy.src_port is not None:
            if self.elements['srcPort'].advertise == self.ON_CHANGE:
                self._publish_policy_srcPort(id, policy.src_port, method)

        if policy.dst_port is not None:
            if self.elements['dstPort'].advertise == self.ON_CHANGE:
                self._publish_policy_dstPort(id, policy.dst_port, method)

    def _publish_policy_leafs_periodic(self, policy, period):

        id = policy.id

        if self.elements['policy'].advertise == self.PERIODIC and self.elements['policy'].period == period:
            self._publish_policy(id, policy)

        if policy.description is not None:
            if self.elements['description'].advertise == self.PERIODIC and self.elements['description'].period == period:
                self._publish_policy_description(id, policy.description)

        if policy.action is not None:
            if self.elements['action'].advertise == self.PERIODIC and self.elements['action'].period == period:
                self._publish_policy_action(id, policy.action)

        if policy.protocol is not None:
            if self.elements['protocol'].advertise == self.PERIODIC and self.elements['protocol'].period == period:
                self._publish_policy_protocol(id, policy.protocol)

        if policy.in_interface is not None:
            if self.elements['inInterface'].advertise == self.PERIODIC and self.elements['inInterface'].period == period:
                self._publish_policy_inInterface(id, policy.in_interface)

        if policy.out_interface is not None:
            if self.elements['outInterface'].advertise == self.PERIODIC and self.elements['outInterface'].period == period:
                self._publish_policy_outInterface(id, policy.out_interface)

        if policy.src_address is not None:
            if self.elements['srcAddress'].advertise == self.PERIODIC and self.elements['srcAddress'].period == period:
                self._publish_policy_srcAddress(id, policy.src_address)

        if policy.dst_address is not None:
            if self.elements['dstAddress'].advertise == self.PERIODIC and self.elements['dstAddress'].period == period:
                self._publish_policy_dstAddress(id, policy.dst_address)

        if policy.src_port is not None:
            if self.elements['srcPort'].advertise == self.PERIODIC and self.elements['srcPort'].period == period:
                self._publish_policy_srcPort(id, policy.src_port)

        if policy.dst_port is not None:
            if self.elements['dstPort'].advertise == self.PERIODIC and self.elements['dstPort'].period == period:
                self._publish_policy_dstPort(id, policy.dst_port)

    def _timer_periodic_callback(self, period):

        while True:

            time.sleep(period)

            logging.debug("timer callback, period:" + str(period))
            curr_policies = self.policyController.get_policies()
            for policy in curr_policies:
                self._publish_policy_leafs_periodic(policy, period)


    ################### Private publish functions ###################
    def _publish_policy(self, id, data, method=None):
        policy_dict = self.policyParser.get_policy_dict(data)
        url = self.url_policy + "/" + id
        self.ddController.publish_on_bus(url, method, policy_dict)

    def _publish_policy_description(self, id, data, method=None):
        url = self.url_policy + "/" + id + self.url_description
        self.ddController.publish_on_bus(url, method, data)

    def _publish_policy_action(self, id, data, method=None):
        url = self.url_policy + "/" + id + self.url_action
        self.ddController.publish_on_bus(url, method, data)

    def _publish_policy_protocol(self, id, data, method=None):
        url = self.url_policy + "/" + id + self.url_protocol
        self.ddController.publish_on_bus(url, method, data)

    def _publish_policy_inInterface(self, id, data, method=None):
        url = self.url_policy + "/" + id + self.url_inInterface
        self.ddController.publish_on_bus(url, method, data)

    def _publish_policy_outInterface(self, id, data, method=None):
        url = self.url_policy + "/" + id + self.url_outInterface
        self.ddController.publish_on_bus(url, method, data)

    def _publish_policy_srcAddress(self, id, data, method=None):
        url = self.url_policy + "/" + id + self.url_srcAddress
        self.ddController.publish_on_bus(url, method, data)

    def _publish_policy_dstAddress(self, id, data, method=None):
        url = self.url_policy + "/" + id + self.url_dstAddress
        self.ddController.publish_on_bus(url, method, data)

    def _publish_policy_srcPort(self, id, data, method=None):
        url = self.url_policy + "/" + id + self.url_srcPort
        self.ddController.publish_on_bus(url, method, data)

    def _publish_policy_dstPort(self, id, data, method=None):
        url = self.url_policy + "/" + id + self.url_dstPort
        self.ddController.publish_on_bus(url, method, data)