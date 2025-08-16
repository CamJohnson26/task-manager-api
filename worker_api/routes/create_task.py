# worker_api/routes/create_task.py

from flask import Blueprint, jsonify, request, g
from authlib.integrations.flask_oauth2 import current_token

from auth0.auth_protector import require_auth
from task_manager_db.db_actions import get_user_by_sub_db, create_task_db

create_task_bp = Blueprint('create_task', __name__)


@create_task_bp.route('/tasks', methods=['POST'])
@require_auth()
def create_task():
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
    interval = data.get('interval')  # No default for interval

    # Create the task
    new_task = create_task_db(
        user_id, title, description, task_type, due_date, priority, status, effort, percent_completed, interval
    )

    if not new_task:
        return jsonify({"error": "Failed to create task"}), 500

    # Convert the task tuple to a dictionary
    task_dict = {
        "id": new_task[0],
        "user_id": new_task[1],
        "title": new_task[2],
        "description": new_task[3],
        "type": new_task[4],
        "due_date": new_task[5],
        "priority": new_task[6],
        "status": new_task[7],
        "effort": new_task[8],
        "percent_completed": new_task[9]
    }

    # Add completed_at field if it exists
    if len(new_task) > 10 and new_task[10] is not None:
        task_dict["completed_at"] = new_task[10]

    # Add interval field if it exists
    if len(new_task) > 11 and new_task[11] is not None:
        task_dict["interval"] = new_task[11]

    return jsonify(task_dict), 201  # 201 Created status code
