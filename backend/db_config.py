import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="@SorsuBC#404",
        database="medherbs_db"
    )
