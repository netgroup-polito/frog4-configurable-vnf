import logging

class WhitelistParser():

    def parse_whitelist(self, json_firewall_configuration):
        return json_firewall_configuration['whitelist']

    def parse_url(self, json_url):
        return json_url['url']


    # Give a whitelist url it returns a dictionary
    def get_url_dict(self, url):
        url_dict = {}
        url_dict['url'] = url
        return url_dict