# routes/get_route.py

from flask import Blueprint

from auth0.auth_protector import require_auth
from task_manager_db.db_actions import get_entity_db

get_entity_bp = Blueprint('entity', __name__)


@get_entity_bp.route('/entity')
@require_auth()
def get_entity():
    return get_entity_db()