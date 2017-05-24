import json
import logging

from flask import request, Response
from flask_restplus import Resource

from dhcp.controller.dhcp_controller import DhcpController
from dhcp.rest_api.api import api

config_ns = api.namespace('dhcp/globalIpPool', 'Dhcp Server Configuration Resource')

@config_ns.route('', methods=['GET'])
class DhcpServer_Configuration(Resource):
    @config_ns.response(200, 'Dhcp server configuration retrieved.')
    @config_ns.response(404, 'Dhcp server not found.')
    @config_ns.response(500, 'Internal Error.')
    def get(self):
        """
        Gets the configuration of the dhcp server
        """
        try:
            dhcpController = DhcpController()
            json_data = json.dumps(dhcpController.get_dhcp_server_configuration())
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except ValueError as ve:
            logging.debug(ve)
            return Response(status=404)
        except Exception as err:
            logging.debug(err)
            return Response(status=500)

@config_ns.route('/gatewayIp', methods=['GET','PUT'])
class DhcpServer_Configuration_Gateway(Resource):
    @config_ns.response(200, 'Gateway parameters retrieved.')
    @config_ns.response(404, 'Dhcp server not found.')
    @config_ns.response(500, 'Internal Error.')
    def get(self):
        """
        Gets the gateway parameters
        """
        try:
            dhcpController = DhcpController()
            json_data = json.dumps(dhcpController.get_dhcp_server_configuration_gateway())
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except ValueError as ve:
            logging.debug(ve)
            return Response(status=404)
        except Exception as err:
            logging.debug(err)
            return Response(status=500)

    @config_ns.param("Gateway parameters", "Gateway parameters to update", "body", type="string", required=True)
    @config_ns.response(202, 'Gateway parameters correctly updated.')
    @config_ns.response(404, 'Dhcp server not found.')
    @config_ns.response(400, 'Bad request.')
    @config_ns.response(500, 'Internal Error.')
    def put(self):
        """
        Update the gateway parameters
        """
        try:
            dhcpController = DhcpController()
            json_data = json.loads(request.data.decode())
            dhcpController.update_gateway(json_data)
            return Response(status=202)

        except ValueError as ve:
            logging.debug(ve)
            return Response(status=404)
        except Exception as err:
            logging.debug(err)
            return Response(status=500)

@config_ns.route('/gatewayIp/gatewayAddress', methods=['GET','PUT'])
class DhcpServer_Configuration_Gateway_Address(Resource):
    @config_ns.response(200, 'Gateway address retrieved.')
    @config_ns.response(404, 'Dhcp server not found.')
    @config_ns.response(500, 'Internal Error.')
    def get(self):
        """
        Gets the gateway address parameter
        """
        try:
            dhcpController = DhcpController()
            json_data = json.dumps(dhcpController.get_dhcp_server_configuration_gateway_address())
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except ValueError as ve:
            logging.debug(ve)
            return Response(status=404)
        except Exception as err:
            logging.debug(err)
            return Response(status=500)

    @config_ns.param("Gateway address", "Gateway address to update", "body", type="string", required=True)
    @config_ns.response(202, 'Gateway address correctly updated.')
    @config_ns.response(404, 'Dhcp server not found.')
    @config_ns.response(400, 'Bad request.')
    @config_ns.response(500, 'Internal Error.')
    def put(self):
        """
        Update the gateway address parameter
        """
        try:
            dhcpController = DhcpController()
            json_data = request.data.decode()
            dhcpController.update_gateway_address(json_data)
            return Response(status=202)

        except ValueError as ve:
            logging.debug(ve)
            return Response(status=404)
        except Exception as err:
            logging.debug(err)
            return Response(status=500)

@config_ns.route('/gatewayIp/gatewayMask', methods=['GET','PUT'])
class DhcpServer_Configuration_Gateway_Netmask(Resource):
    @config_ns.response(200, 'Gateway netmask retrieved.')
    @config_ns.response(404, 'Dhcp server not found.')
    @config_ns.response(500, 'Internal Error.')
    def get(self):
        """
        Gets the gateway netmask parameter
        """
        try:
            dhcpController = DhcpController()
            json_data = json.dumps(dhcpController.get_dhcp_server_configuration_gateway_netmask())
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except ValueError as ve:
            logging.debug(ve)
            return Response(status=404)
        except Exception as err:
            logging.debug(err)
            return Response(status=500)

    @config_ns.param("Gateway netmask", "Gateway netmask to update", "body", type="string", required=True)
    @config_ns.response(202, 'Gateway netmask correctly updated.')
    @config_ns.response(404, 'Dhcp server not found.')
    @config_ns.response(400, 'Bad request.')
    @config_ns.response(500, 'Internal Error.')
    def put(self):
        """
        Update the netmask parameter
        """
        try:
            dhcpController = DhcpController()
            json_data = request.data.decode()
            dhcpController.update_gateway_netmask(json_data)
            return Response(status=202)

        except ValueError as ve:
            logging.debug(ve)
            return Response(status=404)
        except Exception as err:
            logging.debug(err)
            return Response(status=500)

