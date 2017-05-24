import json
import logging

from flask import request, Response
from flask_restplus import Resource

from dhcp.controller.dhcp_controller import DhcpController
from dhcp.rest_api.api import api

dhcp_ns = api.namespace('dhcp', 'Dhcp Server Global Resource')

@dhcp_ns.route('', methods=['GET'])
class DhcpServer(Resource):
    @dhcp_ns.response(200, 'Dhcp status retrieved.')
    @dhcp_ns.response(500, 'Internal Error.')
    def get(self):
        """
        Gets the status of the dhcp server
        """
        try:
            dhcpController = DhcpController()
            json_data = json.dumps(dhcpController.get_dhcp_status())
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except Exception as err:
            logging.debug(err)
            return Response(status=500)

@dhcp_ns.route('/globalIpPool', methods=['GET'])
class DhcpServer_Configuration(Resource):
    @dhcp_ns.response(200, 'Dhcp server configuration retrieved.')
    @dhcp_ns.response(404, 'Dhcp server not found.')
    @dhcp_ns.response(500, 'Internal Error.')
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

@dhcp_ns.route('/globalIpPool/gatewayIp', methods=['GET','PUT'])
class DhcpServer_Configuration_Gateway(Resource):
    @dhcp_ns.response(200, 'Gateway parameters retrieved.')
    @dhcp_ns.response(404, 'Dhcp server not found.')
    @dhcp_ns.response(500, 'Internal Error.')
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

    @dhcp_ns.param("Gateway parameters", "Gateway parameters to update", "body", type="string", required=True)
    @dhcp_ns.response(202, 'Gateway parameters correctly updated.')
    @dhcp_ns.response(404, 'Dhcp server not found.')
    @dhcp_ns.response(400, 'Bad request.')
    @dhcp_ns.response(500, 'Internal Error.')
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

@dhcp_ns.route('/globalIpPool/gatewayIp/gatewayAddress', methods=['GET','PUT'])
class DhcpServer_Configuration_Gateway_Address(Resource):
    @dhcp_ns.response(200, 'Gateway address retrieved.')
    @dhcp_ns.response(404, 'Dhcp server not found.')
    @dhcp_ns.response(500, 'Internal Error.')
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

    @dhcp_ns.param("Gateway address", "Gateway address to update", "body", type="string", required=True)
    @dhcp_ns.response(202, 'Gateway address correctly updated.')
    @dhcp_ns.response(404, 'Dhcp server not found.')
    @dhcp_ns.response(400, 'Bad request.')
    @dhcp_ns.response(500, 'Internal Error.')
    def put(self):
        """
        Update the gateway address parameter
        """
        try:
            dhcpController = DhcpController()
            json_data = json.loads(request.data.decode())
            dhcpController.update_gateway_address(json_data)
            return Response(status=202)

        except ValueError as ve:
            logging.debug(ve)
            return Response(status=404)
        except Exception as err:
            logging.debug(err)
            return Response(status=500)

@dhcp_ns.route('/globalIpPool/gatewayIp/gatewayMask', methods=['GET','PUT'])
class DhcpServer_Configuration_Gateway_Netmask(Resource):
    @dhcp_ns.response(200, 'Gateway netmask retrieved.')
    @dhcp_ns.response(404, 'Dhcp server not found.')
    @dhcp_ns.response(500, 'Internal Error.')
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

    @dhcp_ns.param("Gateway netmask", "Gateway netmask to update", "body", type="string", required=True)
    @dhcp_ns.response(202, 'Gateway netmask correctly updated.')
    @dhcp_ns.response(404, 'Dhcp server not found.')
    @dhcp_ns.response(400, 'Bad request.')
    @dhcp_ns.response(500, 'Internal Error.')
    def put(self):
        """
        Update the netmask parameter
        """
        try:
            dhcpController = DhcpController()
            json_data = json.loads(request.data.decode())
            dhcpController.update_gateway_netmask(json_data)
            return Response(status=202)

        except ValueError as ve:
            logging.debug(ve)
            return Response(status=404)
        except Exception as err:
            logging.debug(err)
            return Response(status=500)

