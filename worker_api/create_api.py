# create_api.py

from flask import Flask
from flask_cors import CORS

from dotenv import load_dotenv
from os import getenv

from worker_api.routes.get_entity import get_entity_bp
from worker_api.routes.get_private import get_private_bp
from worker_api.routes.get_route import get_route_bp
from worker_api.routes.get_me import get_me_bp
from worker_api.routes.get_tasks import get_tasks_bp
from worker_api.routes.create_task import create_task_bp

load_dotenv()


def create_api():
    app = Flask(__name__)

    allowed_origins = getenv('ALLOWED_ORIGINS')
    CORS(app, origins=allowed_origins)

    app.register_blueprint(get_route_bp)
    app.register_blueprint(get_private_bp)
    app.register_blueprint(get_entity_bp)
    app.register_blueprint(get_me_bp)
    app.register_blueprint(get_tasks_bp)
    app.register_blueprint(create_task_bp)

    return app
