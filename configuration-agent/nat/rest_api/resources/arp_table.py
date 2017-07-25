from flask import request, Response
from flask_restplus import Resource
import json
import logging

from nat.nat_controller import NatController
from nat.rest_api.api import api

arp_table_ns = api.namespace('nat', 'Arp Table Resource')

@arp_table_ns.route('/arp-table', methods=['GET', 'POST'])
@arp_table_ns.route('/arp-table/<id>', methods=['DELETE'])
class Arp_Table(Resource):
    @arp_table_ns.param("Arp entry", "Arp entry to add", "body", type="string", required=True)
    @arp_table_ns.response(202, 'Arp entry correctly added.')
    @arp_table_ns.response(400, 'Bad request.')
    @arp_table_ns.response(500, 'Internal Error.')
    def post(self):
        """
        Add an arp entry
        """
        try:
            natController = NatController()
            json_data = json.loads(request.data.decode())
            natController.add_arp_entry(json_data)
            return Response(status=202)

        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

    @arp_table_ns.response(200, 'Arp table retrieved.')
    @arp_table_ns.response(500, 'Internal Error.')
    def get(self):
        """
        Get the arp table
        """
        try:
            natController = NatController()
            json_data = json.dumps(natController.get_arp_table())
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

    @arp_table_ns.response(202, 'Arp entry deleted.')
    @arp_table_ns.response(404, 'Arp entry not found.')
    @arp_table_ns.response(500, 'Internal Error.')
    def delete(self, id):
        """
        Remove the configuration of an interface 
        """
        try:
            natController = NatController()
            natController.delete_arp_entry(id)
            return Response(status=202)

        except ValueError as ve:
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

@arp_table_ns.route('/arp-table/<id>/mac_address', methods=['GET','PUT'])
class Arp_Table_MacAddress(Resource):
    @arp_table_ns.response(200, 'Mac address retrieved.')
    @arp_table_ns.response(500, 'Internal Error.')
    def get(self, id):
        """
        Get the mac address  
        """
        try:
            natController = NatController()
            json_data = json.dumps(natController.get_arp_table_mac_address(id))
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

    @arp_table_ns.param("Mac address", "Mac address to update", "body", type="string", required=True)
    @arp_table_ns.response(202, 'Mac address correctly updated.')
    @arp_table_ns.response(404, 'Arp entry not found.')
    @arp_table_ns.response(400, 'Bad request.')
    @arp_table_ns.response(500, 'Internal Error.')
    def put(self, id):
        """
        Update the mac address 
        """
        try:
            natController = NatController()
            mac_address = request.data.decode()
            natController.update_arp_table_mac_address(id, mac_address)
            return Response(status=202)

        except ValueError as ve:
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")