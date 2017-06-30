from common.config_instance import ConfigurationInstance
from nat.service.nat_service import NatService

class NatController():

    def __init__(self):
        self.natService = NatService()
        self.nf_type = ConfigurationInstance.get_nf_type(self)

    def set_ip_forward(self, public_interface_name):
        if self.nf_type == "docker" or self.nf_type == "vm":
            self.natService.set_ip_forward(public_interface_name)

    def unset_ip_forward(self, public_interface_name):
        if self.nf_type == "docker" or self.nf_type == "vm":
            self.natService.unset_ip_forward(public_interface_name)

    # Nat/public-interface
    def get_public_interface_name(self):
        if self.nf_type == "docker" or self.nf_type == "vm":
            try:
                return self.natService.get_public_interface_name()
            except Exception as e:
                return None

    # Nat/private-interface
    def get_private_interface_name(self):
        pass

    # Nat/nat-table
    def get_nat_table(self):
        if self.nf_type == "docker" or self.nf_type == "vm":
            return self.natService.get_nat_table()

    def add_nat_session(self, nat_session):
        if self.nf_type == "docker" or self.nf_type == "vm":
            return self.natService.add_nat_session(nat_session)
