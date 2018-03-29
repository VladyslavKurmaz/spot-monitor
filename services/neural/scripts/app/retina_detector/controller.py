import logging
from flask import Blueprint, request, jsonify

import cv2
import numpy as np

from detector.retina_detector import RetinaDetector

logger = logging.getLogger('gunicorn.error')

detector = Blueprint('detector', __name__)

deformable_detector = RetinaDetector()


@detector.route('/detect', methods=['POST'])
def detect():
    nparr = np.frombuffer(request.data, np.uint8)
    im = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    res = deformable_detector.predict(im)
    logger.debug("[DETECTOR] {}".format(res))
    return jsonify(res)
