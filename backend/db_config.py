from dotenv import load_dotenv
import mysql.connector
import os

# Load environment variables mula sa .env file
load_dotenv()

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "localhost"),
            port=int(os.getenv("MYSQL_PORT", 3306)),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", "@SorsuBC#404"),
            database=os.getenv("MYSQL_DATABASE", "medherbs_db")
        )
        print("✅ Database connection successful!")
        return connection
    except mysql.connector.Error as err:
        print(f"❌ Error connecting to database: {err}")
        return None