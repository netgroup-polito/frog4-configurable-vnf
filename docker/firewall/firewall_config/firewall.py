import logging
import json
import netifaces
import iptc
import os
import inspect

from configuration_agent.firewall_config.vnf_interface import VNF

from configuration_agent import utils
from configuration_agent.utils import Bash
from configuration_agent.common.interface import Interface

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%H:%M:%S')

class Firewall(VNF):

    yang_module_name = 'config-firewall'
    type = 'fw'

    def __init__(self, management_iface):

        self.yang_model = self.get_yang()
        assert management_iface is not None, "You have to pass the management interface name to the class constructor"
        self.configuration_interface = management_iface
        self.mac_address = utils.get_mac_address(self.configuration_interface)

        self.interfaces = []
        self.wanInterface = {}
        self.policies = []
        self.blacklist = []
        self.whitelist = []


    def set_configuration(self, json_instance):
        """
        Set the status of the VNF starting from a json instance
        :param json_instance:
        :type json_instance:
        :return:
        """

        logging.debug("Configuration received!")

        json_interfaces = json_instance[self.yang_module_name+':'+'interfaces']["ifEntry"]
        json_wanInterface = json_instance[self.yang_module_name + ':' + 'firewall']["wan-interface"]
        json_policies = json_instance[self.yang_module_name+':'+'firewall']["policies"]
        json_blacklist = json_instance[self.yang_module_name + ':' + 'firewall']["blacklist"]
        json_whitelist = json_instance[self.yang_module_name + ':' + 'firewall']["whitelist"]

        # Save all json interface in a map<interface-name>
        json_interfaces_map = {}
        for json_interface in json_interfaces:
            json_interfaces_map[json_interface['name']] = json_interface

        # Replace for each policy, in-interface and out-interface with the object interface
        for policy in json_policies:
            if ('in-interface' in policy):
                policy['in-interface'] = json_interfaces_map[policy['in-interface']]
            if ('out-interface' in policy):
                policy['out-interface'] = json_interfaces_map[policy['out-interface']]

        logging.debug("Loading configuration...\n")

        self._set_interfaces(json_interfaces, json_wanInterface)

        # Reset current iptables
        logging.debug("Reset iptables...")
        Bash('iptables -F')
        logging.debug("Reset iptables...done!\n")

        self._set_policies(json_policies)
        self._set_whitelist(json_whitelist)
        self._set_blacklist(json_blacklist)

        logging.debug("Loading configuration...done!\n")

    def _set_interfaces(self, json_interfaces, json_wanInterface):

        logging.debug("Scanning interfaces...")
        logging.debug("There are " + str(len(json_interfaces)) + " interfaces\n")

        # Transparent interfaces
        toLan_iface = {}
        toWan_iface = {}

        for interface in json_interfaces:

            logging.debug("Scan interface: ")
            logging.debug(interface)

            """
            Check if the interface is transparent
            Conditions: management = false AND it has no ipv4 configuration
            """
            if 'management' not in interface:
                if 'ipv4_configuration' not in interface:
                    logging.debug("Found a transparent interface: " + interface['name'])
                    if(interface['name']==json_wanInterface):
                        toWan_iface = interface
                    else:
                        toLan_iface = interface
                    continue
            else:
                if interface['management'] is False:
                    if 'ipv4_configuration' not in interface:
                        logging.debug("Found a transparent interface: " + interface['name'])
                        if (interface['name'] == json_wanInterface):
                            toWan_iface = interface
                        else:
                            toLan_iface = interface
                        continue

            if 'ipv4_configuration' in interface:
                logging.debug("Setting interface " + interface['name'] + "...")
                name = interface['name']
                ipv4_parameters = interface['ipv4_configuration']
                configurationType = ipv4_parameters['configurationType']
                if 'address' not in ipv4_parameters:
                    address = None
                else:
                    address = ipv4_parameters['address']
                if 'netmask' not in ipv4_parameters:
                    netmask = "255.255.255.0"
                else:
                    netmask = ipv4_parameters['netmask']
                if 'default_gw' not in interface:
                    default_gw = None
                else:
                    default_gw = interface['default_gw']

                new_interface = Interface(name = name,
                                  ipv4_address = address,
                                  netmask = netmask,
                                  configuration_type = configurationType,
                                  default_gw = default_gw)

                try:
                    new_interface.set_interface()
                except Exception as ex:
                    logging.debug("Setting interface " + interface['name'] + "...Error:" + ex.message + "\n")

            logging.debug("Setting interface " + interface['name'] + "...done!\n")

        assert toLan_iface is not None and toWan_iface is not None, "Error: transparent interfaces have to be 2"
        logging.debug("Creating bridge...\n")
        br_name = "br0"
        self._create_bridge(br_name, toLan_iface['name'], toWan_iface['name'])
        logging.debug("Creating bridge...done\n")

        # Set the rule that drop all traffic from fw_host to lan_iface
        br_iface = None
        for interface in self._get_interfaces_dict():
            if(interface['name'] == br_name):
                br_iface = interface
                break
        assert br_iface is not None, "Error: not found bridge interface"
        Bash('ebtables -A OUTPUT -p IPv4 --ip-src ' + br_iface['address'] + ' --out-interface ' + toLan_iface['name'] + ' -j DROP')

        logging.debug("Scanning interfaces...done!\n")

    def _create_bridge(self, br_name, if1, if2):
        Bash('ifconfig ' + if1 + 'down')
        Bash('ifconfig ' + if2 + 'down')
        Bash('ifconfig ' + if1 + 'up 0.0.0.0')
        Bash('ifconfig ' + if2 + 'up 0.0.0.0')
        Bash('brctl addbr ' + br_name)
        Bash('brctl addif ' + br_name + ' ' + if1)
        Bash('brctl addif ' + br_name + ' ' + if2)
        Bash('route del default')
        Bash('/usr/sbin/dhclient ' + br_name + ' -v')


    def _set_policies(self, json_policies):

        # Filter: INPUT, OUTPUT, FORWARD
        # FORWARD because i want a transparent proxy
        filter_type = "FORWARD"

        logging.debug("Setting Policies...")
        logging.debug("There are " + str(len(json_policies)) + " policies to set\n")

        for policy in json_policies[::-1]:

            policy_name = policy['policy-name'] if('policy-name' in policy) else ""
            logging.debug("Setting policy " + policy_name + "...")
            logging.debug(policy)

            rule = iptc.Rule()
            """
            if('in-interface' in policy):
                rule.in_interface = policy['in-interface']['name']
            if('out-interface' in policy):
                rule.out_interface = policy['out-interface']['name']
            """
            if('source-address' in policy and 'source-mask' in policy):
                rule.src = policy['source-address']
                #rule.src = policy['source-address']+'/'+policy['source-mask']
            if('destination-address' in policy and 'destination-mask' in policy):
                rule.dst = policy['destination-address']
                #rule.dst = policy['destination-address'] + '/' + policy['destination-mask']
            if('protocol' in policy):
                if(policy['protocol']!="all"):
                    rule.protocol = policy['protocol']
                    match = rule.create_match(policy['protocol'])

            if('source-port' in policy):
                match.sport = policy['source-port']
            if('destination-port' in policy):
                match.dport = policy['destination-port']
            if('description' in policy):
                match = rule.create_match("comment")
                match.comment = policy['description']

            rule.target = iptc.Target(rule, policy['action'].upper())

            chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), filter_type)
            chain.insert_rule(rule)

            logging.debug("Setting policy " + policy_name + "...done!\n")

        logging.debug("Setting Policies...done!\n")

    def _set_blacklist(self, json_blacklist):

        logging.debug("Setting blacklist...")
        logging.debug("There are " + str(len(json_blacklist)) + " uri to set\n")

        for uri in json_blacklist:
            logging.debug("Adding uri: " + uri['uri'] + "...")
            Bash('iptables -I FORWARD -s '+ uri['uri'] + ' -j DROP -m comment --comment=blacklist:' + uri['uri'])
            Bash('iptables -I FORWARD -d ' + uri['uri'] + ' -j DROP -m comment --comment=blacklist:' + uri['uri'])
            logging.debug("Adding uri: " + uri['uri'] + "...done!")

        logging.debug("Setting blacklist...done!\n")

    def _set_whitelist(self, json_whitelist):

        logging.debug("Setting whitelist...")
        logging.debug("There are " + str(len(json_whitelist)) + " uri to set\n")

        for uri in json_whitelist:
            logging.debug("Adding uri: " + uri['uri'] + "...")
            Bash('iptables -I FORWARD -s ' + uri['uri'] + ' -j ACCEPT -m comment --comment=whitelist:' + uri['uri'])
            Bash('iptables -I FORWARD -d '+ uri['uri'] + ' -j ACCEPT -m comment --comment=whitelist:' + uri['uri'])
            logging.debug("Adding uri: " + uri['uri'] + "...done!")

        logging.debug("Setting whitelist...done!\n")


    def get_status(self):
        """
        Return the current state of the firewall including interfaces and policies
        :return: json file
        """

        logging.debug("Getting the current state in a json file...")

        json_instance = {self.yang_module_name + ':' + 'interfaces': {'ifEntry': []},
                         self.yang_module_name + ':' + 'firewall': {'wan-interface': {}},
                         self.yang_module_name + ':' + 'firewall': {'policies': []},
                         self.yang_module_name + ':' + 'firewall': {'blacklist': []},
                         self.yang_module_name + ':' + 'firewall': {'whitelist': []}
                         }

        # Get interfaces
        json_instance[self.yang_module_name + ':' + 'interfaces']['ifEntry'] = []
        self.interfaces = json_instance[self.yang_module_name+':'+'interfaces']['ifEntry']
        for interface in self._get_interfaces_dict():
            self.interfaces.append(interface)

        # Get wan-interface
        json_instance[self.yang_module_name + ':' + 'firewall']['wan-interface'] = {}
        self.wanInterface = {}

        # Get policies including blacklist and whitelist
        json_instance[self.yang_module_name + ':' + 'firewall']['policies'] = []
        json_instance[self.yang_module_name + ':' + 'firewall']['whitelist'] = []
        json_instance[self.yang_module_name + ':' + 'firewall']['blacklist'] = []
        self.policies = json_instance[self.yang_module_name + ':' + 'firewall']['policies']
        self.whitelist = json_instance[self.yang_module_name + ':' + 'firewall']['whitelist']
        self.blacklist = json_instance[self.yang_module_name + ':' + 'firewall']['blacklist']
        for policy in self._get_policies_dict():
            if ('type' not in policy):
                self.policies.append(policy)
            elif (policy['type'] == "whitelist"):
                self.whitelist.append(policy['uri'])
            elif (policy['type'] == "blacklist"):
                self.blacklist.append(policy['uri'])

        # Remove duplicates
        self.blacklist = set(self.blacklist)
        self.whitelist = set(self.whitelist)

        logging.debug("Getting the current state in a json file...done!\n")

        return json.dumps(json_instance)

    def _get_policies_dict(self):
        '''
        Get a python dictionary with the policies of the VNF
        '''
        table = iptc.Table(iptc.Table.FILTER)
        table.refresh()
        policies = []
        for chain in table.chains:
            for rule in chain.rules:
                policy_dict = self._get_policy_dict(rule)
                policies.append(policy_dict)
        return policies

    def _get_policy_dict(self, rule):
        dict = {}
        for match in rule.matches:
            if match.name == "comment":
                tmp = match.comment.split(':')
                if tmp[0] == "blacklist" or tmp[0] == "whitelist":
                    dict['type'] = tmp[0]
                    dict['uri'] = tmp[1]
                    return dict
                else:
                    dict['description'] = match.comment
            if match.sport is not None:
                dict['source-port'] = match.sport
            if match.dport is not None:
                dict['destination-port'] = match.dport
        if (rule.in_interface is not None):
            dict['in-interface'] = rule.in_interface
        if (rule.out_interface is not None):
            dict['out-interface'] = rule.out_interface
        if (rule.src != "0.0.0.0/0.0.0.0"):
            tmp = rule.src.split('/')
            dict['source-address'] = tmp[0]
            dict['source-mask'] = tmp[1]
        if (rule.dst != "0.0.0.0/0.0.0.0"):
            tmp = rule.dst.split('/')
            dict['destination-address'] = tmp[0]
            dict['destination-mask'] = tmp[1]
            # rule.protocol returns "ip" instead of "all"
        if (rule.protocol != "ip"):
            dict['protocol'] = rule.protocol
        dict['action'] = rule.target.name

        return dict;

    def _get_interfaces_dict(self):
        '''
        Get a python dictionary with the interfaces of the VNF
        '''
        interfaces = []
        for interface in self._get_interfaces():
            interface_dict = self._get_interface_dict(interface)
            interfaces.append(interface_dict)
        return interfaces

    def _get_interfaces(self):
        '''
        Retrieve the interfaces of the VM
        '''
        vm_interfaces = []
        interfaces = netifaces.interfaces()
        for interface in interfaces:
            if interface == 'lo':
                continue
            default_gw = ''
            configuration_type = None
            gws = netifaces.gateways()
            if gws['default'] != {} and gws['default'][netifaces.AF_INET][1] == interface:
                default_gw = gws['default'][netifaces.AF_INET][0]
            interface_af_link_info = netifaces.ifaddresses(interface)[17]
            if 2 in netifaces.ifaddresses(interface):
                interface_af_inet_info = netifaces.ifaddresses(interface)[2]
                ipv4_address = interface_af_inet_info[0]['addr']
                netmask = interface_af_inet_info[0]['netmask']
            else:
                ipv4_address = ""
                netmask = ""
            if interface == self.configuration_interface:
                configuration_type = 'dhcp'

            vm_interfaces.append(Interface(name=interface, status=None,
                                             mac_address=interface_af_link_info[0]['addr'],
                                             ipv4_address=ipv4_address,
                                             netmask=netmask,
                                             default_gw=default_gw,
                                             configuration_type=configuration_type))
            return vm_interfaces

    def _get_interface_dict(self, interface):
        dict = {}
        dict['name'] = interface.name
        if interface.configuration_type is not None:
            dict['configurationType'] = interface.configuration_type
        else:
            dict['configurationType'] = 'not_defined'
        if interface.ipv4_address is not None and interface.ipv4_address != "":
            dict['address'] = interface.ipv4_address
        if interface.netmask is not None and interface.netmask != "":
            dict['netmask'] = interface.netmask
        if interface.default_gw is not None and interface.ipv4_address != "":
            dict['default_gw'] = interface.default_gw
        return dict


    def get_mac_address(self):
        return self.mac_address

    def set_yang_model(self):
        pass

    def get_yang(self):
        '''
        Get from file the yang model of this VNF
        '''
        base_path = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))

        with open (base_path+"/"+self.yang_module_name+".yang", "r") as yang_model_file:
            return yang_model_file.read()
