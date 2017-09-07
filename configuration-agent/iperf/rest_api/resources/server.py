from flask import request, Response
from flask_restplus import Resource, fields
import json
import logging

from iperf.iperf_controller import IperfController
from iperf.rest_api.api import api

server_ns = api.namespace('server', 'Iperf Server Resource')

server_configuration_model = api.model('Server Configuration', {
    'address': fields.String(required=True, description='Address', type='string', default='127.0.0.1'),
    'port': fields.String(required=True, description='Port', type='string', default='5010'),
})
@server_ns.route("/start", methods=['POST'])
class IperfServer_Configuration(Resource):
    @server_ns.expect(server_configuration_model)
    @server_ns.response(202, 'Iperf server correctly started.')
    @server_ns.response(400, 'Bad request.')
    @server_ns.response(500, 'Internal Error.')
    def post(self):
        """
        Start iperf server
        """
        try:
            iperfController = IperfController()
            json_data = json.loads(request.data.decode())
            resp_data = iperfController.start_iperf_server(json_data)
            resp = Response(resp_data, status=200, mimetype="application/text")
            return resp

        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")
