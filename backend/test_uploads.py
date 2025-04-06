import pymysql

conn = pymysql.connect(host='localhost', user='root', password='', db='your_db_name')
cursor = conn.cursor()
cursor.execute("SELECT 1;")
print("Database connection successful!")
cursor.close()
conn.close()
