from flask import request, Response
from flask_restplus import Resource
import json
import logging

from firewall.firewall_controller import FirewallController
from firewall.rest_api.api import api

policy_ns = api.namespace('firewall', 'Policy Resource')
firewallController = FirewallController()

@policy_ns.route('/policies', methods=['GET','POST'])
@policy_ns.route('/policies/<id>', methods=['GET','PUT','DELETE'])
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
            json_data = json.loads(request.data.decode())
            firewallController.add_policy(json_data)
            return Response(status=202)

        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

    @policy_ns.response(200, 'Policy retrieved.')
    @policy_ns.response(404, 'Policy not found.')
    @policy_ns.response(500, 'Internal Error.')
    def get(self, id=None):
        """
        Get a policy
        """
        try:
            if id is None:
                json_data = json.dumps(firewallController.get_policies())
            else:
                json_data = json.dumps(firewallController.get_policy(id))
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except ValueError as ve:
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

    """
    @policy_ns.param("Policy", "Policy to update", "body", type="string", required=True)
    @policy_ns.response(202, 'Policy correctly updated.')
    @policy_ns.response(400, 'Bad request.')
    @policy_ns.response(500, 'Internal Error.')
    def put(self, id):
        
        #Update a policy
        
        try:
            firewallController = FirewallController()
            json_data = json.loads(request.data.decode())
            firewallController.update_policy(id, json_data)
            return Response(status=202)

        except ValueError as ve:
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")
    """

    @policy_ns.response(202, 'Policy deleted.')
    @policy_ns.response(404, 'Policy not found.')
    @policy_ns.response(500, 'Internal Error.')
    def delete(self, id):
        """
        Remove a policy
        """
        try:
            firewallController.delete_policy(id)
            return Response(status=202)

        except ValueError as ve:
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

@policy_ns.route('/policies/<id>/description', methods=['GET','PUT'])
class Policy_Description(Resource):
    @policy_ns.response(200, 'Policy description parameter retrieved.')
    @policy_ns.response(404, 'Policy not found.')
    @policy_ns.response(500, 'Internal Error.')
    def get(self, id):
        """
        Get the policy description parameter
        """
        try:
            json_data = json.dumps(firewallController.get_policy_description(id))
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except ValueError as ve:
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

@policy_ns.route('/policies/<id>/action', methods=['GET','PUT'])
class Policy_Action(Resource):
    @policy_ns.response(200, 'Policy action parameter retrieved.')
    @policy_ns.response(404, 'Policy not found.')
    @policy_ns.response(500, 'Internal Error.')
    def get(self, id):
        """
        Get the policy action parameter
        """
        try:
            json_data = json.dumps(firewallController.get_policy_action(id))
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except ValueError as ve:
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

@policy_ns.route('/policies/<id>/protocol', methods=['GET','PUT'])
class Policy_Protocol(Resource):
    @policy_ns.response(200, 'Policy protocol parameter retrieved.')
    @policy_ns.response(404, 'Policy not found.')
    @policy_ns.response(500, 'Internal Error.')
    def get(self, id):
        """
        Get the policy protocol parameter
        """
        try:
            json_data = json.dumps(firewallController.get_policy_protocol(id))
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except ValueError as ve:
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

@policy_ns.route('/policies/<id>/in-interface', methods=['GET','PUT'])
class Policy_InInterface(Resource):
    @policy_ns.response(200, 'Policy in-interface parameter retrieved.')
    @policy_ns.response(404, 'Policy not found.')
    @policy_ns.response(500, 'Internal Error.')
    def get(self, id):
        """
        Get the policy in-interface parameter
        """
        try:
            json_data = json.dumps(firewallController.get_policy_in_interface(id))
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except ValueError as ve:
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

@policy_ns.route('/policies/<id>/out-interface', methods=['GET','PUT'])
class Policy_OutInterface(Resource):
    @policy_ns.response(200, 'Policy out-interface parameter retrieved.')
    @policy_ns.response(404, 'Policy not found.')
    @policy_ns.response(500, 'Internal Error.')
    def get(self, id):
        """
        Get the policy out-interface parameter
        """
        try:
            json_data = json.dumps(firewallController.get_policy_out_interface(id))
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except ValueError as ve:
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

@policy_ns.route('/policies/<id>/src-address', methods=['GET','PUT'])
class Policy_SrcAddress(Resource):
    @policy_ns.response(200, 'Policy src-address parameter retrieved.')
    @policy_ns.response(404, 'Policy not found.')
    @policy_ns.response(500, 'Internal Error.')
    def get(self, id):
        """
        Get the policy src-address parameter
        """
        try:
            json_data = json.dumps(firewallController.get_policy_src_address(id))
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except ValueError as ve:
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

@policy_ns.route('/policies/<id>/dst-address', methods=['GET','PUT'])
class Policy_DstAddress(Resource):
    @policy_ns.response(200, 'Policy dst-address parameter retrieved.')
    @policy_ns.response(404, 'Policy not found.')
    @policy_ns.response(500, 'Internal Error.')
    def get(self, id):
        """
        Get the policy dst-address parameter
        """
        try:
            json_data = json.dumps(firewallController.get_policy_dst_address(id))
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except ValueError as ve:
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

@policy_ns.route('/policies/<id>/src-port', methods=['GET','PUT'])
class Policy_SrcPort(Resource):
    @policy_ns.response(200, 'Policy src-port parameter retrieved.')
    @policy_ns.response(404, 'Policy not found.')
    @policy_ns.response(500, 'Internal Error.')
    def get(self, id):
        """
        Get the policy src-port parameter
        """
        try:
            json_data = json.dumps(firewallController.get_policy_src_port(id))
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except ValueError as ve:
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

@policy_ns.route('/policies/<id>/dst-port', methods=['GET','PUT'])
class Policy_DstPort(Resource):
    @policy_ns.response(200, 'Policy dst-port parameter retrieved.')
    @policy_ns.response(404, 'Policy not found.')
    @policy_ns.response(500, 'Internal Error.')
    def get(self, id):
        """
        Get the policy dst-port parameter
        """
        try:
            json_data = json.dumps(firewallController.get_policy_dst_port(id))
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except ValueError as ve:
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")