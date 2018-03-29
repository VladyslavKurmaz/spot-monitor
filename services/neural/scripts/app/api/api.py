from flask import Blueprint, request, jsonify

import cv2
import numpy as np

from src.detector.deformable_detector import DeformableDetector
# from src.detector.retina_detector import RetinaDetector

detector_api = Blueprint('detector_api', __name__)

detector = DeformableDetector()


@detector_api.route('/detect', methods=['POST'])
def detect():
    nparr = np.frombuffer(request.data, np.uint8)
    im = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    res = detector.predict(im)
    return jsonify(res)
