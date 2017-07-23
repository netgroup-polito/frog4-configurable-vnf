class NatCoreParser():

    def parse_public_interface(self, json_nat_params):
        return json_nat_params['public-interface']

    def parse_private_interface(self, json_nat_params):
        return json_nat_params['private-interface']