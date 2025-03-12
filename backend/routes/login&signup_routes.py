from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from db_config import get_db_connection
import mysql.connector  # ← Idinagdag ito para maiwasan ang "mysql is not defined" error

app = Flask(__name__)

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'All fields are required'}), 400

    password_hash = generate_password_hash(password)

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # **Check kung may existing email bago mag-insert**
        cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            return jsonify({'error': 'Email already registered'}), 400  # HTTP 400: Bad Request

        # **Insert user kung walang duplicate**
        cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                       (username, email, password_hash))
        conn.commit()
        return jsonify({'message': 'User registered successfully'}), 201  # HTTP 201: Created

    except mysql.connector.Error as err:
        return jsonify({'error': f'Database error: {err}'}), 500  # HTTP 500: Internal Server Error

    finally:
        cursor.close()
        conn.close()


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    
    cursor.close()
    conn.close()

    if user and check_password_hash(user['password_hash'], password):
        return jsonify({'message': 'Login successful', 'user': user['username']}), 200  # HTTP 200: OK
    else:
        return jsonify({'error': 'Invalid email or password'}), 401  # HTTP 401: Unauthorized


if __name__ == '__main__':
    app.run(debug=True, port=5000)
