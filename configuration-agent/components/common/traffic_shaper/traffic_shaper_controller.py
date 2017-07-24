from components.common.traffic_shaper.traffic_shaper_service import TrafficShaperService
#from common.config_instance import ConfigurationInstance
import logging

class TrafficShaperController():

    def __init__(self):
        self.trafficShaperService = TrafficShaperService()
        #self.nf_type = ConfigurationInstance.get_nf_type(self)
        self.traffic_shaper_map = {}
        logging.debug("TrafficShaperController istanziato")


    def start_bandwitdh_shaping(self, trafficShaper):
        #if self.nf_type == "docker" or self.nf_type == "vm":
        #self.trafficShaperService.start_bandwitdh_shaping(trafficShaper)
        self.traffic_shaper_map[trafficShaper.interface_name] = trafficShaper

    def stop_bandwitdh_shaping(self, interface_name):
        #if self.nf_type == "docker" or self.nf_type == "vm":
        #self.trafficShaperService.stop_bandwitdh_shaping(interface_name)
        del self.traffic_shaper_map[interface_name]

    def update_bandwidth_shaping_download_limit(self, interface_name, download_limit):
        traffic_shaper = self.traffic_shaper_map[interface_name]
        traffic_shaper.download_limit = download_limit
        #self.stop_bandwitdh_shaping(interface_name)
        #self.start_bandwitdh_shaping(traffic_shaper)
        self.traffic_shaper_map[interface_name] = traffic_shaper

    def update_bandwidth_shaping_upload_limit(self, interface_name, upload_limit):
        traffic_shaper = self.traffic_shaper_map[interface_name]
        traffic_shaper.upload_limit = upload_limit
        #self.stop_bandwitdh_shaping(interface_name)
        #self.start_bandwitdh_shaping(traffic_shaper)
        self.traffic_shaper_map[interface_name] = traffic_shaper

    def traffic_shaper_exists(self, interface_name):
        if interface_name in self.traffic_shaper_map:
            return True
        else:
            return False

    def get_all_traffic_shapers(self):
        pass

    def get_traffic_shaper(self, interface_name):
        #if self.nf_type == "docker" or self.nf_type == "vm":
        return self.traffic_shaper_map[interface_name]
        #self.trafficShaperService.get_status(interface_name)

