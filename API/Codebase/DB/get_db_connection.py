'''
import mariadb

def get_db_connection():
    try:
        conn = mariadb.connect(
            host="localhost",
            user="root",
            password="pass123",
            database="flask_db"
        )
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        return None
'''