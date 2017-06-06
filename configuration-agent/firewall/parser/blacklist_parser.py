import logging

class BlacklistParser():

    # it receives the json block that describe the blacklist
    # and returns an array of url objects
    def parse_blacklist(self, json_blacklist):
        blacklist = []
        for json_url in json_blacklist:
            url = self.parse_url(json_url)
            blacklist.append(url)

        return blacklist

    def parse_url(self, json_url):
        return json_url['url']


    # Give a blacklist url it returns a dictionary
    def get_url_dict(self, url):
        url_dict = {}
        url_dict['url'] = url
        return url_dict