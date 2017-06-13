import json
import logging

from flask import request, Response
from flask_restplus import Resource

from nat.controller.nat_global_controller import NatGlobalController as NatController
from nat.rest_api.api import api

nat_ns = api.namespace('nat', 'Nat Resource')

@nat_ns.route('', methods=['GET'])
class Nat(Resource):
    @nat_ns.response(200, 'Nat status retrieved.')
    @nat_ns.response(500, 'Internal Error.')
    def get(self):
        """
        Gets the status of the nat
        """
        try:
            natController = NatController()
            json_data = json.dumps(natController.get_nat_status())
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except Exception as err:
            logging.debug(err)
            return Response(status=500)

@nat_ns.route('/public-interface', methods=['GET','PUT'])
class Nat_PublicInterface(Resource):
    @nat_ns.response(200, 'Public interface retrieved.')
    @nat_ns.response(500, 'Internal Error.')
    def get(self):
        """
        Gets the public-interface
        """
        try:
            natController = NatController()
            json_data = json.dumps(natController.get_public_interface_id())
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except Exception as err:
            logging.debug(err)
            return Response(status=500)

    @nat_ns.param("Public interface", "Public interface to update", "body", type="string", required=True)
    @nat_ns.response(202, 'Public interface correctly updated.')
    @nat_ns.response(400, 'Bad request.')
    @nat_ns.response(500, 'Internal Error.')
    def put(self):
        """
        Update the public-interface
        """
        try:
            natController = NatController()
            json_data = json.loads(request.data.decode())
            natController.set_ip_forward(json_data)
            return Response(status=202)

        except Exception as err:
            logging.debug(err)
            return Response(status=500)

@nat_ns.route('/private-interface', methods=['GET'])
class Nat_PrivateInterface(Resource):
    @nat_ns.response(200, 'Private interface retrieved.')
    @nat_ns.response(500, 'Internal Error.')
    def get(self):
        """
        Gets the private-interface
        """
        try:
            natController = NatController()
            json_data = json.dumps(natController.get_private_interface_id())
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except Exception as err:
            logging.debug(err)
            return Response(status=500)


@nat_ns.route('/nat-table', methods=['GET'])
class Nat_Table(Resource):
    @nat_ns.response(200, 'Nat table retrieved.')
    @nat_ns.response(500, 'Internal Error.')
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
            logging.debug(err)
            return Response(status=500)