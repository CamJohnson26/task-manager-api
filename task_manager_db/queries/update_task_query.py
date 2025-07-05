# task_manager_db/queries/update_task_query.py

def update_task_query(connection_pool, task_id, user_id, title, description, task_type, due_date, priority, status, effort, percent_completed):
    conn = None
    try:
        conn = connection_pool.getconn()
        cursor = conn.cursor()
        
        # First, verify that the task belongs to the user
        cursor.execute("""
            SELECT id FROM public.task WHERE id = %s AND user_id = %s;
        """, (task_id, user_id))
        
        existing_task = cursor.fetchone()
        
        if not existing_task:
            print(f"Task {task_id} not found or does not belong to user {user_id}")
            return None
        
        # Update the task in the database
        cursor.execute("""
            UPDATE public.task SET
                title = %s,
                description = %s,
                type = %s,
                due_date = %s,
                priority = %s,
                status = %s,
                effort = %s,
                percent_completed = %s
            WHERE id = %s AND user_id = %s
            RETURNING id, user_id, title, description, type, due_date, priority, status, effort, percent_completed;
        """, (title, description, task_type, due_date, priority, status, effort, percent_completed, task_id, user_id))
        
        # Get the updated task
        updated_task = cursor.fetchone()
        
        # Commit the transaction
        conn.commit()
        
        cursor.close()
        
        if updated_task is not None:
            print(f"Updated task with id {updated_task[0]} for user {user_id}")
            return updated_task
        else:
            print(f"Failed to update task {task_id} for user {user_id}")
            return None
    except Exception as e:
        print(f"Error updating task: {e}")
        if conn:
            conn.rollback()
        return None
    finally:
        if conn:
            connection_pool.putconn(conn)