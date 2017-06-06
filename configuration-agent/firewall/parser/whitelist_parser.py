import logging

class WhitelistParser():

    # it receives the json block that describe the whitelist
    # and returns an array of url objects
    def parse_whitelist(self, json_whitelist):
        whitelist = []
        for json_url in json_whitelist:
            url = self.parse_url(json_url)
            whitelist.append(url)

        return whitelist

    def parse_url(self, json_url):
        return json_url['url']


    # Give a whitelist url it returns a dictionary
    def get_url_dict(self, url):
        url_dict = {}
        url_dict['url'] = url
        return url_dict