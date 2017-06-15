from flask import Flask

from firewall.rest_api.api import firewall_blueprint
from firewall.rest_api.resources.interface import api as interface_api
from firewall.rest_api.resources.firewall import api as firewall_api
from firewall.rest_api.resources.blacklist import api as blacklist_api
from firewall.rest_api.resources.whitelist import api as whitelist_api
from firewall.rest_api.resources.policy import api as policy_api

import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%H:%M:%S')

app = Flask(__name__)
app.register_blueprint(firewall_blueprint)
logging.info("Flask Successfully started")