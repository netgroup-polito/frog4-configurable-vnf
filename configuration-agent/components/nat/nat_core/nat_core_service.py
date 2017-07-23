from common.utils import Bash
import iptc

class NatCoreService():

    def set_ip_forward(self, public_interface_name):
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



