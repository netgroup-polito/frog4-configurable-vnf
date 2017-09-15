from common.config_instance import ConfigurationInstance
from components.ids.ids_service import IdsService
import logging

class IdsController():

    def __init__(self):
        self.idsService = IdsService()
        self.nf_type = ConfigurationInstance().get_nf_type()
        #self.current_configuration = None

    def get_configuration(self):
        pass

    def set_configuration(self, ids_configuration):
        if self.nf_type == "docker" or self.nf_type == "vm":
            self.idsService.set_configuration(ids_configuration.network_to_defend)

        if len(ids_configuration.attacks_to_monitor) > 0:
            self.configure_attacks(ids_configuration.attacks_to_monitor)

    def configure_attacks(self, attacks_to_monitor):
        for attack in attacks_to_monitor:
            if attack.__eq__("port_scan"):
                self.configure_detection_portScan()
            else:
                logging.debug("attack: " + attack + " unknown")


    def configure_detection_portScan(self):
        if self.nf_type == "docker" or self.nf_type == "vm":
            self.idsService.configure_detection_portScan()

    def start_monitor(self):
        if self.nf_type == "docker" or self.nf_type == "vm":
            pass

