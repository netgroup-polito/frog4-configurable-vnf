class NatParser():

    def parse_interfaces(self, json_configuration):
        conf_interfaces = json_configuration["config-nat:interfaces"]
        json_interfaces = conf_interfaces['ifEntry']
        return json_interfaces

    def parse_nat_configuration(self, json_configuration):
        return json_configuration["config-nat:nat"]


