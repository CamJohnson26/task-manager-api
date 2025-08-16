# task_manager_db/queries/get_task_by_id_query.py

def get_task_by_id_query(connection_pool, task_id, user_id):
    conn = None
    try:
        conn = connection_pool.getconn()
        cursor = conn.cursor()
        
        # Query to get a specific task by ID and user_id (for security)
        cursor.execute("""
            SELECT 
                t.*,
                (
                    SELECT MAX(ce.completed_at)
                    FROM public.completion_event ce
                    WHERE ce.task_id = t.id
                ) as last_completed
            FROM public.task t
            WHERE t.id = %s AND t.user_id = %s;
        """, (task_id, user_id))
        
        record = cursor.fetchone()
        cursor.close()
        
        if record is not None:
            print(f"Found task {task_id} for user {user_id}")
            return record
        else:
            print(f"Couldn't find task {task_id} for user {user_id}")
            return None
    except Exception as e:
        print(f"Error getting task by ID: {e}")
        return None
    finally:
        if conn:
            connection_pool.putconn(conn)