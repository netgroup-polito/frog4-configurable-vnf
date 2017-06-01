from dhcp.controller.dhcp_server_controller import DhcpServerController
from dhcp.parser.dhcp_server_parser import DhcpServerParser
from file_monitor import FileMonitor
from common.constants import Constants

from dhcp.dd_controller.element import Element
from config_instance import ConfigurationInstance
from threading import Thread

import logging
import time


class DhcpServerMonitor():

    def __init__(self, dd_controller, curr_dhcpServer_configuration):

        self.EVENT_ADD = Constants.EVENT_ADD
        self.EVENT_UPDATE = Constants.EVENT_UPDATE
        self.EVENT_DELETE = Constants.EVENT_DELETE

        ######################### YANG CONSTANTS #########################
        self.SILENT = Constants.ADVERTISE_SILENT
        self.ON_CHANGE = Constants.ADVERTISE_ON_CHANGE
        self.PERIODIC = Constants.ADVERTISE_PERIODIC

        self.url_dhcpServerConfiguration = "config-dhcp-server:server/globalIpPool"
        self.url_gateway = self.url_dhcpServerConfiguration + "/gatewayIp"
        self.url_gateway_address = self.url_gateway + "/gatewayAddress"
        self.url_gateway_netmask = self.url_gateway + "/gatewayMask"
        self.url_sections = self.url_dhcpServerConfiguration + "/sections"
        self.url_section_startIP = "/sectionStartIp"
        self.url_section_endIP = "/sectionEndIp"
        self.url_dns = self.url_dhcpServerConfiguration + "/dns"
        self.url_dns_primaryServer = self.url_dns + "/primaryServer"
        self.url_dns_secondaryServer = self.url_dns + "/secondaryServer"
        self.url_dns_domainName = self.url_dns + "/domainName"
        self.url_defaultLeaseTime = self.url_dhcpServerConfiguration + "/defaultLeaseTime"
        self.url_maxLeaseTime = self.url_dhcpServerConfiguration + "/maxLeaseTime"

        self.elements = {}
        self.elements['globalIpPool'] = Element(advertise=self.ON_CHANGE)
        self.elements['gateway'] = Element(advertise=self.PERIODIC, period=5000)
        self.elements['gatewayAddress'] = Element(advertise=self.ON_CHANGE)
        self.elements['gatewayNetmask'] = Element(advertise=self.ON_CHANGE)
        self.elements['sections'] = Element(advertise=self.SILENT)
        self.elements['section'] = Element(advertise=self.SILENT)
        self.elements['sectionStartIp'] = Element(advertise=self.SILENT)
        self.elements['sectionEndIp'] = Element(advertise=self.ON_CHANGE)
        self.elements['defaultLeaseTime'] = Element(advertise=self.SILENT)
        self.elements['maxLeaseTime'] = Element(advertise=self.ON_CHANGE)
        self.elements['dns'] = Element(advertise=self.ON_CHANGE)
        self.elements['primaryServer'] = Element(advertise=self.SILENT)
        self.elements['secondaryServer'] = Element(advertise=self.ON_CHANGE)
        self.elements['domainName'] = Element(advertise=self.ON_CHANGE)
        ##################################################################

        self.periods = []
        for key, element in self.elements.items():
            if element.advertise == self.PERIODIC:
                element.period = element.period / 1000
                if element.period not in self.periods:
                    self.periods.append(element.period)

        self.on_change_interval = ConfigurationInstance.get_on_change_interval(self)
        logging.debug("on_change_interval: " + str(self.on_change_interval))

        self.dhcpServerConfig_old = curr_dhcpServer_configuration
        self.dhcpServerConfig_new = None

        self.ddController = dd_controller
        self.dhcpServerController = DhcpServerController()
        self.dhcpServerParser = DhcpServerParser()
        #self.fileMonitor = FileMonitor()

    def start_monitoring(self):

        logging.debug("Dhcp server monitoring started!")

        for period in self.periods:
            Thread(target=self._timer_periodic_callback, args=([period])).start()

        while True:
            
            curr_dhcpServerConfig = self.dhcpServerController.get_dhcp_server_configuration()
            self._publish_dhcpServerConfig_leafs_on_change(self.dhcpServerConfig_old, curr_dhcpServerConfig)
            self.dhcpServerConfig_old = curr_dhcpServerConfig
            
            time.sleep(self.on_change_interval)
        
        """
        file_to_monitor = "/home/giuseppe/Desktop/hello.txt"
        #file_to_monitor = "/etc/dhcp/dhcpd.conf"
        event_type = "modify"
        self.fileMonitor.initialize(file_to_monitor, event_type, self._dhcpServerConfig_on_change_callback)
        self.fileMonitor.start_monitoring()
        """

    def _timer_periodic_callback(self, period):

        while True:

            time.sleep(period)

            logging.debug("timer callback, period:" + str(period))
            curr_dhcpServerConfig = self.dhcpServerController.get_dhcp_server_configuration()
            self._publish_dhcpServerConfig_leafs_periodic(curr_dhcpServerConfig, period)

    def _publish_dhcpServerConfig_leafs_periodic(self, dhcpServerConfig, period):

        if self.elements['globalIpPool'].advertise == self.PERIODIC and self.elements['globalIpPool'].period == period:
            self._publish_dhcpServerConfig(dhcpServerConfig)

        if dhcpServerConfig.gateway is not None:
            if self.elements['gateway'].advertise == self.PERIODIC and self.elements['gateway'].period == period:
                self._publish_dhcpServerConfig_gateway(dhcpServerConfig.gateway)

            if dhcpServerConfig.gateway.address is not None:
                if self.elements['gatewayAddress'].advertise == self.PERIODIC and self.elements['gatewayAddress'].period == period:
                    self._publish_dhcpServerConfig_gateway_address(dhcpServerConfig.gateway.address)

            if dhcpServerConfig.gateway.netmask is not None:
                if self.elements['gatewayNetmask'].advertise == self.PERIODIC and self.elements['gatewayNetmask'].period == period:
                    self._publish_dhcpServerConfig_gateway_netmask(dhcpServerConfig.gateway.netmask)

        if len(dhcpServerConfig.sections) > 0:

            sections = dhcpServerConfig.sections

            if self.elements['sections'].advertise == self.PERIODIC and self.elements['sections'].period == period:
                self._publish_dhcpServerConfig_sections(sections)

            if self.elements['section'].advertise == self.PERIODIC and self.elements['sections'].period == period:
                for section in sections:
                    id = section.start_ip
                    self._publish_dhcpServerConfig_section(id, section)

                    if self.elements['sectionStartIp'].advertise == self.PERIODIC and self.elements['sectionStartIp'].period == period:
                        self._publish_dhcpServerConfig_section_startIP(id, section.start_ip)

                    if self.elements['sectionEndIp'].advertise == self.PERIODIC and self.elements['sectionEndIp'].period == period:
                        self._publish_dhcpServerConfig_section_endIP(id, section.end_ip)

        if dhcpServerConfig.dns is not None:
            if self.elements['dns'].advertise == self.PERIODIC and self.elements['dns'].period == period:
                self._publish_dhcpServerConfig_dns(dhcpServerConfig.dns)

            if dhcpServerConfig.dns.primary_server is not None:
                if self.elements['primaryServer'].advertise == self.PERIODIC and self.elements['primaryServer'].period == period:
                    self._publish_dhcpServerConfig_dns_primaryServer(dhcpServerConfig.dns.primary_server)

            if dhcpServerConfig.dns.secondary_server is not None:
                if self.elements['secondaryServer'].advertise == self.PERIODIC and self.elements['secondaryServer'].period == period:
                    self._publish_dhcpServerConfig_dns_secondaryServer(dhcpServerConfig.dns.secondary_server)

            if dhcpServerConfig.dns.domain_name is not None:
                if self.elements['domainName'].advertise == self.PERIODIC and self.elements['domainName'].period == period:
                    self._publish_dhcpServerConfig_dns_domainName(dhcpServerConfig.dns.domain_name)

        if dhcpServerConfig.default_lease_time is not None:
            if self.elements['defaultLeaseTime'].advertise == self.PERIODIC and self.elements['defaultLeaseTime'].period == period:
                self._publish_dhcpServerConfig_defaultLeaseTime(dhcpServerConfig.default_lease_time)

        if dhcpServerConfig.max_lease_time is not None:
            if self.elements['maxLeaseTime'].advertise == self.PERIODIC and self.elements['maxLeaseTime'].period == period:
                self._publish_dhcpServerConfig_maxLeaseTime(dhcpServerConfig.max_lease_time)

    """
    def _dhcpServerConfig_on_change_callback(self):
        print("/etc/dhcp/dhcpd.conf file changed")
        #curr_dhcpServerConfig = self.dhcpServerController.get_dhcp_server_configuration()
        #self._publish_dhcpServerConfig_leafs_on_change(self.dhcpServerConfig_old, curr_dhcpServerConfig)
        #self.dhcpServerConfig_old = curr_dhcpServerConfig
    """

    def _publish_dhcpServerConfig_leafs_on_change(self, old_dhcpServerConfig, new_dhcpServerConfig):

        if self.elements['globalIpPool'].advertise == self.ON_CHANGE:
            self._check_diff_on_dhcpServerConfig(old_dhcpServerConfig, new_dhcpServerConfig)

        if self.elements['gateway'].advertise == self.ON_CHANGE:
            self._check_diff_on_dhcpServerConfig_gateway(old_dhcpServerConfig.gateway, new_dhcpServerConfig.gateway)

        if self.elements['gatewayAddress'].advertise == self.ON_CHANGE:
            self._check_diff_on_dhcpServerConfig_gateway_address(old_dhcpServerConfig.gateway.address, new_dhcpServerConfig.gateway.address)

        if self.elements['gatewayNetmask'].advertise == self.ON_CHANGE:
            self._check_diff_on_dhcpServerConfig_gateway_netmask(old_dhcpServerConfig.gateway.netmask, new_dhcpServerConfig.gateway.netmask)

        if self.elements['sections'].advertise == self.ON_CHANGE:
            self._check_diff_on_dhcpServerConfig_sections(old_dhcpServerConfig.sections, new_dhcpServerConfig.sections)

        if self.elements['section'].advertise == self.ON_CHANGE:
            self._check_diff_on_dhcpServerConfig_section(old_dhcpServerConfig.sections, new_dhcpServerConfig.sections)

        if self.elements['sectionStartIp'].advertise == self.ON_CHANGE:
            pass

        if self.elements['sectionEndIp'].advertise == self.ON_CHANGE:
            pass

        if self.elements['dns'].advertise == self.ON_CHANGE:
            self._check_diff_on_dhcpServerConfig_dns(old_dhcpServerConfig.dns, new_dhcpServerConfig.dns)

        if self.elements['primaryServer'].advertise == self.ON_CHANGE:
            self._check_diff_on_dhcpServerConfig_dns_primaryServer(old_dhcpServerConfig.dns.primary_server, new_dhcpServerConfig.dns.primary_server)

        if self.elements['secondaryServer'].advertise == self.ON_CHANGE:
            self._check_diff_on_dhcpServerConfig_dns_secondaryServer(old_dhcpServerConfig.dns.secondary_server, new_dhcpServerConfig.dns.secondary_server)

        if self.elements['domainName'].advertise == self.ON_CHANGE:
            self._check_diff_on_dhcpServerConfig_dns_domainName(old_dhcpServerConfig.dns.domain_name, new_dhcpServerConfig.dns.domain_name)

        if self.elements['defaultLeaseTime'].advertise == self.ON_CHANGE:
            self._check_diff_on_dhcpServerConfig_defaultLeaseTime(old_dhcpServerConfig.default_lease_time, new_dhcpServerConfig.default_lease_time)

        if self.elements['maxLeaseTime'].advertise == self.ON_CHANGE:
            self._check_diff_on_dhcpServerConfig_maxLeaseTime(old_dhcpServerConfig.max_lease_time, new_dhcpServerConfig.max_lease_time)


    def _check_diff_on_dhcpServerConfig(self, old_dhcpServerConfig, new_dhcpServerConfig):
        if old_dhcpServerConfig is None and new_dhcpServerConfig is not None:
            self._publish_dhcpServerConfig(new_dhcpServerConfig, self.EVENT_ADD)
        elif old_dhcpServerConfig is not None and new_dhcpServerConfig is None:
            self._publish_dhcpServerConfig(old_dhcpServerConfig, self.EVENT_DELETE)
        else:
            if not old_dhcpServerConfig.__eq__(new_dhcpServerConfig):
                self._publish_dhcpServerConfig(new_dhcpServerConfig, self.EVENT_UPDATE)

    def _check_diff_on_dhcpServerConfig_gateway(self, old_gateway, new_gateway):
        if old_gateway is None and new_gateway is not None:
            self._publish_dhcpServerConfig_gateway(new_gateway, self.EVENT_ADD)
        elif old_gateway is not None and new_gateway is None:
            self._publish_dhcpServerConfig_gateway(old_gateway, self.EVENT_DELETE)
        else:
            if not old_gateway.__eq__(new_gateway):
                self._publish_dhcpServerConfig_gateway(new_gateway, self.EVENT_UPDATE)

    def _check_diff_on_dhcpServerConfig_gateway_address(self, old_gateway_address, new_gateway_address):
        if old_gateway_address is None and new_gateway_address is not None:
            self._publish_dhcpServerConfig_gateway_address(new_gateway_address, self.EVENT_ADD)
        elif old_gateway_address is not None and new_gateway_address is None:
            self._publish_dhcpServerConfig_gateway_address(old_gateway_address, self.EVENT_DELETE)
        else:
            if not old_gateway_address.__eq__(new_gateway_address):
                self._publish_dhcpServerConfig_gateway_address(new_gateway_address, self.EVENT_UPDATE)

    def _check_diff_on_dhcpServerConfig_gateway_netmask(self, old_gateway_netmask, new_gateway_netmask):
        if old_gateway_netmask is None and new_gateway_netmask is not None:
            self._publish_dhcpServerConfig_gateway_netmask(new_gateway_netmask, self.EVENT_ADD)
        elif old_gateway_netmask is not None and new_gateway_netmask is None:
            self._publish_dhcpServerConfig_gateway_netmask(old_gateway_netmask, self.EVENT_DELETE)
        else:
            if not old_gateway_netmask.__eq__(new_gateway_netmask):
                self._publish_dhcpServerConfig_gateway_netmask(new_gateway_netmask, self.EVENT_UPDATE)

    def _check_diff_on_dhcpServerConfig_sections(self, old_sections, new_sections):
        if len(old_sections)==0 and len(new_sections)>0:
            self._publish_dhcpServerConfig_sections(new_sections, self.EVENT_ADD)
        elif len(old_sections)>0 and len(new_sections)==0:
            self._publish_dhcpServerConfig_sections(new_sections, self.EVENT_DELETE)
        else:
            self._publish_dhcpServerConfig_sections(new_sections, self.EVENT_UPDATE)

    def _check_diff_on_dhcpServerConfig_section(self, old_sections, new_sections):
        for old_section in old_sections:
            section = next((x for x in self.new_sections if x.start_ip == old_section.start_ip), None)
            if section is not None:
                if not section.__eq__(old_section):
                    self._publish_dhcpServerConfig_section(section, self.EVENT_UPDATE)
            else:
                self._publish_dhcpServerConfig_section(section, self.EVENT_DELETE)
        for new_section in new_sections:
            section = next((x for x in self.old_sections if x.start_ip == new_section.start_ip), None)
            if section is None:
                self._publish_dhcpServerConfig_section(section, self.EVENT_ADD)

    def _check_diff_on_dhcpServerConfig_section_startIP(self):
        pass

    def _check_diff_on_dhcpServerConfig_section_endIP(self):
        pass

    def _check_diff_on_dhcpServerConfig_dns(self, old_dns, new_dns):
        if old_dns is None and new_dns is not None:
            self._publish_dhcpServerConfig_dns(new_dns, self.EVENT_ADD)
        elif old_dns is not None and new_dns is None:
            self._publish_dhcpServerConfig_dns(old_dns, self.EVENT_DELETE)
        else:
            if not old_dns.__eq__(new_dns):
                self._publish_dhcpServerConfig_dns(new_dns, self.EVENT_UPDATE)

    def _check_diff_on_dhcpServerConfig_dns_primaryServer(self, old_primaryServer, new_primaryServer):
        if old_primaryServer is None and new_primaryServer is not None:
            self._publish_dhcpServerConfig_dns_primaryServer(new_primaryServer, self.EVENT_ADD)
        elif old_primaryServer is not None and new_primaryServer is None:
            self._publish_dhcpServerConfig_dns_primaryServer(old_primaryServer, self.EVENT_DELETE)
        else:
            if not old_primaryServer.__eq__(new_primaryServer):
                self._publish_dhcpServerConfig_dns_primaryServer(new_primaryServer, self.EVENT_UPDATE)

    def _check_diff_on_dhcpServerConfig_dns_secondaryServer(self, old_secondaryServer, new_secondaryServer):
        if old_secondaryServer is None and new_secondaryServer is not None:
            self._publish_dhcpServerConfig_dns_secondaryServer(new_secondaryServer, self.EVENT_ADD)
        elif old_secondaryServer is not None and new_secondaryServer is None:
            self._publish_dhcpServerConfig_dns_secondaryServer(old_secondaryServer, self.EVENT_DELETE)
        else:
            if not old_secondaryServer.__eq__(new_secondaryServer):
                self._publish_dhcpServerConfig_dns_secondaryServer(new_secondaryServer, self.EVENT_UPDATE)

    def _check_diff_on_dhcpServerConfig_dns_domainName(self, old_domainName, new_domainName):
        if old_domainName is None and new_domainName is not None:
            self._publish_dhcpServerConfig_dns_domainName(new_domainName, self.EVENT_ADD)
        elif old_domainName is not None and new_domainName is None:
            self._publish_dhcpServerConfig_dns_domainName(old_domainName, self.EVENT_DELETE)
        else:
            if not old_domainName.__eq__(new_domainName):
                self._publish_dhcpServerConfig_dns_domainName(new_domainName, self.EVENT_UPDATE)

    def _check_diff_on_dhcpServerConfig_defaultLeaseTime(self, old_defaultLeaseTime, new_defaultLeaseTime):
        if old_defaultLeaseTime is None and new_defaultLeaseTime is not None:
            self._publish_dhcpServerConfig_defaultLeaseTime(new_defaultLeaseTime, self.EVENT_ADD)
        elif old_defaultLeaseTime is not None and new_defaultLeaseTime is None:
            self._publish_dhcpServerConfig_defaultLeaseTime(old_defaultLeaseTime, self.EVENT_DELETE)
        else:
            if not old_defaultLeaseTime.__eq__(new_defaultLeaseTime):
                self._publish_dhcpServerConfig_defaultLeaseTime(new_defaultLeaseTime, self.EVENT_UPDATE)

    def _check_diff_on_dhcpServerConfig_maxLeaseTime(self, old_maxLeaseTime, new_maxLeaseTime):
        if old_maxLeaseTime is None and new_maxLeaseTime is not None:
            self._publish_dhcpServerConfig_maxLeaseTime(new_maxLeaseTime, self.EVENT_ADD)
        elif old_maxLeaseTime is not None and new_maxLeaseTime is None:
            self._publish_dhcpServerConfig_maxLeaseTime(old_maxLeaseTime, self.EVENT_DELETE)
        else:
            if not old_maxLeaseTime.__eq__(new_maxLeaseTime):
                self._publish_dhcpServerConfig_maxLeaseTime(new_maxLeaseTime, self.EVENT_UPDATE)


    ################### Private publish functions ###################
    def _publish_dhcpServerConfig(self, data, method=None):
        dhcpServerConfig_dict = self.dhcpServerParser.get_dhcp_server_configuration_dict(data)
        url = self.url_dhcpServerConfiguration
        self.ddController.publish_on_bus(url, method, dhcpServerConfig_dict)

    def _publish_dhcpServerConfig_gateway(self, data, method=None):
        gateway_dict = self.dhcpServerParser.get_dhcp_server_configuration_gateway_dict(data)
        url = self.url_gateway
        self.ddController.publish_on_bus(url, method, gateway_dict)

    def _publish_dhcpServerConfig_gateway_address(self, data, method=None):
        url = self.url_gateway_address
        self.ddController.publish_on_bus(url, method, data)

    def _publish_dhcpServerConfig_gateway_netmask(self, data, method=None):
        url = self.url_gateway_netmask
        self.ddController.publish_on_bus(url, method, data)

    def _publish_dhcpServerConfig_sections(self, data, method=None):
        sections_dict = []
        for section in data:
            section_dict = self.dhcpServerParser.get_dhcp_server_configuration_section_dict(section)
            sections_dict.append(section_dict)
        url = self.url_sections
        self.ddController.publish_on_bus(url, method, sections_dict)

    def _publish_dhcpServerConfig_section(self, id, data, method=None):
        section_dict = self.dhcpServerParser.get_dhcp_server_configuration_section_dict(data)
        url = self.url_sections + "/" + id
        self.ddController.publish_on_bus(url, method, section_dict)

    def _publish_dhcpServerConfig_section_startIP(self, id, data, method=None):
        url = self.url_sections + "/" + id + self.url_section_startIP
        self.ddController.publish_on_bus(url, method, data)

    def _publish_dhcpServerConfig_section_endIP(self, id, data, method=None):
        url = self.url_sections + "/" + id + self.url_section_endIP
        self.ddController.publish_on_bus(url, method, data)

    def _publish_dhcpServerConfig_dns(self, data, method=None):
        dns_dict = self.dhcpServerParser.get_dhcp_server_configuration_dns_dict(data)
        url = self.url_dns
        self.ddController.publish_on_bus(url, method, dns_dict)

    def _publish_dhcpServerConfig_dns_primaryServer(self, data, method=None):
        url = self.url_dns_primaryServer
        self.ddController.publish_on_bus(url, method, data)

    def _publish_dhcpServerConfig_dns_secondaryServer(self, data, method=None):
        url = self.url_dns_secondaryServer
        self.ddController.publish_on_bus(url, method, data)

    def _publish_dhcpServerConfig_dns_domainName(self, data, method=None):
        url = self.url_dns_domainName
        self.ddController.publish_on_bus(url, method, data)

    def _publish_dhcpServerConfig_defaultLeaseTime(self, data, method=None):
        url = self.url_defaultLeaseTime
        self.ddController.publish_on_bus(url, method, data)

    def _publish_dhcpServerConfig_maxLeaseTime(self, data, method=None):
        url = self.url_maxLeaseTime
        self.ddController.publish_on_bus(url, method, data)