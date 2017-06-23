from flask import Flask, request

from dhcp.rest_api.api import dhcp_blueprint
from dhcp.rest_api.resources.interface import api as interface_api
from dhcp.rest_api.resources.dhcp_server import api as dhcp_api
from dhcp.rest_api.resources.dhcp_server_configuration import api as dhcp_config_api
from dhcp.rest_api.resources.dhcp_server_clients import api as dhcp_client_api

import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%H:%M:%S')

app = Flask(__name__)
app.register_blueprint(dhcp_blueprint)
logging.info("Flask Successfully started")

@app.after_request
def after_request(response):
    logging.debug("'%s' '%s' '%s' '%s' '%s' " % (request.remote_addr, request.method, request.scheme, request.full_path, response.status))
    return response