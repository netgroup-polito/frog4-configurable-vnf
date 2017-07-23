from flask import request, Response
from flask_restplus import Resource
import json
import logging

from firewall.firewall_controller import FirewallController
from firewall.rest_api.api import api

fw_ns = api.namespace('firewall', 'Firewall Resource')

@fw_ns.route('', methods=['GET','PUT'])
class Firewall(Resource):
    @fw_ns.response(200, 'Firewall status retrieved.')
    @fw_ns.response(500, 'Internal Error.')
    def get(self):
        """
        Gets the status of the firewall
        """
        try:
            firewallController = FirewallController()
            json_data = json.dumps(firewallController.get_firewall_status())
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except Exception as err:
            logging.debug(err)
            return Response(status=500)

    @fw_ns.param("Firewall Configuration", "Firewall Configuration to update", "body", type="string", required=True)
    @fw_ns.response(202, 'Nat configuration updated.')
    @fw_ns.response(400, 'Bad request.')
    @fw_ns.response(500, 'Internal Error.')
    def put(self):
        """
        Update the firewall configuration
        """
        try:
            firewallController = FirewallController()
            json_data = json.loads(request.data.decode())
            firewallController.set_configuration(json_data)
            return Response(status=202)

        except Exception as err:
            logging.debug(err)
            return Response(status=500)
