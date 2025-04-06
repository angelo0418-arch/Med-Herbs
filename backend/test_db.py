from config.db_config import get_db_connection

# ✅ Test database connection
conn = get_db_connection()
if conn is None:
    print("❌ Failed to connect to the database")
else:
    print("✅ Successfully connected to the database")

# Before executing SQL, ensure connection works
cursor = conn.cursor()
