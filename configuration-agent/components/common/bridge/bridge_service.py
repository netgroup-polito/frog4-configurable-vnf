from common.utils import Bash

class BridgeService():

    def create_bridge(self, bridge):
        Bash('ifconfig ' + bridge.iface1 + ' 0')
        Bash('ifconfig ' + bridge.iface2 + ' 0')
        Bash('brctl addbr ' + bridge.name)
        Bash('brctl addif ' + bridge.name + ' ' + bridge.iface1)
        Bash('brctl addif ' + bridge.name + ' ' + bridge.iface2)
        Bash('ifconfig ' + bridge.name + ' up')
        #Bash('route del default')
        #Bash('/usr/sbin/dhclient ' + bridge.name + ' -v')

    def update_bridge(self, bridge):
        Bash('ifconfig ' + bridge.iface1 + ' down')
        Bash('ifconfig ' + bridge.iface2 + ' down')
        Bash('ifconfig ' + bridge.iface1 + ' 0')
        Bash('ifconfig ' + bridge.iface2 + ' 0')
        Bash('brctl delif ' + bridge.name + ' ' + bridge.iface1 + ' ' + bridge.iface2)
        Bash('ifconfig ' + bridge.name + ' down')
        Bash('brctl delbr ' + bridge.name)
        Bash('brctl addbr ' + bridge.name)
        Bash('brctl addif ' + bridge.name + ' ' + bridge.iface1)
        Bash('brctl addif ' + bridge.name + ' ' + bridge.iface2)
        Bash('route del default')
        Bash('/usr/sbin/dhclient ' + bridge.name + ' -v')

    def get_bridges(self):
        pass

    def get_bridge(self, name):
        pass