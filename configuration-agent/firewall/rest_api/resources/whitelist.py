from flask import request, Response
from flask_restplus import Resource
import json
import logging

from firewall.firewall_controller import FirewallController
from firewall.rest_api.api import api

whitelist_ns = api.namespace('firewall', 'Whitelist Resource')
firewallController = FirewallController()

@whitelist_ns.route('/whitelist', methods=['GET','POST'])
@whitelist_ns.route('/whitelist/<id>', methods=['DELETE'])
class Whitelist(Resource):
    @whitelist_ns.param("Url", "Url to add", "body", type="string", required=True)
    @whitelist_ns.response(202, 'Url correctly added.')
    @whitelist_ns.response(400, 'Bad request.')
    @whitelist_ns.response(500, 'Internal Error.')
    def post(self):
        """
        Add an url to the whitelist
        """
        try:
            json_data = json.loads(request.data.decode())
            firewallController.add_whitelist_url(json_data)
            return Response(status=202)

        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

    @whitelist_ns.response(200, 'Url retrieved.')
    @whitelist_ns.response(500, 'Internal Error.')
    def get(self):
        """
        Get all the urls from the whitelist
        """
        try:
            json_data = json.dumps(firewallController.get_whitelist())
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

    @whitelist_ns.response(202, 'Url deleted.')
    @whitelist_ns.response(404, 'Url not found.')
    @whitelist_ns.response(500, 'Internal Error.')
    def delete(self, id):
        """
        Remove an url from the whitelist
        """
        try:
            firewallController.delete_whitelist_url(id)
            return Response(status=202)

        except ValueError as ve:
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")