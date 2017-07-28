from common.utils import Bash
import logging

class TrafficShaperService():

    def enable_forwarding(self):
        Bash('echo 1 > /proc/sys/net/ipv4/ip_forward')

    def start_bandwitdh_shaping(self, TrafficShaper):

        # We'll use Hierarchical Token Bucket (HTB) to shape bandwidth.
        # For detailed configuration options, please consult Linux man
        # page.

        iface_name = TrafficShaper.interface_name
        iface_addr = TrafficShaper.interface_address

        dwld = None
        if TrafficShaper.download_limit is not None:
            dwld = TrafficShaper.download_limit

        upld = None
        if TrafficShaper.upload_limit is not None:
            upld = TrafficShaper.upload_limit

        # Filter options for limiting the intended interface.
        U32 = "tc filter add dev "+iface_name+" protocol ip parent 1:0 prio 1 u32"

        Bash("tc qdisc add dev "+iface_name+" root handle 1: htb default 30")
        if dwld is not None:
           Bash("class add dev "+iface_name+" parent 1: classid 1:1 htb rate "+dwld)
        if upld is not None:
            Bash("class add dev " + iface_name + " parent 1: classid 1:2 htb rate " + upld)
        if dwld is not None:
            Bash(U32+" match ip dst "+iface_addr+"/32 flowid 1:1")
        if upld is not None:
            Bash(U32+" match ip dst "+iface_addr+"/32 flowid 1:2")

        # The first line creates the root qdisc, and the next two lines
        # create two child qdisc that are to be used to shape download
        # and upload bandwidth.
        #
        # The 4th and 5th line creates the filter to match the interface.
        # The 'dst' IP address is used to limit download speed, and the
        # 'src' IP address is used to limit upload speed.

    def stop_bandwitdh_shaping(self, iface_name):
        Bash("tc qdisc del dev "+iface_name+" root")


    def get_status(self, iface_name):
        bash = Bash("tc -s qdisc ls dev "+iface_name)
        result = bash.get_output()
        logging.debug(result)
        return result