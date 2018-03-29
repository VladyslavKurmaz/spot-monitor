from flask import Flask

app = Flask(__name__)

app.config.from_object('conf')

# from deformable_detector.controller import detector
from retina_detector.controller import detector

app.register_blueprint(detector)

