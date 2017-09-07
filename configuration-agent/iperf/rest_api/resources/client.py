from flask import request, Response
from flask_restplus import Resource, fields
import json
import logging

from iperf.iperf_controller import IperfController
from iperf.rest_api.api import api

client_ns = api.namespace('client', 'Iperf Client Resource')

client_configuration_model = api.model('Client Configuration', {
    'server_address': fields.String(required=True, description='Server address', type='string'),
    'server_port': fields.String(required=True, description='Server port', type='string', default='5010'),
    'protocol': fields.String(required=False, description='Protocol', type='string', default="tcp"),
    'duration': fields.Integer(required=False, description='Duration', type='integer', default=10),
    'bidirectional': fields.Boolean(required=False, description='Bidirectional', type='boolean', default=False)
})
@client_ns.route("/start", methods=['POST'])
class IperfClient_Configuration(Resource):
    @client_ns.expect(client_configuration_model)
    @client_ns.response(202, 'Iperf client correctly started.')
    @client_ns.response(400, 'Bad request.')
    @client_ns.response(500, 'Internal Error.')
    def post(self):
        """
        Start iperf client
        """
        try:
            iperfController = IperfController()
            json_data = json.loads(request.data.decode())
            resp_data = iperfController.start_iperf_client(json_data)
            resp = Response(resp_data, status=200, mimetype="application/text")
            return resp

        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

