from flask import Flask

app = Flask(__name__)

app.config.from_object('conf')

from .warp_service.server import suspicious

app.register_blueprint(suspicious)

