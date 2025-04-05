from db_connection import connect_db

def add_room(room_type, price):
    conn = connect_db()
    cursor = conn.cursor()

    query = "INSERT INTO rooms (room_type, price, available) VALUES (%s, %s, TRUE)"
    cursor.execute(query, (room_type, price))

    conn.commit()
    conn.close()
    print(f"Room of type {room_type} added successfully!")

from db_connection import connect_db

def remove_user(email):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        # First, check if the user exists
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user:
            cursor.execute("DELETE FROM users WHERE email = %s", (email,))
            conn.commit()
            print(f"User with email {email} has been removed.")
        else:
            print("User not found.")
    except Exception as e:
        print("Error while removing user:", e)
    finally:
        conn.close()

def view_rooms():
    conn = connect_db()
    cursor = conn.cursor()

    query = "SELECT id, room_type, price, available FROM rooms"
    cursor.execute(query)
    rooms = cursor.fetchall()

    conn.close()

    if rooms:
        print("\nAvailable Rooms:")
        print("ID | Type | Price | Available")
        print("---------------------------------")
        for room in rooms:
            print(f"{room[0]} | {room[1]} | {room[2]} | {'Yes' if room[3] else 'No'}")
    else:
        print("No rooms available.")
