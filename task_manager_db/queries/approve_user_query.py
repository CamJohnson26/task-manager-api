# task_manager_db/queries/approve_user_query.py

def approve_user_query(connection_pool, user_id):
    conn = None
    try:
        conn = connection_pool.getconn()
        cursor = conn.cursor()

        # Update the user's approved status to true
        cursor.execute("""
            UPDATE public.user
            SET approved = true
            WHERE id = %s
            RETURNING id, auth0_id, email, is_admin, approved;
        """, (user_id,))

        # Get the updated user
        updated_user = cursor.fetchone()

        # Commit the transaction
        conn.commit()

        cursor.close()

        if updated_user is not None:
            print(f"Approved user with id {user_id}")
            return updated_user
        else:
            print(f"Couldn't find user with id {user_id}")
            return None
    except Exception as e:
        print(f"Error approving user: {e}")
        if conn:
            conn.rollback()
        return None
    finally:
        if conn:
            connection_pool.putconn(conn)
