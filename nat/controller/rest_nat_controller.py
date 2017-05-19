class RestNatController():

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


    # Nat
    def get_nat_status(self):
        pass

    # Nat/Wan-interface
    def set_ip_forward(self, json_nat_configurations):
        pass

    def unset_ip_forward(self, json_nat_configurations):
        pass

    def get_wan_interface(self):
        pass

    # Nat/StaticBindings
    def add_floating_ip(self, json_floating_ip):
        pass

    def update_floating_ip(self, private_address, json_floating_ip):
        pass

    def update_floating_ip_private_address(self, private_address, json_private_address):
        pass

    def update_floating_ip_public_address(self, private_address, json_private_address):
        pass

    def delete_floating_ip(self, private_address):
        pass

    def get_all_floating_ip(self):
        pass

    def get_floating_ip(self, private_address):
        pass

    def get_floating_ip_private_address(self, private_address):
        pass

    def get_floating_ip_public_address(self, private_address):
        pass