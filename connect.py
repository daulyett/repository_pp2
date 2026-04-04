import psycopg2
from config import host, database, user, password

def connect():
    try:
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        return conn
    except Exception as e:
        print("Connection error:", e)