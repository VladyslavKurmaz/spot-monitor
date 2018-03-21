from flask import Flask

app = Flask(__name__)

app.config.from_object('conf')

from .camera_server.server import camera_server

app.register_blueprint(camera_server)
