from components.common.traffic_shaper.traffic_shaper_service import TrafficShaperService
#from common.config_instance import ConfigurationInstance

class TrafficShaperController():

    def __init__(self):
        self.trafficShaperService = TrafficShaperService()
        #self.nf_type = ConfigurationInstance.get_nf_type(self)


    def start_bandwitdh_shaping(self, TrafficShaper):
        #if self.nf_type == "docker" or self.nf_type == "vm":
        self.trafficShaperService.start_bandwitdh_shaping(TrafficShaper)

    def stop_bandwitdh_shaping(self):
        #if self.nf_type == "docker" or self.nf_type == "vm":
        self.trafficShaperService.stop_bandwitdh_shaping(interface_name)


    def get_status(self):
        #if self.nf_type == "docker" or self.nf_type == "vm":
        self.trafficShaperService.get_status(interface_name)

