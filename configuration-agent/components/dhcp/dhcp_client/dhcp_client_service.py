from components.dhcp.dhcp_client.dhcp_client_model import Client
from common.utils import Bash
from isc_dhcp_leases import Lease, IscDhcpLeases

class DhcpClientService():

    def get_clients(self):

        clients = []
        leases = IscDhcpLeases('/var/lib/dhcp/dhcpd.leases')
        list = leases.get_current()
        for key in list:
            lease = list[key]
            mac_address = lease.ethernet
            ip_address = lease.ip
            hostname = lease.hostname
            lease_time = str(lease.end)
            client = Client(mac_address, ip_address, hostname, lease_time)
            clients.append(client)

        return clients

    def get_client(self, mac_address):
        clients = self.get_clients()
        for client in clients:
            if client.mac_address == mac_address:
                return client
        return None