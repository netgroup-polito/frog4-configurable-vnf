from flask import Blueprint
from flask_restplus import Api

dhcp_blueprint = Blueprint('root', __name__)
api = Api(dhcp_blueprint, version='1.0', title='Dhcp Server API', description='Dhcp Server API',
          doc='/api_docs/')
