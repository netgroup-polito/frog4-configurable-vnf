from common.service.bridge_service import BridgeService

class BridgeController():

    def __init__(self):
        self.bridgeService = BridgeService()

    def create_bridge(self, bridge):
        self.bridgeService.create_bridge(bridge)

    def get_bridges(self):
        return self.bridgeService.get_bridges()

    def get_bridge(self, name):
        return self.bridgeService.get_bridge(name)

