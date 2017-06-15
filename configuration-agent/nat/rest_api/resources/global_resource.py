import json
import logging

from flask import request, Response
from flask_restplus import Resource

from nat.controller.nat_global_controller import NatGlobalController as NatController
from nat.rest_api.api import api

nat_ns = api.namespace('config-nat', 'Nat Global Resource')

@nat_ns.route('', methods=['GET'])
class Nat(Resource):
    @nat_ns.response(200, 'Nat status retrieved.')
    @nat_ns.response(500, 'Internal Error.')
    def get(self):
        """
        Gets the full status of the nat
        """
        try:
            natController = NatController()
            json_data = json.dumps(natController.get_full_status())
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except Exception as err:
            logging.debug(err)
            return Response(status=500)