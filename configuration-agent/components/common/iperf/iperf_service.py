import iperf3
import logging

class IperfService():

    def __init__(self):
        self.result = None

    def start_iperf_client(self, iperf_client):
        client = iperf3.Client()
        client.server_hostname = iperf_client.server_address
        client.port = iperf_client.server_port
        client.protocol = iperf_client.protocol
        client.duration = iperf_client.duration
        client.reverse = iperf_client.bidirectional
        print("Connecting to " + client.server_hostname + ":" + str(client.port))
        result = client.run()

        if result.error:
            print(result.error)
            return result.error
        else:
            print("duration: " + str(result.duration))
            print(round(result.sent_MB_s, 2))
            print(round(result.received_MB_s, 2))
            print(result)


    def stop_iperf_client(self):
        pass

    def start_iperf_server(self, iperf_server):
        logging.debug(iperf_server.__str__())
        server = iperf3.Server()
        server.bind_address = iperf_server.address
        server.port = iperf_server.port
        #server.verbose = False
        print("Server listening on " + str(server.port))
        result = server.run()

    def stop_iperf_server(self):
        pass

    def get_result(self):
        logging.debug(self.result)

