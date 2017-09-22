from components.firewall.policy.policy_service import PolicyService
from common.config_instance import ConfigurationInstance

class PolicyController():

    def __init__(self):
        self.policyService = PolicyService()
        self.nf_type = ConfigurationInstance().get_nf_type()

    def add_policy(self, policy, table="FILTER", chain="FORWARD"):
        if self.nf_type=="docker" or self.nf_type=="vm":
            self.policyService.add_policy(policy, table, chain)

    def get_policies(self, table="FILTER", chain="ALL"):
        if self.nf_type == "docker" or self.nf_type == "vm":
            return self.policyService.get_policies(table, chain)

    def get_policy(self, id, table="FILTER", chain="FORWARD"):
        if self.nf_type == "docker" or self.nf_type == "vm":
            return self.policyService.get_policy(id, table, chain)

    def delete_policies(self, table="FILTER", chain="FORWARD"):
        if self.nf_type == "docker" or self.nf_type == "vm":
            self.policyService.remove_policies(table, chain)

    def delete_policy(self, id, table="FILTER", chain="FORWARD"):
        if self.nf_type == "docker" or self.nf_type == "vm":
            self.policyService.remove_policy(id, table, chain)

    def policy_exists(self, id):
        if self.get_policy(id) is not None:
            return True
        else:
            return False

    def clear_policy_repo(self):
        if self.nf_type == "docker" or self.nf_type == "vm":
            self.policyService.clear_policy_repo()