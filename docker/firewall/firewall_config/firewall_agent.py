import logging

from configuration_agent.agent import ConfigurationAgent
from configuration_agent.firewall_config.firewall import Firewall

#logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%H:%M:%S')
ConfigurationAgent(Firewall)