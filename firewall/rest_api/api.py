from flask import Blueprint
from flask_restplus import Api

firewall_blueprint = Blueprint('root', __name__)
api = Api(firewall_blueprint, version='1.0', title='Firewall API', description='Firewall API',
          doc='/api_docs/')
