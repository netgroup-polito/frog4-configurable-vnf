import json
import logging

from flask import request, Response
from flask_restplus import Resource

from nat.controller.nat_controller import NatController
from nat.rest_api.api import api

floatingIP_ns = api.namespace('nat/floatingIP', 'Floating IP Resource')

@floatingIP_ns.route('', methods=['GET','POST'])
@floatingIP_ns.route('/<id>', methods=['GET','PUT','DELETE'])
class Nat_FloatingIP(Resource):
    @floatingIP_ns.param("Floating IP", "Floating IP to add", "body", type="string", required=True)
    @floatingIP_ns.response(202, 'Floating IP correctly added.')
    @floatingIP_ns.response(400, 'Bad request.')
    @floatingIP_ns.response(500, 'Internal Error.')
    def post(self):
        """
        Add a Floating IP
        """
        try:
            natController = NatController()
            json_data = json.loads(request.data.decode())
            natController.add_floating_ip(json_data)
            return Response(status=202)

        except Exception as err:
            logging.debug(err)
            return Response(status=500)

    @floatingIP_ns.response(200, 'Floating IP retrieved.')
    @floatingIP_ns.response(500, 'Internal Error.')
    def get(self, id=None):
        """
        Get a Floating IP
        """
        try:
            natController = NatController()
            if id is None:
                json_data = json.dumps(natController.get_all_floating_ip())
            else:
                json_data = json.dumps(natController.get_floating_ip(id))
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except ValueError as ve:
            logging.debug(ve)
            return Response(status=404)
        except Exception as err:
            logging.debug(err)
            return Response(status=500)

    @floatingIP_ns.param("Floating IP", "Floating IP to update", "body", type="string", required=True)
    @floatingIP_ns.response(202, 'Floating IP correctly updated.')
    @floatingIP_ns.response(400, 'Bad request.')
    @floatingIP_ns.response(500, 'Internal Error.')
    def put(self, id):
        """
        Update a Floating IP
        """
        try:
            natController = NatController()
            json_data = json.loads(request.data.decode())
            natController.update_floating_ip(id, json_data)
            return Response(status=202)

        except ValueError as ve:
            logging.debug(ve)
            return Response(status=404)
        except Exception as err:
            logging.debug(err)
            return Response(status=500)

    @floatingIP_ns.response(202, 'Floating IP deleted.')
    @floatingIP_ns.response(404, 'Floating IP not found.')
    @floatingIP_ns.response(500, 'Internal Error.')
    def delete(self, id):
        """
        Remove a Floating IP
        """
        try:
            natController = NatController()
            natController.delete_floating_ip(id)
            return Response(status=202)

        except ValueError as ve:
            logging.debug(ve)
            return Response(status=404)
        except Exception as err:
            logging.debug(err)
            return Response(status=500)

@floatingIP_ns.route('/floatingIP/<id>/privateAddress', methods=['GET','PUT'])
class Nat_FloatingIP_PrivateAddress(Resource):
    @floatingIP_ns.response(200, 'Floating IP private address retrieved.')
    @floatingIP_ns.response(500, 'Internal Error.')
    def get(self, id=None):
        """
        Gets the Floating IP private address parameter
        """
        try:
            natController = NatController()
            json_data = json.dumps(natController.get_floating_ip_private_address(id))
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except ValueError as ve:
            logging.debug(ve)
            return Response(status=404)
        except Exception as err:
            logging.debug(err)
            return Response(status=500)

    @floatingIP_ns.param("Floating IP private address", "Floating IP private address to update", "body", type="string", required=True)
    @floatingIP_ns.response(202, 'Floating IP private address correctly updated.')
    @floatingIP_ns.response(400, 'Bad request.')
    @floatingIP_ns.response(500, 'Internal Error.')
    def put(self, id):
        """
        Update the Floating IP private address parameter
        """
        try:
            natController = NatController()
            json_data = request.data.decode()
            natController.update_floating_ip_private_address(id, json_data)
            return Response(status=202)

        except ValueError as ve:
            logging.debug(ve)
            return Response(status=404)
        except Exception as err:
            logging.debug(err)
            return Response(status=500)

@floatingIP_ns.route('/floatingIP/<id>/publicAddress', methods=['PUT'])
class Nat_FloatingIP_PublicAddress(Resource):
    @floatingIP_ns.response(200, 'Floating IP public address retrieved.')
    @floatingIP_ns.response(500, 'Internal Error.')
    def get(self, id=None):
        """
        Gets the Floating IP public address parameter
        """
        try:
            natController = NatController()
            json_data = json.dumps(natController.get_floating_ip_public_address(id))
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except ValueError as ve:
            logging.debug(ve)
            return Response(status=404)
        except Exception as err:
            logging.debug(err)
            return Response(status=500)

    @floatingIP_ns.param("Floating IP public address", "Floating IP public address to update", "body", type="string", required=True)
    @floatingIP_ns.response(202, 'Floating IP public address correctly updated.')
    @floatingIP_ns.response(400, 'Bad request.')
    @floatingIP_ns.response(500, 'Internal Error.')
    def put(self, id):
        """
        Update the Floating IP public address parameter
        """
        try:
            natController = NatController()
            json_data = request.data.decode()
            natController.update_floating_ip_public_address(id, json_data)
            return Response(status=202)

        except ValueError as ve:
            logging.debug(ve)
            return Response(status=404)
        except Exception as err:
            logging.debug(err)
            return Response(status=500)