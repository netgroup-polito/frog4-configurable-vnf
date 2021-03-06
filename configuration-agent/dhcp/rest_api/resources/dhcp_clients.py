from flask import request, Response
from flask_restplus import Resource
import json
import logging

from dhcp.dhcp_controller import DhcpController
from dhcp.rest_api.api import api

client_ns = api.namespace('dhcp', 'Dhcp Server Client Resource')

@client_ns.route('/clients', methods=['GET'])
@client_ns.route('/clients/<id>', methods=['GET'])
class Client(Resource):
    @client_ns.response(200, 'Client retrieved.')
    @client_ns.response(404, 'Client not found.')
    @client_ns.response(500, 'Internal Error.')
    def get(self, id=None):
        """
        Gets the dhcp client  
        """
        try:
            dhcpController = DhcpController()
            if id is None:
                json_data = json.dumps(dhcpController.get_clients())
            else:
                json_data = json.dumps(dhcpController.get_client(id))
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except ValueError as ve:
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

@client_ns.route('/clients/<id>/ip_address', methods=['GET'])
class Client_IpAdress(Resource):
    @client_ns.response(200, 'Client ip address retrieved.')
    @client_ns.response(404, 'Client not found.')
    @client_ns.response(500, 'Internal Error.')
    def get(self, id):
        """
        Gets the dhcp client ip address
        """
        try:
            dhcpController = DhcpController()
            json_data = json.dumps(dhcpController.get_client_ip_address(id))
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except ValueError as ve:
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

@client_ns.route('/clients/<id>/mac_address', methods=['GET'])
class Client_MacAdress(Resource):
    @client_ns.response(200, 'Client mac address retrieved.')
    @client_ns.response(404, 'Client not found.')
    @client_ns.response(500, 'Internal Error.')
    def get(self, id):
        """
        Gets the dhcp client mac address
        """
        try:
            dhcpController = DhcpController()
            json_data = json.dumps(dhcpController.get_client_mac_address(id))
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except ValueError as ve:
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

@client_ns.route('/clients/<id>/hostname', methods=['GET'])
class Client_Hostname(Resource):
    @client_ns.response(200, 'Client hostname retrieved.')
    @client_ns.response(404, 'Client not found.')
    @client_ns.response(500, 'Internal Error.')
    def get(self, id):
        """
        Gets the dhcp client hostname
        """
        try:
            dhcpController = DhcpController()
            json_data = json.dumps(dhcpController.get_client_hostname(id))
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except ValueError as ve:
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

@client_ns.route('/clients/<id>/valid_until', methods=['GET'])
class Client_ValidUntil(Resource):
    @client_ns.response(200, 'Client date validity retrieved.')
    @client_ns.response(404, 'Client not found.')
    @client_ns.response(500, 'Internal Error.')
    def get(self, id):
        """
        Gets the dhcp client date validity
        """
        try:
            dhcpController = DhcpController()
            json_data = json.dumps(dhcpController.get_client_valid_until(id))
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except ValueError as ve:
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")