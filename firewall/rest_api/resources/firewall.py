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

@fw_ns.route('/policies', methods=['GET','POST'])
@fw_ns.route('/policies/<id>', methods=['GET','PUT','DELETE'])
class Policy(Resource):
    @fw_ns.param("Policy", "Policy to add", "body", type="string", required=True)
    @fw_ns.response(202, 'Policy correctly added.')
    @fw_ns.response(400, 'Bad request.')
    @fw_ns.response(500, 'Internal Error.')
    def post(self):
        """
        Add a policy
        """
        try:
            firewallController = FirewallController()
            json_data = json.loads(request.data.decode())
            firewallController.add_policy(json_data)
            return Response(status=202)

        except Exception as err:
            logging.debug(err)
            return Response(status=500)

    @fw_ns.response(200, 'Policy retrieved.')
    @fw_ns.response(500, 'Internal Error.')
    def get(self, id=None):
        """
        Get a policy
        """
        try:
            firewallController = FirewallController()
            if id is None:
                json_data = json.dumps(firewallController.get_policies())
            else:
                json_data = json.dumps(firewallController.get_policy(id))
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except ValueError as ve:
            logging.debug(ve)
            return Response(status=204)
        except Exception as err:
            logging.debug(err)
            return Response(status=500)

    @fw_ns.param("Policy", "Policy to update", "body", type="string", required=True)
    @fw_ns.response(202, 'Policy correctly updated.')
    @fw_ns.response(400, 'Bad request.')
    @fw_ns.response(500, 'Internal Error.')
    def put(self, id):
        """
        Update a policy
        """
        try:
            firewallController = FirewallController()
            json_data = json.loads(request.data.decode())
            firewallController.update_policy(id, json_data)
            return Response(status=202)

        except ValueError as ve:
            logging.debug(ve)
            return Response(status=204)
        except Exception as err:
            logging.debug(err)
            return Response(status=500)

    @fw_ns.response(202, 'Policy deleted.')
    @fw_ns.response(204, 'Policy not found.')
    @fw_ns.response(500, 'Internal Error.')
    def delete(self, id):
        """
        Remove a policy
        """
        try:
            firewallController = FirewallController()
            firewallController.delete_policy(id)
            return Response(status=202)

        except ValueError as ve:
            logging.debug(ve)
            return Response(status=204)
        except Exception as err:
            logging.debug(err)
            return Response(status=500)

@fw_ns.route('/blacklist', methods=['GET','POST'])
@fw_ns.route('/blacklist/<id>', methods=['DELETE'])
class Blacklist(Resource):
    @fw_ns.param("Url", "Url to add", "body", type="string", required=True)
    @fw_ns.response(202, 'Url correctly added.')
    @fw_ns.response(400, 'Bad request.')
    @fw_ns.response(500, 'Internal Error.')
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

    @fw_ns.response(200, 'Url retrieved.')
    @fw_ns.response(500, 'Internal Error.')
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

    @fw_ns.response(202, 'Url deleted.')
    @fw_ns.response(204, 'Url not found.')
    @fw_ns.response(500, 'Internal Error.')
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
            return Response(status=204)
        except Exception as err:
            logging.debug(err)
            return Response(status=500)

@fw_ns.route('/whitelist', methods=['GET','POST'])
@fw_ns.route('/whitelist/<id>', methods=['DELETE'])
class Whitelist(Resource):
    @fw_ns.param("Url", "Url to add", "body", type="string", required=True)
    @fw_ns.response(202, 'Url correctly added.')
    @fw_ns.response(400, 'Bad request.')
    @fw_ns.response(500, 'Internal Error.')
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

    @fw_ns.response(200, 'Url retrieved.')
    @fw_ns.response(500, 'Internal Error.')
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

    @fw_ns.response(202, 'Url deleted.')
    @fw_ns.response(204, 'Url not found.')
    @fw_ns.response(500, 'Internal Error.')
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
            return Response(status=204)
        except Exception as err:
            logging.debug(err)
            return Response(status=500)