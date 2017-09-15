class IdsParser():

    def parse_interfaces(self, json_configuration):
        conf_interfaces = json_configuration["config-ids:interfaces"]
        json_interfaces = conf_interfaces['ifEntry']
        return json_interfaces

    def parse_ids(self, json_configuration):
        return json_configuration["config-ids:ids"]