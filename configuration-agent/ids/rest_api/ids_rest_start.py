from flask import Flask, request
import logging

from ids.rest_api.api import ids_blueprint
from ids.rest_api.resources.interface import api as interface_api
from ids.rest_api.resources.ids import api as ids_api

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%H:%M:%S')

app = Flask(__name__)
app.register_blueprint(ids_blueprint)
logging.info("Flask Successfully started")

@app.after_request
def after_request(response):
    logging.debug("'%s' '%s' '%s' '%s' '%s' " % (request.remote_addr, request.method, request.scheme, request.full_path, response.status))
    return response

