# worker_api/routes/get_tasks.py

from flask import Blueprint, jsonify, g
from authlib.integrations.flask_oauth2 import current_token

from auth0.auth_protector import require_auth
from task_manager_db.db_actions import get_user_by_sub_db, get_tasks_by_user_id_db

get_tasks_bp = Blueprint('tasks', __name__)


@get_tasks_bp.route('/tasks')
@require_auth()
def get_tasks():
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
    user_id = user[1]  # Assuming the id is the first column in the user table

    # Get the tasks for the user
    tasks = get_tasks_by_user_id_db(user_id)

    # Process tasks to include last_completed only for recurring tasks
    processed_tasks = []
    for task in tasks:
        task_dict = {
            "id": task[0],
            "user_id": task[1],
            "title": task[2],
            "description": task[3],
            "type": task[4],
            "due_date": task[5],
            "priority": task[6],
            "status": task[7],
            "effort": task[8],
            "percent_completed": task[9]
        }

        # Add completed_at field if it exists
        if len(task) > 11 and task[11] is not None:
            task_dict["completed_at"] = task[11]

        # Add last_completed field only for recurring tasks
        if task[4] == "recurring" and task[10]:  # task[4] is type, task[10] is last_completed
            task_dict["last_completed"] = task[10]

        processed_tasks.append(task_dict)

    return jsonify(processed_tasks)
