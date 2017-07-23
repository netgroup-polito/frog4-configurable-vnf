from components.dhcp.dhcp_server.dhcp_server_service import DhcpServerService
from common.config_instance import ConfigurationInstance

class DhcpServerController():

    def __init__(self):
        self.dhcpServerService = DhcpServerService()
        self.nf_type = ConfigurationInstance.get_nf_type(self)

    def configure_dhcp_server(self, dhcp_server):
        if self.nf_type == "docker" or self.nf_type == "vm":
            self.dhcpServerService.configure_dhcp_server(dhcp_server)

    def add_section(self, section):
        current_dhcp_server_configuration = self.get_dhcp_server_configuration()
        sections = current_dhcp_server_configuration.sections
        sections.append(section)
        self.configure_dhcp_server(current_dhcp_server_configuration)
        return current_dhcp_server_configuration

    def update_default_lease_time(self, default_lease_time):
        current_dhcp_server_configuration = self.get_dhcp_server_configuration()
        current_dhcp_server_configuration.default_lease_time = default_lease_time
        self.configure_dhcp_server(current_dhcp_server_configuration)
        return current_dhcp_server_configuration

    def update_max_lease_time(self, max_lease_time):
        current_dhcp_server_configuration = self.get_dhcp_server_configuration()
        current_dhcp_server_configuration.max_lease_time = max_lease_time
        self.configure_dhcp_server(current_dhcp_server_configuration)
        return current_dhcp_server_configuration

    def update_subnet(self, subnet):
        current_dhcp_server_configuration = self.get_dhcp_server_configuration()
        current_dhcp_server_configuration.subnet = subnet
        self.configure_dhcp_server(current_dhcp_server_configuration)
        return current_dhcp_server_configuration

    def update_subnet_mask(self, subnet_mask):
        current_dhcp_server_configuration = self.get_dhcp_server_configuration()
        current_dhcp_server_configuration.subnet_mask = subnet_mask
        self.configure_dhcp_server(current_dhcp_server_configuration)
        return current_dhcp_server_configuration

    def update_router(self, router):
        current_dhcp_server_configuration = self.get_dhcp_server_configuration()
        current_dhcp_server_configuration.router = router
        self.configure_dhcp_server(current_dhcp_server_configuration)
        return current_dhcp_server_configuration

    def update_dns_primary_server(self, dns_primary_server):
        current_dhcp_server_configuration = self.get_dhcp_server_configuration()
        current_dhcp_server_configuration.dns_primary_server = dns_primary_server
        self.configure_dhcp_server(current_dhcp_server_configuration)
        return current_dhcp_server_configuration

    def update_dns_secondary_server(self, dns_secondary_server):
        current_dhcp_server_configuration = self.get_dhcp_server_configuration()
        current_dhcp_server_configuration.dns_secondary_server = dns_secondary_server
        self.configure_dhcp_server(current_dhcp_server_configuration)
        return current_dhcp_server_configuration

    def update_domain_name(self, dns_domain_name):
        current_dhcp_server_configuration = self.get_dhcp_server_configuration()
        current_dhcp_server_configuration.dns_domain_name = dns_domain_name
        self.configure_dhcp_server(current_dhcp_server_configuration)
        return current_dhcp_server_configuration

    def update_section(self, section_start_ip, section):
        current_dhcp_server_configuration = self.get_dhcp_server_configuration()
        sections = current_dhcp_server_configuration.sections
        for curr_section in sections:
            if curr_section.start_ip == section_start_ip:
                curr_section = section
        self.configure_dhcp_server(current_dhcp_server_configuration)
        return current_dhcp_server_configuration

    def update_section_start_ip(self, section_start_ip, start_ip):
        current_dhcp_server_configuration = self.get_dhcp_server_configuration()
        sections = current_dhcp_server_configuration.sections
        for section in sections:
            if section.start_ip == section_start_ip:
                section.start_ip = start_ip
        self.configure_dhcp_server(current_dhcp_server_configuration)
        return current_dhcp_server_configuration

    def update_section_end_ip(self, section_start_ip, end_ip):
        current_dhcp_server_configuration = self.get_dhcp_server_configuration()
        sections = current_dhcp_server_configuration.sections
        for section in sections:
            if section.start_ip == section_start_ip:
                section.end_ip = end_ip
        self.configure_dhcp_server(current_dhcp_server_configuration)
        return current_dhcp_server_configuration

    def configuration_exists(self):
        try:
            self.dhcpServerService.get_dhcp_server_configuration()
            return True
        except Exception as e:
            return False

    def get_dhcp_server_configuration(self):
        if self.nf_type == "docker" or self.nf_type == "vm":
            return self.dhcpServerService.get_dhcp_server_configuration()

    def get_dhcp_server_configuration_default_lease_time(self):
        dhcp_server_configuration = self.get_dhcp_server_configuration()
        return dhcp_server_configuration.default_lease_time

    def get_dhcp_server_configuration_max_lease_time(self):
        dhcp_server_configuration = self.get_dhcp_server_configuration()
        return dhcp_server_configuration.max_lease_time

    def get_dhcp_server_configuration_subnet(self):
        dhcp_server_configuration = self.get_dhcp_server_configuration()
        return dhcp_server_configuration.subnet

    def get_dhcp_server_configuration_subnet_mask(self):
        dhcp_server_configuration = self.get_dhcp_server_configuration()
        return dhcp_server_configuration.subnet_mask

    def get_dhcp_server_configuration_router(self):
        dhcp_server_configuration = self.get_dhcp_server_configuration()
        return dhcp_server_configuration.router

    def get_dhcp_server_configuration_dns_primary_server(self):
        dhcp_server_configuration = self.get_dhcp_server_configuration()
        return dhcp_server_configuration.dns_primary_server

    def get_dhcp_server_configuration_dns_secondary_server(self):
        dhcp_server_configuration = self.get_dhcp_server_configuration()
        return dhcp_server_configuration.dns_secondary_server

    def get_dhcp_server_configuration_dns_domain_name(self):
        dhcp_server_configuration = self.get_dhcp_server_configuration()
        return dhcp_server_configuration.dns_domain_name

    def get_dhcp_server_configuration_sections(self):
        dhcp_server_configuration = self.get_dhcp_server_configuration()
        sections = dhcp_server_configuration.sections
        return sections

    def get_dhcp_server_configuration_section(self, section_start_ip):
        dhcp_server_configuration = self.get_dhcp_server_configuration()
        sections = dhcp_server_configuration.sections
        section_found = None
        for section in sections:
            if section.start_ip == section_start_ip:
                section_found = section
                break
        return section_found

    def get_dhcp_server_configuration_section_start_ip(self, section_start_ip):
        dhcp_server_configuration = self.get_dhcp_server_configuration()
        sections = dhcp_server_configuration.sections
        for section in sections:
            if section.start_ip == section_start_ip:
                return section.start_ip
        return None

    def get_dhcp_server_configuration_section_end_ip(self, section_start_ip):
        dhcp_server_configuration = self.get_dhcp_server_configuration()
        sections = dhcp_server_configuration.sections
        for section in sections:
            if section.start_ip == section_start_ip:
                return section.end_ip
        return None
