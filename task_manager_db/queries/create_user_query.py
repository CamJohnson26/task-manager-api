# task_manager_db/queries/create_user_query.py

def create_user_query(connection_pool, auth0_id, email):
    conn = None
    try:
        conn = connection_pool.getconn()
        cursor = conn.cursor()
        
        # Insert the user into the database with approved=false
        cursor.execute("""
            INSERT INTO public.user (auth0_id, email, approved)
            VALUES (%s, %s, false)
            RETURNING auth0_id, id, email, approved;
        """, (auth0_id, email))
        
        # Get the newly created user
        new_user = cursor.fetchone()
        
        # Commit the transaction
        conn.commit()
        
        cursor.close()
        
        if new_user is not None:
            print(f"Created user with auth0_id {auth0_id}")
            return new_user
        else:
            print(f"Failed to create user with auth0_id {auth0_id}")
            return None
    except Exception as e:
        print(f"Error creating user: {e}")
        if conn:
            conn.rollback()
        return None
    finally:
        if conn:
            connection_pool.putconn(conn)