import json
import logging

from flask import request, Response
from flask_restplus import Resource

from dhcp.controller.dhcp_controller import DhcpController
from dhcp.rest_api.api import api

dhcp_ns = api.namespace('dhcp', 'Dhcp Server Global Resource')

@dhcp_ns.route('', methods=['GET'])
class DhcpServer(Resource):
    @dhcp_ns.response(200, 'Dhcp status retrieved.')
    @dhcp_ns.response(500, 'Internal Error.')
    def get(self):
        """
        Gets the status of the dhcp server
        """
        try:
            dhcpController = DhcpController()
            json_data = json.dumps(dhcpController.get_dhcp_status())
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except Exception as err:
            logging.debug(err)
            return Response(status=500)

