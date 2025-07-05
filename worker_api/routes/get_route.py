# routes/get_route.py

from flask import Blueprint, jsonify
from authlib.integrations.flask_oauth2 import current_token

from auth0.auth_protector import require_auth
from task_manager_db.db_actions import get_user_by_sub_db

get_route_bp = Blueprint('home', __name__)


@get_route_bp.route('/')
@require_auth()
def get_route():
    # Get the authenticated user's sub from the token claims
    try:
        # Try to access the token directly
        if hasattr(current_token, 'sub'):
            sub = current_token.get("sub")
        else:
            return jsonify({"error": "Authentication information not found"}), 401
    except Exception as e:
        return jsonify({"error": f"Error accessing token: {str(e)}"}), 401

    if not sub:
        return jsonify({"error": "Sub not found in token"}), 400

    # Get the user from the database
    user = get_user_by_sub_db(sub)

    if not user:
        return jsonify({"error": "User not found"}), 404

    # Check if the user is approved
    if not user[4]:  # user[4] is the approved field
        return jsonify({"error": "User not approved. Please contact an administrator."}), 403

    return "Hello World!"
