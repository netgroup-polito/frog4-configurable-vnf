class RestFirewallController():

    def set_configuration(self, json_configuration):
        pass

    def get_full_status(self):
        pass


    # Interfaces
    def get_interfaces_status(self):
        pass

    # Interfaces/ifEntry
    def configure_interface(self, json_interface):
        pass

    def update_interface(self, name, json_interface):
        pass

    def update_interface_address(self, ifname, json_address):
        pass

    def update_interface_netmask(self, ifname, json_netmask):
        pass

    def update_interface_default_gw(self, ifname, json_default_gw):
        pass

    def get_interfaces_ifEntry(self):
        pass

    def get_interface(self, name):
        pass

    def get_interface_ipv4Configuration(self, name):
        pass

    def get_interface_ipv4Configuration_address(self, name):
        pass

    def get_interface_ipv4Configuration_netmask(self, name):
        pass

    def get_interface_ipv4Configuration_default_gw(self, name):
        pass

    def get_interface_ipv4Configuration_mac_address(self, name):
        pass

    def reset_interface(self, name):
        pass

    # Interfaces/Wan-interface
    def get_wan_interface(self):
        pass

    def set_wan_interface(self, json_wan_interface):
        pass


    # Firewall
    def get_firewall_status(self):
        pass

    # Firewall/Policies
    def add_policy(self, json_policy):
        pass

    def update_policy(self, id, json_policy):
        pass

    def update_policy_description(self, id, json_description):
        pass

    def update_policy_action(self, id, json_action):
        pass

    def update_policy_protocol(self, id, json_protocol):
        pass

    def update_policy_in_interface(self, id, json_in_interface):
        pass

    def update_policy_out_interface(self, id, json_out_interface):
        pass

    def update_policy_src_address(self, id, json_src_address):
        pass

    def update_policy_dst_address(self, id, json_dst_address):
        pass

    def update_policy_src_port(self, id, json_src_port):
        pass

    def update_policy_dst_port(self, id, json_dst_port):
        pass

    def get_policies(self):
        pass

    def get_policy(self, id):
        pass

    def get_policy_description(self, id):
        pass

    def get_policy_action(self, id):
        pass

    def get_policy_protocol(self, id):
        pass

    def get_policy_in_interface(self, id):
        pass

    def get_policy_out_interface(self, id):
        pass

    def get_policy_src_address(self, id):
        pass

    def get_policy_dst_address(self, id):
        pass

    def get_policy_src_port(self, id):
        pass

    def get_policy_dst_port(self, id):
        pass

    def delete_policies(self):
        pass

    def delete_policy(self, id):
        pass

    # Firewall/Blacklist
    def configure_blacklist_url(self, json_url):
        pass

    def get_blacklist(self):
        pass

    def delete_blacklist(self):
        pass

    def delete_blacklist_url(self, url):
        pass

    # Firewall/Whitelist
    def configure_whitelist_url(self, json_url):
        pass

    def get_whitelist(self):
        pass

    def delete_whitelist(self):
        pass

    def delete_whitelist_url(self, url):
        pass