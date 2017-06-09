from common.agent import ConfigurationAgent
from common.utils import check_validity_initial_params
from dhcp.dd_controller.dd_dhcp_controller import DoubleDeckerDhcpController

import sys
import logging

class DhcpAgent():

    def __init__(self, nf_type, datadisk_path, on_change_interval=None):

        logging.debug("Dhcp agent started...")

        configurationAgent = ConfigurationAgent("dhcp", nf_type, datadisk_path, on_change_interval)

        configurationAgent.create_dd_controller(DoubleDeckerDhcpController)

        configurationAgent.set_initial_configuration()

        configurationAgent.register_agent()

        configurationAgent.start_dd_controller()

        configurationAgent.start_rest_controller("dhcp.rest_api.dhcp_rest_start")


if __name__ == "__main__":
        res = check_validity_initial_params(sys.argv)
        if type(res) != str:
            nf_type = res[0]
            datadisk_path = res[1]
            on_change_interval = res[2]
            DhcpAgent(nf_type, datadisk_path, on_change_interval)
        else:
            error = res
            print(error)