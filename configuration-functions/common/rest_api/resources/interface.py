from flask import Response
from flask_restplus import Resource
from rest_api.api import api
from cf_core.management_interface_controller import ManagementInterfaceController
import json

interface_ns = api.namespace('interface_management', 'Interface Resource')
managementInterfaceController = ManagementInterfaceController()

@interface_ns.route('', methods=['GET'])
class InterfaceManagement(Resource):
    @interface_ns.response(200, 'Interfaces retrieved.')
    @interface_ns.response(500, 'Internal Error.')
    def get(self):
        """
        Gets the status of management interface
        """
        try:
            name_iface_management = managementInterfaceController.get_name_management_interface()
            json_data = json.dumps(managementInterfaceController.get_interface(name_iface_management))
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")