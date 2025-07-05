# task_manager_db/queries/delete_task_query.py

def delete_task_query(connection_pool, task_id, user_id):
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
            return False
        
        # Delete the task from the database
        cursor.execute("""
            DELETE FROM public.task
            WHERE id = %s AND user_id = %s
            RETURNING id;
        """, (task_id, user_id))
        
        # Check if a row was deleted
        deleted_task = cursor.fetchone()
        
        # Commit the transaction
        conn.commit()
        
        cursor.close()
        
        if deleted_task is not None:
            print(f"Deleted task with id {deleted_task[0]} for user {user_id}")
            return True
        else:
            print(f"Failed to delete task {task_id} for user {user_id}")
            return False
    except Exception as e:
        print(f"Error deleting task: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            connection_pool.putconn(conn)