# worker_api/routes/get_me.py

from flask import Blueprint, jsonify, g

from auth0.auth_protector import require_auth
from task_manager_db.db_actions import get_user_by_sub_db, create_user_db
from authlib.integrations.flask_oauth2 import current_token

get_me_bp = Blueprint('me', __name__)


@get_me_bp.route('/me')
@require_auth()
def get_me():
    # Get the authenticated user's email from the token claims
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

    # If user doesn't exist, create a new user with approved=false
    if not user:
        # Try to get email from token
        email = None
        try:
            if hasattr(current_token, 'email'):
                email = current_token.get("email")
        except Exception:
            pass

        # If email is not available, use a placeholder with the sub
        if not email:
            email = f"{sub}@placeholder.com"

        # Create the user
        user = create_user_db(sub, email)

        if not user:
            return jsonify({"error": "Failed to create user"}), 500

    return jsonify(user)
