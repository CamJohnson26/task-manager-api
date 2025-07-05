# MY_DB/db_actions.py
from dotenv import load_dotenv

import os

from task_manager_db.queries.get_entity_query import get_entity_query
from task_manager_db.queries.get_user_by_sub_query import get_user_by_email_query

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
