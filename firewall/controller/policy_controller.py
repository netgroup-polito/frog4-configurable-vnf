from firewall.service.policy_service import PolicyService
from config_instance import ConfigurationInstance

class PolicyController():

    def __init__(self):
        self.policyService = PolicyService()
        self.nf_type = ConfigurationInstance.get_nf_type(self)

    def configure_policy(self, policy, table="FILTER", chain="FORWARD"):
        if self.nf_type=="docker" or self.nf_type=="vm":
            self.policyService.configure_policy(policy, table, chain)

    def get_policies(self, table="FILTER", chain="ALL"):
        if self.nf_type == "docker" or self.nf_type == "vm":
            return self.policyService.get_policies(table, chain)

    def get_policy(self, id, table="FILTER", chain="ALL"):
        if self.nf_type == "docker" or self.nf_type == "vm":
            return self.policyService.get_policy(id, table, chain)

    def delete_policies(self):
        pass

    def delete_policy(self, id):
        pass