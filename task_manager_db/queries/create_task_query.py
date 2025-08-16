# task_manager_db/queries/create_task_query.py

def create_task_query(connection_pool, user_id, title, description, task_type, due_date, priority, status, effort, percent_completed, interval=None):
    conn = None
    try:
        conn = connection_pool.getconn()
        cursor = conn.cursor()

        # Insert the task into the database
        cursor.execute("""
            INSERT INTO public.task (
                user_id, title, description, type, due_date, priority, status, effort, percent_completed, interval
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            ) RETURNING id, user_id, title, description, type, due_date, priority, status, effort, percent_completed, interval;
        """, (user_id, title, description, task_type, due_date, priority, status, effort, percent_completed, interval))

        # Get the newly created task
        new_task = cursor.fetchone()

        # Commit the transaction
        conn.commit()

        cursor.close()

        if new_task is not None:
            print(f"Created task with id {new_task[0]} for user {user_id}")
            return new_task
        else:
            print(f"Failed to create task for user {user_id}")
            return None
    except Exception as e:
        print(f"Error creating task: {e}")
        if conn:
            conn.rollback()
        return None
    finally:
        if conn:
            connection_pool.putconn(conn)
