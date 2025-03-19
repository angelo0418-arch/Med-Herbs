from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from db_config import get_db_connection
import mysql.connector
from flask import Blueprint, render_template, redirect, url_for, session

# ✅ Gumawa ng `auth_bp` Blueprint
auth_bp = Blueprint('auth_bp', __name__)

# ✅ LOGIN ROUTE (Dapat gamitin ang `auth_bp.route` at hindi `app.route`)
@auth_bp.route('/login', methods=['POST'])
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
        return jsonify({'message': 'Login successful', 'status': 'success'}), 200
    else:
        return jsonify({'error': 'Invalid email or password'}), 401  # HTTP 401: Unauthorized


@auth_bp.route('/signup', methods=['POST'])
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
        cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            return jsonify({'error': 'Email already registered'}), 400  

        cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                    (username, email, password_hash))
        conn.commit()
        return jsonify({'message': 'User registered successfully'}), 201  

    except mysql.connector.Error as err:
        return jsonify({'error': f'Database error: {err}'}), 500  

    finally:
        cursor.close()
        conn.close()


@auth_bp.route('/logout')
def logout():
    session.clear()  # I-clear ang session para ma-log out ang user
    return redirect(url_for('auth_bp.login'))  # I-redirect pabalik sa login page