from flask import request, Response
from flask_restplus import Resource, fields
from rest_api.api import api
from cf_core.nfs_controller import NfsController
import json

nfs_ns = api.namespace('nfs', 'Network Functions Resource')

nfs_configuration_model = api.model('Server Configuration', {
    'dhcp': fields.String(required=True, description='Dhcp UUID', type='string'),
    'firewall': fields.String(required=True, description='Firewall UUID', type='string'),
})
@nfs_ns.route('', methods=['GET','PUT','POST'])
class Nfs(Resource):
    @nfs_ns.expect(nfs_configuration_model)
    @nfs_ns.response(202, 'Nfs successfully set.')
    @nfs_ns.response(400, 'Bad request.')
    @nfs_ns.response(500, 'Internal Error.')
    def post(self):
        """
        Set the nfs
        """
        try:
            json_data = json.loads(request.data.decode())
            NfsController().set_nfs(json_data)
            return Response(status=202)

        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

    @nfs_ns.response(200, 'Nfs retrieved.')
    @nfs_ns.response(500, 'Internal Error.')
    def get(self):
        """
        Get the nfs monitored
        """
        try:
            json_data = json.dumps(NfsController().get_nfs())
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except ValueError as ve:
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

@nfs_ns.route('/dhcp', methods=['GET','PUT'])
class Nfs_Dhcp(Resource):
    @nfs_ns.response(200, 'Dhcp id retrieved.')
    @nfs_ns.response(500, 'Internal Error.')
    def get(self):
        # Get the id of dhcp
        try:
            json_data = json.dumps(NfsController().get_dhcp_id())
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except ValueError as ve:
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

    @nfs_ns.param("Dhcp id", "Dhcp id to update", "body", type="string", required=True)
    @nfs_ns.response(202, 'Id correctly updated.')
    @nfs_ns.response(400, 'Bad request.')
    @nfs_ns.response(500, 'Internal Error.')
    def put(self):
        # Update the id of the dhcp
        try:
            id = request.data.decode()
            NfsController().set_dhcp_id(id)
            return Response(status=202)

        except ValueError as ve:
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

@nfs_ns.route('/firewall', methods=['GET','PUT'])
class Nfs_Firewall(Resource):
    @nfs_ns.response(200, 'Firewall id retrieved.')
    @nfs_ns.response(500, 'Internal Error.')
    def get(self):
        #Get the id of firewall
        try:
            json_data = json.dumps(NfsController().get_firewall_id())
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except ValueError as ve:
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

    @nfs_ns.param("Firewall id", "Firewall id to update", "body", type="string", required=True)
    @nfs_ns.response(202, 'Id correctly updated.')
    @nfs_ns.response(400, 'Bad request.')
    @nfs_ns.response(500, 'Internal Error.')
    def put(self):
        #Update the id of the firewall
        try:
            id = request.data.decode()
            NfsController().set_firewall_id(id)
            return Response(status=202)

        except ValueError as ve:
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")