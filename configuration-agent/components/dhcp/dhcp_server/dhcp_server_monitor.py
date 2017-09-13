from components.dhcp.dhcp_server.dhcp_server_controller import DhcpServerController
from components.dhcp.dhcp_server.dhcp_server_parser import DhcpServerParser
from common.constants import Constants
from common.element import Element
from common.config_instance import ConfigurationInstance
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

        self.url_dhcpServerConfiguration = "config-dhcp-server:server/"
        self.url_defaultLeaseTime = self.url_dhcpServerConfiguration + "/defaultLeaseTime"
        self.url_maxLeaseTime = self.url_dhcpServerConfiguration + "/maxLeaseTime"
        self.url_subnet = self.url_dhcpServerConfiguration + "/subnet"
        self.url_subnetMask = self.url_dhcpServerConfiguration + "/subnetMask"
        self.url_router = self.url_dhcpServerConfiguration + "/router"
        self.url_dns_primaryServer = self.url_dhcpServerConfiguration + "/dnsPrimaryServer"
        self.url_dns_secondaryServer = self.url_dhcpServerConfiguration + "/dnsSecondaryServer"
        self.url_dns_domainName = self.url_dhcpServerConfiguration + "/dnsDomainName"
        self.url_sections = self.url_dhcpServerConfiguration + "/sections"
        self.url_section_startIP = "/sectionStartIp"
        self.url_section_endIP = "/sectionEndIp"

        self.elements = {}
        self.elements['server'] = Element(advertise=self.ON_CHANGE)
        self.elements['defaultLeaseTime'] = Element(advertise=self.SILENT)
        self.elements['maxLeaseTime'] = Element(advertise=self.SILENT)
        self.elements['subnet'] = Element(advertise=self.SILENT)
        self.elements['subnetMask'] = Element(advertise=self.SILENT)
        self.elements['router'] = Element(advertise=self.SILENT)
        self.elements['dnsPrimaryServer'] = Element(advertise=self.SILENT)
        self.elements['dnsSecondaryServer'] = Element(advertise=self.SILENT)
        self.elements['dnsDomainName'] = Element(advertise=self.SILENT)
        self.elements['sections'] = Element(advertise=self.SILENT)
        self.elements['section'] = Element(advertise=self.SILENT)
        self.elements['sectionStartIp'] = Element(advertise=self.SILENT)
        self.elements['sectionEndIp'] = Element(advertise=self.SILENT)
        ##################################################################

        self.periods = []
        for key, element in self.elements.items():
            if element.advertise == self.PERIODIC:
                element.period = element.period / 1000
                if element.period not in self.periods:
                    self.periods.append(element.period)

        self.on_change_interval = ConfigurationInstance().get_on_change_interval()
        logging.debug("on_change_interval: " + str(self.on_change_interval))

        self.dhcpServerConfig_old = curr_dhcpServer_configuration
        self.dhcpServerConfig_new = None

        self.ddController = dd_controller
        self.dhcpServerController = DhcpServerController()
        self.dhcpServerParser = DhcpServerParser()

    def start_monitoring(self):

        logging.debug("Dhcp server monitoring started!")

        for period in self.periods:
            Thread(target=self._timer_periodic_callback, args=([period])).start()

        while True:
            
            curr_dhcpServerConfig = self.dhcpServerController.get_dhcp_server_configuration()
            self._publish_dhcpServerConfig_leafs_on_change(self.dhcpServerConfig_old, curr_dhcpServerConfig)
            self.dhcpServerConfig_old = curr_dhcpServerConfig
            
            time.sleep(self.on_change_interval)


    def _timer_periodic_callback(self, period):

        while True:

            time.sleep(period)

            logging.debug("timer callback, period:" + str(period))
            curr_dhcpServerConfig = self.dhcpServerController.get_dhcp_server_configuration()
            self._publish_dhcpServerConfig_leafs_periodic(curr_dhcpServerConfig, period)

    def _publish_dhcpServerConfig_leafs_periodic(self, dhcpServerConfig, period):

        if self.elements['server'].advertise == self.PERIODIC and self.elements['server'].period == period:
            self._publish_dhcpServerConfig(dhcpServerConfig)

        if dhcpServerConfig.default_lease_time is not None:
            if self.elements['defaultLeaseTime'].advertise == self.PERIODIC and self.elements['defaultLeaseTime'].period == period:
                self._publish_dhcpServerConfig_defaultLeaseTime(dhcpServerConfig.default_lease_time)

        if dhcpServerConfig.max_lease_time is not None:
            if self.elements['maxLeaseTime'].advertise == self.PERIODIC and self.elements['maxLeaseTime'].period == period:
                self._publish_dhcpServerConfig_maxLeaseTime(dhcpServerConfig.max_lease_time)

        if dhcpServerConfig.subnet is not None:
            if self.elements['subnet'].advertise == self.PERIODIC and self.elements['subnet'].period == period:
                self._publish_dhcpServerConfig_subnet(dhcpServerConfig.subnet)

        if dhcpServerConfig.subnet_mask is not None:
            if self.elements['subnetMask'].advertise == self.PERIODIC and self.elements['subnetMask'].period == period:
                self._publish_dhcpServerConfig_subnetMask(dhcpServerConfig.subnet_mask)

        if dhcpServerConfig.router is not None:
            if self.elements['router'].advertise == self.PERIODIC and self.elements['router'].period == period:
                self._publish_dhcpServerConfig_router(dhcpServerConfig.router)

        if dhcpServerConfig.dns_primary_server is not None:
            if self.elements['dnsPrimaryServer'].advertise == self.PERIODIC and self.elements['dnsPrimaryServer'].period == period:
                self._publish_dhcpServerConfig_dns_primaryServer(dhcpServerConfig.dns_primary_server)

        if dhcpServerConfig.dns_secondary_server is not None:
            if self.elements['dnsSecondaryServer'].advertise == self.PERIODIC and self.elements['dnsSecondaryServer'].period == period:
                self._publish_dhcpServerConfig_dns_secondaryServer(dhcpServerConfig.dns_secondary_server)

        if dhcpServerConfig.dns_domain_name is not None:
            if self.elements['dnsDomainName'].advertise == self.PERIODIC and self.elements['dnsDomainName'].period == period:
                self._publish_dhcpServerConfig_dns_domainName(dhcpServerConfig.dns_domain_name)

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


    def _publish_dhcpServerConfig_leafs_on_change(self, old_dhcpServerConfig, new_dhcpServerConfig):

        if self.elements['server'].advertise == self.ON_CHANGE:
            self._check_diff_on_dhcpServerConfig(old_dhcpServerConfig, new_dhcpServerConfig)

        if self.elements['defaultLeaseTime'].advertise == self.ON_CHANGE:
            self._check_diff_on_dhcpServerConfig_defaultLeaseTime(old_dhcpServerConfig.default_lease_time, new_dhcpServerConfig.default_lease_time)

        if self.elements['maxLeaseTime'].advertise == self.ON_CHANGE:
            self._check_diff_on_dhcpServerConfig_maxLeaseTime(old_dhcpServerConfig.max_lease_time, new_dhcpServerConfig.max_lease_time)

        if self.elements['subnet'].advertise == self.ON_CHANGE:
            self._check_diff_on_dhcpServerConfig_subnet(old_dhcpServerConfig.subnet, new_dhcpServerConfig.subnet)

        if self.elements['subnetMask'].advertise == self.ON_CHANGE:
            self._check_diff_on_dhcpServerConfig_subnetMask(old_dhcpServerConfig.subnet_mask, new_dhcpServerConfig.subnet_mask)

        if self.elements['router'].advertise == self.ON_CHANGE:
            self._check_diff_on_dhcpServerConfig_router(old_dhcpServerConfig.router, new_dhcpServerConfig.router)

        if self.elements['dnsPrimaryServer'].advertise == self.ON_CHANGE:
            self._check_diff_on_dhcpServerConfig_dns_primaryServer(old_dhcpServerConfig.dns_primary_server, new_dhcpServerConfig.dns_primary_server)

        if self.elements['dnsSecondaryServer'].advertise == self.ON_CHANGE:
            self._check_diff_on_dhcpServerConfig_dns_secondaryServer(old_dhcpServerConfig.dns_secondary_server, new_dhcpServerConfig.dns_secondary_server)

        if self.elements['dnsDomainName'].advertise == self.ON_CHANGE:
            self._check_diff_on_dhcpServerConfig_dns_domainName(old_dhcpServerConfig.dns_domain_name, new_dhcpServerConfig.dns_domain_name)

        if self.elements['sections'].advertise == self.ON_CHANGE:
            self._check_diff_on_dhcpServerConfig_sections(old_dhcpServerConfig.sections, new_dhcpServerConfig.sections)

        if self.elements['section'].advertise == self.ON_CHANGE:
            self._check_diff_on_dhcpServerConfig_section(old_dhcpServerConfig.sections, new_dhcpServerConfig.sections)

        if self.elements['sectionStartIp'].advertise == self.ON_CHANGE:
            pass

        if self.elements['sectionEndIp'].advertise == self.ON_CHANGE:
            pass


    def _check_diff_on_dhcpServerConfig(self, old_dhcpServerConfig, new_dhcpServerConfig):
        if old_dhcpServerConfig is None and new_dhcpServerConfig is not None:
            self._publish_dhcpServerConfig(new_dhcpServerConfig, self.EVENT_ADD)
        elif old_dhcpServerConfig is not None and new_dhcpServerConfig is None:
            self._publish_dhcpServerConfig(old_dhcpServerConfig, self.EVENT_DELETE)
        else:
            if not old_dhcpServerConfig.__eq__(new_dhcpServerConfig):
                self._publish_dhcpServerConfig(new_dhcpServerConfig, self.EVENT_UPDATE)

    def _check_diff_on_dhcpServerConfig_defaultLeaseTime(self, old_defaultLeaseTime, new_defaultLeaseTime):
        if old_defaultLeaseTime is None and new_defaultLeaseTime is not None:
            self._publish_dhcpServerConfig_defaultLeaseTime(new_defaultLeaseTime, self.EVENT_ADD)
        elif old_defaultLeaseTime is not None and new_defaultLeaseTime is None:
            self._publish_dhcpServerConfig_defaultLeaseTime(old_defaultLeaseTime, self.EVENT_DELETE)
        else:
            if not old_defaultLeaseTime.__eq__(new_defaultLeaseTime):
                self._publish_dhcpServerConfig_defaultLeaseTime(new_defaultLeaseTime, self.EVENT_UPDATE)

    def _check_diff_on_dhcpServerConfig_subnet(self, old_subnet, new_subnet):
        if old_subnet is None and new_subnet is not None:
            self._publish_dhcpServerConfig_subnet(new_subnet, self.EVENT_ADD)
        elif old_subnet is not None and new_subnet is None:
            self._publish_dhcpServerConfig_subnet(old_subnet, self.EVENT_DELETE)
        else:
            if not old_subnet.__eq__(new_subnet):
                self._publish_dhcpServerConfig_subnet(new_subnet, self.EVENT_UPDATE)

    def _check_diff_on_dhcpServerConfig_subnetMask(self, old_subnetMask, new_subnetMask):
        if old_subnetMask is None and new_subnetMask is not None:
            self._publish_dhcpServerConfig_subnetMask(new_subnetMask, self.EVENT_ADD)
        elif old_subnetMask is not None and new_subnetMask is None:
            self._publish_dhcpServerConfig_subnetMask(old_subnetMask, self.EVENT_DELETE)
        else:
            if not old_subnetMask.__eq__(new_subnetMask):
                self._publish_dhcpServerConfig_subnetMask(new_subnetMask, self.EVENT_UPDATE)

    def _check_diff_on_dhcpServerConfig_router(self, old_router, new_router):
        if old_router is None and new_router is not None:
            self._publish_dhcpServerConfig_router(new_router, self.EVENT_ADD)
        elif old_router is not None and new_router is None:
            self._publish_dhcpServerConfig_router(old_router, self.EVENT_DELETE)
        else:
            if not old_router.__eq__(new_router):
                self._publish_dhcpServerConfig_router(new_router, self.EVENT_UPDATE)

    def _check_diff_on_dhcpServerConfig_maxLeaseTime(self, old_maxLeaseTime, new_maxLeaseTime):
        if old_maxLeaseTime is None and new_maxLeaseTime is not None:
            self._publish_dhcpServerConfig_maxLeaseTime(new_maxLeaseTime, self.EVENT_ADD)
        elif old_maxLeaseTime is not None and new_maxLeaseTime is None:
            self._publish_dhcpServerConfig_maxLeaseTime(old_maxLeaseTime, self.EVENT_DELETE)
        else:
            if not old_maxLeaseTime.__eq__(new_maxLeaseTime):
                self._publish_dhcpServerConfig_maxLeaseTime(new_maxLeaseTime, self.EVENT_UPDATE)

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

    def _check_diff_on_dhcpServerConfig_sections(self, old_sections, new_sections):
        if len(old_sections) == 0 and len(new_sections) > 0:
            self._publish_dhcpServerConfig_sections(new_sections, self.EVENT_ADD)
        elif len(old_sections) > 0 and len(new_sections) == 0:
            self._publish_dhcpServerConfig_sections(new_sections, self.EVENT_DELETE)
        else:
            self._publish_dhcpServerConfig_sections(new_sections, self.EVENT_UPDATE)

    def _check_diff_on_dhcpServerConfig_section(self, old_sections, new_sections):
        for old_section in old_sections:
            section = next((x for x in new_sections if x.start_ip == old_section.start_ip), None)
            if section is not None:
                if not section.__eq__(old_section):
                    self._publish_dhcpServerConfig_section(section, self.EVENT_UPDATE)
            else:
                self._publish_dhcpServerConfig_section(section, self.EVENT_DELETE)
        for new_section in new_sections:
            section = next((x for x in old_sections if x.start_ip == new_section.start_ip), None)
            if section is None:
                self._publish_dhcpServerConfig_section(section, self.EVENT_ADD)

    def _check_diff_on_dhcpServerConfig_section_startIP(self):
        pass

    def _check_diff_on_dhcpServerConfig_section_endIP(self):
        pass


    ################### Private publish functions ###################
    def _publish_dhcpServerConfig(self, data, method=None):
        dhcpServerConfig_dict = self.dhcpServerParser.get_dhcp_server_configuration_dict(data)
        url = self.url_dhcpServerConfiguration
        self.ddController.publish_on_bus(url, method, dhcpServerConfig_dict)

    def _publish_dhcpServerConfig_defaultLeaseTime(self, data, method=None):
        url = self.url_defaultLeaseTime
        self.ddController.publish_on_bus(url, method, data)

    def _publish_dhcpServerConfig_maxLeaseTime(self, data, method=None):
        url = self.url_maxLeaseTime
        self.ddController.publish_on_bus(url, method, data)

    def _publish_dhcpServerConfig_subnet(self, data, method=None):
        url = self.url_subnet
        self.ddController.publish_on_bus(url, method, data)

    def _publish_dhcpServerConfig_subnetMask(self, data, method=None):
        url = self.url_subnetMask
        self.ddController.publish_on_bus(url, method, data)

    def _publish_dhcpServerConfig_router(self, data, method=None):
        url = self.url_router
        self.ddController.publish_on_bus(url, method, data)

    def _publish_dhcpServerConfig_dns_primaryServer(self, data, method=None):
        url = self.url_dns_primaryServer
        self.ddController.publish_on_bus(url, method, data)

    def _publish_dhcpServerConfig_dns_secondaryServer(self, data, method=None):
        url = self.url_dns_secondaryServer
        self.ddController.publish_on_bus(url, method, data)

    def _publish_dhcpServerConfig_dns_domainName(self, data, method=None):
        url = self.url_dns_domainName
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