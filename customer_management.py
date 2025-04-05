from db_connection import connect_db
from datetime import datetime

def view_available_rooms():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, room_type, price FROM rooms WHERE available = TRUE")
    rooms = cursor.fetchall()
    conn.close()

    if rooms:
        print("\nAvailable Rooms:")
        print("ID | Type | Price")
        for room in rooms:
            print(f"{room[0]} | {room[1]} | ₹{room[2]}")
    else:
        print("No available rooms.")

def book_room(user_id):
    conn = connect_db()
    cursor = conn.cursor()

    room_type = input("Enter room type (single/double/suite): ").strip().lower()
    cursor.execute("SELECT id FROM rooms WHERE room_type = %s AND available = TRUE LIMIT 1", (room_type,))
    room = cursor.fetchone()

    if not room:
        print("No available room of that type.")
        conn.close()
        return

    room_id = room[0]
    checkin_datetime = datetime.now()

    cursor.execute("""
        INSERT INTO bookings (user_id, room_type, check_in, room_id)
        VALUES (%s, %s, %s, %s)
    """, (user_id, room_type, checkin_datetime, room_id))

    cursor.execute("UPDATE rooms SET available = FALSE WHERE id = %s", (room_id,))
    conn.commit()

    print(f"Room booked successfully! Your Room ID is: {room_id}")
    conn.close()
    
    
    
def checkout_room(user_id):
    conn = connect_db()
    cursor = conn.cursor()

    room_id = input("Enter Room ID to checkout: ").strip()
    cursor.execute("""
        SELECT id, room_type, check_in FROM bookings
        WHERE user_id = %s AND check_out IS NULL AND room_id = %s
    """, (user_id, room_id))
    booking = cursor.fetchone()

    if not booking:
        print("No active booking found for this room.")
        conn.close()
        return

    booking_id, room_type, checkin = booking
    now = datetime.now()
    duration_days = (now.date() - checkin.date()).days or 1

    if room_type == "single":
        rate = 1000
    elif room_type == "double":
        rate = 2000
    else:
        rate = 5000

    total_price = duration_days * rate

    # Check duplicate payment
    cursor.execute("SELECT id FROM payments WHERE booking_id = %s", (booking_id,))
    if cursor.fetchone():
        print("⚠️ Payment already done for this booking.")
        conn.close()
        return

    print(f"You stayed for {duration_days} day(s). Total to pay: ₹{total_price}")
    confirm = input("Proceed to pay? (yes/no): ").lower()
    if confirm == "yes":
        cursor.execute("UPDATE bookings SET check_out = %s WHERE id = %s", (now, booking_id))
        cursor.execute("""
            INSERT INTO payments (booking_id, user_id, amount, status)
            VALUES (%s, %s, %s, %s)
        """, (booking_id, user_id, total_price, "paid"))
        cursor.execute("UPDATE rooms SET available = TRUE WHERE id = %s", (room_id,))
        conn.commit()
        print("Checked out and payment done.")
    else:
        print(" Checkout cancelled.")

    conn.close()

def view_active_bookings(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT room_id, room_type, check_in FROM bookings
        WHERE user_id = %s AND check_out IS NULL
    """, (user_id,))
    active = cursor.fetchall()
    conn.close()

    if active:
        print("\n-> Active Bookings:")
        for row in active:
            print(f"Room ID: {row[0]} | Type: {row[1]} | Check-in: {row[2].strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        print("No active bookings.")

def view_booking_history(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT room_id, room_type, check_in, check_out FROM bookings
        WHERE user_id = %s AND check_out IS NOT NULL
    """, (user_id,))
    past = cursor.fetchall()
    conn.close()

    if past:
        print("\n📜 Booking History:")
        for row in past:
            check_in_time = row[2].strftime('%Y-%m-%d %H:%M:%S')
            check_out_time = row[3].strftime('%Y-%m-%d %H:%M:%S')
            print(f"Room ID: {row[0]} | Type: {row[1]} | From: {check_in_time} To: {check_out_time}")
    else:
        print("No past bookings.")
