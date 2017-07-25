from common.agent import ConfigurationAgent
from common.utils import check_validity_initial_params
from traffic_shaper.traffic_shaper_monitor import TrafficShaperMonitor

import sys
import logging

class TrafficShaperAgent():

    def __init__(self, nf_type, datadisk_path, on_change_interval=None):

        logging.debug("Traffic Shaper agent started...")

        configurationAgent = ConfigurationAgent("traffic_shaper", nf_type, datadisk_path, on_change_interval)

        configurationAgent.start_monitoring(TrafficShaperMonitor)

        configurationAgent.start_rest_controller("traffic_shaper.rest_api.traffic_shaper_rest_start")


if __name__ == "__main__":
        res = check_validity_initial_params(sys.argv)
        if type(res) != str:
            nf_type = res[0]
            datadisk_path = res[1]
            on_change_interval = res[2]
            TrafficShaperAgent(nf_type, datadisk_path, on_change_interval)
        else:
            error = res
            print(error)