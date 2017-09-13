from components.firewall.blacklist.blacklist_service import BlacklistService
from common.config_instance import ConfigurationInstance

class BlacklistController():

    def __init__(self):
        self.blacklistService = BlacklistService()
        self.nf_type = ConfigurationInstance().get_nf_type()

    def configure_url(self, url):
        if self.nf_type == "docker" or self.nf_type == "vm":
            self.blacklistService.configure_url(url)

    def get_blacklist(self):
        if self.nf_type == "docker" or self.nf_type == "vm":
            return self.blacklistService.get_blacklist()

    def get_url(self, url):
        if self.nf_type == "docker" or self.nf_type == "vm":
            return self.blacklistService.get_url(url)

    def url_exists(self, url):
        url_found = self.get_url(url)
        if url_found is not None:
            return True
        else:
            return False

    def delete_blacklist(self):
        pass

    def delete_url(self, url):
        self.blacklistService.delete_url(url)