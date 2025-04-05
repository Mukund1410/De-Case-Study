from db_connection import connect_db

def register_user(name, email, password, role):
    conn = connect_db()
    cursor = conn.cursor()
    query = "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)"
    values = (name, email, password, role)
    cursor.execute(query, values)
    conn.commit()
    print("User registered successfully!")
    conn.close()

def login_user(email, password):
    conn = connect_db()
    cursor = conn.cursor()
    query = "SELECT id, name, role FROM users WHERE email = %s AND password = %s"
    cursor.execute(query, (email, password))
    user = cursor.fetchone()
    conn.close()
    return user  # Returns (id, role) or None

