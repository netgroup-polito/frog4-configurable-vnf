from components.firewall.policy.policy_controller import PolicyController
from components.firewall.policy.policy_parser import PolicyParser
from components.firewall.policy.policy_model import Policy
from common.element import Element
from common.constants import Constants
from common.config_instance import ConfigurationInstance
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

        self.elements = {}
        self.elements['policy'] = Element(advertise=self.ON_CHANGE)
        ##################################################################

        self.periods = []
        for key, element in self.elements.items():
            if element.advertise == self.PERIODIC:
                element.period = element.period / 1000
                if element.period not in self.periods:
                    self.periods.append(element.period)

        self.on_change_interval = ConfigurationInstance().get_on_change_interval()
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
            old_policy = next((x for x in self.policies_old if x.id == policy.id), None)
            if old_policy is None:
                self.policies_new.append(policy)
            else:
                if not policy.__eq__(old_policy):
                    policy_map['old'] = old_policy
                    policy_map['new'] = policy
                    self.policies_updated.append(policy_map)
        # Check if a policy was removed
        for old_policy in self.policies_old:
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

    def _publish_policy_leafs_periodic(self, policy, period):
        id = policy.id
        if self.elements['policy'].advertise == self.PERIODIC and self.elements['policy'].period == period:
            self._publish_policy(id, policy)


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
        logging.debug("_publish_policy with id: " + id)
        print("_publish_policy with id: " + id)
        url = self.url_policy + "/" + id
        logging.debug("_publish_policy at url: " + url)
        print("_publish_policy at url: " + url)
        self.ddController.publish_on_bus(url, method, policy_dict)
