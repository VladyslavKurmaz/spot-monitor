from flask import Blueprint, request, jsonify, Response
from flask_cors import CORS
from flask_restful import Api, Resource

from src.camera_manager import CameraManager

manager = CameraManager()

camera_server = Blueprint('camera_server', __name__)

errors = {
    'NotFound':
        {
            'status': False,
            'message': "404. Resource not found. Try /cameras /cameras/<int:idf> /stream/<int:idf>",
            'data': []
        }
}

api = Api(camera_server, catch_all_404s=True, errors=errors)

CORS(camera_server)


def construct_response(status, message, data, code):
    response = jsonify({"status": status, "message": message, "data": data})
    response.status_code = code
    return response


class CameraAPI(Resource):
    """
        API for single camera management
    """
    def get(self, idf):
        ret = manager.get_camera(idf)
        if ret is None:
            return construct_response(False, "No such camera", [], 404)
        else:
            return construct_response(True, "Success", [ret], 200)

    def delete(self, idf):
        ret, obj = manager.delete_camera(idf)
        if ret:
            return construct_response(True, "Deleted", [obj], 200)
        else:
            return construct_response(False, "No such camera", [], 404)

    def put(self, idf):
        # TODO: implement put request
        return construct_response(False, "NotImplemented", [idf], 404)

    def patch(self, idf):
        # TODO: implement patch request
        return construct_response(False, "NotImplemented", [idf], 404)


class CamerasAPI(Resource):
    """
        API for batch camera management
    """
    def get(self):
        cam_list = manager.get_cameras()
        return construct_response(True, "Success", cam_list, 200)

    def post(self):
        camera_conf = request.json
        ret, cam = manager.add_camera(camera_conf)
        if ret:
            return construct_response(True, "Camera added", [cam], 201)
        else:
            return construct_response(False, "Camera already exists", [cam], 400)


def gen(func):
    while True:
        frame = func()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


class StreamAPI(Resource):
    def get(self, idf):
        get_frame = manager.get_stream(idf)
        return Response(gen(get_frame), mimetype='multipart/x-mixed-replace; boundary=frame')


api.add_resource(CameraAPI, '/cameras/<int:idf>')
api.add_resource(CamerasAPI, '/cameras', '/cameras/')
api.add_resource(StreamAPI, '/stream/<int:idf>')


