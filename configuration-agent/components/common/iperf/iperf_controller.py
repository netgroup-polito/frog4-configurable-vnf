from components.iperf.iperf_service import IperfService
from components.iperf.iperf_service_native import IperfServiceNative
#from common.config_instance import ConfigurationInstance

class IperfController():

    def __init__(self):
        self.iperfService = IperfService()
        self.iperfServiceNative = IperfServiceNative()
        #self.nf_type = ConfigurationInstance.get_nf_type(self)


    def start_iperf_client(self, iperf_client):
        #if self.nf_type == "docker" or self.nf_type == "vm":
        return self.iperfServiceNative.start_iperf_client(iperf_client)

    def stop_iperf_client(self):
        #if self.nf_type == "docker" or self.nf_type == "vm":
        self.iperfService.stop_iperf_client()


    def start_iperf_server(self, iperf_server):
        #if self.nf_type == "docker" or self.nf_type == "vm":
        return self.iperfServiceNative.start_iperf_server(iperf_server)

    def stop_iperf_server(self):
        #if self.nf_type == "docker" or self.nf_type == "vm":
        self.iperfService.stop_iperf_server()