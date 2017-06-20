from flask import Flask

from nat.rest_api.api import nat_blueprint
from nat.rest_api.resources.root_resource import api as root_resource
from nat.rest_api.resources.interface import api as interface_api
from nat.rest_api.resources.nat import api as nat_api
#from nat.rest_api.resources.floating_ip import api as floatingIP_api

import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%H:%M:%S')

app = Flask(__name__)
app.register_blueprint(nat_blueprint)
logging.info("Flask Successfully started")