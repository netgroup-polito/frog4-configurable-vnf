from nat.model.nat_session import NatSession
from utils import Bash

import iptc
import netifaces
import pynetfilter_conntrack

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

    def get_nat_table(self):
        ct = pynetfilter_conntrack.Conntrack()
        nat_table = []
        for item in ct.dump_table(netifaces.AF_INET)[0]:
            nat_session = NatSession(
                id=None,
                protocol=item.orig_l4proto,
                src_address=item.orig_ipv4_src,
                src_port=item.orig_port_src,
                dst_address=item.orig_ipv4_dst,
                dst_port=item.orig_port_dst,
                translated_address=item.repl_ipv4_src,
                translated_port=item.repl_port_src,
                tcp_state=item.tcp_state
            )
            nat_table.append(nat_session)
            print(nat_session.__str__())
        return nat_table

