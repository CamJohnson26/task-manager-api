# worker_api/routes/delete_task.py

from flask import Blueprint, jsonify, g
from authlib.integrations.flask_oauth2 import current_token

from auth0.auth_protector import require_auth
from task_manager_db.db_actions import get_user_by_sub_db, delete_task_db

delete_task_bp = Blueprint('delete_task', __name__)


@delete_task_bp.route('/tasks/<task_id>', methods=['DELETE'])
@require_auth()
def delete_task(task_id):
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

    # Get the user_id from the user record
    user_id = user[1]  # Assuming the id is the second column in the user table

    # Delete the task
    success = delete_task_db(task_id, user_id)
    
    if not success:
        return jsonify({"error": "Failed to delete task. Task not found or does not belong to user."}), 404
    
    return jsonify({"message": "Task deleted successfully"}), 200  # 200 OK status code