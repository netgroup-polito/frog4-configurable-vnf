from flask import Blueprint
from flask_restplus import Api

iperf_blueprint = Blueprint('root', __name__)
api = Api(iperf_blueprint, version='1.0', title='Iperf API', description='Iperf API',
          doc='/api_docs/')
