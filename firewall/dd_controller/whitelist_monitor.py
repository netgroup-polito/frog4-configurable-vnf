from firewall.dd_controller.element import Element
from firewall.controller.whitelist_controller import WhitelistController

from common.constants import Constants
from config_instance import ConfigurationInstance
from threading import Thread

import logging
import time


class WhitelistMonitor():
    def __init__(self, dd_controller, curr_whitelist):
        self.EVENT_ADD = Constants.EVENT_ADD
        self.EVENT_UPDATE = Constants.EVENT_UPDATE
        self.EVENT_DELETE = Constants.EVENT_DELETE

        ######################### YANG CONSTANTS #########################
        self.SILENT = Constants.ADVERTISE_SILENT
        self.ON_CHANGE = Constants.ADVERTISE_ON_CHANGE
        self.PERIODIC = Constants.ADVERTISE_PERIODIC

        self.url_whitelist = "config-firewall:firewall/whitelist"
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

        self.whitelist_old = curr_whitelist
        print("whitelist_old: " + str(len(self.whitelist_old)))
        self.whitelist_new = []
        self.whitelist_updated = []
        self.whitelist_removed = []

        self.ddController = dd_controller
        self.whitelistController = WhitelistController()

    def start_monitoring(self):
        logging.debug("Whitelist monitoring started!")

        for period in self.periods:
            Thread(target=self._timer_periodic_callback, args=([period])).start()

        while True:

            self._get_new_whitelist()

            # print("whitelist_new: " + str(len(self.whitelist_new)))
            if len(self.whitelist_new) > 0:
                for url in self.whitelist_new:
                    id = url
                    self._publish_policy_leafs_on_change(id, url, self.EVENT_ADD)
                self.whitelist_new = []

            # print("whitelist_removed: " + str(len(self.whitelist_removed)))
            if len(self.whitelist_removed) > 0:
                for url in self.whitelist_removed:
                    id = url
                    self._publish_policy_leafs_on_change(id, url, self.EVENT_DELETE)
                self.whitelist_removed = []

            # print("whitelist_updated: " + str(len(self.whitelist_updated)))
            if len(self.whitelist_updated) > 0:
                for whitelist_map in self.whitelist_updated:
                    old_url = whitelist_map['old']
                    new_url = whitelist_map['new']
                    url_diff = self._find_diff(old_url, new_url)
                    logging.debug(url_diff.__str__())
                    id = new_url
                    self._publish_policy_leafs_on_change(id, url_diff, self.EVENT_UPDATE)
                self.whitelist_updated = []

            time.sleep(self.on_change_interval)

    def _get_new_whitelist(self):
        curr_whitelist = self.whitelistController.get_whitelist()
        whitelist_map = {}
        # Check new or modified whitelist_url
        for url in curr_whitelist:
            # get the old whitelist_url whose url is the same of the new url
            old_url = next((x for x in self.whitelist_old if x == url), None)
            if old_url is None:
                self.whitelist_new.append(url)
            else:
                if not url.__eq__(old_url):
                    whitelist_map['old'] = old_url
                    whitelist_map['new'] = url
                    self.whitelist_updated.append(whitelist_map)
        # Check if a whitelist_url was removed
        for old_url in self.whitelist_old:
            # get the old whitelist_url whose url is the same of the new url
            url = next((x for x in curr_whitelist if x == old_url), None)
            if url is None:
                self.whitelist_removed.append(old_url)
        self.whitelist_old = curr_whitelist

    def _find_diff(self, old_policy, new_policy):
        return new_policy

    def _publish_policy_leafs_on_change(self, id, whitelist_url, method):

        if self.elements['url'].advertise == self.ON_CHANGE:
            self._publish_whitelist_url(id, whitelist_url, method)

    def _publish_policy_leafs_periodic(self, whitelist_url, period):

        id = whitelist_url

        if self.elements['url'].advertise == self.PERIODIC and self.elements['url'].period == period:
            self._publish_whitelist_url(id, whitelist_url)

    def _timer_periodic_callback(self, period):

        while True:

            time.sleep(period)

            logging.debug("timer callback, period:" + str(period))
            curr_whitelist = self.whitelistController.get_whitelist()
            for url in curr_whitelist:
                self._publish_whitelist_url(url, period)

    ################### Private publish functions ###################
    def _publish_whitelist_url(self, id, data, method=None):
        url = self.url_whitelist + "/" + id + self.url_name
        self.ddController.publish_on_bus(url, method, data)