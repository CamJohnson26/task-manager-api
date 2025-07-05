# task_manager_db/queries/get_all_users_query.py

def get_all_users_query(connection_pool):
    conn = None
    try:
        conn = connection_pool.getconn()
        cursor = conn.cursor()
        cursor.execute("""SELECT id, auth0_id, email, is_admin, approved FROM public.user;""")
        records = cursor.fetchall()
        cursor.close()
        if records is not None:
            print(f"Found {len(records)} users")
            return records
        else:
            print("Couldn't find any users")
            return []
    except Exception as e:
        print(e)
        return []
    finally:
        if conn:
            connection_pool.putconn(conn)
