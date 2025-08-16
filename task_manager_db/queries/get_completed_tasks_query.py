# task_manager_db/queries/get_completed_tasks_query.py

def get_completed_tasks_query(connection_pool, user_id):
    conn = None
    try:
        conn = connection_pool.getconn()
        cursor = conn.cursor()
        
        # Query to get completed tasks with their most recent completion event
        cursor.execute("""
            SELECT 
                t.*,
                (
                    SELECT MAX(ce.completed_at)
                    FROM public.completion_event ce
                    WHERE ce.task_id = t.id
                ) as last_completed
            FROM public.task t
            WHERE t.user_id = %s AND t.status = 'completed'
            ORDER BY t.due_date ASC;
        """, (user_id,))
        
        records = cursor.fetchall()
        cursor.close()
        
        if records is not None:
            print(f"Found {len(records)} completed tasks for user {user_id}")
            return records
        else:
            print(f"Couldn't find completed tasks for user {user_id}")
            return []
    except Exception as e:
        print(f"Error getting completed tasks: {e}")
        return []
    finally:
        if conn:
            connection_pool.putconn(conn)