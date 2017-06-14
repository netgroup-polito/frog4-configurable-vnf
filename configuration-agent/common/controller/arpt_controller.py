from common.service.arpt_service import ArpTableService
from common.config_instance import ConfigurationInstance

class ArpTableController():

    def __init__(self):
        self.arpTableService = ArpTableService()
        self.nf_type = ConfigurationInstance.get_nf_type(self)

    def add_arp_entry(self, ip_address, mac_address):
        if self.nf_type == "docker" or self.nf_type == "vm":
            self.arpTableService.add_arp_entry(ip_address, mac_address)

    def delete_arp_entry(self, ip_address):
        if self.nf_type == "docker" or self.nf_type == "vm":
            self.arpTableService.delete_arp_entry(ip_address)

    def get_arp_table(self):
        if self.nf_type == "docker" or self.nf_type == "vm":
            return self.arpTableService.get_arp_table()

    def get_mac_address(self, ip_address):
        if self.nf_type == "docker" or self.nf_type == "vm":
            return self.arpTableService.get_mac_address(ip_address)

    def arp_entry_exist(self, ip_address):
        if self.get_mac_address(ip_address) is not None:
            return True
        else:
            return False
