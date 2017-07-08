from nat.model.nat_session import NatSession
from common.utils import Bash

import iptc
import netifaces
import pynetfilter_conntrack

class NatService():

    def set_ip_forward(self, public_interface_name):
        #print("nat configured... fake! ahah")
        #return
        Bash('echo 1 > /proc/sys/net/ipv4/ip_forward')
        Bash('iptables -t nat -A POSTROUTING -o ' + public_interface_name + ' -j MASQUERADE')

    def unset_ip_forward(self, public_interface_name):
        Bash('echo 0 > /proc/sys/net/ipv4/ip_forward')
        Bash('iptables -t nat -D POSTROUTING -o ' + public_interface_name + ' -j MASQUERADE')

    def get_public_interface_name(self):
        '''
        This agent assumes to be attached to an homegateway NAT, so it assumes that only one interface is connected to the WAN and that
        it exists only one iptables MASQUERADE rule
        :return:
        '''
        prerouting_index = 3
        table = iptc.Table(iptc.Table.NAT)
        table.refresh()
        try:
            wan_interface_name = None
            for rule in table.chains[prerouting_index].rules:
                if rule.out_interface is not None and rule.target.standard_target == 'MASQUERADE':
                    wan_interface_name = rule.out_interface
            return wan_interface_name
        except Exception as e:
            raise Exception("Error reading nat table...\n" + str(e))

    def get_private_interface_name(self):
        pass

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
                translated_address=item.repl_ipv4_dst,
                translated_port=item.repl_port_dst,
                tcp_state=item.tcp_state
            )
            # Discard tcp connection not natted
            if not nat_session.src_address.__eq__(nat_session.translated_address):
                nat_table.append(nat_session)
        return nat_table

    def add_nat_session(self, nat_session):
        pass

