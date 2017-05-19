class RestDhcpController():

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


    # Dhcp Server
    def get_dhcp_status(self):
        pass

    # Dhcp Server/Configuration
    def configure_dhcp_server(self, json_dhcp_server_params):
        pass

    def update_gateway(self, json_gateway_params):
        pass

    def update_gateway_address(self, json_address):
        pass

    def update_gateway_netmask(self, json_netmask):
        pass

    def add_section(self, json_section):
        pass

    def update_section(self, section_start_ip, json_section):
        pass

    def update_section_start_ip(self, section_start_ip, json_start_ip):
        pass

    def update_section_end_ip(self, section_start_ip, json_end_ip):
        pass

    def update_default_lease_time(self, json_default_lease_time):
        pass

    def update_max_lease_time(self, json_max_lease_time):
        pass

    def update_dns(self, json_dns_params):
        pass

    def update_dns_primary_server(self, json_primary_server):
        pass

    def update_dns_secondary_server(self, json_secondary_server):
        pass

    def update_domain_name(self, json_domain_name):
        pass

    def get_dhcp_server_configuration(self):
        pass

    def get_dhcp_server_configuration_gateway(self):
        pass

    def get_dhcp_server_configuration_gateway_address(self):
        pass

    def get_dhcp_server_configuration_netmask(self):
        pass

    def get_dhcp_server_configuration_sections(self):
        pass

    def get_dhcp_server_configuration_section(self, section_start_ip):
        pass

    def get_dhcp_server_configuration_section_start_ip(self, section_start_ip):
        pass

    def get_dhcp_server_configuration_section_end_ip(self, section_start_ip):
        pass

    def get_dhcp_server_configuration_default_lease_time(self):
        pass

    def get_dhcp_server_configuration_max_lease_time(self):
        pass

    def get_dhcp_server_configuration_dns(self):
        pass

    def get_dhcp_server_configuration_primary_dns(self):
        pass

    def get_dhcp_server_configuration_secondary_dns(self):
        pass

    def get_dhcp_server_configuration_domain_name(self):
        pass

    # Dhcp Server/Clients
    def get_clients(self):
        pass

    def get_client(self, mac_address):
        pass

    def get_client_ip_address(self, mac_address):
        pass

    def get_client_hostname(self, mac_address):
        pass

    def get_client_valid_until(self, mac_address):
        pass