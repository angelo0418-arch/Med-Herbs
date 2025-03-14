import mysql.connector
import os

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", 3306)),  # Ensure it's an integer
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "@SorsuBC#404"),  # Consider securing this
        database=os.getenv("MYSQL_DATABASE", "medherbs_db")
    )
