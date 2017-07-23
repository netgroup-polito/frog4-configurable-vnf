class IperfParser():

    def parse_interfaces(self, json_configuration):
        conf_interfaces = json_configuration["config-iperf:interfaces"]
        json_interfaces = conf_interfaces['ifEntry']
        return json_interfaces

    def parse_iperf_configuration(self, json_configuration):
        return json_configuration["config-iperf:iperf"]