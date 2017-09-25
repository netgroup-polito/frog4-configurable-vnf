from flask import Blueprint
from flask_restplus import Api

root_blueprint = Blueprint('root', __name__)
api = Api(root_blueprint, version='1.0', title='Configuration Functions API', description='Configuration Functions API', doc='/api_docs/')
