from flask import Flask

app = Flask(__name__)

app.config.from_object('conf')

from api.api import detector

app.register_blueprint(detector)

