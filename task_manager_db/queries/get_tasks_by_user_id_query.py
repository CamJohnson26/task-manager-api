# task_manager_db/queries/get_tasks_by_user_id_query.py

def get_tasks_by_user_id_query(connection_pool, user_id):
    conn = None
    try:
        conn = connection_pool.getconn()
        cursor = conn.cursor()
        
        # Query to get tasks with their most recent completion event for recurring tasks
        cursor.execute("""
            SELECT 
                t.*,
                (
                    SELECT MAX(ce.completed_at)
                    FROM public.completion_event ce
                    WHERE ce.task_id = t.id
                ) as last_completed
            FROM public.task t
            WHERE t.user_id = %s
            ORDER BY t.due_date ASC;
        """, (user_id,))
        
        records = cursor.fetchall()
        cursor.close()
        
        if records is not None:
            print(f"Found {len(records)} tasks for user {user_id}")
            return records
        else:
            print(f"Couldn't find tasks for user {user_id}")
            return []
    except Exception as e:
        print(e)
        return []
    finally:
        if conn:
            connection_pool.putconn(conn)