from nat.service.floating_ip_service import FloatingIpService
from config_instance import ConfigurationInstance

class FloatingIpController():

    def __init__(self):
        self.floatingIpService = FloatingIpService()
        self.nf_type = ConfigurationInstance.get_nf_type(self)

    def configure_floating_ip(self, floating_ip, wan_interface):
        if self.nf_type == "docker" or self.nf_type == "vm":
            self.floatingIpService.configure_floating_ip(floating_ip, wan_interface)

    def get_all_floating_ip(self):
        if self.nf_type == "docker" or self.nf_type == "vm":
            return self.floatingIpService.get_all_floating_ip()

    def get_floating_ip(self, public_address):
        if self.nf_type == "docker" or self.nf_type == "vm":
            return self.floatingIpService.get_floating_ip(public_address)

    def delete_floating_ip(self, public_address):
        if self.nf_type == "docker" or self.nf_type == "vm":
            return self.floatingIpService.delete_floating_ip(public_address)

    def floating_ip_exists(self, public_address):
        if self.get_floating_ip(public_address) is None:
            return False
        else:
            return True


