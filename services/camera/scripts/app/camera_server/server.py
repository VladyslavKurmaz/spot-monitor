from flask import Blueprint, request, jsonify
from flask_cors import CORS
from flask_restful import Api, Resource

from .src.camera_server import CameraManager

manager = CameraManager()

camera_server = Blueprint('camera_server', __name__)

errors = {
    'NotFound':
        {
            'code': False,
            'message': "404. Resource not found. Try /cameras /cameras/<int:id>",
            'data': []
        }
}

api = Api(camera_server, catch_all_404s=True, errors=errors)

CORS(camera_server)


def construct_response(code, message, data):
    return {"code": code, "message": message, "data": data}


class CameraAPI(Resource):
    """
        API for single camera management
    """
    def get(self, idf):
        ret = manager.get_camera(idf)
        if ret is None:
            response = jsonify(construct_response(False, "No such camera", []))
            response.status_code = 404
        else:
            response = jsonify(construct_response(True, "Success", [ret]))
            response.status_code = 200

        return response

    def delete(self, idf):
        ret, obj = manager.delete_camera(idf)
        if ret:
            response = jsonify(construct_response(True, "Deleted", [obj]))
            response.status_code = 200
        else:
            response = jsonify(construct_response(False, "No such camera", []))
            response.status_code = 404

        return response

    def put(self, idf):
        # TODO: implement put request
        response = jsonify(construct_response(False, "NotImplemented", [idf]))
        response.status_code = 404
        return response

    def patch(self, idf):
        # TODO: implement patch request
        response = jsonify(construct_response(False, "NotImplemented", [idf]))
        response.status_code = 404
        return response


class CamerasAPI(Resource):
    """
        API for batch camera management
    """
    def get(self):
        cam_list = manager.get_cameras()
        response = jsonify(construct_response(True, "Success", cam_list))
        response.status_code = 200
        return response

    def post(self):
        camera_conf = request.json
        ret, cam = manager.add_camera(camera_conf)
        if ret:
            response = jsonify(construct_response(True, "Camera added", [cam]))
            response.status_code = 201
        else:
            response = jsonify(construct_response(False, "Camera already exists", [cam]))
            response.status_code = 404
        return response


api.add_resource(CameraAPI, '/cameras/<int:idf>')
api.add_resource(CamerasAPI, '/cameras', '/cameras/')


