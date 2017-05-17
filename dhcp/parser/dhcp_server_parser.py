from dhcp.model.dhcp_server import Gateway
from dhcp.model.dhcp_server import Range
from dhcp.model.dhcp_server import Dns
from dhcp.model.dhcp_server import DhcpServer

class DhcpServerParser():
    
    def parse_dhcp_server(self, json_dhcp_server_params):
        gateway = None
        if 'gatewayIp' in json_dhcp_server_params:
            gateway = self.parse_gateway(json_dhcp_server_params['gatewayIp'])

        ranges = []
        if 'sections' in json_dhcp_server_params:
            ranges = self.parse_sections(json_dhcp_server_params['sections'])

        default_lease_time = None
        if 'defaultLeaseTime' in json_dhcp_server_params:
            default_lease_time = self.parse_default_lease_time(json_dhcp_server_params)

        max_lease_time = None
        if 'maxLeaseTime' in json_dhcp_server_params:
            max_lease_time = self.parse_max_lease_time(json_dhcp_server_params)

        domain_name_server = None
        if 'domainNameServer' in json_dhcp_server_params:
            domain_name_server = self.parse_domain_name_server(json_dhcp_server_params)
        domain_name = None
        if 'domainName' in json_dhcp_server_params:
            domain_name = self.parse_domain_name(json_dhcp_server_params)
        dns = Dns(domain_name_server, domain_name)

        return DhcpServer(gateway, ranges, default_lease_time, max_lease_time, dns)

    def parse_gateway(self, json_gateway_params):
        address = None
        if 'gatewayAddress' in json_gateway_params:
            address = self.parse_gateway_address(json_gateway_params)

        netmask = None
        if 'gatewayMask' in json_gateway_params:
            netmask = self.parse_gateway_netmask(json_gateway_params)

        return Gateway(address, netmask)

    def parse_gateway_address(self, json_gateway_params):
        return json_gateway_params['gatewayAddress']

    def parse_gateway_netmask(self, json_gateway_params):
        return json_gateway_params['gatewayMask']

    def parse_sections(self, json_sections):
        sections = []
        for json_section in json_sections['section']:
            section = self.parse_section(json_section)
            sections.append(section)
        return sections

    def parse_section(self, json_section):
        start_ip = None
        if 'sectionStartIp' in json_section:
            start_ip = self.parse_start_ip(json_section)

        end_ip = None
        if 'sectionEndIp' in json_section:
            end_ip = self.parse_end_ip(json_section)

        return Range(start_ip, end_ip)

    def parse_start_ip(self, json_range_params):
        return json_range_params['sectionStartIp']

    def parse_end_ip(self, json_range_params):
        return json_range_params['sectionEndIp']

    def parse_default_lease_time(self, json_dhcp_server_params):
        return json_dhcp_server_params['defaultLeaseTime']

    def parse_max_lease_time(self, json_dhcp_server_params):
        return json_dhcp_server_params['maxLeaseTime']

    def parse_dns(self, json_dns_params):
        domain_name_server = None
        if 'domainNameServer' in json_dns_params:
            domain_name_server = self.parse_domain_name_server(json_dns_params)

        domain_name = None
        if 'domainName' in json_dns_params:
            domain_name = self.parse_domain_name(json_dns_params)

        return Dns(domain_name_server, domain_name)

    def parse_domain_name_server(self, json_dns_params):
        return json_dns_params['domainNameServer']

    def parse_domain_name(self, json_dns_params):
        return json_dns_params['domainName']


    def get_dhcp_server_configuration_dict(self, dhcp_server):

        dhcp_server_dict = {}

        gateway_dict = {}
        if dhcp_server.gateway.address is not None:
            gateway_dict['gatewayAddress'] = dhcp_server.gateway.address
        if dhcp_server.gateway.netmask is not None:
            gateway_dict['gatewayMask'] = dhcp_server.gateway.netmask
        dhcp_server_dict['gatewayIp'] = gateway_dict

        ranges_dict = []
        range_dict = {}
        for range in dhcp_server.ranges:
            range_dict['sectionStartIp'] = range.start_ip
            range_dict['sectionEndIp'] = range.end_ip
            ranges_dict.append(range_dict)
        sections = {}
        sections['section'] = ranges_dict
        dhcp_server_dict['sections'] = sections

        if dhcp_server.default_lease_time is not None:
            dhcp_server_dict['defaultLeaseTime'] = dhcp_server.default_lease_time

        if dhcp_server.max_lease_time is not None:
            dhcp_server_dict['maxLeaseTime'] = dhcp_server.max_lease_time

        if dhcp_server.dns.domain_name_server is not None:
            dhcp_server_dict['domainNameServer'] = dhcp_server.dns.domain_name_server

        if dhcp_server.dns.domain_name is not None:
            dhcp_server_dict['domainName'] = dhcp_server.dns.domain_name

        return dhcp_server_dict

    def get_client_dict(self, client):

        client_dict = {}

        if client.mac_address is not None:
            client_dict['mac_address'] = client.mac_address

        if client.ip_address is not None:
            client_dict['ip_address'] = client.ip_address

        if client.hostname is not None:
            client_dict['hostname'] = client.hostname

        if client.valid_until is not None:
            client_dict['valid_until'] = client.valid_until

        return client_dict
