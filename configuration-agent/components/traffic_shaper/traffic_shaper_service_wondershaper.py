from common.utils import Bash
import logging

class TrafficShaperServiceWondershaper():

    def enable_forwarding(self):
        Bash('echo 1 > /proc/sys/net/ipv4/ip_forward')

    def start_bandwitdh_shaping(self, TrafficShaper):

        iface_name = TrafficShaper.interface_name

        dwld = 0
        if TrafficShaper.download_limit is not None:
            dwld = str(TrafficShaper.download_limit * 1024)

        upld = 0
        if TrafficShaper.upload_limit is not None:
            upld = str(TrafficShaper.upload_limit * 1024)

        cmd = "wondershaper " + iface_name + " " + dwld + " " + upld
        logging.debug(cmd)
        Bash(cmd)

    def stop_bandwitdh_shaping(self, iface_name):
        cmd = "wondershaper clear " + iface_name
        logging.debug(cmd)
        Bash(cmd)