import json
import logging

from flask import request, Response
from flask_restplus import Resource

from firewall.controller.firewall_controller import FirewallController
from firewall.rest_api.api import api

whitelist_ns = api.namespace('firewall/whitelist', 'Whitelist Resource')

@whitelist_ns.route('', methods=['GET','POST'])
@whitelist_ns.route('/<id>', methods=['DELETE'])
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
            firewallController = FirewallController()
            json_data = json.loads(request.data.decode())
            firewallController.add_whitelist_url(json_data)
            return Response(status=202)

        except Exception as err:
            logging.debug(err)
            return Response(status=500)

    @whitelist_ns.response(200, 'Url retrieved.')
    @whitelist_ns.response(500, 'Internal Error.')
    def get(self):
        """
        Get all the urls from the whitelist
        """
        try:
            firewallController = FirewallController()
            json_data = json.dumps(firewallController.get_whitelist())
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except Exception as err:
            logging.debug(err)
            return Response(status=500)

    @whitelist_ns.response(202, 'Url deleted.')
    @whitelist_ns.response(404, 'Url not found.')
    @whitelist_ns.response(500, 'Internal Error.')
    def delete(self, id):
        """
        Remove an url from the whitelist
        """
        try:
            firewallController = FirewallController()
            firewallController.delete_whitelist_url(id)
            return Response(status=202)

        except ValueError as ve:
            logging.debug(ve)
            return Response(status=404)
        except Exception as err:
            logging.debug(err)
            return Response(status=500)