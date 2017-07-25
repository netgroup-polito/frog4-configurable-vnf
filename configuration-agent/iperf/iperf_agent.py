from common.agent import ConfigurationAgent
from common.utils import check_validity_initial_params
from iperf.iperf_monitor import IperfMonitor

import sys
from subprocess import call
import logging

class IperfAgent():

    def __init__(self, nf_type, datadisk_path, on_change_interval=None):

        logging.debug("Iperf agent started...")

        configurationAgent = ConfigurationAgent("iperf", nf_type, datadisk_path, on_change_interval)

        configurationAgent.start_monitoring(IperfMonitor)

        configurationAgent.start_rest_controller("iperf.rest_api.iperf_rest_start")


if __name__ == "__main__":
        res = check_validity_initial_params(sys.argv)
        if type(res) != str:
            nf_type = res[0]
            datadisk_path = res[1]
            on_change_interval = res[2]
            IperfAgent(nf_type, datadisk_path, on_change_interval)
        else:
            error = res
            print(error)