from components.nat.nat_core.nat_core_service import NatCoreService
from common.config_instance import ConfigurationInstance

class NatCoreController():

    def __init__(self):
        self.natCoreService = NatCoreService()
        self.nf_type = ConfigurationInstance.get_nf_type(self)

    def set_ip_forward(self, public_interface_name):
        if self.nf_type == "docker" or self.nf_type == "vm":
            self.natCoreService.set_ip_forward(public_interface_name)

    def unset_ip_forward(self, public_interface_name):
        if self.nf_type == "docker" or self.nf_type == "vm":
            self.natCoreService.unset_ip_forward(public_interface_name)

    # Nat/public-interface
    def get_public_interface_name(self):
        if self.nf_type == "docker" or self.nf_type == "vm":
            try:
                return self.natCoreService.get_public_interface_name()
            except Exception as e:
                return None

    # Nat/private-interface
    def get_private_interface_name(self):
        pass


