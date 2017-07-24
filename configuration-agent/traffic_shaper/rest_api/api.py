from flask import Blueprint
from flask_restplus import Api

traffic_shaper_blueprint = Blueprint('root', __name__)
api = Api(traffic_shaper_blueprint, version='1.0', title='Traffic Shaper API', description='Traffic Shaper API',
          doc='/api_docs/')
