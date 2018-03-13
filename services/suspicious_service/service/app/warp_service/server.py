from flask import Blueprint, request, jsonify

from src.monitor import SpotMonitor


suspisious_detector = Blueprint('suspisious_detector', __name__)

pipelines = {}


@suspisious_detector.route('/detect_susp', methods=['POST'])
def detect_susp():
    cam_id, img = request.data['cam_id'], request.data['img']
    if cam_id not in pipelines.keys():
        pipelines[cam_id] = SpotMonitor(cam_id)
    else:
        pipelines[cam_id].process(img)

    return jsonify("Processed")


@suspisious_detector.route('/get_suspicious', methods=['GET'])
def get_suspicous():
    cam_id = request.data['cam_id']
    if cam_id not in pipelines.keys():
        return jsonify("No such cam_id")
    else:
        return jsonify(pipelines[cam_id].suspicious_regions)
