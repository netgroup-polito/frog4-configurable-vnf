import json
import logging

from flask import request, Response
from flask_restplus import Resource

from firewall.controller.firewall_controller import FirewallController
from firewall.rest_api.api import api

policy_ns = api.namespace('firewall/policies', 'Policy Resource')

@policy_ns.route('', methods=['GET','POST'])
@policy_ns.route('/<id>', methods=['GET','PUT','DELETE'])
class Policy(Resource):
    @policy_ns.param("Policy", "Policy to add", "body", type="string", required=True)
    @policy_ns.response(202, 'Policy correctly added.')
    @policy_ns.response(400, 'Bad request.')
    @policy_ns.response(500, 'Internal Error.')
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

    @policy_ns.response(200, 'Policy retrieved.')
    @policy_ns.response(500, 'Internal Error.')
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

    @policy_ns.param("Policy", "Policy to update", "body", type="string", required=True)
    @policy_ns.response(202, 'Policy correctly updated.')
    @policy_ns.response(400, 'Bad request.')
    @policy_ns.response(500, 'Internal Error.')
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

    @policy_ns.response(202, 'Policy deleted.')
    @policy_ns.response(204, 'Policy not found.')
    @policy_ns.response(500, 'Internal Error.')
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