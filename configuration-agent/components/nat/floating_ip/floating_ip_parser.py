from components.nat.floating_ip.floating_ip_entry_model import FloatingIpEntry

class FloatingIpParser():


    def parse_floating_ip_list(self, json_nat_configuration):
        return json_nat_configuration['floatingIP']

    def parse_floating_ip(self, json_floating_ip_params):
        private_address = None
        if 'private_address' in json_floating_ip_params:
            private_address = self.parse_floating_ip_private_address(json_floating_ip_params)

        public_address = None
        if 'public_address' in json_floating_ip_params:
            public_address = self.parse_floating_ip_public_address(json_floating_ip_params)

        return FloatingIpEntry(private_address, public_address)

    def parse_floating_ip_private_address(self, json_floating_ip_params):
        return json_floating_ip_params['private_address']

    def parse_floating_ip_public_address(self, json_floating_ip_params):
        return json_floating_ip_params['public_address']

    def get_floating_ip_dict(self, floating_ip):

        floating_ip_dict = {}

        if floating_ip.private_address is not None:
            floating_ip_dict['private_address'] = floating_ip.private_address

        if floating_ip.public_address is not None:
            floating_ip_dict['public_address'] = floating_ip.public_address

        return floating_ip_dict