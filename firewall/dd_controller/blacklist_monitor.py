from firewall.dd_controller.element import Element
from firewall.controller.blacklist_controller import BlacklistController

from common.constants import Constants
from config_instance import ConfigurationInstance
from threading import Thread

import logging
import time

class BlacklistMonitor():

    def __init__(self, dd_controller, curr_blacklist):
        self.EVENT_ADD = Constants.EVENT_ADD
        self.EVENT_UPDATE = Constants.EVENT_UPDATE
        self.EVENT_DELETE = Constants.EVENT_DELETE

        ######################### YANG CONSTANTS #########################
        self.SILENT = Constants.ADVERTISE_SILENT
        self.ON_CHANGE = Constants.ADVERTISE_ON_CHANGE
        self.PERIODIC = Constants.ADVERTISE_PERIODIC

        self.url_blacklist = "config-firewall:firewall/blacklist"
        self.url_name = "/url"

        self.elements = {}
        self.elements['url'] = Element(advertise=self.ON_CHANGE)
        ##################################################################

        self.periods = []
        for key, element in self.elements.items():
            if element.advertise == self.PERIODIC:
                element.period = element.period / 1000
                if element.period not in self.periods:
                    self.periods.append(element.period)

        self.on_change_interval = ConfigurationInstance.get_on_change_interval(self)
        logging.debug("on_change_interval: " + str(self.on_change_interval))

        self.blacklist_old = curr_blacklist
        print("blacklist_old: " + str(len(self.blacklist_old)))
        self.blacklist_new = []
        self.blacklist_updated = []
        self.blacklist_removed = []

        self.ddController = dd_controller
        self.blacklistController = BlacklistController()

    def start_monitoring(self):
        logging.debug("Blacklist monitoring started!")

        for period in self.periods:
            Thread(target=self._timer_periodic_callback, args=([period])).start()

        while True:

            self._get_new_blacklist()

            # print("blacklist_new: " + str(len(self.blacklist_new)))
            if len(self.blacklist_new) > 0:
                for url in self.blacklist_new:
                    id = url
                    self._publish_policy_leafs_on_change(id, url, self.EVENT_ADD)
                self.blacklist_new = []

            # print("blacklist_removed: " + str(len(self.blacklist_removed)))
            if len(self.blacklist_removed) > 0:
                for url in self.blacklist_removed:
                    id = url
                    self._publish_policy_leafs_on_change(id, url, self.EVENT_DELETE)
                self.blacklist_removed = []

            # print("blacklist_updated: " + str(len(self.blacklist_updated)))
            if len(self.blacklist_updated) > 0:
                for blacklist_map in self.blacklist_updated:
                    old_url = blacklist_map['old']
                    new_url = blacklist_map['new']
                    url_diff = self._find_diff(old_url, new_url)
                    logging.debug(url_diff.__str__())
                    id = new_url
                    self._publish_policy_leafs_on_change(id, url_diff, self.EVENT_UPDATE)
                self.blacklist_updated = []

            time.sleep(self.on_change_interval)

    def _get_new_blacklist(self):
        curr_blacklist = self.blacklistController.get_blacklist()
        blacklist_map = {}
        # Check new or modified blacklist_url
        for url in curr_blacklist:
            # get the old blacklist_url whose url is the same of the new url
            old_url = next((x for x in self.blacklist_old if x == url), None)
            if old_url is None:
                self.blacklist_new.append(url)
            else:
                if not url.__eq__(old_url):
                    blacklist_map['old'] = old_url
                    blacklist_map['new'] = url
                    self.blacklist_updated.append(blacklist_map)
        # Check if a blacklist_url was removed
        for old_url in self.blacklist_old:
            # get the old blacklist_url whose url is the same of the new url
            url = next((x for x in curr_blacklist if x == old_url), None)
            if url is None:
                self.blacklist_removed.append(old_url)
        self.blacklist_old = curr_blacklist

    def _find_diff(self, old_policy, new_policy):
        return new_policy

    def _publish_policy_leafs_on_change(self, id, blacklist_url, method):

        if self.elements['url'].advertise == self.ON_CHANGE:
            self._publish_blacklist_url(id, blacklist_url, method)

    def _publish_policy_leafs_periodic(self, blacklist_url, period):

        id = blacklist_url

        if self.elements['url'].advertise == self.PERIODIC and self.elements['url'].period == period:
            self._publish_blacklist_url(id, blacklist_url)

    def _timer_periodic_callback(self, period):

        while True:

            time.sleep(period)

            logging.debug("timer callback, period:" + str(period))
            curr_blacklist = self.blacklistController.get_blacklist()
            for url in curr_blacklist:
                self._publish_blacklist_url(url, period)

    ################### Private publish functions ###################
    def _publish_blacklist_url(self, id, data, method=None):
        url = self.url_blacklist + "/" + id + self.url_name
        self.ddController.publish_on_bus(url, method, data)