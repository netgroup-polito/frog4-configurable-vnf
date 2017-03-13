class NatParameters:
    def __init__(self):
        self.floating_ip_list = None
        self.wan_interface = None

    def set_static_bindings(self, static_bindings):
        self.set_floating_ip(static_bindings['floatingIP'])

    def set_floating_ip(self, floating_ip_list_dict):
        self.floating_ip_list = list()

        for floating_ip in floating_ip_list_dict:
            curr_floating = {}
            curr_floating['private_address'] = floating_ip['private_address']
            curr_floating['public_address'] = floating_ip['public_address']
            self.floating_ip_list.append(curr_floating)

    def set_wan_interface(self, wan_interface):
        self.wan_interface = wan_interface

    def get_static_bindings_dict(self):
        static_bindings = {'staticBindings': {'floatingIP': []}}
        floating_ip_mapping = static_bindings['staticBindings']['floatingIP']
        for floating_ip in self.floating_ip_list:
            floating_ip_dict = {}
            floating_ip_dict['private_address'] = floating_ip['private_address']
            floating_ip_dict['public_address'] = floating_ip['public_address']
            floating_ip_mapping.append(floating_ip_dict)
        return static_bindings

    def get_wan_interface_dict(self):
        if self.wan_interface is None:
            return None
        return {'wan_interface': self.wan_interface}