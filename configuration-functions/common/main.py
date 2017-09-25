from cf_core.config import Configuration
from cf_core.config_instance import ConfigurationInstance
from cf_core.message_bus_controller import MessageBusController
from cf_core.cf_controller import ConfigFunctionsController
from rest_api.api import root_blueprint
from rest_api.resources.interface import api as interface_api
from rest_api.resources.nfs import api as nfs_api
from flask import Flask, request
import json
import logging


conf = Configuration()
# Set log level
log_format = '%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)s] %(message)s'
log_date_format = '[%d-%m-%Y %H:%M:%S]'

if conf.LOG_LEVEL == "INFO":
    log_level = logging.INFO
elif conf.LOG_LEVEL == "WARNING":
    log_level = logging.WARNING
else:
    log_level = logging.DEBUG

if conf.LOG_FILE is not None:
    logging.basicConfig(filename=conf.LOG_FILE, level=log_level, format=log_format, datefmt=log_date_format)
else:
    logging.basicConfig(level=log_level, format=log_format, datefmt=log_date_format)


app = Flask(__name__)
app.register_blueprint(root_blueprint)
#gunicorn_error_logger = logging.getLogger('gunicorn.error')
#app.logger.handlers.extend(gunicorn_error_logger.handlers)
#app.logger.setLevel(logging.DEBUG)
#app.logger.info("Flask Successfully started")
logging.debug("Flask Successfully started")

rest_address = ConfigurationInstance().get_rest_address()
logging.debug("Rest Server started on: " + rest_address)

@app.after_request
def after_request(response):
    logging.debug("'%s' '%s' '%s' '%s' '%s' " % (request.remote_addr, request.method, request.scheme, request.full_path, response.status))
    return response

MessageBusController().register_to_bus()
MessageBusController().publish_on_bus("cf_hello", rest_address)
MessageBusController().subscribe("vnf_hello")

# Set the initial configuration
datadisk_path = ConfigurationInstance().get_datadisk_path()
initial_configuration_path = datadisk_path + "/initial_configuration.json"
initial_configuration = None
with open(initial_configuration_path) as configuration:
    json_data = configuration.read()
    initial_configuration = json.loads(json_data)
ConfigFunctionsController().set_configuration(initial_configuration)

