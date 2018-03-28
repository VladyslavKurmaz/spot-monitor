from flask import Blueprint, request, jsonify
from flask_cors import CORS
from flask_restful import Api, Resource

from src.spotmanager import SpotManager

monitor_manager = SpotManager()

suspicious = Blueprint('suspicious', __name__)

errors = {
    'NotFound':
        {
            'status': False,
            'message': "404. Resource not found. Try /suspicious /suspicious/<int:id>",
            'data': []
        }
}

api = Api(suspicious, catch_all_404s=True, errors=errors)

CORS(suspicious)


def construct_response(status, message, data, code):
    response = jsonify({"status": status, "message": message, "data": data})
    response.status_code = code
    return response


class SuspiciousAPI(Resource):
    """
        Api for suspicious service
    """
    def get(self, idf=None):
        if idf is None:
            all_regions = monitor_manager.get_all()
            return construct_response(True, "All suspicious region", all_regions, 200)
        else:
            ret, susp = monitor_manager.get_region(idf)
            if ret:
                return construct_response(True, "Suspicious region", [susp], 200)
            else:
                return construct_response(False, "No such monitor", [], 404)

    def post(self, idf=None):
        if idf is None:
            cam_id = request.json['cam_id']
            if monitor_manager.create_monitor(cam_id):
                return construct_response(True, "Monitor created", [{"endpoint": "/{}".format(cam_id)}], 201)
            else:
                return construct_response(False, "Monitor already exists", [], 400)
        else:
            im = request.data
            ret, susp = monitor_manager.process_img(idf, im)
            if ret:
                return construct_response(True, "Processed", [susp], 200)
            else:
                return construct_response(False, "No such monitor", [], 404)
            
    def delete(self, idf):
        ret, obj = monitor_manager.delete_monitor(idf)
        if ret:
            return construct_response(True, "Monitor deleted", [obj], 200)
        else:
            return construct_response(False, "No such monitor", [obj], 404)


api.add_resource(SuspiciousAPI, '/suspicious', '/suspicious/', '/suspicious/<int:idf>')
