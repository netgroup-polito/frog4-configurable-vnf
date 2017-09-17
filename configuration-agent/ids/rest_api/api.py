from flask import Blueprint
from flask_restplus import Api

ids_blueprint = Blueprint('root', __name__)
api = Api(ids_blueprint, version='1.0', title='IDS API', description='Ids API',
          doc='/api_docs/')
