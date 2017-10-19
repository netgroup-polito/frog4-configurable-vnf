from common.utils import Bash
import logging

class IdsService():

    def __init__(self):
        pass

    def set_configuration(self, network_to_defend):

        str =  "# Setup the network addresses you are protecting\n"
        str += "ipvar HOME_NET " + network_to_defend + "\n\n"

        str += "# Set up the external network addresses. Leave as 'any' in most situations\n"
        str += "ipvar EXTERNAL_NET any\n"

        with open("/etc/snort/snort.conf", "w") as text_file:
            print("{}".format(str), file=text_file)

        Bash('cat /my_snort.conf >> /etc/snort/snort.conf')


    def configure_detection_portScan(self):

        # Add portScan configuration in snort.config
        str =  "\n# Target-Based stateful inspection/stream reassembly.  For more inforation, see README.stream5\n"
        str += "preprocessor stream5_global: track_tcp yes, track_udp yes\n"
        str += "preprocessor stream5_tcp: log_asymmetric_traffic no, policy windows\n"
        str += "preprocessor stream5_udp: timeout 180\n\n"
        str += "# Portscan detection.  For more information, see README.sfportscan\n"
        str += "preprocessor sfportscan: proto  { all } scan_type { portscan } memcap { 10000000 } sense_level { low }\n\n"
        with open("/etc/snort/snort.conf", "a") as text_file:
            print("{}".format(str), file=text_file)

        # Add TCP Port Scanning rule to snort_rules
        # Here we are using detection filter to generate an alert whenever there"
        # are more than 30 TCP connections are attempted within a 60-second interval"
        rule = "alert tcp any any -> $HOME_NET any (msg:'TCP Port Scanning'; detection_filter:track by_src, count 30, seconds 60; sid:1000006; rev:2;)"
        with open("/etc/snort/rules/local.rules", "a") as text_file:
            print("{}".format(rule), file=text_file)

        # Configure threshold
        str = "# The following command tells snort to limit the alerts for the rule with the sid of 1000006 to 1 per every 20 seconds\n"
        str += "event_filter gen_id 1, sig_id 1000006, type limit, track by_src, count 1, seconds 20\n"
        with open("/etc/snort/threshold.conf", "a") as text_file:
            print("{}".format(str), file=text_file)

    def configure_detection_pingFlood(self):
        # Add Ping flood rule to snort_rules
        # Here we are using detection filter to generate an alert whenever there"
        # are more than 100 ICMP Echo Request within a 1-second interval"
        #rule = "alert icmp any any -> $HOME_NET any (msg:'Ping flood'; detection_filter:track by_src, count 99, seconds 1; gid:1000031; sid:1000031; rev:1;)"
        rule = "alert icmp any any -> $HOME_NET any (msg:'Ping flood'; detection_filter:track by_src, count 99, seconds 5; sid:1000031; rev:1;)"
        with open("/etc/snort/rules/local.rules", "a") as text_file:
            print("{}".format(rule), file=text_file)

        # Configure threshold
        str = "# The following command tells snort to limit the alerts for the rule with the sid of 1000031 to 1 per every 20 seconds\n"
        str += "event_filter gen_id 1, sig_id 1000031, type limit, track by_src, count 1, seconds 20\n"
        with open("/etc/snort/threshold.conf", "a") as text_file:
            print("{}".format(str), file=text_file)

    def start_ids(self):
        Bash("snort -c /etc/snort/snort.conf -i eth1 -D")