import json
import logging

from flask import request, Response
from flask_restplus import Resource

from firewall.controller.firewall_controller import FirewallController
from firewall.rest_api.api import api

fw_ns = api.namespace('firewall', 'Firewall Global Resource')


@fw_ns.route('', methods=['GET'])
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
