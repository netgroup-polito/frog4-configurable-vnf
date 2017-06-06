from common.utils import Bash

import iptc
import logging

class WhitelistService():

    # configure a whitelist url
    def configure_url(self, url):
        Bash('iptables -I FORWARD -s ' + url.name + ' -j ACCEPT -m comment --comment=whitelist:' + url.name)
        Bash('iptables -I FORWARD -d ' + url.name + ' -j ACCEPT -m comment --comment=whitelist:' + url.name)

    # return all current whitelist
    def get_whitelist(self):
        whitelist = []
        table = iptc.Table(iptc.Table.FILTER)
        table.refresh()
        for chain in table.chains:
            for rule in chain.rules:
                for match in rule.matches:
                    if match.name == "comment":
                        tmp = match.comment.split(':')
                        if tmp[0] == "whitelist":
                            url = tmp[1]
                            whitelist.append(url)
        # set() removes duplicate objects
        return set(whitelist)

    # return a specific whitelist url
    def get_url(self, url):
        whitelist = self.get_whitelist()
        for curr_url in whitelist:
            if curr_url == url:
                return url
        return None


    def delete_whitelist(self):
        pass

    def delete_url(self, url):
        Bash('iptables -D FORWARD -s ' + url.name + ' -j ACCEPT -m comment --comment=whitelist:' + url.name)
        Bash('iptables -D FORWARD -d ' + url.name + ' -j ACCEPT -m comment --comment=whitelist:' + url.name)


