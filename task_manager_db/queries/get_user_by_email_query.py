# task_manager_db/queries/get_user_by_email_query.py

def get_user_by_email_query(connection_pool, email):
    conn = None
    try:
        conn = connection_pool.getconn()
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM public.user WHERE email = %s;""", (email,))
        record = cursor.fetchone()
        cursor.close()
        if record is not None:
            print(f"Found user with email {email}")
            return record
        else:
            print(f"Couldn't find user with email {email}")
            return None
    except Exception as e:
        print(e)
        return None
    finally:
        if conn:
            connection_pool.putconn(conn)