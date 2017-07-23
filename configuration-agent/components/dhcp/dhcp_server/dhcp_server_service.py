from components.dhcp.dhcp_server.dhcp_server_model import DhcpServer, Section
from components.common.interface.interface_controller import InterfaceController
from common.utils import Bash

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
            with open('/etc/dhcp/dhcpd.conf', 'w') as dhcpd_file:
                dhcpd_file.write('default-lease-time ' + dhcp_server.default_lease_time + ';\n')
                dhcpd_file.write('max-lease-time ' + dhcp_server.max_lease_time + ';\n')
                dhcpd_file.write('option subnet-mask ' + dhcp_server.subnet_mask + ';\n')
                dhcpd_file.write('option routers ' + dhcp_server.router + ';\n')
                dhcpd_file.write('option domain-name-servers ' + dhcp_server.dns_primary_server)
                if dhcp_server.dns_secondary_server is not None:
                    dhcpd_file.write(', ' + dhcp_server.dns_secondary_server)
                dhcpd_file.write(';\n')
                dhcpd_file.write('option domain-name "' + dhcp_server.dns_domain_name + '";\n')
                dhcpd_file.write('subnet ' + dhcp_server.subnet + ' netmask ' + dhcp_server.subnet_mask + ' {\n')
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
            with open('/etc/default/isc-dhcp-server', 'w') as isc_dhcp_server_file:
                isc_dhcp_server_file.write(isc_dhcp_server)
                isc_dhcp_server_file.truncate()
        except Exception as e:
            raise IOError("Unable to create file: /etc/default/isc-dhcp-server")

        # Restart service
        Bash('service isc-dhcp-server restart')
        if len(interfaces) == 0:
            Bash('service isc-dhcp-server stop')

    def get_dhcp_server_configuration(self):
        try:
            with open('/etc/dhcp/dhcpd.conf') as dhcpd_file:
                dhcpd_lines = dhcpd_file.readlines()
            dhcpd_file.close()
        except Exception as e:
            raise IOError("/etc/dhcp/dhcpd.conf not found")

        default_lease_time = None,
        max_lease_time = None,
        subnet = None,
        subnet_mask = None,
        router = None,
        dns_primary_server = None,
        dns_secondary_server = None,
        dns_domain_name = None,
        sections = []

        for line in dhcpd_lines:
            command = line.strip().split(' ')[0]

            if command == "default-lease-time":
                default_lease_time = line.split('default-lease-time ')[1].split(';')[0]
            elif command == "max-lease-time":
                max_lease_time = line.split('max-lease-time ')[1].split(';')[0]
            elif command == "option":
                option = line.strip().split(' ')[1]
                if option == "routers":
                    router = line.split('option routers ')[1].split(';')[0]
                elif option == "subnet-mask":
                    subnet_mask = line.split('option subnet-mask ')[1].split(';')[0]
                elif option == "domain-name-servers":
                    servers = line.split('option domain-name-servers ')[1].split(';')[0]
                    if ',' in servers:
                        servers = servers.split(", ")
                        dns_primary_server = servers[0]
                        dns_secondary_server = servers[1]
                    else:
                        dns_primary_server = servers
                elif option == "domain-name":
                    dns_domain_name = line.split('option domain-name "')[1].split('";')[0]
            elif command == "subnet":
                subnet = line.split(' ')[1]
            elif command == "range":
                start_ip = line.strip().split('range ')[1].split(' ')[0]
                end_ip = line.strip().split('range ')[1].split(' ')[1].split(';')[0]
                section = Section(start_ip, end_ip)
                sections.append(section)

        return DhcpServer(default_lease_time,
                          max_lease_time,
                          subnet,
                          subnet_mask,
                          router,
                          dns_primary_server,
                          dns_secondary_server,
                          dns_domain_name,
                          sections)

