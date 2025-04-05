import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sitaram_@1",
        database="hotel_db"
    )
