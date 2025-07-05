# worker_api/routes/approve_user.py

from flask import Blueprint, jsonify
from authlib.integrations.flask_oauth2 import current_token

from auth0.auth_protector import require_auth
from task_manager_db.db_actions import get_user_by_sub_db, approve_user_db

approve_user_bp = Blueprint('approve_user', __name__)


@approve_user_bp.route('/users/<user_id>/approve', methods=['PUT'])
@require_auth()
def approve_user(user_id):
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

    # Check if the user is an admin (approved=true)
    # user[3] is the approved field
    if len(user) < 4 or not user[3]:
        return jsonify({"error": "Unauthorized. Admin access required."}), 403

    # Approve the user
    updated_user = approve_user_db(user_id)

    if not updated_user:
        return jsonify({"error": "Failed to approve user. User not found."}), 404

    # Convert the user tuple to a dictionary
    user_dict = {
        "id": updated_user[0],
        "auth0_id": updated_user[1],
        "email": updated_user[2],
        "approved": updated_user[3]
    }

    return jsonify(user_dict)