@dhcp_ns.route('/globalIpPool/sections', methods=['GET','POST'])
@dhcp_ns.route('/globalIpPool/sections<id>', methods=['GET','PUT'])
class DhcpServer_Configuration_Section(Resource):
    @dhcp_ns.param("Section", "Section to add", "body", type="string", required=True)
    @dhcp_ns.response(202, 'Section correctly added.')
    @dhcp_ns.response(404, 'Dhcp server not found.')
    @dhcp_ns.response(400, 'Bad request.')
    @dhcp_ns.response(500, 'Internal Error.')
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

    @dhcp_ns.response(200, 'Section retrieved.')
    @dhcp_ns.response(404, 'Dhcp server not found.')
    @dhcp_ns.response(500, 'Internal Error.')
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

    @dhcp_ns.param("Section", "Section to update", "body", type="string", required=True)
    @dhcp_ns.response(202, 'Section correctly updated.')
    @dhcp_ns.response(404, 'Dhcp server not found.')
    @dhcp_ns.response(400, 'Bad request.')
    @dhcp_ns.response(500, 'Internal Error.')
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

@dhcp_ns.route('/globalIpPool/sections/<id>/sectionStartIp', methods=['PUT'])
class DhcpServer_Configuration_Section_EndIP(Resource):
    @dhcp_ns.param("Section start ip", "Section start ip to update", "body", type="string", required=True)
    @dhcp_ns.response(202, 'Section start ip correctly updated.')
    @dhcp_ns.response(404, 'Dhcp server not found.')
    @dhcp_ns.response(400, 'Bad request.')
    @dhcp_ns.response(500, 'Internal Error.')
    def put(self, id):
        """
        Update the section start ip parameter
        """
        try:
            dhcpController = DhcpController()
            json_data = json.loads(request.data.decode())
            dhcpController.update_section_start_ip(id, json_data)
            return Response(status=202)

        except ValueError as ve:
            logging.debug(ve)
            return Response(status=404)
        except Exception as err:
            logging.debug(err)
            return Response(status=500)

@dhcp_ns.route('/globalIpPool/sections/<id>/sectionEndIp', methods=['GET','PUT'])
class DhcpServer_Configuration_Section_EndIP(Resource):
    @dhcp_ns.response(200, 'Section end ip retrieved.')
    @dhcp_ns.response(404, 'Dhcp server not found.')
    @dhcp_ns.response(500, 'Internal Error.')
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

    @dhcp_ns.param("Section end ip", "Section end ip to update", "body", type="string", required=True)
    @dhcp_ns.response(202, 'Section end ip correctly updated.')
    @dhcp_ns.response(404, 'Dhcp server not found.')
    @dhcp_ns.response(400, 'Bad request.')
    @dhcp_ns.response(500, 'Internal Error.')
    def put(self, id):
        """
        Update the section end ip parameter
        """
        try:
            dhcpController = DhcpController()
            json_data = json.loads(request.data.decode())
            dhcpController.update_section_end_ip(id, json_data)
            return Response(status=202)

        except ValueError as ve:
            logging.debug(ve)
            return Response(status=404)
        except Exception as err:
            logging.debug(err)
            return Response(status=500)

@dhcp_ns.route('/globalIpPool/dns', methods=['GET','PUT'])
class DhcpServer_Configuration_Dns(Resource):
    @dhcp_ns.response(200, 'Dns parameters retrieved.')
    @dhcp_ns.response(404, 'Dhcp server not found.')
    @dhcp_ns.response(500, 'Internal Error.')
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

    @dhcp_ns.param("Dns parameters", "Dns parameters to update", "body", type="string", required=True)
    @dhcp_ns.response(202, 'Dns parameters correctly updated.')
    @dhcp_ns.response(404, 'Dhcp server not found.')
    @dhcp_ns.response(400, 'Bad request.')
    @dhcp_ns.response(500, 'Internal Error.')
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