@config_ns.route('/sections', methods=['GET','POST'])
@config_ns.route('/sections<id>', methods=['GET','PUT'])
class DhcpServer_Configuration_Section(Resource):
    @config_ns.param("Section", "Section to add", "body", type="string", required=True)
    @config_ns.response(202, 'Section correctly added.')
    @config_ns.response(404, 'Dhcp server not found.')
    @config_ns.response(400, 'Bad request.')
    @config_ns.response(500, 'Internal Error.')
    def post(self):
        """
        Add a section
        """
        try:
            dhcpController = DhcpController()
            json_data = json.loads(request.data.decode())
            dhcpController.add_section(json_data)
            return Response(status=202)

        except ValueError as ve:
            logging.debug(ve)
            return Response(status=404)
        except Exception as err:
            logging.debug(err)
            return Response(status=500)

    @config_ns.response(200, 'Section retrieved.')
    @config_ns.response(404, 'Dhcp server not found.')
    @config_ns.response(500, 'Internal Error.')
    def get(self, id=None):
        """
        Gets the section
        """
        try:
            dhcpController = DhcpController()
            if id is None:
                json_data = json.dumps(dhcpController.get_dhcp_server_configuration_sections())
            else:
                json_data = json.dumps(dhcpController.get_dhcp_server_configuration_section(id))
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except ValueError as ve:
            logging.debug(ve)
            return Response(status=404)
        except Exception as err:
            logging.debug(err)
            return Response(status=500)

    @config_ns.param("Section", "Section to update", "body", type="string", required=True)
    @config_ns.response(202, 'Section correctly updated.')
    @config_ns.response(404, 'Dhcp server not found.')
    @config_ns.response(400, 'Bad request.')
    @config_ns.response(500, 'Internal Error.')
    def put(self):
        """
        Update the section
        """
        try:
            dhcpController = DhcpController()
            json_data = json.loads(request.data.decode())
            dhcpController.update_section(json_data)
            return Response(status=202)

        except ValueError as ve:
            logging.debug(ve)
            return Response(status=404)
        except Exception as err:
            logging.debug(err)
            return Response(status=500)

@config_ns.route('/sections/<id>/sectionStartIp', methods=['PUT'])
class DhcpServer_Configuration_Section_EndIP(Resource):
    @config_ns.param("Section start ip", "Section start ip to update", "body", type="string", required=True)
    @config_ns.response(202, 'Section start ip correctly updated.')
    @config_ns.response(404, 'Dhcp server not found.')
    @config_ns.response(400, 'Bad request.')
    @config_ns.response(500, 'Internal Error.')
    def put(self, id):
        """
        Update the section start ip parameter
        """
        try:
            dhcpController = DhcpController()
            json_data = request.data.decode()
            dhcpController.update_section_start_ip(id, json_data)
            return Response(status=202)

        except ValueError as ve:
            logging.debug(ve)
            return Response(status=404)
        except Exception as err:
            logging.debug(err)
            return Response(status=500)

@config_ns.route('/sections/<id>/sectionEndIp', methods=['GET','PUT'])
class DhcpServer_Configuration_Section_EndIP(Resource):
    @config_ns.response(200, 'Section end ip retrieved.')
    @config_ns.response(404, 'Dhcp server not found.')
    @config_ns.response(500, 'Internal Error.')
    def get(self, id):
        """
        Gets the section end ip parameter
        """
        try:
            dhcpController = DhcpController()
            json_data = json.dumps(dhcpController.get_dhcp_server_configuration_section_end_ip(id))
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except ValueError as ve:
            logging.debug(ve)
            return Response(status=404)
        except Exception as err:
            logging.debug(err)
            return Response(status=500)

    @config_ns.param("Section end ip", "Section end ip to update", "body", type="string", required=True)
    @config_ns.response(202, 'Section end ip correctly updated.')
    @config_ns.response(404, 'Dhcp server not found.')
    @config_ns.response(400, 'Bad request.')
    @config_ns.response(500, 'Internal Error.')
    def put(self, id):
        """
        Update the section end ip parameter
        """
        try:
            dhcpController = DhcpController()
            json_data = request.data.decode()
            dhcpController.update_section_end_ip(id, json_data)
            return Response(status=202)

        except ValueError as ve:
            logging.debug(ve)
            return Response(status=404)
        except Exception as err:
            logging.debug(err)
            return Response(status=500)

