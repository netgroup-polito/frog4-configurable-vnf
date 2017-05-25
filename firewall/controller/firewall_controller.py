from common.controller.interface_controller import InterfaceController
from common.controller.bridge_controller import BridgeController
from common.model.bridge import Bridge
from common.parser.interface_parser import InterfaceParser
from firewall.controller.policy_controller import PolicyController
from firewall.model.policy import Policy
from firewall.parser.policy_parser import PolicyParser
from firewall.controller.blacklist_controller import BlacklistController
from firewall.parser.blacklist_parser import BlacklistParser
from firewall.controller.whitelist_controller import WhitelistController
from firewall.parser.whitelist_parser import WhitelistParser

import logging

class FirewallController():

    def __init__(self):
        self.interfaceController = InterfaceController()
        self.interfaceParser = InterfaceParser()

        self.bridgeController = BridgeController()

        self.policyController = PolicyController()
        self.policyParser = PolicyParser()

        self.blacklistController = BlacklistController()
        self.blacklistParser = BlacklistParser()

        self.whitelistController = WhitelistController()
        self.whitelistParser = WhitelistParser()

        self.transparent_intefaces = []
        self.wan_interface = None


    def set_configuration(self, json_configuration):

        conf_interfaces = json_configuration["config-firewall:interfaces"]

        json_interfaces = conf_interfaces['ifEntry']
        for json_iface in json_interfaces:
            self.configure_interface(json_iface)

        self.set_wan_interface(json_configuration)

        if len(self.transparent_intefaces) >= 2:
            to_lan_interface = None
            to_wan_interface = None
            for tr_iface in self.transparent_intefaces:
                if tr_iface.name == self.wan_interface.name:
                    tr_iface = to_wan_interface
                else:
                    tr_iface = to_lan_interface
            assert to_lan_interface is not None and to_wan_interface is not None, "Error: transparent interfaces have to be 2"
            bridge = Bridge("br0", to_lan_interface, to_wan_interface)
            if self.create_bridge(bridge):
                br_iface = self.interfaceController.get_interface(bridge.name)
                policy = Policy(description="drop all traffic from fw_host to lan_iface",
                                action="drop",
                                protocol="ipv4",
                                out_interface=to_lan_interface,
                                src_address=br_iface.ipv4_configuration.address)
                self.policyController.configure_policy(policy, table="FILTER", chain="OUTPUT")
                #Bash('ebtables -A OUTPUT -p IPv4 --ip-src ' + br_iface.ipv4_configuration.address + ' --out-interface ' + to_lan_interface + ' -j DROP')

        conf_firewall = json_configuration["config-firewall:firewall"]

        json_policies = conf_firewall['policies']
        for json_policy in json_policies:
            #self.configure_policy(json_policy)
            pass

        json_blacklist = conf_firewall['blacklist']
        for json_url in json_blacklist:
            url = self.blacklistParser.parse_url(json_url)
            #self.configure_blacklist_url(url)
            pass

        json_whitelist = conf_firewall['whitelist']
        for json_url in json_whitelist:
            url = self.whitelistParser.parse_url(json_url)
            #self.configure_whitelist_url(url)
            pass


    def get_full_status(self):

        status = {}

        status["config-firewall:interfaces"] = self.get_interfaces_status()
        status["config-firewall:firewall"] = self.get_firewall_status()

        return status


    # Interfaces
    def get_interfaces_status(self):
        conf_interfaces = {}
        conf_interfaces["ifEntry"] = self.get_interfaces()
        conf_interfaces["wan-interface"] = self.get_wan_interface()
        return conf_interfaces

    # Interfaces/ifEntry
    def get_interfaces(self):
        interfaces = self.interfaceController.get_interfaces()
        interfaces_dict = []
        for interface in interfaces:
            interfaces_dict.append(self.interfaceParser.get_interface_dict(interface))
        return interfaces_dict

    def get_interface(self, name):
        interface = self.interfaceController.get_interface(name)
        if interface is None:
            raise ValueError("could not find interface: " + name)
        interface_dict = self.interfaceParser.get_interface_dict(interface)
        return interface_dict

    def configure_interface(self, json_interface):
        interface = self.interfaceParser.parse_interface(json_interface)
        if interface.type == "transparent":
            self.transparent_intefaces.append(interface)
            return
        else:
            iface_found = self.interfaceController.get_interface(interface.name)
            if iface_found is not None:
                if iface_found.__eq__(interface):
                    return
            self.interfaceController.configure_interface(interface)

            logging.debug("Configured interface: " + interface.__str__())

    def update_interface(self, name, json_interface):
        interface = self.interfaceParser.parse_interface(json_interface)
        if interface.type != "transparent":
            if self.interfaceController.interface_exists(name):
                self.interfaceController.configure_interface(interface)

                logging.debug("Updated interface: " + interface.__str__())
            else:
                raise ValueError("could not find interface: " + name)

    def reset_interface(self, name):
        if not self.interfaceController.interface_exists(name):
            raise ValueError("could not find interface: " + name)
        self.interfaceController.reset_interface(name)

    def update_interface_ipv4Configuration(self, ifname, json_ipv4Configuration):
        ipv4Configuration = self.interfaceParser.parse_ipv4_configuration(json_ipv4Configuration)
        if self.interfaceController.interface_exists(ifname):
            self.interfaceController.configure_interface_ipv4Configuration(ifname, ipv4Configuration)
        else:
            raise ValueError("could not find interface: " + ifname)

    def update_interface_ipv4Configuration_address(self, ifname, address):
        if self.interfaceController.interface_exists(ifname):
            self.interfaceController.configure_interface_ipv4Configuration_address(ifname, address)
        else:
            raise ValueError("could not find interface: " + ifname)

    def update_interface_ipv4Configuration_netmask(self, ifname, netmask):
        if self.interfaceController.interface_exists(ifname):
            self.interfaceController.configure_interface_ipv4Configuration_netmask(ifname, netmask)
        else:
            raise ValueError("could not find interface: " + ifname)

    def update_interface_ipv4Configuration_default_gw(self, ifname, default_gw):
        if self.interfaceController.interface_exists(ifname):
            self.interfaceController.configure_interface_ipv4Configuration_default_gw(ifname, default_gw)
        else:
            raise ValueError("could not find interface: " + ifname)

    def get_interface_ipv4Configuration(self, name):
        if not self.interfaceController.interface_exists(name):
            raise ValueError("could not find interface: " + name)
        interface = self.interfaceController.get_interface(name)
        ipv4_configuration_dict = self.interfaceParser.get_interface_ipv4Configuration(interface.ipv4_configuration)
        return ipv4_configuration_dict

    def get_interface_ipv4Configuration_address(self, name):
        if not self.interfaceController.interface_exists(name):
            raise ValueError("could not find interface: " + name)
        interface = self.interfaceController.get_interface(name)
        return interface.ipv4_configuration.address

    def get_interface_ipv4Configuration_netmask(self, name):
        if not self.interfaceController.interface_exists(name):
            raise ValueError("could not find interface: " + name)
        interface = self.interfaceController.get_interface(name)
        return interface.ipv4_configuration.netmask

    def get_interface_ipv4Configuration_default_gw(self, name):
        if not self.interfaceController.interface_exists(name):
            raise ValueError("could not find interface: " + name)
        interface = self.interfaceController.get_interface(name)
        return interface.ipv4_configuration.default_gw

    def get_interface_ipv4Configuration_mac_address(self, name):
        if not self.interfaceController.interface_exists(name):
            raise ValueError("could not find interface: " + name)
        interface = self.interfaceController.get_interface(name)
        return interface.ipv4_configuration.mac_address


    # Interfaces/Wan-interface
    def get_wan_interface(self):
        return self.wan_interface

    def set_wan_interface(self, json_configuration):
        self.wan_interface = json_configuration['wan-interface']


    # Bridge
    def create_bridge(self, bridge):
        br_found = self.interfaceController.get_interface(bridge.name)
        if br_found is not None:
            self.bridgeController.create_bridge(bridge)
            logging.debug("Created bridge: " + bridge.__str__())
            return True
        else:
            return False


    # Firewall
    def get_firewall_status(self):
        firewall = {}
        firewall['policies'] = self.get_policies()
        firewall['blacklist'] = self.get_blacklist()
        firewall['whitelist'] = self.get_whitelist()
        return firewall

    # Firewall/Policies
    def add_policy(self, json_policy):
        policy = self.policyParser.parse_policies(json_policy)
        policies = self.policyController.get_policies()
        for pol in policies:
            if pol.__str__(policy):
                return
        id = self.policyController.add_policy(policy)
        logging.debug("Configured policy: " + policy.__str__())
        return id

    def update_policy(self, id, json_policy):
        pass

    def update_policy_description(self, id, description):
        pass

    def update_policy_action(self, id, action):
        pass

    def update_policy_protocol(self, id, protocol):
        pass

    def update_policy_in_interface(self, id, in_interface):
        pass

    def update_policy_out_interface(self, id, out_interface):
        pass

    def update_policy_src_address(self, id, src_address):
        pass

    def update_policy_dst_address(self, id, dst_address):
        pass

    def update_policy_src_port(self, id, src_port):
        pass

    def update_policy_dst_port(self, id, dst_port):
        pass

    def get_policies(self):
        policies = self.policyController.get_policies()
        policies_dict = []
        for policy in policies:
            policies_dict.append(self.policyParser.get_policy_dict(policy))
        return policies_dict

    def get_policy(self, id):
        policy = self.policyController.get_policy(id)
        if policy is None:
            raise ValueError("could not find policy: " + id)
        policy_dict = self.policyParser.get_policy_dict(policy)
        return policy_dict

    def get_policy_description(self, id):
        if not self.policyController.policy_exists(id):
            raise ValueError("could not find policy: " + id)
        policy = self.policyController.get_policy(id)
        return policy.description

    def get_policy_action(self, id):
        if not self.policyController.policy_exists(id):
            raise ValueError("could not find policy: " + id)
        policy = self.policyController.get_policy(id)
        return policy.action

    def get_policy_protocol(self, id):
        if not self.policyController.policy_exists(id):
            raise ValueError("could not find policy: " + id)
        policy = self.policyController.get_policy(id)
        return policy.protocol

    def get_policy_in_interface(self, id):
        if not self.policyController.policy_exists(id):
            raise ValueError("could not find policy: " + id)
        policy = self.policyController.get_policy(id)
        return policy.in_interface

    def get_policy_out_interface(self, id):
        if not self.policyController.policy_exists(id):
            raise ValueError("could not find policy: " + id)
        policy = self.policyController.get_policy(id)
        return policy.out_interface

    def get_policy_src_address(self, id):
        if not self.policyController.policy_exists(id):
            raise ValueError("could not find policy: " + id)
        policy = self.policyController.get_policy(id)
        return policy.src_address

    def get_policy_dst_address(self, id):
        if not self.policyController.policy_exists(id):
            raise ValueError("could not find policy: " + id)
        policy = self.policyController.get_policy(id)
        return policy.dst_address

    def get_policy_src_port(self, id):
        if not self.policyController.policy_exists(id):
            raise ValueError("could not find policy: " + id)
        policy = self.policyController.get_policy(id)
        return policy.src_port

    def get_policy_dst_port(self, id):
        if not self.policyController.policy_exists(id):
            raise ValueError("could not find policy: " + id)
        policy = self.policyController.get_policy(id)
        return policy.dst_port

    def delete_policies(self):
        pass

    def delete_policy(self, id):
        if self.policyController.policy_exists(id):
            self.policyController.delete_policy(id)
        else:
            raise ValueError("could not find policy: " + id)

    # Firewall/Blacklist
    def add_blacklist_url(self, url):
        blacklist = self.blacklistController.get_blacklist()
        for curr_url in blacklist:
            if curr_url.__eq__(url):
                return
        self.blacklistController.configure_url(url)
        logging.debug("Configured blacklist url: " + url)

    def get_blacklist(self):
        blacklist = self.blacklistController.get_blacklist()
        blacklist_dict = []
        for url in blacklist:
            blacklist_dict.append(self.blacklistParser.get_url_dict(url))
        return blacklist_dict

    def delete_blacklist(self):
        pass

    def delete_blacklist_url(self, url):
        self.blacklistController.delete_url(url)

    # Firewall/Whitelist
    def add_whitelist_url(self, url):
        whitelist = self.whitelistController.get_whitelist()
        for curr_url in whitelist:
            if curr_url.__eq__(url):
                return
        self.whitelistController.configure_url(url)
        logging.debug("Configured whitelist url: " + url)

    def get_whitelist(self):
        whitelist = self.whitelistController.get_whitelist()
        whitelist_dict = []
        for url in whitelist:
            whitelist_dict.append(self.whitelistParser.get_url_dict(url))
        return whitelist_dict

    def delete_whitelist(self):
        pass

    def delete_whitelist_url(self, url):
        self.whitelistController.delete_url(url)