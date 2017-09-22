from components.iperf.model import IperfClient
from components.iperf.model import IperfServer

class IperfParser():

    def parse_server(self, json_configuration):
        return json_configuration['server']

    def parse_server_configuration(self, json_server_params):

        address = json_server_params['address']
        port = json_server_params['port']

        return IperfServer(address, port)


    def parse_client(self, json_configuration):
        return json_configuration['client']

    def parse_client_configuration(self, json_client_params):

        server_address = None
        if 'server_address' in json_client_params:
            server_address = json_client_params['server_address']

        server_port = None
        if 'server_port' in json_client_params:
            server_port = json_client_params['server_port']

        protocol = None
        if 'protocol' in json_client_params:
            protocol = json_client_params['protocol']

        duration = None
        if 'duration' in json_client_params:
            duration = json_client_params['duration']

        bidirectional = None
        if 'bidirectional' in json_client_params:
            bidirectional = json_client_params['bidirectional']

        bitrate = None
        if 'bitrate' in json_client_params:
            bitrate = json_client_params['bitrate']

        return IperfClient(server_address,
                           server_port,
                           protocol,
                           duration,
                           bidirectional,
                           bitrate)



