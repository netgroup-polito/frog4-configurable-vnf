from flask import Flask, request
import logging

from iperf.rest_api.api import iperf_blueprint
from iperf.rest_api.resources.client import api as client_api
from iperf.rest_api.resources.server import api as server_api
#from iperf.rest_api.resources.stat import api as stats_api
from iperf.rest_api.resources.interface import api as interface_api

# set log level
log_format = '%(asctime)s [%(levelname)s] %(filename)s:%(lineno)s %(message)s'
log_date_format = '[%d-%m-%Y %H:%M:%S]'
logging.basicConfig(level=logging.DEBUG, format=log_format, datefmt=log_date_format)

app = Flask(__name__)
app.register_blueprint(iperf_blueprint)
logging.info("Flask Successfully started")

@app.after_request
def after_request(response):
    logging.debug("'%s' '%s' '%s' '%s' '%s' " % (request.remote_addr, request.method, request.scheme, request.full_path, response.status))
    return response