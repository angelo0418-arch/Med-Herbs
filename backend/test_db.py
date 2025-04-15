from db_config import get_db_connection

conn = get_db_connection()
cursor = conn.cursor()

# Sample data para sa insert
user_id = 1  # Siguraduhing may user_id na ito sa `users` table
image_path = 'path/to/image.jpg'
identified_herb = 'Sample Herb'

# Insert data sa uploads table
cursor.execute(
    "INSERT INTO uploads (user_id, image_path, identified_herb) VALUES (%s, %s, %s)",
    (user_id, image_path, identified_herb)
)

# I-commit ang transaction
conn.commit()

# I-verify kung successful ang insert
cursor.execute("SELECT * FROM uploads")
print("Uploads Table Data:", cursor.fetchall())

cursor.close()
conn.close()
