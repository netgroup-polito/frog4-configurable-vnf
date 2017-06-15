from common.utils import Bash

import iptc
import logging

class BlacklistService():

    # configure a blacklist url
    def configure_url(self, url):
        Bash('iptables -I FORWARD -s ' + url.name + ' -j DROP -m comment --comment=blacklist:' + url.name)
        Bash('iptables -I FORWARD -d ' + url.name + ' -j DROP -m comment --comment=blacklist:' + url.name)

    # return all current blacklist
    def get_blacklist(self):
        blacklist = []
        table = iptc.Table(iptc.Table.FILTER)
        table.refresh()
        for chain in table.chains:
            for rule in chain.rules:
                for match in rule.matches:
                    if match.name == "comment":
                        tmp = match.comment.split(':')
                        if tmp[0] == "blacklist":
                            url = name=tmp[1]
                            blacklist.append(url)
        #set() removes duplicate objects
        return set(blacklist)

    # return a specific blacklist url
    def get_url(self, url):
        blacklist = self.get_blacklist()
        for curr_url in blacklist:
            if curr_url == url:
                return url
        return None


    def delete_blacklist(self):
        pass

    def delete_url(self, url):
        Bash('iptables -D FORWARD -s ' + url.name + ' -j DROP -m comment --comment=blacklist:' + url.name)
        Bash('iptables -D FORWARD -d ' + url.name + ' -j DROP -m comment --comment=blacklist:' + url.name)


