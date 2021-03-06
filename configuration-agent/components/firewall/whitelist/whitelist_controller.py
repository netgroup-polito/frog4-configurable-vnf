from components.firewall.whitelist.whitelist_service import WhitelistService
from common.config_instance import ConfigurationInstance

class WhitelistController():

    def __init__(self):
        self.whitelistService = WhitelistService()
        self.nf_type = ConfigurationInstance().get_nf_type()

    def configure_url(self, url):
        if self.nf_type == "docker" or self.nf_type == "vm":
            self.whitelistService.configure_url(url)

    def get_whitelist(self):
        if self.nf_type == "docker" or self.nf_type == "vm":
            return self.whitelistService.get_whitelist()

    def get_url(self, url):
        if self.nf_type == "docker" or self.nf_type == "vm":
            return self.whitelistService.get_url(url)

    def url_exists(self, url):
        url_found = self.get_url(url)
        if url_found is not None:
            return True
        else:
            return False

    def delete_whitelist(self):
        pass

    def delete_url(self, url):
        self.whitelistService.delete_url(url)