from common.utils import Bash
import logging

class IperfServiceNative():

    def __init__(self):
        self.result = None

    def start_iperf_client(self, iperf_client):
        cmd = "iperf3 --client " + iperf_client.server_address + \
              " --port " + iperf_client.server_port + \
              " --time " + str(iperf_client.duration)
        if iperf_client.protocol.__eq__("udp"):
            cmd += " --udp"
        if iperf_client.bidirectional is True:
            cmd += " --reverse"
        logging.debug("iperf client cmd: " + cmd)
        bash = Bash(cmd)
        result = bash.get_output()
        print(result)
        return result


    def stop_iperf_client(self):
        pass

    def start_iperf_server(self, iperf_server):
        cmd = "iperf3 --server " + iperf_server.address + \
              " --port " + iperf_server.port + \
              " --one-off"
        logging.debug("iperf server cmd: " + cmd)
        bash = Bash(cmd)
        result = bash.get_output()
        print(result)
        return result

    def stop_iperf_server(self):
        pass

    def get_result(self):
        logging.debug(self.result)