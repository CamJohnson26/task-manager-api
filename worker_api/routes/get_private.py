# worker_api/routes/get_private.py
from flask import Blueprint, jsonify

from auth0.auth_protector import require_auth

get_private_bp = Blueprint('get_private', __name__)


@get_private_bp.route('/private')
@require_auth()
def get_private():
    return 'Hello, World! (shhh)'
