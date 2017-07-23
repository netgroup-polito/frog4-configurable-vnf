from common.config_instance import ConfigurationInstance
from components.common.bridge.bridge_service import BridgeService

class BridgeController():

    def __init__(self):
        self.bridgeService = BridgeService()
        self.nf_type = ConfigurationInstance.get_nf_type(self)

    def create_bridge(self, bridge):
        if self.nf_type == "docker" or self.nf_type == "vm":
            self.bridgeService.create_bridge(bridge)

    def get_bridges(self):
        if self.nf_type == "docker" or self.nf_type == "vm":
            return self.bridgeService.get_bridges()

    def get_bridge(self, name):
        if self.nf_type == "docker" or self.nf_type == "vm":
            return self.bridgeService.get_bridge(name)

