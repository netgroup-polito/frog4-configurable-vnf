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
            logging.debug("network_to_defend: " + ids_configuration.network_to_defend)
            self.idsService.set_configuration(ids_configuration.network_to_defend)

        for attack in ids_configuration.attacks_to_monitor:
            self.add_attackToMonitor(attack)

    def add_attackToMonitor(self, attack):
        if attack.__eq__("port_scan"):
            self._configure_detection_portScan()
        elif attack.__eq__("ping_flood"):
            self._configure_detection_pingFlood()
        else:
            logging.debug("attack: " + attack + " unknown")

    def _configure_detection_portScan(self):
        if self.nf_type == "docker" or self.nf_type == "vm":
            self.idsService.configure_detection_portScan()

    def _configure_detection_pingFlood(self):
        if self.nf_type == "docker" or self.nf_type == "vm":
            self.idsService.configure_detection_pingFlood()

    def start_ids(self):
        if self.nf_type == "docker" or self.nf_type == "vm":
            self.idsService.start_ids()

