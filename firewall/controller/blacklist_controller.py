from firewall.service.blacklist_service import BlacklistService
from config_instance import ConfigurationInstance

class BlacklistController():

    def __init__(self):
        self.blacklistService = BlacklistService()
        self.nf_type = ConfigurationInstance.get_nf_type(self)

    def configure_url(self, url):
        if self.nf_type=="docker" or self.nf_type=="vm":
            self.blacklistService.configure_url(url)

    def get_blacklist(self):
        if self.nf_type == "docker" or self.nf_type == "vm":
            return self.blacklistService.get_blacklist()

    def get_url(self, url):
        if self.nf_type == "docker" or self.nf_type == "vm":
            return self.blacklistService.get_url(url)

    def delete_blacklist(self):
        pass

    def delete_url(self, url):
        self.blacklistService.delete_url(url)