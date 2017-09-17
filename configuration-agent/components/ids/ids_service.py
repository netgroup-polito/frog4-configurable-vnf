from common.utils import Bash

class IdsService():

    def __init__(self):
        pass

    def set_configuration(self, network_to_defend):

        str =  "# Setup the network addresses you are protecting\n"
        str += "ipvar HOME_NET " + network_to_defend + "\n\n"

        str = "# Set up the external network addresses. Leave as 'any' in most situations\n"
        str += "ipvar EXTERNAL_NET any\n\n"

        Bash('echo ' + str + ' > /etc/snort/snort.conf')
        Bash('cat /my_snort.conf >> /etc/snort/snort.conf')


    def configure_detection_portScan(self):

        # Add portScan configuration in snort.config
        str =  "# Target-Based stateful inspection/stream reassembly.  For more inforation, see README.stream5\n"
        str += "preprocessor stream5_global: track_tcp yes, track_udp yes\n"
        str += "preprocessor stream5_tcp: log_asymmetric_traffic no, policy windows\n"
        str += "preprocessor stream5_udp: timeout 180\n\n"
        str += "# Portscan detection.  For more information, see README.sfportscan\n"
        str += "preprocessor sfportscan: proto  { all } scan_type { portscan } memcap { 10000000 } sense_level { low }\n\n"
        Bash('echo ' + str + ' >> /etc/snort/snort.conf')

        # Add TCP Port Scanning rule to snort_rules
        rule = "alert tcp any any -> $HOME_NET any (msg:”TCP Port Scanning”; detection_filter:track by_src, count 30, seconds 60; sid:1000006; rev:2;)"
        Bash('echo ' + rule + ' >> /etc/snort/rules/local.rules')

        # Configure threshold
        str =  "# Here we are using detection filter to generate an alert whenever there\n"
        str += "# are more than 30 TCP connections are attempted within a 60-second interval.\n"
        str += "event_filter gen_id 1, sig_id 1000006, type limit, track by_src, count 1, seconds 60\n"
        Bash('echo ' + str + ' >> /etc/snort/threshold.conf')

    def start_ids(self):
        pass