class DhcpParser():

    def parse_interfaces(self, json_configuration):
        conf_interfaces = json_configuration['config-dhcp-server:interfaces']
        json_interfaces = conf_interfaces['ifEntry']
        return json_interfaces

    def parse_dhcp_server(self, json_configuration):
        return json_configuration['config-dhcp-server:server']