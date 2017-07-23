from components.dhcp.dhcp_client.dhcp_client_model import Client
from common.utils import Bash

class DhcpClientService():

    def get_clients(self):
        clients = []

        Bash("dhcp-lease-list --lease /var/lib/dhcp/dhcpd.leases > dhcp_leases.txt")
        try:
            #with open('/home/giuseppe/Desktop/mydhcp_leases.txt') as lease_file:
            with open('dhcp_leases.txt') as lease_file:
                lease_lines = lease_file.readlines()[2:]
        except Exception as e:
            return clients
            #raise IOError("file dhcp_leases not found. Probably an error occours during the generation")

        for line in lease_lines:
            line = " ".join(line.split()) #removes multiples space
            values = line.split(" ")
            client = Client(values[0], values[1], values[2], values[3]+" "+values[4])
            clients.append(client)

        return clients

    def get_client(self, mac_address):
        clients = self.get_clients()
        for client in clients:
            if client.mac_address == mac_address:
                return client
        return None