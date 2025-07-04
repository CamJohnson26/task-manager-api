# create_api.py

from flask import Flask
from flask_cors import CORS

from dotenv import load_dotenv
from os import getenv

from worker_api.routes.get_route import get_route_bp

load_dotenv()


def create_api():
    app = Flask(__name__)

    allowed_origins = getenv('ALLOWED_ORIGINS')
    CORS(app, origins=allowed_origins)

    app.register_blueprint(get_route_bp)

    return app
