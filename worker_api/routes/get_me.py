# worker_api/routes/get_me.py

from flask import Blueprint, jsonify, g

from auth0.auth_protector import require_auth
from task_manager_db.db_actions import get_user_by_email_db

get_me_bp = Blueprint('me', __name__)


@get_me_bp.route('/me')
@require_auth()
def get_me():
    # Get the authenticated user's email from the token claims
    # In Auth0, the email claim is typically available as 'email' in the token
    try:
        email = g.auth.claims.get('email')
    except AttributeError:
        return jsonify({"error": "Authentication claims not found"}), 401

    if not email:
        return jsonify({"error": "Email not found in token"}), 400
    
    # Get the user from the database
    user = get_user_by_email_db(email)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify(user)