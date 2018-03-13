from flask import Blueprint, request, jsonify

import cv2
import numpy as np

from detector.deformable_detector import DeformableDetector

detector = Blueprint('detector', __name__)

deformable_detector = DeformableDetector()


@detector.route('/detect', methods=['POST'])
def detect():
    if request.headers['content-type'] == 'image/jpeg':
        nparr = np.frombuffer(request.data, np.uint8)
        im = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        res = deformable_detector.predict(im)
        return jsonify(res)
    else:
        return jsonify("[API] Incorrect content-type in headers '{}'. Must be 'image/jpeg'".format(
            request.headers['content-type']))
