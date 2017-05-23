from flask import Flask

#from dhcp.rest_api.api import dhcp_blueprint
from dhcp.rest_api.resources.interface import api as interface_api
#from dhcp.rest_api.resources.dhcp_server import api as dhcp_api
#from dhcp.rest_api.resources.dhcp_server_configuration import api as dhcp_config_api
#from dhcp.rest_api.resources.dhcp_server_clients import api as dhcp_client_api

from nat.rest_api.api import nat_blueprint
#from nat.rest_api.resources.interface import api as interface_api
from nat.rest_api.resources.nat import api as nat_api
from nat.rest_api.resources.floating_ip import api as floatingIP_api

#from firewall.rest_api.api import firewall_blueprint
#from firewall.rest_api.resources.interface import api as interface_api
#from firewall.rest_api.resources.firewall import api as firewall_api
#from firewall.rest_api.resources.blacklist import api as blacklist_api
#from firewall.rest_api.resources.whitelist import api as whitelist_api
#from firewall.rest_api.resources.policy import api as policy_api

import logging


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%H:%M:%S')

app = Flask(__name__)
#app.register_blueprint(dhcp_blueprint)
#app.register_blueprint(firewall_blueprint)
app.register_blueprint(nat_blueprint)
logging.info("Flask Successfully started")