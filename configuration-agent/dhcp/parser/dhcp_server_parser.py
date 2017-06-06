from dhcp.model.dhcp_server import Gateway
from dhcp.model.dhcp_server import Section
from dhcp.model.dhcp_server import Dns
from dhcp.model.dhcp_server import DhcpServer

class DhcpServerParser():
    
    def parse_dhcp_server(self, json_dhcp_server_params):
        gateway = None
        if 'gatewayIp' in json_dhcp_server_params:
            gateway = self.parse_gateway(json_dhcp_server_params['gatewayIp'])

        sections = []
        if 'sections' in json_dhcp_server_params:
            sections = self.parse_sections(json_dhcp_server_params['sections'])

        default_lease_time = None
        if 'defaultLeaseTime' in json_dhcp_server_params:
            default_lease_time = self.parse_default_lease_time(json_dhcp_server_params)

        max_lease_time = None
        if 'maxLeaseTime' in json_dhcp_server_params:
            max_lease_time = self.parse_max_lease_time(json_dhcp_server_params)

        dns = None
        if 'dns' in json_dhcp_server_params:
            dns = self.parse_dns(json_dhcp_server_params['dns'])

        return DhcpServer(gateway, sections, default_lease_time, max_lease_time, dns)

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
        for json_section in json_sections:
            section = self.parse_section(json_section)
            sections.append(section)
        return sections

    def parse_section(self, json_section):
        start_ip = None
        if 'sectionStartIp' in json_section:
            start_ip = self.parse_section_start_ip(json_section)

        end_ip = None
        if 'sectionEndIp' in json_section:
            end_ip = self.parse_section_end_ip(json_section)

        return Section(start_ip, end_ip)

    def parse_section_start_ip(self, json_section_params):
        return json_section_params['sectionStartIp']

    def parse_section_end_ip(self, json_section_params):
        return json_section_params['sectionEndIp']

    def parse_default_lease_time(self, json_dhcp_server_params):
        return json_dhcp_server_params['defaultLeaseTime']

    def parse_max_lease_time(self, json_dhcp_server_params):
        return json_dhcp_server_params['maxLeaseTime']

    def parse_dns(self, json_dns_params):
        primary_server = None
        if 'primaryServer' in json_dns_params:
            primary_server = self.parse_dns_primary_server(json_dns_params)

        secondary_server = None
        if 'secondaryServer' in json_dns_params:
            secondary_server = self.parse_dns_secondary_server(json_dns_params)

        domain_name = None
        if 'domainName' in json_dns_params:
            domain_name = self.parse_dns_domain_name(json_dns_params)

        return Dns(primary_server, secondary_server, domain_name)

    def parse_dns_primary_server(self, json_dns_params):
        return json_dns_params['primaryServer']

    def parse_dns_secondary_server(self, json_dns_params):
        return json_dns_params['secondaryServer']

    def parse_dns_domain_name(self, json_dns_params):
        return json_dns_params['domainName']


    def get_dhcp_server_configuration_dict(self, dhcp_server):

        dhcp_server_dict = {}

        gateway_dict = {}
        if dhcp_server.gateway is not None:
            gateway_dict = self.get_dhcp_server_configuration_gateway_dict(dhcp_server.gateway)
        dhcp_server_dict['gatewayIp'] = gateway_dict

        sections_dict = []
        section_dict = {}
        for section in dhcp_server.sections:
            section_dict = self.get_dhcp_server_configuration_section_dict(section)
            sections_dict.append(section_dict)
        dhcp_server_dict['sections'] = sections_dict

        if dhcp_server.default_lease_time is not None:
            dhcp_server_dict['defaultLeaseTime'] = dhcp_server.default_lease_time

        if dhcp_server.max_lease_time is not None:
            dhcp_server_dict['maxLeaseTime'] = dhcp_server.max_lease_time

        dns_dict = {}
        if dhcp_server.dns is not None:
            dns_dict = self.get_dhcp_server_configuration_dns_dict(dhcp_server.dns)
        dhcp_server_dict['dns'] = dns_dict

        return dhcp_server_dict

    def get_dhcp_server_configuration_gateway_dict(self, gateway):
        gateway_dict = {}
        if gateway.address is not None:
            gateway_dict['gatewayAddress'] = gateway.address
        if gateway.netmask is not None:
            gateway_dict['gatewayMask'] = gateway.netmask
        return gateway_dict

    def get_dhcp_server_configuration_section_dict(self, section):
        section_dict = {}
        if section.start_ip is not None:
            section_dict['sectionStartIp'] = section.start_ip
        if section.end_ip is not None:
            section_dict['sectionEndIp'] = section.end_ip
        return section_dict

    def get_dhcp_server_configuration_dns_dict(self, dns):
        dns_dict = {}
        if dns.primary_server is not None:
            dns_dict['primaryServer'] = dns.primary_server
        if dns.secondary_server is not None:
            dns_dict['secondaryServer'] = dns.secondary_server
        if dns.domain_name is not None:
            dns_dict['domainNameServer'] = dns.domain_name
        return dns_dict


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
