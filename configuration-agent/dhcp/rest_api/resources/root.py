from flask import request, Response
from flask_restplus import Resource
import json
import logging

from dhcp.dhcp_controller import DhcpController
from dhcp.rest_api.api import api

dhcp_root_ns = api.namespace('', 'Dhcp Root Resource')

@dhcp_root_ns.route('/', methods=['GET','PUT'])
class DhcpRoot(Resource):
    @dhcp_root_ns.response(200, 'Dhcp full status retrieved.')
    @dhcp_root_ns.response(500, 'Internal Error.')
    def get(self):
        """
        Gets the status of the dhcp server
        """
        try:
            dhcpController = DhcpController()
            json_data = json.dumps(dhcpController.get_full_status())
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

    @dhcp_root_ns.param("Dhcp Configuration", "Dhcp Configuration to update", "body", type="string", required=True)
    @dhcp_root_ns.response(202, 'Nat configuration updated.')
    @dhcp_root_ns.response(400, 'Bad request.')
    @dhcp_root_ns.response(500, 'Internal Error.')
    def put(self):
        """
        Update the dhcp configuration
        """
        try:
            dhcpController = DhcpController()
            json_data = json.loads(request.data.decode())
            dhcpController.set_configuration(json_data)
            return Response(status=202)

        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")