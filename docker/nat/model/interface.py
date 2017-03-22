class Interface:

    def __init__(self, name=None, configuration_type=None, mac_address=None, address=None, netmask='24', default_gw=None, management=None):
        self.name = name
        self.configuration_type = configuration_type
        self.mac_address = mac_address
        self.address = address
        self.netmask = netmask
        self.default_gw = default_gw
        self.management = management


    def set_interface(self, interface_dict):
        self.address = None
        self.default_gw = None
        self.management = None

        if 'name' in interface_dict:
            self.name = interface_dict['name']
        if 'configurationType' in interface_dict:
            self.configuration_type = interface_dict['configurationType']
        if 'address' in interface_dict:
            self.address = interface_dict['address']
        if 'default_gw' in interface_dict:
            self.default_gw = interface_dict['default_gw']
        if 'management' in interface_dict:
            self.management = interface_dict['management']
        if 'mac_address' in interface_dict:
            self.mac_address = interface_dict['mac_address']

        assert self.name is not None
        assert self.configuration_type is not None

    def get_interface_dict(self):
        dict = {}
        dict['name'] = self.name
        dict['configurationType'] = self.configuration_type
        dict['mac_address'] = self.mac_address
        if self.address is not None:
            dict['address'] = self.address
        if self.default_gw is not None:
            dict['default_gw'] = self.default_gw
        if self.management is not None:
            dict['management'] = self.management
        return dict
