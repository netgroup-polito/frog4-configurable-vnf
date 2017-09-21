from flask import request, Response
from flask_restplus import Resource
import json
import logging

from firewall.firewall_controller import FirewallController
from firewall.rest_api.api import api

blacklist_ns = api.namespace('firewall', 'Blacklist Resource')
firewallController = FirewallController()

@blacklist_ns.route('/blacklist', methods=['GET','POST'])
@blacklist_ns.route('/blacklist/<id>', methods=['DELETE'])
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
            json_data = json.loads(request.data.decode())
            firewallController.add_blacklist_url(json_data)
            return Response(status=202)

        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

    @blacklist_ns.response(200, 'Url retrieved.')
    @blacklist_ns.response(500, 'Internal Error.')
    def get(self):
        """
        Get all the urls from the blacklist
        """
        try:
            json_data = json.dumps(firewallController.get_blacklist())
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

    @blacklist_ns.response(202, 'Url deleted.')
    @blacklist_ns.response(404, 'Url not found.')
    @blacklist_ns.response(500, 'Internal Error.')
    def delete(self, id):
        """
        Remove an url from the blacklist
        """
        try:
            firewallController.delete_blacklist_url(id)
            return Response(status=202)

        except ValueError as ve:
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")