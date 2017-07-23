from components.iperf.model.iperf_client import IperfClient
from components.iperf.model.iperf_server import IperfServer
#from components.common.iperf.model.stat import Stats

class IperfParser():

    def parse_server_configuration(self, json_server_params):

        address = json_server_params['address']
        port = json_server_params['port']

        return IperfServer(address, port)


    def parse_client_configuration(self, json_client_params):

        server_address = json_client_params['server_address']
        port_address = json_client_params['server_port']
        protocol = json_client_params['protocol']
        duration = json_client_params['duration']
        bidirectional = json_client_params['bidirectional']

        return IperfClient(server_address,
                           port_address,
                           protocol,
                           duration,
                           bidirectional)


    def get_stats_dict(self, stats):
        pass


