# worker_api/routes/complete_task.py

from flask import Blueprint, jsonify, request
from authlib.integrations.flask_oauth2 import current_token
from datetime import datetime

from auth0.auth_protector import require_auth
from task_manager_db.db_actions import get_user_by_sub_db, get_task_by_id_db, update_task_db

complete_task_bp = Blueprint('complete_task', __name__)


@complete_task_bp.route('/tasks/<task_id>/complete', methods=['PUT'])
@require_auth()
def complete_task(task_id):
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

    # Get the user_id from the user record
    user_id = user[1]  # Assuming the id is the second column in the user table

    # Get the current task data from the database
    current_task = get_task_by_id_db(task_id, user_id)

    if not current_task:
        return jsonify({"error": "Task not found or does not belong to user."}), 404

    # Set the status to "completed" and percent_completed to 100.0
    status = "completed"
    percent_completed = 100.0

    # Use the current task data for all other fields
    title = current_task[2]  # Assuming title is the 3rd column (index 2)
    description = current_task[3]  # Assuming description is the 4th column (index 3)
    task_type = current_task[4]  # Assuming type is the 5th column (index 4)
    due_date = current_task[5]  # Assuming due_date is the 6th column (index 5)
    priority = current_task[6]  # Assuming priority is the 7th column (index 6)
    effort = current_task[8]  # Assuming effort is the 9th column (index 8)

    # Get the interval if it exists
    interval = None
    if len(current_task) > 12:
        interval = current_task[12]

    # Set the completed_at timestamp
    completed_at = datetime.now()

    # Update the task
    updated_task = update_task_db(
        task_id, user_id, title, description, task_type, due_date, priority, status, effort, percent_completed, completed_at, interval
    )

    if not updated_task:
        return jsonify({"error": "Failed to complete task. Task not found or does not belong to user."}), 404

    # Convert the task tuple to a dictionary
    task_dict = {
        "id": updated_task[0],
        "user_id": updated_task[1],
        "title": updated_task[2],
        "description": updated_task[3],
        "type": updated_task[4],
        "due_date": updated_task[5],
        "priority": updated_task[6],
        "status": updated_task[7],
        "effort": updated_task[8],
        "percent_completed": updated_task[9],
        "completed_at": updated_task[10]
    }

    # Add interval field if it exists
    if len(updated_task) > 11 and updated_task[11] is not None:
        task_dict["interval"] = updated_task[11]

    return jsonify(task_dict), 200  # 200 OK status code
