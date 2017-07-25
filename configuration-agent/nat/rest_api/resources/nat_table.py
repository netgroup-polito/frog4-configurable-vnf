from flask import request, Response
from flask_restplus import Resource
import json
import logging

from nat.nat_controller import NatController
from nat.rest_api.api import api

nat_table_ns = api.namespace('nat', 'Nat Table Resource')

@nat_table_ns.route('/nat-table', methods=['GET'])
class Nat_Table(Resource):
    @nat_table_ns.response(200, 'Nat table retrieved.')
    @nat_table_ns.response(500, 'Internal Error.')
    def get(self):
        """
        Gets the nat table
        """
        try:
            natController = NatController()
            json_data = json.dumps(natController.get_nat_table())
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")