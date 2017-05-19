from flask import request, Response
from flask_restplus import Resource
import logging
from dhcp.controller.rest_api.api import api

nffg_ns = api.namespace('Interface', 'Interface Resource')

@nffg_ns.route('/<interface_id>', methods=['POST','PUT','DELETE','GET'],
               doc={'params': {'interface_name': {'description': 'The interface name', 'in': 'path'}}})


class InterfaceResource(Resource):

    @nffg_ns.response(200, 'Interface retrieved.')
    @nffg_ns.response(204, 'Interface not found.')
    @nffg_ns.response(500, 'Internal Error.')
    def get(self, name=None):
        pass

    @nffg_ns.param("Interface", "Interface to configure", "body", type="string", required=True)
    @nffg_ns.response(202, 'Interface correctly configured.')
    @nffg_ns.response(400, 'Bad request.')
    @nffg_ns.response(500, 'Internal Error.')
    def post(self, json_interface):
        pass

    @nffg_ns.param("Interface", "Interface to update", "body", type="string", required=True)
    @nffg_ns.response(202, 'Interface correctly updated.')
    @nffg_ns.response(204, 'Interface not found.')
    @nffg_ns.response(400, 'Bad request.')
    @nffg_ns.response(500, 'Internal Error.')
    def put(self, name, json_interface):
        pass

    @nffg_ns.response(202, 'Interface deleted.')
    @nffg_ns.response(204, 'Interface not found.')
    @nffg_ns.response(500, 'Internal Error.')
    def delete(self, name):
        pass

