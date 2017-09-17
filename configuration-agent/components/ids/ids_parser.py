from components.ids.ids_model import Ids

class IdsParser():

    def parse_ids(self, json_ids):
        return json_ids['configuration']

    def parse_ids_configuration(self, json_configuration):

        network_to_defend = None
        if 'network_to_defend' in json_configuration:
            network_to_defend = json_configuration['network_to_defend']

        attacks_to_monitor = []
        if 'attack_to_monitor' in json_configuration:
            attacks_to_monitor = self.parse_attacks_to_monitor(json_configuration['attack_to_monitor'])

        return Ids(network_to_defend, attacks_to_monitor)

    def parse_attacks_to_monitor(self, json_attack_to_monitor):
        attacks_to_monitor = []
        for json_attack in json_attack_to_monitor:
            attacks_to_monitor.append(json_attack['name'])
        return attacks_to_monitor

    def get_ids_configuration_dict(self, ids_configuration):

        ids_configuration_dict = {}

        if ids_configuration.network_to_defend is not None:
            ids_configuration_dict['network_to_defend'] = ids_configuration.network_to_defend

        attacks_dict = []
        attack_dict = {}
        for attack in ids_configuration.attacks_to_monitor:
            attack_dict['name'] = attack
            attacks_dict.append(attack_dict)
        ids_configuration_dict['attack_to_monitor'] = attacks_dict

        return ids_configuration_dict

    def get_attack_detected_dict(self, attack_name, src_addr, dst_addr):

        dict = {}

        dict['attack_name'] = attack_name
        dict['src_address'] = src_addr
        dict['dst_address'] = dst_addr

        return dict


