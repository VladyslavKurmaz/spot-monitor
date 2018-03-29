from flask import Flask

app = Flask(__name__)

app.config.from_object('conf')

from api.api import detector_api

app.register_blueprint(detector_api)

