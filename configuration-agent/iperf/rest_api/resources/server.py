from flask import request, Response
from flask_restplus import Resource
import json
import logging

from iperf_controller import IperfController
from rest_api.api import api

server_ns = api.namespace('server', 'Iperf Server Resource')

@server_ns.route("/start", methods=['POST'])
class IperfServer_Configuration(Resource):
    @server_ns.param("Start Iperf server", "Server configuration", "body", type="string", required=True)
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
            logging.debug(err)
            return Response(status=500)