@config_ns.route('/dns', methods=['GET','PUT'])
class DhcpServer_Configuration_Dns(Resource):
    @config_ns.response(200, 'Dns parameters retrieved.')
    @config_ns.response(404, 'Dhcp server not found.')
    @config_ns.response(500, 'Internal Error.')
    def get(self):
        """
        Gets the dns parameters
        """
        try:
            dhcpController = DhcpController()
            json_data = json.dumps(dhcpController.get_dhcp_server_configuration_dns())
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except ValueError as ve:
            logging.debug(ve)
            return Response(status=404)
        except Exception as err:
            logging.debug(err)
            return Response(status=500)

    @config_ns.param("Dns parameters", "Dns parameters to update", "body", type="string", required=True)
    @config_ns.response(202, 'Dns parameters correctly updated.')
    @config_ns.response(404, 'Dhcp server not found.')
    @config_ns.response(400, 'Bad request.')
    @config_ns.response(500, 'Internal Error.')
    def put(self):
        """
        Update the dns parameters
        """
        try:
            dhcpController = DhcpController()
            json_data = json.loads(request.data.decode())
            dhcpController.update_dns(json_data)
            return Response(status=202)

        except ValueError as ve:
            logging.debug(ve)
            return Response(status=404)
        except Exception as err:
            logging.debug(err)
            return Response(status=500)

@config_ns.route('/dns/primaryServer', methods=['GET','PUT'])
class DhcpServer_Configuration_Dns_PrimaryServer(Resource):
    @config_ns.response(200, 'Dns primary server retrieved.')
    @config_ns.response(404, 'Dhcp server not found.')
    @config_ns.response(500, 'Internal Error.')
    def get(self):
        """
        Gets the dns primary server parameter
        """
        try:
            dhcpController = DhcpController()
            json_data = json.dumps(dhcpController.get_dhcp_server_configuration_dns_primary_server())
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except ValueError as ve:
            logging.debug(ve)
            return Response(status=404)
        except Exception as err:
            logging.debug(err)
            return Response(status=500)

    @config_ns.param("Dns primary server", "Dns primary server to update", "body", type="string", required=True)
    @config_ns.response(202, 'Dns primary server correctly updated.')
    @config_ns.response(404, 'Dhcp server not found.')
    @config_ns.response(400, 'Bad request.')
    @config_ns.response(500, 'Internal Error.')
    def put(self):
        """
        Update the dns primary server parameter
        """
        try:
            dhcpController = DhcpController()
            json_data = request.data.decode()
            dhcpController.update_dns_primary_server(json_data)
            return Response(status=202)

        except ValueError as ve:
            logging.debug(ve)
            return Response(status=404)
        except Exception as err:
            logging.debug(err)
            return Response(status=500)

@config_ns.route('/dns/secondaryServer', methods=['GET','PUT'])
class DhcpServer_Configuration_Dns_SecondaryServer(Resource):
    @config_ns.response(200, 'Dns secondary server retrieved.')
    @config_ns.response(404, 'Dhcp server not found.')
    @config_ns.response(500, 'Internal Error.')
    def get(self):
        """
        Gets the dns secondary server parameter
        """
        try:
            dhcpController = DhcpController()
            json_data = json.dumps(dhcpController.get_dhcp_server_configuration_dns_secondary_server())
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except ValueError as ve:
            logging.debug(ve)
            return Response(status=404)
        except Exception as err:
            logging.debug(err)
            return Response(status=500)

    @config_ns.param("Dns secondary server", "Dns secondary server to update", "body", type="string", required=True)
    @config_ns.response(202, 'Dns secondary server correctly updated.')
    @config_ns.response(404, 'Dhcp server not found.')
    @config_ns.response(400, 'Bad request.')
    @config_ns.response(500, 'Internal Error.')
    def put(self):
        """
        Update the dns secondary server parameter
        """
        try:
            dhcpController = DhcpController()
            json_data = request.data.decode()
            dhcpController.update_dns_secondary_server(json_data)
            return Response(status=202)

        except ValueError as ve:
            logging.debug(ve)
            return Response(status=404)
        except Exception as err:
            logging.debug(err)
            return Response(status=500)

