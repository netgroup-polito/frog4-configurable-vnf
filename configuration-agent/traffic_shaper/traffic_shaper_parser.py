class TrafficShaperParser():

    def parse_interfaces(self, json_configuration):
        conf_interfaces = json_configuration["config-traffic-shaper:interfaces"]
        json_interfaces = conf_interfaces['ifEntry']
        return json_interfaces

    def parse_traffic_shaper_configuration(self, json_configuration):
        return json_configuration["config-traffic-shaper:traffic_shaper"]