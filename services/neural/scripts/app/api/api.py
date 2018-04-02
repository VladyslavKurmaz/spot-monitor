from flask import Blueprint, request, jsonify

import cv2
import numpy as np

# from src.detector.deformable_detector import DeformableDetector as Detector
from src.detector.retina_detector import RetinaDetector as Detector

detector_api = Blueprint('detector_api', __name__)

detector = Detector()


@detector_api.route('/detect', methods=['POST'])
def detect():
    nparr = np.frombuffer(request.data, np.uint8)
    im = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    res = detector.predict(im)
    return jsonify(res)
