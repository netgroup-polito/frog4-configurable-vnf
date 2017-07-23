class FirewallParser():

    def parse_interfaces(self, json_configuration):
        conf_interfaces = json_configuration["config-firewall:interfaces"]
        json_interfaces = conf_interfaces['ifEntry']
        return json_interfaces

    def parse_firewall_configuration(self, json_configuration):
        return json_configuration["config-firewall:firewall"]

    def parse_wan_interface(self, json_firewall_configuration):
        return json_firewall_configuration['wan-interface']