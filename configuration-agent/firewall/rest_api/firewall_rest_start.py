from flask import Flask, request
import logging

from firewall.rest_api.api import firewall_blueprint
from firewall.rest_api.resources.blacklist import api as blacklist_api
from firewall.rest_api.resources.firewall import api as firewall_api
from firewall.rest_api.resources.interface import api as interface_api
from firewall.rest_api.resources.policy import api as policy_api
from firewall.rest_api.resources.root import api as root_api
from firewall.rest_api.resources.whitelist import api as whitelist_api

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%H:%M:%S')

app = Flask(__name__)
app.register_blueprint(firewall_blueprint)
logging.info("Flask Successfully started")

@app.after_request
def after_request(response):
    logging.debug("'%s' '%s' '%s' '%s' '%s' " % (request.remote_addr, request.method, request.scheme, request.full_path, response.status))
    return response