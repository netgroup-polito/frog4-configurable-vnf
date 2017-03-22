from configuration_agent.model.natParameters import NatParameters
from configuration_agent.model.interface import Interface


class NatModel:
    yang_module_name = 'config-nat'

    def __init__(self):
        self.nat_parameters = None
        self.interfaces = None

    def set_nat_model(self, nat_model):
        self.nat_parameters = NatParameters()
        self.interfaces = list()

        self.nat_parameters.set_static_bindings(nat_model[self.yang_module_name + ':' + 'nat']['staticBindings'])
        if 'wan-interface' in nat_model[self.yang_module_name + ':' + 'nat']:
            self.nat_parameters.set_wan_interface(nat_model[self.yang_module_name + ':' + 'nat']['wan-interface'])
        else:
            self.nat_parameters.set_wan_interface(None)
        for interface in nat_model[self.yang_module_name+':'+'interfaces']['ifEntry']:
            interface_tmp = Interface()
            interface_tmp.set_interface(interface)
            self.interfaces.append(interface_tmp)

    def get_nat_model_dict(self):
        json_instance = {self.yang_module_name + ':' + 'interfaces': {'ifEntry': []},
                         self.yang_module_name + ':' + 'nat': {}}
        interfaces = json_instance[self.yang_module_name + ':' + 'interfaces']['ifEntry']
        nat = json_instance[self.yang_module_name + ':' + 'nat']

        for interface in self.interfaces:
            interfaces.append(interface.get_interface_dict())
        nat.update(self.nat_parameters.get_static_bindings_dict())
        nat.update(self.nat_parameters.get_wan_interface_dict())
        return json_instance
