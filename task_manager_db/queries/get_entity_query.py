# task_manager_db/queries/get_entity_query.py

def get_entity_query(connection_pool):
    conn = None
    try:
        conn = connection_pool.getconn()
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM public.user;""")
        records = cursor.fetchall()
        cursor.close()
        if records is not None:
            print(f"Fetched {len(records)} records")
            return records
        else:
            print(f"Couldn't find")
            return None
    except Exception as e:
        print(e)
    finally:
        connection_pool.putconn(conn)