@config_ns.route('/dns/domainName', methods=['GET','PUT'])
class DhcpServer_Configuration_Dns_DomainName(Resource):
    @config_ns.response(200, 'Dns domain name retrieved.')
    @config_ns.response(404, 'Dhcp server not found.')
    @config_ns.response(500, 'Internal Error.')
    def get(self):
        """
        Gets the dns domain name parameter
        """
        try:
            dhcpController = DhcpController()
            json_data = json.dumps(dhcpController.get_dhcp_server_configuration_dns_domain_name())
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except ValueError as ve:
            logging.debug(ve)
            return Response(status=404)
        except Exception as err:
            logging.debug(err)
            return Response(status=500)

    @config_ns.param("Dns domain name", "Dns domain name to update", "body", type="string", required=True)
    @config_ns.response(202, 'Dns domain name correctly updated.')
    @config_ns.response(404, 'Dhcp server not found.')
    @config_ns.response(400, 'Bad request.')
    @config_ns.response(500, 'Internal Error.')
    def put(self):
        """
        Update the dns domain name parameter
        """
        try:
            dhcpController = DhcpController()
            json_data = request.data.decode()
            dhcpController.update_dns_domain_name(json_data)
            return Response(status=202)

        except ValueError as ve:
            logging.debug(ve)
            return Response(status=404)
        except Exception as err:
            logging.debug(err)
            return Response(status=500)

@config_ns.route('/defaultLeaseTime', methods=['GET','PUT'])
class DhcpServer_Configuration_DefaultLeaseTime(Resource):
    @config_ns.response(200, 'Default lease time retrieved.')
    @config_ns.response(404, 'Dhcp server not found.')
    @config_ns.response(500, 'Internal Error.')
    def get(self):
        """
        Gets the default lease time parameter
        """
        try:
            dhcpController = DhcpController()
            json_data = json.dumps(dhcpController.get_dhcp_server_configuration_default_lease_time())
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except ValueError as ve:
            logging.debug(ve)
            return Response(status=404)
        except Exception as err:
            logging.debug(err)
            return Response(status=500)

    @config_ns.param("Default lease time", "Default lease time to update", "body", type="string", required=True)
    @config_ns.response(202, 'Default lease time correctly updated.')
    @config_ns.response(404, 'Dhcp server not found.')
    @config_ns.response(400, 'Bad request.')
    @config_ns.response(500, 'Internal Error.')
    def put(self):
        """
        Update the default lease time parameter
        """
        try:
            dhcpController = DhcpController()
            json_data = request.data.decode()
            dhcpController.update_default_lease_time(json_data)
            return Response(status=202)

        except ValueError as ve:
            logging.debug(ve)
            return Response(status=404)
        except Exception as err:
            logging.debug(err)
            return Response(status=500)

@config_ns.route('/maxLeaseTime', methods=['GET','PUT'])
class DhcpServer_Configuration_MaxLeaseTime(Resource):
    @config_ns.response(200, 'Max lease time retrieved.')
    @config_ns.response(404, 'Dhcp server not found.')
    @config_ns.response(500, 'Internal Error.')
    def get(self):
        """
        Gets the max lease time parameter
        """
        try:
            dhcpController = DhcpController()
            json_data = json.dumps(dhcpController.get_dhcp_server_configuration_max_lease_time())
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except ValueError as ve:
            logging.debug(ve)
            return Response(status=404)
        except Exception as err:
            logging.debug(err)
            return Response(status=500)

    @config_ns.param("Max lease time", "Max lease time to update", "body", type="string", required=True)
    @config_ns.response(202, 'Max lease time correctly updated.')
    @config_ns.response(404, 'Dhcp server not found.')
    @config_ns.response(400, 'Bad request.')
    @config_ns.response(500, 'Internal Error.')
    def put(self):
        """
        Update the max lease time parameter
        """
        try:
            dhcpController = DhcpController()
            json_data = request.data.decode()
            dhcpController.update_max_lease_time(json_data)
            return Response(status=202)

        except ValueError as ve:
            logging.debug(ve)
            return Response(status=404)
        except Exception as err:
            logging.debug(err)
            return Response(status=500)
