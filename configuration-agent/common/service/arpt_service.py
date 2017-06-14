from common.model.arp_entry import ArpEntry
from common.utils import Bash

class ArpTableService():

    def add_arp_entry(self, ip_address, mac_address):
        Bash('arp -s ' + ip_address + ' ' + mac_address)

    def delete_arp_entry(self, ip_address):
        Bash('arp -d ' + ip_address)

    def get_arp_table(self):
        try:
            with open('/proc/net/arp') as arpt:
                lines = arpt.readlines()
            arpt.close()
        except Exception as e:
            raise IOError("Unable to read arp table: /proc/net/arp not found")

        arp_table = []
        for line in lines[1:]:
            args = line.strip().split()
            ip_address = args[0]
            mac_address = args[3]
            arp_entry = ArpEntry(ip_address, mac_address)
            arp_table.append(arp_entry)
        return arp_table

    def get_mac_address(self, ip_address):
        arp_table = self.get_arp_table()
        for arp_entry in arp_table:
            if arp_entry.ip_address.__eq__(ip_address):
                return arp_entry.mac_address
        return None