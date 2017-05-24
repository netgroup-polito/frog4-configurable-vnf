import json
import logging

from flask import request, Response
from flask_restplus import Resource

from firewall.controller.firewall_controller import FirewallController
from firewall.rest_api.api import api

blacklist_ns = api.namespace('firewall/blacklist', 'Blacklist Resource')

@blacklist_ns.route('', methods=['GET','POST'])
@blacklist_ns.route('/<id>', methods=['DELETE'])
class Blacklist(Resource):
    @blacklist_ns.param("Url", "Url to add", "body", type="string", required=True)
    @blacklist_ns.response(202, 'Url correctly added.')
    @blacklist_ns.response(400, 'Bad request.')
    @blacklist_ns.response(500, 'Internal Error.')
    def post(self):
        """
        Add an url to the blacklist
        """
        try:
            firewallController = FirewallController()
            json_data = json.loads(request.data.decode())
            firewallController.add_blacklist_url(json_data)
            return Response(status=202)

        except Exception as err:
            logging.debug(err)
            return Response(status=500)

    @blacklist_ns.response(200, 'Url retrieved.')
    @blacklist_ns.response(500, 'Internal Error.')
    def get(self):
        """
        Get all the urls from the blacklist
        """
        try:
            firewallController = FirewallController()
            json_data = json.dumps(firewallController.get_blacklist())
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except Exception as err:
            logging.debug(err)
            return Response(status=500)

    @blacklist_ns.response(202, 'Url deleted.')
    @blacklist_ns.response(404, 'Url not found.')
    @blacklist_ns.response(500, 'Internal Error.')
    def delete(self, id):
        """
        Remove an url from the blacklist
        """
        try:
            firewallController = FirewallController()
            firewallController.delete_blacklist_url(id)
            return Response(status=202)

        except ValueError as ve:
            logging.debug(ve)
            return Response(status=404)
        except Exception as err:
            logging.debug(err)
            return Response(status=500)