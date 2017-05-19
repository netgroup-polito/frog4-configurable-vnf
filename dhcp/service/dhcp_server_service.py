from dhcp.model.dhcp_server import Gateway
from dhcp.model.dhcp_server import Section
from dhcp.model.dhcp_server import Dns
from dhcp.model.dhcp_server import DhcpServer
from dhcp.model.client import Client
from common.controller.interface_controller import InterfaceController
from utils import Bash

class DhcpServerService():

    def configure_dhcp_server(self, dhcp_server):
        '''
        example of configuration

        default-lease-time 600;
        max-lease-time 7200;
        option subnet-mask 255.255.255.0;
        option broadcast-address 192.168.1.255;
        option routers 192.168.1.254;
        option domain-name-servers 192.168.1.1, 192.168.1.2;
        option domain-name "mydomain.example";

        subnet 192.168.1.0 netmask 255.255.255.0 {
            range 192.168.1.10 192.168.1.100;
            range 192.168.1.150 192.168.1.200;
        }
        '''
        try:
            with open('/home/giuseppe/Desktop/SETdhcpd.conf', 'w') as dhcpd_file:
            #with open('/etc/dhcp/dhcpd.conf', 'w') as dhcpd_file:
                dhcpd_file.write('default-lease-time ' + dhcp_server.default_lease_time + ';\n')
                dhcpd_file.write('max-lease-time ' + dhcp_server.max_lease_time + ';\n')
                dhcpd_file.write('option subnet-mask ' + dhcp_server.gateway.address + ';\n')
                dhcpd_file.write('option routers ' + dhcp_server.gateway.netmask + ';\n')
                dhcpd_file.write('option domain-name-servers ' + dhcp_server.dns.primary_server)
                if dhcp_server.dns.secondary_server is not None:
                    dhcpd_file.write(', ' + dhcp_server.dns.secondary_server)
                dhcpd_file.write(';\n')
                dhcpd_file.write('option domain-name "' + dhcp_server.dns.domain_name + '";\n')
                dhcpd_file.write('subnet ' + dhcp_server.gateway.address + ' netmask ' + dhcp_server.gateway.netmask + ' {\n')
                for section in dhcp_server.sections:
                    dhcpd_file.write('    range ' + section.start_ip + ' ' + section.end_ip + ';\n')
                dhcpd_file.write('}')
                dhcpd_file.truncate()
        except Exception as e:
            raise IOError("Error during the creation of file: /etc/dhcp/dhcpd.conf \n" + str(e))

        interfacesController = InterfaceController()
        interfaces = interfacesController.get_interfaces()
        isc_dhcp_server = 'INTERFACES="'
        k = 0
        for interface in interfaces:
            if k != 0:
                isc_dhcp_server += ' '
            isc_dhcp_server += interface.name
            k+=1
        isc_dhcp_server += '"'
        try:
            with open('/home/giuseppe/Desktop/SETisc-dhcp-server', 'w') as isc_dhcp_server_file:
            #with open('/etc/default/isc-dhcp-server', 'w') as isc_dhcp_server_file:
                isc_dhcp_server_file.write(isc_dhcp_server)
                isc_dhcp_server_file.truncate()
        except Exception as e:
            raise IOError("Unable to create file: /etc/default/isc-dhcp-server")

        # Restart service
        #Bash('service isc-dhcp-server restart')
        #if interfaces.length == 0:
            #Bash('service isc-dhcp-server stop')

    def get_dhcp_server_configuration(self):
        try:
            with open('/home/giuseppe/Desktop/mydhcp.conf') as dhcpd_file:
            #with open('/etc/dhcp/dhcpd.conf') as dhcpd_file:
                dhcpd_lines = dhcpd_file.readlines()
        except Exception as e:
            raise IOError("/etc/dhcp/dhcpd.conf not found")

        gateway_address = None
        gateway_netmask = None
        sections = []
        default_lease_time = None
        max_lease_time = None
        primary_server = None
        secondary_server = None
        domain_name = None

        for line in dhcpd_lines:
            command = line.strip().split(' ')[0]

            if command == "default-lease-time":
                default_lease_time = line.split('default-lease-time ')[1].split(';')[0]
            elif command == "max-lease-time":
                max_lease_time = line.split('max-lease-time ')[1].split(';')[0]
            elif command == "option":
                option = line.strip().split(' ')[1]
                if option == "routers":
                    gateway_address = line.split('option routers ')[1].split(';')[0]
                elif option == "subnet-mask":
                    gateway_netmask = line.split('option subnet-mask ')[1].split(';')[0]
                elif option == "domain-name-servers":
                    servers = line.split('option domain-name-servers ')[1].split(';')[0]
                    if ',' in servers:
                        servers = servers.split(", ")
                        primary_server = servers[0]
                        secondary_server = servers[1]
                    else:
                        primary_server = servers
                elif option == "domain-name":
                    domain_name = line.split('option domain-name "')[1].split('";')[0]
            elif command == "subnet":
                pass
            elif command == "range":
                start_ip = line.strip().split('range ')[1].split(' ')[0]
                end_ip = line.strip().split('range ')[1].split(' ')[1].split(';')[0]
                section = Section(start_ip, end_ip)
                sections.append(section)

        gateway = Gateway(gateway_address, gateway_netmask)
        dns = Dns(primary_server, secondary_server, domain_name)
        return DhcpServer(gateway, sections, default_lease_time, max_lease_time, dns)

    def get_clients(self):
        clients = []

        #Bash("dhcp-lease-list --lease /var/lib/dhcp/dhcpd.leases > dhcp_leases.txt")
        try:
            with open('/home/giuseppe/Desktop/mydhcp_leases.txt') as lease_file:
            #with open('dhcp_leases') as lease_file:
                lease_lines = lease_file.readlines()[2:]
        except Exception as e:
            raise IOError("file dhcp_leases not found. Probably an error occours during the generation")

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