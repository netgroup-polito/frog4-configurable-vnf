from common.agent import ConfigurationAgent
from common.utils import check_validity_initial_params
from firewall.dd_controller.dd_firewall_controller import DoubleDeckerFirewallController

import sys
import logging

class FirewallAgent():

    def __init__(self, nf_type, datadisk_path, on_change_interval=None):

        logging.debug("Firewall agent started...")

        configurationAgent = ConfigurationAgent("firewall", nf_type, datadisk_path, on_change_interval)

        configurationAgent.create_dd_controller(DoubleDeckerFirewallController)

        configurationAgent.set_initial_configuration()

        configurationAgent.register_agent()

        configurationAgent.start_dd_controller()

        configurationAgent.start_rest_controller("firewall.rest_api.firewall_rest_start")


if __name__ == "__main__":
        res = check_validity_initial_params(sys.argv)
        if type(res) != str:
            nf_type = res[0]
            datadisk_path = res[1]
            on_change_interval = res[2]
            FirewallAgent(nf_type, datadisk_path, on_change_interval)
        else:
            error = res
            print(error)