@dhcp_ns.route('/globalIpPool/dns/primaryServer', methods=['GET','PUT'])
class DhcpServer_Configuration_Dns_PrimaryServer(Resource):
    @dhcp_ns.response(200, 'Dns primary server retrieved.')
    @dhcp_ns.response(404, 'Dhcp server not found.')
    @dhcp_ns.response(500, 'Internal Error.')
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

    @dhcp_ns.param("Dns primary server", "Dns primary server to update", "body", type="string", required=True)
    @dhcp_ns.response(202, 'Dns primary server correctly updated.')
    @dhcp_ns.response(404, 'Dhcp server not found.')
    @dhcp_ns.response(400, 'Bad request.')
    @dhcp_ns.response(500, 'Internal Error.')
    def put(self):
        """
        Update the dns primary server parameter
        """
        try:
            dhcpController = DhcpController()
            json_data = json.loads(request.data.decode())
            dhcpController.update_dns_primary_server(json_data)
            return Response(status=202)

        except ValueError as ve:
            logging.debug(ve)
            return Response(status=404)
        except Exception as err:
            logging.debug(err)
            return Response(status=500)

@dhcp_ns.route('/globalIpPool/dns/secondaryServer', methods=['GET','PUT'])
class DhcpServer_Configuration_Dns_SecondaryServer(Resource):
    @dhcp_ns.response(200, 'Dns secondary server retrieved.')
    @dhcp_ns.response(404, 'Dhcp server not found.')
    @dhcp_ns.response(500, 'Internal Error.')
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

    @dhcp_ns.param("Dns secondary server", "Dns secondary server to update", "body", type="string", required=True)
    @dhcp_ns.response(202, 'Dns secondary server correctly updated.')
    @dhcp_ns.response(404, 'Dhcp server not found.')
    @dhcp_ns.response(400, 'Bad request.')
    @dhcp_ns.response(500, 'Internal Error.')
    def put(self):
        """
        Update the dns secondary server parameter
        """
        try:
            dhcpController = DhcpController()
            json_data = json.loads(request.data.decode())
            dhcpController.update_dns_secondary_server(json_data)
            return Response(status=202)

        except ValueError as ve:
            logging.debug(ve)
            return Response(status=404)
        except Exception as err:
            logging.debug(err)
            return Response(status=500)

@dhcp_ns.route('/globalIpPool/dns/domainName', methods=['GET','PUT'])
class DhcpServer_Configuration_Dns_DomainName(Resource):
    @dhcp_ns.response(200, 'Dns domain name retrieved.')
    @dhcp_ns.response(404, 'Dhcp server not found.')
    @dhcp_ns.response(500, 'Internal Error.')
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

    @dhcp_ns.param("Dns domain name", "Dns domain name to update", "body", type="string", required=True)
    @dhcp_ns.response(202, 'Dns domain name correctly updated.')
    @dhcp_ns.response(404, 'Dhcp server not found.')
    @dhcp_ns.response(400, 'Bad request.')
    @dhcp_ns.response(500, 'Internal Error.')
    def put(self):
        """
        Update the dns domain name parameter
        """
        try:
            dhcpController = DhcpController()
            json_data = json.loads(request.data.decode())
            dhcpController.update_dns_domain_name(json_data)
            return Response(status=202)

        except ValueError as ve:
            logging.debug(ve)
            return Response(status=404)
        except Exception as err:
            logging.debug(err)
            return Response(status=500)

