from flask import request, Response
from flask_restplus import Resource
import json
import logging

from traffic_shaper.traffic_shaper_controller import TrafficShaperController
from traffic_shaper.rest_api.api import api

traffic_shaper_ns = api.namespace('traffic_shaper', 'Traffic Shaper Resource')
trafficShaperController = TrafficShaperController()

@traffic_shaper_ns.route("/bandwidth_shaping/<if_name>", methods=['PUT','GET','DELETE'])
@traffic_shaper_ns.route("/bandwidth_shaping", methods=['POST','GET'])
class TrafficShaper_Configuration(Resource):
    @traffic_shaper_ns.param("Bandwidth configuration", "Bandwidth configuration", "body", type="string", required=True)
    @traffic_shaper_ns.response(200, 'Bandwitdh shaping started.')
    @traffic_shaper_ns.response(400, 'Bad request.')
    @traffic_shaper_ns.response(500, 'Internal Error.')
    def post(self):
        """
        Start bandwitdh shaping
        """
        try:
            #trafficShaperController = TrafficShaperController()
            json_data = json.loads(request.data.decode())
            resp_data = trafficShaperController.start_bandwitdh_shaping(json_data)
            resp = Response(resp_data, status=200, mimetype="application/text")
            return resp

        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

    @traffic_shaper_ns.param("Interface name", "Interface name", "body", type="string", required=True)
    @traffic_shaper_ns.response(200, 'Bandwitdh shaping configuration updated.')
    @traffic_shaper_ns.response(404, 'Interface not found.')
    @traffic_shaper_ns.response(400, 'Bad request.')
    @traffic_shaper_ns.response(500, 'Internal Error.')
    def put(self, if_name):
        """
        Update bandwitdh shaping configuration
        """
        try:
            #trafficShaperController = TrafficShaperController()
            json_data = json.loads(request.data.decode())
            trafficShaperController.start_bandwitdh_shaping(json_data)
            return Response(status=200)


        except ValueError as ve:
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

    @traffic_shaper_ns.param("Interface name", "Interface name", "body", type="string", required=True)
    @traffic_shaper_ns.response(200, 'Bandwitdh shaping stopped.')
    @traffic_shaper_ns.response(404, 'Interface not found.')
    @traffic_shaper_ns.response(400, 'Bad request.')
    @traffic_shaper_ns.response(500, 'Internal Error.')
    def delete(self, if_name):
        """
        Stop bandwitdh shaping
        """
        try:
            #trafficShaperController = TrafficShaperController()
            trafficShaperController.stop_bandwitdh_shaping(if_name)
            return Response(status=200)


        except ValueError as ve:
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")

    @traffic_shaper_ns.response(200, 'Status retrieved.')
    @traffic_shaper_ns.response(404, 'Interface not found.')
    @traffic_shaper_ns.response(500, 'Internal Error.')
    def get(self, if_name=None):
        """
        Get the a traffic shapher status
        """
        try:
            #trafficShaperController = TrafficShaperController()
            if if_name is not None:
                json_data = json.dumps(trafficShaperController.get_traffic_shaper(if_name))
            else:
                json_data = json.dumps(trafficShaperController.get_all_traffic_shapers())
            resp = Response(json_data, status=200, mimetype="application/json")
            return resp

        except ValueError as ve:
            return Response(json.dumps(str(ve)), status=404, mimetype="application/json")
        except Exception as err:
            return Response(json.dumps(str(err)), status=500, mimetype="application/json")


