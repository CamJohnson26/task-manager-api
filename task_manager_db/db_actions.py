# MY_DB/db_actions.py
from dotenv import load_dotenv

import os

from task_manager_db.queries.get_entity_query import get_entity_query
from task_manager_db.queries.get_user_by_sub_query import get_user_by_email_query
from task_manager_db.queries.get_tasks_by_user_id_query import get_tasks_by_user_id_query
from task_manager_db.queries.create_task_query import create_task_query
from task_manager_db.queries.update_task_query import update_task_query

from psycopg2 import pool

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

connection_pool = pool.SimpleConnectionPool(
    1,      # Minimum number of connections
    10,     # Maximum number of connections
    DATABASE_URL
)


def get_entity_db():
    return get_entity_query(connection_pool)


def get_user_by_sub_db(email):
    return get_user_by_email_query(connection_pool, email)


def get_tasks_by_user_id_db(user_id):
    return get_tasks_by_user_id_query(connection_pool, user_id)


def create_task_db(user_id, title, description, task_type, due_date, priority, status, effort, percent_completed):
    return create_task_query(connection_pool, user_id, title, description, task_type, due_date, priority, status, effort, percent_completed)


def update_task_db(task_id, user_id, title, description, task_type, due_date, priority, status, effort, percent_completed):
    return update_task_query(connection_pool, task_id, user_id, title, description, task_type, due_date, priority, status, effort, percent_completed)
