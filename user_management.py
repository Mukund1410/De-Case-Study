from db_connection import connect_db

def register_user(name, email, password, role):
    conn = connect_db()
    cursor = conn.cursor()

    query = "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)"
    try:
        cursor.execute(query, (name, email, password, role))
        conn.commit()
        print("Registration successful!")
    except:
        print("Email already registered.")

    conn.close()

def login_user(email, password):
    conn = connect_db()
    cursor = conn.cursor()

    query = "SELECT id, name, role FROM users WHERE email = %s AND password = %s"
    cursor.execute(query, (email, password))
    user = cursor.fetchone()

    conn.close()

    return user  # Returns (id, role) if valid, else None

