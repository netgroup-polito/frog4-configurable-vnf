import json
import logging

from flask import request, Response
from flask_restplus import Resource

from nat.controller.nat_global_controller import NatGlobalController as NatController
from nat.rest_api.api import api

root_ns = api.namespace('', 'Nat Root Resource')

@root_ns.route('/', methods=['GET','PUT'])
class Nat(Resource):
    @root_ns.response(200, 'Nat status retrieved.')
    @root_ns.response(500, 'Internal Error.')
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

    @root_ns.param("Nat configuration", "Nat configuration to update", "body", type="string", required=True)
    @root_ns.response(202, 'Nat configuration correctly updated.')
    @root_ns.response(400, 'Bad request.')
    @root_ns.response(500, 'Internal Error.')
    def put(self):
        """
        Push the full configuration to the nat
        """
        try:
            natController = NatController()
            json_data = json.loads(request.data.decode())
            natController.set_configuration(json_data)
            return Response(status=202)

        except Exception as err:
            logging.debug(err)
            return Response(status=500)