from flask import Blueprint, request, jsonify

from src.camera_server import CameraManager


manager = CameraManager()
camera_server = Blueprint('camera_server', __name__)


@camera_server.route('/cameras', methods=['GET', 'POST'])
def cameras():
    """
    Expected request data format:
        request.data = {
            "cameras":
            [
                {
                    'ip': "<ip_addr>",
                    'user': "<username>",
                    'password': "<password>",
                    'endpoint': "<ip_addr_where_to_send_frames>"
                }

            ]
        }
    """
    if request.method == 'GET':
        cam_list = manager.get_cameras()

        return jsonify(cam_list)
    elif request.method == 'POST':
        cameras_conf = request.data
        for camera in cameras_conf['cameras']:
            manager.add_camera(camera)

        return jsonify("Added")


