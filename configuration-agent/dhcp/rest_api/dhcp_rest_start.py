from flask import Flask, request
import logging

from dhcp.rest_api.api import dhcp_blueprint
from dhcp.rest_api.resources.dhcp import api as dhcp_api
from dhcp.rest_api.resources.dhcp_clients import api as dhcp_clients_api
from dhcp.rest_api.resources.dhcp_server import api as dhcp_server_api
from dhcp.rest_api.resources.interface import api as interface_api
from dhcp.rest_api.resources.root import api as root_api

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%H:%M:%S')

app = Flask(__name__)
app.register_blueprint(dhcp_blueprint)
logging.info("Flask Successfully started")

@app.after_request
def after_request(response):
    logging.debug("'%s' '%s' '%s' '%s' '%s' " % (request.remote_addr, request.method, request.scheme, request.full_path, response.status))
    return response