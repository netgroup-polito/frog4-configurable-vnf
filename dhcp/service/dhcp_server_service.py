from dhcp.model.dhcp_server import Gateway
from dhcp.model.dhcp_server import Range
from dhcp.model.dhcp_server import Dns
from dhcp.model.dhcp_server import DhcpServer
from dhcp.model.client import Client
from utils import Bash

class DhcpServerService():

    def configure_dhcp_server(self, dhcp_server):
        pass

    def get_dhcp_server_configuration(self):
        try:
            with open('/home/giuseppe/Desktop/mydhcp.conf') as dhcpd_file:
            #with open('/etc/dhcp/dhcpd.conf') as dhcpd_file:
                dhcpd_lines = dhcpd_file.readlines()
        except Exception as e:
            raise IOError("/etc/dhcp/dhcpd.conf not found")

        gateway_address = None
        gateway_netmask = None
        ranges = []
        default_lease_time = None
        max_lease_time = None
        domain_name_server = None
        domain_name = None

        for line in dhcpd_lines:
            command = line.strip().split(' ')[0]

            if command == "default-lease-time":
                default_lease_time =  line.split('default-lease-time ')[1].split(';')[0]
            elif command == "max-lease-time":
                max_lease_time = line.split('max-lease-time ')[1].split(';')[0]
            elif command == "option":
                option = line.strip().split(' ')[1]
                if option == "routers":
                    gateway_address = line.split('option routers ')[1].split(';')[0]
                elif option == "subnet-mask":
                    gateway_netmask = line.split('option subnet-mask ')[1].split(';')[0]
                elif option == "domain-name-servers":
                    domain_name_server = line.split('option domain-name-servers ')[1].split(';')[0]
                elif option == "domain-name":
                    domain_name = line.split('option domain-name "')[1].split('";')[0]
            elif command == "subnet":
                pass
            elif command == "range":
                start_ip = line.strip().split('range ')[1].split(' ')[0]
                end_ip = line.strip().split('range ')[1].split(' ')[1].split(';')[0]
                range = Range(start_ip, end_ip)
                ranges.append(range)

        gateway = Gateway(gateway_address, gateway_netmask)
        dns = Dns(domain_name_server, domain_name)
        return DhcpServer(gateway, ranges, default_lease_time, max_lease_time, dns)

    def get_clients(self):
        clients = []

        #Bash("dhcp-lease-list --lease /var/lib/dhcp/dhcpd.leases > dhcp_leases.txt")
        try:
            with open('/home/giuseppe/Desktop/mydhcp_leases.txt') as lease_file:
            #with open('dhcp_leases') as lease_file:
                lease_lines = lease_file.readlines()[2:]
        except Exception as e:
            raise IOError("dhcp_leases not found. Probably an error occours during the generation")

        for line in lease_lines:
            line = " ".join(line.split()) #removes multiples space
            values = line.split(" ")
            client = Client(values[0], values[1], values[2], values[3]+" "+values[4])
            clients.append(client)

        return clients