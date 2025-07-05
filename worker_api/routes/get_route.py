# routes/get_route.py

from flask import Blueprint

from auth0.auth_protector import require_auth

get_route_bp = Blueprint('home', __name__)


@get_route_bp.route('/')
@require_auth()
def get_route():
    return "Hello World!"