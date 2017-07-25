from flask import request, Response
from flask_restplus import Resource
import json
import logging

from dhcp.dhcp_controller import DhcpController
from dhcp.rest_api.api import api

config_ns = api.namespace('dhcp', 'Dhcp Server Configuration Resource')

@config_ns.route('/server', methods=['GET'])
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
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

@config_ns.route('/server/defaultLeaseTime', methods=['GET','PUT'])
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
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

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
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

@config_ns.route('/server/maxLeaseTime', methods=['GET','PUT'])
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
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

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
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

@config_ns.route('/server/subnet', methods=['GET','PUT'])
class DhcpServer_Configuration_Subnet(Resource):
    @config_ns.response(200, 'Subnet retrieved.')
    @config_ns.response(404, 'Dhcp server not found.')
    @config_ns.response(500, 'Internal Error.')
    def get(self):
        """
        Gets the subnet parameter
        """
        try:
            dhcpController = DhcpController()
            json_data = json.dumps(dhcpController.get_dhcp_server_configuration_subnet())
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except ValueError as ve:
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

    @config_ns.param("Subnet", "Subnet to update", "body", type="string", required=True)
    @config_ns.response(202, 'Subnet correctly updated.')
    @config_ns.response(404, 'Dhcp server not found.')
    @config_ns.response(400, 'Bad request.')
    @config_ns.response(500, 'Internal Error.')
    def put(self):
        """
        Update the subnet parameter
        """
        try:
            dhcpController = DhcpController()
            json_data = request.data.decode()
            dhcpController.update_subnet(json_data)
            return Response(status=202)

        except ValueError as ve:
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

@config_ns.route('/server/subnetMask', methods=['GET','PUT'])
class DhcpServer_Configuration_SubnetMask(Resource):
    @config_ns.response(200, 'Subnet mask retrieved.')
    @config_ns.response(404, 'Dhcp server not found.')
    @config_ns.response(500, 'Internal Error.')
    def get(self):
        """
        Gets the subnet mask parameter
        """
        try:
            dhcpController = DhcpController()
            json_data = json.dumps(dhcpController.get_dhcp_server_configuration_subnet_mask())
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except ValueError as ve:
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

    @config_ns.param("Subnet mask", "Subnet mask to update", "body", type="string", required=True)
    @config_ns.response(202, 'Subnet mask correctly updated.')
    @config_ns.response(404, 'Dhcp server not found.')
    @config_ns.response(400, 'Bad request.')
    @config_ns.response(500, 'Internal Error.')
    def put(self):
        """
        Update the subnet mask parameter
        """
        try:
            dhcpController = DhcpController()
            json_data = request.data.decode()
            dhcpController.update_subnet_mask(json_data)
            return Response(status=202)

        except ValueError as ve:
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

@config_ns.route('/server/router', methods=['GET','PUT'])
class DhcpServer_Configuration_Router(Resource):
    @config_ns.response(200, 'Router retrieved.')
    @config_ns.response(404, 'Dhcp server not found.')
    @config_ns.response(500, 'Internal Error.')
    def get(self):
        """
        Gets the router parameter
        """
        try:
            dhcpController = DhcpController()
            json_data = json.dumps(dhcpController.get_dhcp_server_configuration_router())
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except ValueError as ve:
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

    @config_ns.param("Router", "Router to update", "body", type="string", required=True)
    @config_ns.response(202, 'Router correctly updated.')
    @config_ns.response(404, 'Dhcp server not found.')
    @config_ns.response(400, 'Bad request.')
    @config_ns.response(500, 'Internal Error.')
    def put(self):
        """
        Update the router parameter
        """
        try:
            dhcpController = DhcpController()
            json_data = request.data.decode()
            dhcpController.update_router(json_data)
            return Response(status=202)

        except ValueError as ve:
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

@config_ns.route('/server/dnsPrimaryServer', methods=['GET','PUT'])
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
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

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
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

@config_ns.route('/server/dnsSecondaryServer', methods=['GET','PUT'])
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
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

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
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

@config_ns.route('/server/dnsDomainName', methods=['GET','PUT'])
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
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

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
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

@config_ns.route('/server/sections', methods=['GET','POST'])
@config_ns.route('/server/sections<id>', methods=['GET','PUT'])
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
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

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
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

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
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

@config_ns.route('/server/sections/<id>/sectionStartIp', methods=['PUT'])
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
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

@config_ns.route('/server/sections/<id>/sectionEndIp', methods=['GET','PUT'])
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
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

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
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")