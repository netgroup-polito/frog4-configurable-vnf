'''
Created on Dec 18, 2015

@author: fabiomignini
'''
from importlib import reload
import logging
#import xmltodict
try:
    import StringIO
except ImportError:
    from io import StringIO
import json
import types
import collections
import os
import inspect
import netifaces
import iptc


from pyang.__init__ import Context, FileRepository
from pyang.translators.yin import YINPlugin
from pyang import plugin
from configuration_agent.nat_config.vnf_interface import VNF

from configuration_agent import utils
from configuration_agent.utils import Bash
from configuration_agent.nat_config import InterfaceService
from configuration_agent.model.natModel import NatModel
from configuration_agent.model.interface import Interface


class Nat(VNF):
    '''
    Class that configure and export
    the status of a NAT VNF
    '''

    yang_module_name = 'config-nat'

    def __init__(self, management_iface):
        self.yang_model = self.get_yang()
        assert management_iface is not None, "You have to pass the management interface name to the class constructor"
        self.configuration_interface = management_iface
        self.mac_address = utils.get_mac_address(self.configuration_interface)
        self.wan_interface = None
        self.nat = NatModel()

    def get_yang(self):
        '''
        Get from file the yang model of this VNF
        '''
        base_path = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))

        with open(base_path+"/"+self.yang_module_name+".yang", "r") as yang_model_file:
            return yang_model_file.read()

    def get_status(self):
        '''
        Get the status of the VNF
        '''
        self.get_interfaces()
        self.get_floating()
        return json.dumps(self.nat.get_nat_model_dict())

    def set_configuration(self, json_instance):
        '''
        Set the status of the VNF starting from a
        json instance
        '''
        logging.debug(json_instance)
        self.clean_nat()
        self.nat.set_nat_model(json_instance)
        self.wan_interface = self.nat.nat_parameters.wan_interface
        logging.debug("\nScanning interfaces...")
        wan_iface = None
        for interface in self.nat.interfaces:

            if interface.name == self.wan_interface:
                logging.debug("Found a wan interface: " + interface.name)
                wan_iface = interface
                continue

            logging.debug("Setting interface " + interface.name + "...")
            try:
                InterfaceService.set_interface(interface)
            except Exception as ex:
                logging.debug("Setting interface " + interface.name + "...Error:" + ex.message + "\n")
            logging.debug("Setting interface " + interface.name + "...done!")

        logging.debug("Scanning interfaces...done!")

        assert wan_iface is not None, "Error: no wan interface found"
        logging.debug("Setting wan interface " + wan_iface.name + "...")
        Bash('route del default')
        try:
            InterfaceService.set_interface(wan_iface)
        except Exception as ex:
            logging.debug("Setting wan interface " + interface.name + "...Error:" + ex.message + "\n")
        logging.debug("Setting wan interface " + wan_iface.name + "...done!")

        logging.debug("Enabling nat...")
        self.set_nat(wan_iface.name)
        logging.debug("Enabling nat...done!")

        #self.get_interfaces()
        #self.get_interfaces_dict()
        #self.floating_ip = json_instance[self.yang_module_name+':'+'staticBindings']['floatingIP']
        self.set_floating()


    def set_floating(self):
        logging.debug("setting floating IP:")
        for address in self.nat.nat_parameters.floating_ip_list:
            logging.debug("private address " + address['private_address'] + " => public address" + address['public_address'])
            Bash('iptables -t nat -I POSTROUTING -s ' + address['private_address'] + ' -j SNAT --to ' + address['public_address'])
            Bash('iptables -t nat -I PREROUTING -d ' + address['public_address'] + ' -j DNAT --to-destination ' + address['private_address'])
            wan_interface_name = self.get_wan_interface_name()
            Bash('ip addr add ' + address['public_address'] + ' dev ' + wan_interface_name)

    def get_floating(self):
        '''
        Retrieve the floating ip entries
        A floating IP is described by 2 rules of the NAT table:
            a) 'PREROUTING' chain: dst = public_address become dst = private_address
            b) 'POSTROUTING' chain: src = private_address become src = public_address
        First I save all the possible floating IPs (found looping through the 'PREROUTING' chain) into a temporary list
        Then I check if they really are floating IP iterating through the 'POSTROUTING' chain (it is mandatory the presence of both the rules for a floating IP to be valid)
        :return:
        '''
        self.nat.nat_parameters.floating_ip_list = []
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
                        floating_ip_object = {}
                        floating_ip_object.public_address = public_address
                        floating_ip_object.private_address = private_address
                        self.nat.nat_parameters.floating_ip_list.append(floating_ip_object)

    def get_interfaces(self):
        '''
        Retrieve the interfaces of the VM
        '''
        interfaces = netifaces.interfaces()
        self.nat.interfaces = []
        for interface in interfaces:
            if interface == 'lo':
                continue
            default_gw = ''
            configuration_type = None
            gws = netifaces.gateways()
            if gws['default'] == {}:
                default_gw = ''
            else:
                for gw in gws[netifaces.AF_INET]:
                    if gw[1] == interface:
                        default_gw = gw[0]
            interface_af_link_info = netifaces.ifaddresses(interface)[17]
            if 2 in netifaces.ifaddresses(interface):
                interface_af_inet_info = netifaces.ifaddresses(interface)[2]
                address = interface_af_inet_info[0]['addr']
                netmask = interface_af_inet_info[0]['netmask']
            else:
                address = ""
                netmask = ""
            if interface == self.configuration_interface:
                management = True
            else:
                management = None

            self.nat.interfaces.append(Interface(name=interface,
                                                 configuration_type=configuration_type,
                                                 mac_address=interface_af_link_info[0]['addr'],
                                                 address=address,
                                                 netmask=netmask,
                                                 default_gw=default_gw,
                                                 management=management))

    def get_wan_interface_name(self):
        '''
        This agent assumes to be attached to an homegateway NAT, so it assumes that only one interface is connected to the WAN and that
        it exists only one iptables MASQUERADE rule
        :return:
        '''
        prerouting_index = 3

        reload(iptc)
        table = iptc.Table(iptc.Table.NAT)
        try:
            wan_interface = None
            for rule in table.chains[prerouting_index].rules:
                if rule.out_interface is not None and rule.target.standard_target == 'MASQUERADE':
                    wan_interface = rule.out_interface
        except Exception as e:
            logging.debug("Error reading nat table...\n" + str(e))
            wan_interface = None
        return wan_interface

    def clean_nat(self):
        '''
        Flush the tables of iptables.
        '''
        Bash('iptables --flush')
        Bash('iptables --table nat --flush')
        Bash('iptables --delete-chain')
        Bash('iptables --table nat --delete-chain')
        Bash('iptables --flush')

    def set_nat(self, wan_interface):
        '''
        Set a rule to performe as a NAT
        in iptables.
        '''
        Bash('cp /etc/sysctl.conf /etc/sysctl.conf.bak')
        Bash('cp '+os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
+'/sysctl.conf /etc/sysctl.conf')

        # Delete and flush iptables
        Bash('iptables --flush')
        Bash('iptables --table nat --flush')
        Bash('iptables --delete-chain')
        Bash('iptables --table nat --delete-chain')
        Bash('iptables --flush')

        #chain = iptc.Chain(iptc.Table(iptc.Table.NAT), "POSTROUTING")
        #rule = iptc.Rule()
        #rule.out_interface = wan_interface
        #target = iptc.Target(rule, "MASQUERADE")
        #rule.target = target
        #chain.insert_rule(rule)
        bash = Bash('iptables -t nat -A POSTROUTING -o '+wan_interface+' -j MASQUERADE')
        #Bash('service iptables restart')

    def base_conf(self):
        Bash('echo "UseDNS no" >> /etc/ssh/sshd_config')

    def get_mac_address(self):
        return self.mac_address

    def set_yang_model(self):
        pass

logging.basicConfig(level=logging.DEBUG)
