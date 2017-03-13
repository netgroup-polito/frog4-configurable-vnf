from configuration_agent.utils import Bash


def set_interface(interface):
    if interface.configuration_type == 'static':
        Bash('ifconfig '+ interface.name+' '+interface.address+'/' + str(interface.netmask))
        if interface.default_gw is not None:
            Bash('route add default gw '+interface.default_gw+' '+interface.name)
    elif interface.configuration_type == 'dhcp':
        if interface.default_gw is not None:
            Bash('route del default gw '+interface.default_gw)
        Bash('ifconfig '+interface.name+' 0')
        Bash('if [ ! -e "/usr/sbin/dhclient" ]; then cp /sbin/dhclient /usr/sbin/dhclient; fi')
        Bash('/usr/sbin/dhclient '+interface.name+' -v')
