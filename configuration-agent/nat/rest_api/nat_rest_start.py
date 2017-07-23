from flask import Flask, request
import logging

from nat.rest_api.api import nat_blueprint
from nat.rest_api.resources.arp_table import api as arp_table_api
from nat.rest_api.resources.floating_ip import api as floating_ip_api
from nat.rest_api.resources.interface import api as interface_api
from nat.rest_api.resources.nat import api as nat_api
from nat.rest_api.resources.nat_table import api as nat_table_api
from nat.rest_api.resources.root import api as root_api

logging.basicConfig(filename="logging_agent.log", level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%H:%M:%S')

app = Flask(__name__)
app.register_blueprint(nat_blueprint)
logging.info("Flask Successfully started")

@app.after_request
def after_request(response):
    logging.debug("'%s' '%s' '%s' '%s' '%s' " % (request.remote_addr, request.method, request.scheme, request.full_path, response.status))
    return response