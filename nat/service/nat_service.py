from utils import Bash

import iptc

class NatService():

    def set_ip_forward(self, wan_interface):
        Bash('echo 1 > /proc/sys/net/ipv4/ip_forward')
        Bash('iptables -t nat -A POSTROUTING -o ' + wan_interface + ' -j MASQUERADE')

    def unset_ip_forward(self, wan_interface):
        Bash('echo 0 > /proc/sys/net/ipv4/ip_forward')
        Bash('iptables -t nat -D POSTROUTING -o ' + wan_interface + ' -j MASQUERADE')

    def get_wan_interface(self):
        '''
        This agent assumes to be attached to an homegateway NAT, so it assumes that only one interface is connected to the WAN and that
        it exists only one iptables MASQUERADE rule
        :return:
        '''
        prerouting_index = 3
        table = iptc.Table(iptc.Table.NAT)
        table.refresh()
        try:
            wan_interface = None
            for rule in table.chains[prerouting_index].rules:
                if rule.out_interface is not None and rule.target.standard_target == 'MASQUERADE':
                    wan_interface = rule.out_interface
            return wan_interface
        except Exception as e:
            raise Exception("Error reading nat table...\n" + str(e))