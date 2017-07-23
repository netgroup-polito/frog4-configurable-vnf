from components.dhcp.dhcp_server.dhcp_server_model import DhcpServer, Section

class DhcpServerParser():

    def parse_dhcp_server_configuration(self, json_dhcp_server_params):

        default_lease_time = None
        if 'defaultLeaseTime' in json_dhcp_server_params:
            default_lease_time = self.parse_default_lease_time(json_dhcp_server_params)

        max_lease_time = None
        if 'maxLeaseTime' in json_dhcp_server_params:
            max_lease_time = self.parse_max_lease_time(json_dhcp_server_params)

        subnet = None
        if 'subnet' in json_dhcp_server_params:
            subnet = self.parse_subnet(json_dhcp_server_params)

        subnet_mask = None
        if 'subnetMask' in json_dhcp_server_params:
            subnet_mask = self.parse_subnet_mask(json_dhcp_server_params)

        router = None
        if 'router' in json_dhcp_server_params:
            router = self.parse_router(json_dhcp_server_params)

        dns_primary_server = None
        if 'dnsPrimaryServer' in json_dhcp_server_params:
            dns_primary_server = self.parse_dns_primary_server(json_dhcp_server_params)

        dns_secondary_server = None
        if 'dnsSecondaryServer' in json_dhcp_server_params:
            dns_secondary_server = self.parse_dns_secondary_server(json_dhcp_server_params)

        dns_domain_name = None
        if 'dnsDomainName' in json_dhcp_server_params:
            dns_domain_name = self.parse_dns_domain_name(json_dhcp_server_params)

        sections = []
        if 'sections' in json_dhcp_server_params:
            sections = self.parse_sections(json_dhcp_server_params['sections'])

        return DhcpServer(default_lease_time,
                          max_lease_time,
                          subnet,
                          subnet_mask,
                          router,
                          dns_primary_server,
                          dns_secondary_server,
                          dns_domain_name,
                          sections)

    def parse_default_lease_time(self, json_dhcp_server_params):
        return json_dhcp_server_params['defaultLeaseTime']

    def parse_max_lease_time(self, json_dhcp_server_params):
        return json_dhcp_server_params['maxLeaseTime']

    def parse_subnet(self, json_dhcp_server_params):
        return json_dhcp_server_params['subnet']

    def parse_subnet_mask(self, json_dhcp_server_params):
        return json_dhcp_server_params['subnetMask']

    def parse_router(self, json_dhcp_server_params):
        return json_dhcp_server_params['router']

    def parse_dns_primary_server(self, json_dhcp_server_params):
        return json_dhcp_server_params['dnsPrimaryServer']

    def parse_dns_secondary_server(self, json_dhcp_server_params):
        return json_dhcp_server_params['dnsSecondaryServer']

    def parse_dns_domain_name(self, json_dhcp_server_params):
        return json_dhcp_server_params['dnsDomainName']

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


    def get_dhcp_server_configuration_dict(self, dhcp_server):

        dhcp_server_dict = {}

        if dhcp_server.default_lease_time is not None:
            dhcp_server_dict['defaultLeaseTime'] = dhcp_server.default_lease_time

        if dhcp_server.max_lease_time is not None:
            dhcp_server_dict['maxLeaseTime'] = dhcp_server.max_lease_time

        if dhcp_server.subnet is not None:
            dhcp_server_dict['subnet'] = dhcp_server.subnet

        if dhcp_server.subnet_mask is not None:
            dhcp_server_dict['subnetMask'] = dhcp_server.subnet_mask

        if dhcp_server.router is not None:
            dhcp_server_dict['router'] = dhcp_server.router

        if dhcp_server.dns_primary_server is not None:
            dhcp_server_dict['dnsPrimaryServer'] = dhcp_server.dns_primary_server

        if dhcp_server.dns_secondary_server is not None:
            dhcp_server_dict['dnsSecondaryServer'] = dhcp_server.dns_secondary_server

        if dhcp_server.dns_domain_name is not None:
            dhcp_server_dict['dnsDomainName'] = dhcp_server.dns_domain_name

        sections_dict = []
        section_dict = {}
        for section in dhcp_server.sections:
            section_dict = self.get_dhcp_server_configuration_section_dict(section)
            sections_dict.append(section_dict)
        dhcp_server_dict['sections'] = sections_dict

        return dhcp_server_dict

    def get_dhcp_server_configuration_section_dict(self, section):
        section_dict = {}
        if section.start_ip is not None:
            section_dict['sectionStartIp'] = section.start_ip
        if section.end_ip is not None:
            section_dict['sectionEndIp'] = section.end_ip
        return section_dict


