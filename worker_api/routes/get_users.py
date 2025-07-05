# worker_api/routes/get_users.py

from flask import Blueprint, jsonify
from authlib.integrations.flask_oauth2 import current_token

from auth0.auth_protector import require_auth
from task_manager_db.db_actions import get_user_by_sub_db, get_all_users_db

get_users_bp = Blueprint('users', __name__)


@get_users_bp.route('/users')
@require_auth()
def get_users():
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

    # Check if the user is an admin
    # user[3] is the is_admin field
    if len(user) < 4 or not user[3]:
        return jsonify({"error": "Unauthorized. Admin access required."}), 403

    # Get all users from the database
    users = get_all_users_db()

    # Process users to return a list of dictionaries
    processed_users = []
    for user in users:
        user_dict = {
            "id": user[0],
            "auth0_id": user[1],
            "email": user[2],
            "approved": user[3]
        }
        processed_users.append(user_dict)

    return jsonify(processed_users)
