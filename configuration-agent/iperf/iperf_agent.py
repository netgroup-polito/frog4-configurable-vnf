from common.utils import check_validity_initial_params
import sys
from subprocess import call
import logging

class IperfAgent():

    def __init__(self, nf_type, datadisk_path, on_change_interval=None):

        logging.debug("Iperf agent started...")

        rest_address = "127.0.0.1"
        rest_port = "9010"
        rest_endpoint = "http://" + rest_address + ":" + rest_port
        logging.info("Rest Server started on: " + rest_endpoint)
        call("gunicorn -b " + rest_address + ':' + rest_port + " -t 500 rest_api.iperf_rest_start:app", shell=True)


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