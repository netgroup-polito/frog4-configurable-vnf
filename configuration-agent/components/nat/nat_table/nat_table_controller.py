from components.nat.nat_table.nat_table_service import NatTableService
from common.config_instance import ConfigurationInstance

class NatTableController():

    def __init__(self):
        self.nat_table_service = NatTableService()
        self.nf_type = ConfigurationInstance().get_nf_type()

    def get_nat_table(self):
        if self.nf_type == "docker" or self.nf_type == "vm":
            return self.nat_table_service.get_nat_table()

    def add_nat_session(self, nat_session):
        if self.nf_type == "docker" or self.nf_type == "vm":
            return self.nat_table_service.add_nat_session(nat_session)
