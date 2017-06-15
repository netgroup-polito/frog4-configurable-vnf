from nat.model.floating_ip import FloatingIp
from common.utils import Bash

import iptc

class FloatingIpService():

    def configure_floating_ip(self, floating_ip, wan_interface):
        Bash('iptables -t nat -I POSTROUTING -s ' + floating_ip.private_address + ' -j SNAT --to ' + floating_ip.public_address)
        Bash('iptables -t nat -I PREROUTING -d ' + floating_ip.public_address + ' -j DNAT --to-destination ' + floating_ip.private_address)
        Bash('ip addr add ' + floating_ip.public_address + ' dev ' + wan_interface)

    def delete_floating_ip(self, floating_ip, wan_interface):
        Bash('iptables -t nat -D POSTROUTING -s ' + floating_ip.private_address + ' -j SNAT --to ' + floating_ip.public_address)
        Bash('iptables -t nat -D PREROUTING -d ' + floating_ip.public_address + ' -j DNAT --to-destination ' + floating_ip.private_address)
        Bash('ip addr del ' + floating_ip.public_address + ' dev ' + wan_interface)

    def get_all_floating_ip(self):
        '''
        Retrieve the floating ip entries
        A floating IP is described by 2 rules of the NAT table:
            a) 'PREROUTING' chain: dst = public_address become dst = private_address
            b) 'POSTROUTING' chain: src = private_address become src = public_address
        First I save all the possible floating IPs (found looping through the 'PREROUTING' chain) into a temporary list
        Then I check if they really are floating IP iterating through the 'POSTROUTING' chain (it is mandatory the presence of both the rules for a floating IP to be valid)
        :return:
        '''
        floating_ip_list = []
        return floating_ip_list

        floating_ip_tmp = {}
        table = iptc.Table(iptc.Table.NAT)
        table.refresh() #it seems that iptc cash table entries among multiple iptc.Table requests
        pre_chain = iptc.Chain(table, "PREROUTING")
        for rule in pre_chain.rules:
            if rule.target.__getattr__('to_destination') is not None:
                if rule.dst is not None:
                    private_address = rule.target.__getattr__('to_destination')
                    public_address = rule.dst.split('/')[0]
                    floating_ip_tmp[public_address] = private_address
        post_chain = iptc.Chain(table, "POSTROUTING")
        for rule in post_chain.rules:
            if rule.target.__getattr__('to_source') is not None:
                if rule.src is not None:
                    private_address = rule.src.split('/')[0]
                    public_address = rule.target.__getattr__('to_source')
                    if public_address in floating_ip_tmp and floating_ip_tmp[public_address] == private_address:
                        floating_ip = FloatingIp(private_address, public_address)
                        floating_ip_list.append(floating_ip)

        return floating_ip_list

    def get_floating_ip(self, public_address):
        floating_ip_list = self.get_all_floating_ip()
        for floating_ip in floating_ip_list:
            if floating_ip.public_address == public_address:
                return floating_ip
        return None
