from components.nat.nat_table.nat_table_controller import NatTableController
from components.nat.nat_table.nat_table_parser import NatTableParser
from common.element import Element
from common.constants import Constants
from common.config_instance import ConfigurationInstance
from threading import Thread
import logging
import time

class NatTableMonitor():

    def __init__(self, dd_controller, curr_nat_sessions):
        self.EVENT_ADD = Constants.EVENT_ADD
        self.EVENT_UPDATE = Constants.EVENT_UPDATE
        self.EVENT_DELETE = Constants.EVENT_DELETE

        ######################### YANG CONSTANTS #########################
        self.SILENT = Constants.ADVERTISE_SILENT
        self.ON_CHANGE = Constants.ADVERTISE_ON_CHANGE
        self.PERIODIC = Constants.ADVERTISE_PERIODIC

        self.url_natSession = "config-nat:nat/nat-table/nat-session"

        self.elements = {}
        self.elements['natSession'] = Element(advertise=self.ON_CHANGE)
        ##################################################################

        self.periods = []
        for key, element in self.elements.items():
            if element.advertise == self.PERIODIC:
                element.period = element.period / 1000
                if element.period not in self.periods:
                    self.periods.append(element.period)

        self.on_change_interval = \

            ConfigurationInstance().get_on_change_interval()
        logging.debug("on_change_interval: " + str(self.on_change_interval))

        self.nat_sessions_old = curr_nat_sessions
        print("nat_sessions_old: " + str(len(self.nat_sessions_old)))
        self.nat_sessions_new = []
        self.nat_sessions_removed = []

        self.ddController = dd_controller
        self.natTableController = NatTableController()
        self.natTableParser = NatTableParser()

    def start_monitoring(self):
        logging.debug("Nat table monitoring started!")

        for period in self.periods:
            Thread(target=self._timer_periodic_callback, args=([period])).start()

        while True:

            self._get_new_natTable()

            # print("nat_sessions_new: " + str(len(self.nat_sessions_new)))
            if len(self.nat_sessions_new) > 0:
                for nat_session in self.nat_sessions_new:
                    self._publish_natSession_leafs_on_change(nat_session, self.EVENT_ADD)
                self.nat_sessions_new = []

            # print("nat_sessions_removed: " + str(len(self.nat_sessions_removed)))
            if len(self.nat_sessions_removed) > 0:
                for nat_session in self.nat_sessions_removed:
                    self._publish_natSession_leafs_on_change(nat_session, self.EVENT_DELETE)
                self.nat_sessions_removed = []

            time.sleep(self.on_change_interval)

    def _get_new_natTable(self):
        curr_nat_sessions = self.natTableController.get_nat_table()
        # Check new or modified nat session
        for nat_session in curr_nat_sessions:
            # for each new curr_session, check if existed before
            old_nat_session = next((x for x in self.nat_sessions_old if (x.__eq__(nat_session))), None)
            if old_nat_session is None:
                self.nat_sessions_new.append(nat_session)
        # Check if a nat_session was removed
        for old_nat_session in self.nat_sessions_old:
            # for each old nat_session check if still exists
            nat_session = next((x for x in curr_nat_sessions if (x.__eq__(old_nat_session))), None)
            if nat_session is None:
                self.nat_sessions_removed.append(old_nat_session)
        self.nat_sessions_old = curr_nat_sessions

    def _timer_periodic_callback(self, period):
        while True:

            time.sleep(period)

            logging.debug("timer callback, period:" + str(period))
            curr_nat_sessions = self.natTableController.get_nat_table()
            for nat_session in curr_nat_sessions:
                self._publish_natSession_leafs_periodic(nat_session, period)

    def _publish_natSession_leafs_on_change(self, nat_session, method):
        if self.elements['natTable'].advertise == self.ON_CHANGE:
            self._publish_natSession(nat_session, method)

    def _publish_natSession_leafs_periodic(self, nat_session, period):
        if self.elements['natTable'].advertise == self.PERIODIC and self.elements['policy'].period == period:
            self._publish_natSession(nat_session)

    ################### Private publish functions ###################
    def _publish_natSession(self, data, method=None):
        natSession_dict = self.natTableParser.get_nat_session_dict(data)
        url = self.url_natSession
        self.ddController.publish_on_bus(url, method, natSession_dict)

