# worker_api/routes/edit_task.py

from flask import Blueprint, jsonify, request, g
from authlib.integrations.flask_oauth2 import current_token

from auth0.auth_protector import require_auth
from task_manager_db.db_actions import get_user_by_sub_db, update_task_db

edit_task_bp = Blueprint('edit_task', __name__)


@edit_task_bp.route('/tasks/<task_id>', methods=['PUT'])
@require_auth()
def edit_task(task_id):
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

    # Get the task data from the request
    data = request.get_json()

    # Validate required fields
    required_fields = ['title', 'description', 'type']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # Extract task data with defaults for optional fields
    title = data['title']
    description = data['description']
    task_type = data['type']
    due_date = data.get('due_date')
    priority = data.get('priority', 1)  # Default priority is 1
    status = data.get('status', 'pending')  # Default status is pending
    effort = data.get('effort', 1)  # Default effort is 1
    percent_completed = data.get('percent_completed', 0.0)  # Default percent_completed is 0.0

    # Update the task
    updated_task = update_task_db(
        task_id, user_id, title, description, task_type, due_date, priority, status, effort, percent_completed
    )

    if not updated_task:
        return jsonify({"error": "Failed to update task. Task not found or does not belong to user."}), 404

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
        "percent_completed": updated_task[9]
    }

    return jsonify(task_dict), 200  # 200 OK status code
