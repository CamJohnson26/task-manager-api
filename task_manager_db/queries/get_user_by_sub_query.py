# task_manager_db/queries/get_user_by_sub_query.py

def get_user_by_email_query(connection_pool, sub):
    conn = None
    try:
        conn = connection_pool.getconn()
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM public.user WHERE auth0_id = %s;""", (sub,))
        record = cursor.fetchone()
        cursor.close()
        if record is not None:
            print(f"Found user with email {sub}")
            return record
        else:
            print(f"Couldn't find user with id {sub}")
            return None
    except Exception as e:
        print(e)
        return None
    finally:
        if conn:
            connection_pool.putconn(conn)