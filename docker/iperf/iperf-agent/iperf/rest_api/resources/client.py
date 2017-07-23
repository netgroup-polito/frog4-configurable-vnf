from flask import request, Response
from flask_restplus import Resource
import json
import logging

from iperf.iperf_controller import IperfController
from iperf.rest_api.api import api

client_ns = api.namespace('client', 'Iperf Client Resource')

@client_ns.route("/start", methods=['POST'])
class IperfClient_Configuration(Resource):
    @client_ns.param("Start Iperf client", "Client configuration", "body", type="string", required=True)
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
            logging.debug(err)
            return Response(status=500)

