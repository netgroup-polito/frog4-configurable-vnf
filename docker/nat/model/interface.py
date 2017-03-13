class Interface:
    def __init__(self):
        self.name = None
        self.configuration_type = None
        self.address = None
        self.default_gw = None
        self.management = None
        self.netmask = 24
        self.mac_address = None

    def __init(self, name, configuration_type, mac_address, address=None, default_gw=None, management=None, netmask=24):
        self.name = name
        self.configuration_type = configuration_type
        self.address = address
        self.default_gw = default_gw
        self.management = management
        self.netmask = netmask
        self.mac_address = mac_address

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
