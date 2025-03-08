import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="@FaithGeloJohnVic#404",
        database="medherbs_user"
    )
    if conn.is_connected():
        print("✅ MySQL Connection Successful!")
except Exception as e:
    print("❌ Connection Failed:", e)
