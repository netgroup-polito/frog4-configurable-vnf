from components.common.arp_table.arp_entry_model import ArpEntry

class ArpTableParser():

    def parse_arp_table(self, json_configuration):
        return json_configuration['arp-table']

    def parse_arp_entries(self, json_arp_table):
        return json_arp_table['arp-entry']

    def parse_arp_entry(self, json_arp_entry):

        ip_address = None
        if 'ip_address' in json_arp_entry:
            ip_address = json_arp_entry['ip_address']

        mac_address = None
        if 'mac_address' in json_arp_entry:
            mac_address = json_arp_entry['mac_address']

        return ArpEntry(ip_address=ip_address,
                        mac_address=mac_address)

    def get_arp_entry_dict(self, arp_entry):

        arp_entry_dict = {}

        arp_entry_dict['ip_address'] = arp_entry.ip_address
        arp_entry_dict['mac_address'] = arp_entry.mac_address

        return arp_entry_dict