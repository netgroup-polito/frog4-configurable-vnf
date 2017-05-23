from flask import Blueprint
from flask_restplus import Api

nat_blueprint = Blueprint('root', __name__)
api = Api(nat_blueprint, version='1.0', title='Nat API', description='Nat API',
          doc='/api_docs/')
