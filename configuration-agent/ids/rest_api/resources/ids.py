from flask import request, Response
from flask_restplus import Resource
import json
import logging

from ids.ids_controller import IdsController
from ids.rest_api.api import api

ids_ns = api.namespace('ids', 'Ids Resource')
idsController = IdsController()

@ids_ns.route('/configuration', methods=['POST'])
class Ids_Config(Resource):
    @ids_ns.param("Ids Configuration", "Ids Configuration", "body", type="string", required=True)
    @ids_ns.response(200, 'Ids Configuration added')
    @ids_ns.response(400, 'Bad request.')
    @ids_ns.response(500, 'Internal Error.')
    def post(self):
        """
        Post Ids Configuration
        """
        try:
            json_data = json.loads(request.data.decode())
            resp_data = idsController.set_ids_configuration(json_data)
            resp = Response(resp_data, status=200, mimetype="application/text")
            return resp

        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")


class Ids_Config_NetworkToDefend(Resource):
    pass

@ids_ns.route('/configuration/attack_to_monitor', methods=['POST'])
class Ids_Config_AttacksToMonitor(Resource):
    @ids_ns.param("Attack to Monitor", "Add an attack name to monitor", "body", type="string", required=True)
    @ids_ns.response(200, 'Attack correctly added.')
    @ids_ns.response(400, 'Attack unknown.')
    @ids_ns.response(400, 'Bad request.')
    @ids_ns.response(500, 'Internal Error.')
    def post(self):
        """
        Add an attack to monitor
        """
        try:
            json_data = json.loads(request.data.decode())
            idsController.add_attackToMonitor(json_data)
            return Response(status=200)

        except ValueError as ve:
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")
