from flask import request, Response
from flask_restplus import Resource
import json
import logging

from ids.ids_controller import IdsController
from ids.rest_api.api import api

interface_ns = api.namespace('interfaces', 'Interface Resource')
idsController = IdsController()

@interface_ns.route('', methods=['GET'])
class Interface(Resource):
    @interface_ns.response(200, 'Interfaces retrieved.')
    @interface_ns.response(500, 'Internal Error.')
    def get(self):
        """
        Gets the status of all interfaces
        """
        try:
            json_data = json.dumps(idsController.get_interfaces_status())
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")


@interface_ns.route('/ifEntry', methods=['GET', 'POST'])
@interface_ns.route('/ifEntry/<id>', methods=['GET','PUT','DELETE'])
class Interface_ifEntry(Resource):
    @interface_ns.param("Interface", "Interface to configure", "body", type="string", required=True)
    @interface_ns.response(201, 'Interface correctly added.')
    @interface_ns.response(400, 'Bad request.')
    @interface_ns.response(500, 'Internal Error.')
    def post(self):
        """
        Configure an interface
        """
        try:
            json_data = json.loads(request.data.decode())
            idsController.configure_interface(json_data)
            return Response(status=202)

        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

    @interface_ns.response(200, 'Interface retrieved.')
    @interface_ns.response(404, 'Interface not found.')
    @interface_ns.response(500, 'Internal Error.')
    def get(self, id=None):
        """
        Get the configuration of an interface
        """
        try:
            if id is None:
                json_data = json.dumps(idsController.get_interfaces())
            else:
                json_data = json.dumps(idsController.get_interface(id))
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except ValueError as ve:
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

    @interface_ns.param("Interface", "Interface to update", "body", type="string", required=True)
    @interface_ns.response(202, 'Interface correctly updated.')
    @interface_ns.response(404, 'Interface not found.')
    @interface_ns.response(400, 'Bad request.')
    @interface_ns.response(500, 'Internal Error.')
    def put(self, id):
        """
        Update the configuration of an interface
        """
        try:
            json_data = json.loads(request.data.decode())
            idsController.update_interface(id, json_data)
            return Response(status=202)

        except ValueError as ve:
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

    @interface_ns.response(202, 'Interface deleted.')
    @interface_ns.response(404, 'Interface not found.')
    @interface_ns.response(500, 'Internal Error.')
    def delete(self, id):
        """
        Remove the configuration of an interface 
        """
        try:
            idsController.reset_interface(id)
            return Response(status=202)

        except ValueError as ve:
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")


@interface_ns.route('/ifEntry/<id>/ipv4_configuration', methods=['GET','PUT'])
class Interface_ifEntry_Ipv4Configuration(Resource):
    @interface_ns.response(200, 'Ipv4 configuration retrieved.')
    @interface_ns.response(404, 'Interface not found.')
    @interface_ns.response(500, 'Internal Error.')
    def get(self, id):
        """
        Get the ipv4 configuration of an interface 
        """
        try:
            json_data = json.dumps(idsController.get_interface_ipv4Configuration(id))
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except ValueError as ve:
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

    @interface_ns.param("Ipv4 Configuration", "Ipv4 configuration to update", "body", type="string", required=True)
    @interface_ns.response(202, 'Ipv4 configuration correctly updated.')
    @interface_ns.response(404, 'Interface not found.')
    @interface_ns.response(400, 'Bad request.')
    @interface_ns.response(500, 'Internal Error.')
    def put(self, id):
        """
        Update the ipv4 configuration of an interface 
        """
        try:
            json_data = json.loads(request.data.decode())
            idsController.update_interface_ipv4Configuration(id, json_data)
            return Response(status=202)

        except ValueError as ve:
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")


@interface_ns.route('/ifEntry/<id>/ipv4_configuration/address', methods=['GET','PUT'])
class Interface_ifEntry_Ipv4Configuration_Address(Resource):
    @interface_ns.response(200, 'Ip address retrieved.')
    @interface_ns.response(404, 'Interface not found.')
    @interface_ns.response(500, 'Internal Error.')
    def get(self, id):
        """
        Get the ip address of an interface  
        """
        try:
            json_data = json.dumps(idsController.get_interface_ipv4Configuration_address(id))
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except ValueError as ve:
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

    @interface_ns.param("Ip Address", "Ip address to update", "body", type="string", required=True)
    @interface_ns.response(202, 'Ip address correctly updated.')
    @interface_ns.response(404, 'Interface not found.')
    @interface_ns.response(400, 'Bad request.')
    @interface_ns.response(500, 'Internal Error.')
    def put(self, id):
        """
        Update the ip address of an interface 
        """
        try:
            address = request.data.decode()
            idsController.update_interface_ipv4Configuration_address(id, address)
            return Response(status=202)

        except ValueError as ve:
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")


@interface_ns.route('/ifEntry/<id>/ipv4_configuration/netmask', methods=['GET','PUT'])
class Interface_ifEntry_Ipv4Configuration_Netmask(Resource):
    @interface_ns.response(200, 'Netmask retrieved.')
    @interface_ns.response(404, 'Interface not found.')
    @interface_ns.response(500, 'Internal Error.')
    def get(self, id):
        """
        Get the netmask of an interface  
        """
        try:
            json_data = json.dumps(idsController.get_interface_ipv4Configuration_netmask(id))
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except ValueError as ve:
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

    @interface_ns.param("Netmask", "Netmask to update", "body", type="string", required=True)
    @interface_ns.response(202, 'Netmask correctly updated.')
    @interface_ns.response(404, 'Interface not found.')
    @interface_ns.response(400, 'Bad request.')
    @interface_ns.response(500, 'Internal Error.')
    def put(self, id):
        """
        Update the netmask of an interface 
        """
        try:
            netmask = request.data.decode()
            idsController.update_interface_ipv4Configuration_netmask(id, netmask)
            return Response(status=202)

        except ValueError as ve:
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")


@interface_ns.route('/ifEntry/<id>/ipv4_configuration/mac_address', methods=['GET'])
class Interface_ifEntry_Ipv4Configuration_DefaultGw(Resource):
    @interface_ns.response(200, 'Mac address retrieved.')
    @interface_ns.response(404, 'Interface not found.')
    @interface_ns.response(500, 'Internal Error.')
    def get(self, id):
        """
        Get the mac address of an interface  
        """
        try:
            json_data = json.dumps(idsController.get_interface_ipv4Configuration_mac_address(id))
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except ValueError as ve:
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")


@interface_ns.route('/ifEntry/<id>/ipv4_configuration/default_gw', methods=['GET','PUT'])
class Interface_ifEntry_Ipv4Configuration_MacAddress(Resource):
    @interface_ns.response(200, 'Default GW retrieved.')
    @interface_ns.response(404, 'Interface not found.')
    @interface_ns.response(500, 'Internal Error.')
    def get(self, id):
        """
        Get the default gw address of an interface  
        """
        try:
            json_data = json.dumps(idsController.get_interface_ipv4Configuration_default_gw(id))
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except ValueError as ve:
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

    @interface_ns.param("Default GW", "Default GW to update", "body", type="string", required=True)
    @interface_ns.response(202, 'Default GW correctly updated.')
    @interface_ns.response(404, 'Interface not found.')
    @interface_ns.response(400, 'Bad request.')
    @interface_ns.response(500, 'Internal Error.')
    def put(self, id):
        """
        Update the default gw of an interface  
        """
        try:
            default_gw = request.data.decode()
            idsController.update_interface_ipv4Configuration_default_gw(id, default_gw)
            return Response(status=202)

        except ValueError as ve:
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")