@dhcp_ns.route('/globalIpPool/defaultLeaseTime', methods=['GET','PUT'])
class DhcpServer_Configuration_DefaultLeaseTime(Resource):
    @dhcp_ns.response(200, 'Default lease time retrieved.')
    @dhcp_ns.response(404, 'Dhcp server not found.')
    @dhcp_ns.response(500, 'Internal Error.')
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

    @dhcp_ns.param("Default lease time", "Default lease time to update", "body", type="string", required=True)
    @dhcp_ns.response(202, 'Default lease time correctly updated.')
    @dhcp_ns.response(404, 'Dhcp server not found.')
    @dhcp_ns.response(400, 'Bad request.')
    @dhcp_ns.response(500, 'Internal Error.')
    def put(self):
        """
        Update the default lease time parameter
        """
        try:
            dhcpController = DhcpController()
            json_data = json.loads(request.data.decode())
            dhcpController.update_default_lease_time(json_data)
            return Response(status=202)

        except ValueError as ve:
            logging.debug(ve)
            return Response(status=404)
        except Exception as err:
            logging.debug(err)
            return Response(status=500)

@dhcp_ns.route('/globalIpPool/maxLeaseTime', methods=['GET','PUT'])
class DhcpServer_Configuration_MaxLeaseTime(Resource):
    @dhcp_ns.response(200, 'Max lease time retrieved.')
    @dhcp_ns.response(404, 'Dhcp server not found.')
    @dhcp_ns.response(500, 'Internal Error.')
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

    @dhcp_ns.param("Max lease time", "Max lease time to update", "body", type="string", required=True)
    @dhcp_ns.response(202, 'Max lease time correctly updated.')
    @dhcp_ns.response(404, 'Dhcp server not found.')
    @dhcp_ns.response(400, 'Bad request.')
    @dhcp_ns.response(500, 'Internal Error.')
    def put(self):
        """
        Update the max lease time parameter
        """
        try:
            dhcpController = DhcpController()
            json_data = json.loads(request.data.decode())
            dhcpController.update_max_lease_time(json_data)
            return Response(status=202)

        except ValueError as ve:
            logging.debug(ve)
            return Response(status=404)
        except Exception as err:
            logging.debug(err)
            return Response(status=500)

@dhcp_ns.route('/clients', methods=['GET'])
@dhcp_ns.route('/clients/<id>', methods=['GET'])
class Client(Resource):
    @dhcp_ns.response(200, 'Client retrieved.')
    @dhcp_ns.response(404, 'Client not found.')
    @dhcp_ns.response(500, 'Internal Error.')
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
            logging.debug(ve)
            return Response(status=404)
        except Exception as err:
            logging.debug(err)
            return Response(status=500)

@dhcp_ns.route('/clients/<id>/ip_address', methods=['GET'])
class Client_IpAdress(Resource):
    @dhcp_ns.response(200, 'Client ip address retrieved.')
    @dhcp_ns.response(404, 'Client not found.')
    @dhcp_ns.response(500, 'Internal Error.')
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
            logging.debug(ve)
            return Response(status=404)
        except Exception as err:
            logging.debug(err)
            return Response(status=500)

@dhcp_ns.route('/clients/<id>/mac_address', methods=['GET'])
class Client_MacAdress(Resource):
    @dhcp_ns.response(200, 'Client mac address retrieved.')
    @dhcp_ns.response(404, 'Client not found.')
    @dhcp_ns.response(500, 'Internal Error.')
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
            logging.debug(ve)
            return Response(status=404)
        except Exception as err:
            logging.debug(err)
            return Response(status=500)

@dhcp_ns.route('/clients/<id>/hostname', methods=['GET'])
class Client_Hostname(Resource):
    @dhcp_ns.response(200, 'Client hostname retrieved.')
    @dhcp_ns.response(404, 'Client not found.')
    @dhcp_ns.response(500, 'Internal Error.')
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
            logging.debug(ve)
            return Response(status=404)
        except Exception as err:
            logging.debug(err)
            return Response(status=500)

@dhcp_ns.route('/clients/<id>/valid_until', methods=['GET'])
class Client_ValidUntil(Resource):
    @dhcp_ns.response(200, 'Client date validity retrieved.')
    @dhcp_ns.response(404, 'Client not found.')
    @dhcp_ns.response(500, 'Internal Error.')
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
            logging.debug(ve)
            return Response(status=404)
        except Exception as err:
            logging.debug(err)
            return Response(status=500)