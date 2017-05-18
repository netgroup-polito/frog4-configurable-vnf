from firewall.service.policy_service import PolicyService
from config_instance import ConfigurationInstance

class PolicyController():

    def __init__(self):
        self.policyService = PolicyService()
        self.nf_type = ConfigurationInstance.get_nf_type(self)
        self.policies_map = {}

    def add_policy(self, policy, table="FILTER", chain="FORWARD"):
        if self.nf_type=="docker" or self.nf_type=="vm":
            self.policyService.add_policy(policy, table, chain)
        id = policy.__hash__()
        self.policies_map[id] = policy

    def get_policies(self, table="FILTER", chain="ALL"):
        if self.nf_type == "docker" or self.nf_type == "vm":
            return self.policyService.get_policies(table, chain)

    def get_policy(self, id):
        if id in self.policies_map:
            return self.policies_map[id]
        else:
            return None

    def policy_exists(self, id):
        if id in self.policies_map:
            return True
        else:
            return False

    def delete_policies(self):
        pass

    def delete_policy(self, id):
        policy = self.policies_map[id]
        if self.nf_type == "docker" or self.nf_type == "vm":
            self.policyService.remove_policy(policy, table="FILTER", chain="FORWARD")
        del self.policies_map[id]