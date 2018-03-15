import json

from flask import Blueprint, request, jsonify


from src.monitor import SpotMonitor


suspicious = Blueprint('suspicious', __name__)

pipelines = {}


@suspicious.route('/detect_susp', methods=['POST'])
def detect_susp():
    cam_id = json.loads(request.files['json'].read())['cam_id']
    im = request.files['img'].read()
    print(cam_id)
    if cam_id not in pipelines.keys():
        pipelines[cam_id] = SpotMonitor(cam_id)

    pipelines[cam_id].process(im)

    return jsonify("Processed")


@suspicious.route('/get_suspicious', methods=['GET'])
def get_suspicous():
    cam_id = json.loads(request.data)['cam_id']
    if cam_id not in pipelines.keys():
        return jsonify("No such cam_id")
    else:
        return jsonify(pipelines[cam_id].suspicious_regions)
