class BlacklistParser():

    def parse_blacklist(self, json_firewall_configuration):
        return json_firewall_configuration['blacklist']

    def parse_url(self, json_url):
        return json_url['url']

    # Give a blacklist url it returns a dictionary
    def get_url_dict(self, url):
        url_dict = {}
        url_dict['url'] = url
        return url_dict