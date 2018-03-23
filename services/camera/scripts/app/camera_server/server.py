from flask import Blueprint, request, jsonify
from flask_cors import CORS
from flask_restful import Api, Resource

from .src.camera_server import CameraManager

manager = CameraManager()

camera_server = Blueprint('camera_server', __name__)

api = Api(camera_server, catch_all_404s=True)

CORS(camera_server)


class CameraAPI(Resource):
    """
        API for single camera management
    """
    def get(self, idf):
        ret = manager.get_camera(str(idf))
        if ret is None:
            return jsonify({"Camera": ["No such camera", False, {}]})
        else:
            return jsonify({"Camera": ["Success", True, manager.get_camera(idf)]})

    def delete(self, idf):
        ret = manager.delete_camera(idf)
        if ret:
            return jsonify({"Camera": ["Deleted", True, idf]})
        else:
            return jsonify({"Camera": ["No such camera", False, idf]})

    def put(self, idf):
        # TODO: implement put request
        return jsonify({"Camera": ["NotImplemented", False, idf]})

    def patch(self, idf):
        # TODO: implement patch request
        return jsonify({"Camera": ["NotImplemented", False, idf]})


class CamerasAPI(Resource):
    """
        API for batch camera management
    """
    def get(self):
        cam_list = manager.get_cameras()
        return jsonify(cam_list)

    def post(self):
        camera_conf = request.json
        ret = manager.add_camera(camera_conf)
        if ret:
            return jsonify({"Camera": ["Success", True, camera_conf['ip']]})
        else:
            return jsonify({"Camera": ["Already exists", False, camera_conf['ip']]})


api.add_resource(CameraAPI, '/cameras/<string:idf>')
api.add_resource(CamerasAPI, '/cameras', '/cameras/')


