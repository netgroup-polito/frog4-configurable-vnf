from dhcp.controller.dhcp_server_controller import DhcpServerController
from dhcp.parser.dhcp_server_parser import DhcpServerParser
from dhcp.model.client import Client
from common.constants import Constants

from dhcp.dd_controller.element import Element
from config_instance import ConfigurationInstance
from threading import Thread

import logging
import time


class DhcpClientsMonitor():

    def __init__(self, dd_controller, curr_dhcp_clients):

        self.EVENT_ADD = Constants.EVENT_ADD
        self.EVENT_UPDATE = Constants.EVENT_UPDATE
        self.EVENT_DELETE = Constants.EVENT_DELETE

        ######################### YANG CONSTANTS #########################
        self.SILENT = Constants.ADVERTISE_SILENT
        self.ON_CHANGE = Constants.ADVERTISE_ON_CHANGE
        self.PERIODIC = Constants.ADVERTISE_PERIODIC

        self.url_clients = "config-dhcp-server:server/clients"
        self.url_macAddress = "/mac_address"
        self.url_ipAddress = "/ip_address"
        self.url_hostname = "/hostname"
        self.url_validUntil = "/valid_until"

        self.elements = {}
        self.elements['client'] = Element(advertise=self.SILENT)
        self.elements['macAddress'] = Element(advertise=self.ON_CHANGE)
        self.elements['ipAddress'] = Element(advertise=self.ON_CHANGE)
        self.elements['hostname'] = Element(advertise=self.ON_CHANGE)
        self.elements['validUntil'] = Element(advertise=self.ON_CHANGE)
        ##################################################################

        self.periods = []
        for key, element in self.elements.items():
            if element.advertise == self.PERIODIC:
                element.period = element.period / 1000
                if element.period not in self.periods:
                    self.periods.append(element.period)

        self.on_change_interval = ConfigurationInstance.get_on_change_interval(self)
        logging.debug("on_change_interval: " + str(self.on_change_interval))

        self.dhcp_clients_old = curr_dhcp_clients
        print("dhcp_clients_old: " + str(len(self.dhcp_clients_old)))
        self.dhcp_clients_new = []
        self.dhcp_clients_updated = []
        self.dhcp_clients_removed = []

        self.ddController = dd_controller
        self.dhcpServerController = DhcpServerController()
        self.dhcpServerParser = DhcpServerParser()

    def start_monitoring(self):

        logging.debug("Dhcp clients monitoring started!")

        for period in self.periods:
            Thread(target=self._timer_periodic_callback, args=([period])).start()

        while True:

            self._get_new_dhcp_clients()

            #print("clients_new: " + str(len(self.dhcp_clients_new)))
            if len(self.dhcp_clients_new) > 0:
                for client in self.dhcp_clients_new:
                    id = client.mac_address
                    self._publish_dhcpClient_leafs_on_change(id, client, self.EVENT_ADD)
                self.dhcp_clients_new = []

            #print("clients_removed: " + str(len(self.dhcp_clients_removed)))
            if len(self.dhcp_clients_removed) > 0:
                for client in self.dhcp_clients_removed:
                    print(client.__str__())
                    id = client.mac_address
                    self._publish_dhcpClient_leafs_on_change(id, client, self.EVENT_DELETE)
                self.dhcp_clients_removed = []

            #print("clients_updated: " + str(len(self.dhcp_clients_updated)))
            if len(self.dhcp_clients_updated) > 0:
                for client_map in self.dhcp_clients_updated:
                    old_client = client_map['old']
                    new_client = client_map['new']
                    client_diff = self._find_diff(old_client, new_client)
                    logging.debug(client_diff.__str__())
                    id = new_client.mac_address
                    self._publish_dhcpClient_leafs_on_change(id, client_diff, self.EVENT_UPDATE)
                self.dhcp_clients_updated = []

            time.sleep(self.on_change_interval)

    def _get_new_dhcp_clients(self):
        curr_clients = self.dhcpServerController.get_clients()
        client_map = {}
        # Check new or modified dhcp clients
        for client in curr_clients:
            # get the old client whose mac_address is the same of the new client
            old_client = next((x for x in self.dhcp_clients_old if x.mac_address == client.mac_address), None)
            if old_client is None:
                self.dhcp_clients_new.append(client)
            else:
                if not client.__eq__(old_client):
                    client_map['old'] = old_client
                    client_map['new'] = client
                    self.dhcp_clients_updated.append(client_map)
        # Check if a client was removed
        for old_client in self.dhcp_clients_old:
            # get the old client whose mac_address is the same of the new client
            client = next((x for x in curr_clients if x.mac_address == old_client.mac_address), None)
            if client is None:
                self.dhcp_clients_removed.append(old_client)
        self.dhcp_clients_old = curr_clients

    def _find_diff(self, old_client, new_client):

        ip_address = None
        if not old_client.ip_address.__eq__(new_client.ip_address):
            ip_address = new_client.ip_address

        hostname = None
        if not old_client.hostname.__eq__(new_client.hostname):
            hostname = new_client.hostname

        valid_until = None
        if not old_client.valid_until.__eq__(new_client.valid_until):
            valid_until = new_client.valid_until

        client = Client(mac_address=None,
                        ip_address=ip_address,
                        hostname=hostname,
                        valid_until=valid_until)

        return client

    def _timer_periodic_callback(self, period):

        while True:
            time.sleep(period)

            logging.debug("timer callback, period:" + str(period))
            curr_clients = self.dhcpServerController.get_clients()
            for client in curr_clients:
                self._publish_dhcpClient_leafs_periodic(client, period)

    def _publish_dhcpClient_leafs_periodic(self, client, period):

        id = client.mac_address

        if self.elements['client'].advertise == self.PERIODIC and self.elements['client'].period == period:
            self._publish_client(id, client)

        if client.mac_address is not None:
            if self.elements['macAddress'].advertise == self.PERIODIC and self.elements['macAddress'].period == period:
                self._publish_client_macAddress(id, client.mac_address)

        if client.ip_address is not None:
            if self.elements['ipAddress'].advertise == self.PERIODIC and self.elements['ipAddress'].period == period:
                self._publish_client_ipAddress(id, client.ip_address)

        if client.hostname is not None:
            if self.elements['hostname'].advertise == self.PERIODIC and self.elements['hostname'].period == period:
                self._publish_client_hostname(id, client.hostname)

        if client.valid_until is not None:
            if self.elements['validUntil'].advertise == self.PERIODIC and self.elements['validUntil'].period == period:
                self._publish_client_validUntil(id, client.valid_until)

    def _publish_dhcpClient_leafs_on_change(self, id, client, method):

        if self.elements['client'].advertise == self.ON_CHANGE:
            self._publish_client(id, client, method)

        if client.mac_address is not None:
            if self.elements['macAddress'].advertise == self.ON_CHANGE:
                self._publish_client_macAddress(id, client.mac_address, method)

        if client.ip_address is not None:
            if self.elements['ipAddress'].advertise == self.ON_CHANGE:
                self._publish_client_ipAddress(id, client.ip_address, method)

        if client.hostname is not None:
            if self.elements['hostname'].advertise == self.ON_CHANGE:
                self._publish_client_hostname(id, client.hostname, method)

        if client.valid_until is not None:
            if self.elements['validUntil'].advertise == self.ON_CHANGE:
                self._publish_client_validUntil(id, client.valid_until, method)


    ################### Private publish functions ###################
    def _publish_client(self, id, data, method=None):
        client_dict = self.dhcpServerParser.get_client_dict(data)
        url = self.url_clients + "/" + id
        self.ddController.publish_on_bus(url, method, client_dict)

    def _publish_client_macAddress(self, id, data, method=None):
        url = self.url_clients + "/" + id + self.url_macAddress
        self.ddController.publish_on_bus(url, method, data)

    def _publish_client_ipAddress(self, id, data, method=None):
        url = self.url_clients + "/" + id + self.url_ipAddress
        self.ddController.publish_on_bus(url, method, data)

    def _publish_client_hostname(self, id, data, method=None):
        url = self.url_clients + "/" + id + self.url_hostname
        self.ddController.publish_on_bus(url, method, data)

    def _publish_client_validUntil(self, id, data, method=None):
        url = self.url_clients + "/" + id + self.url_validUntil
        self.ddController.publish_on_bus(url, method, data)
