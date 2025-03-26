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
        session['user_id'] = user['id']  # ✅ TAMA: May tamang indentation
        session['username'] = user['username']

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


# 🔹 LOGOUT ROUTE (Ayusin sa login_signup_routes.py)
@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()  # Linisin ang session para ma-log out ang user
    return jsonify({'success': True}), 200


# 🔹 GET UPLOAD HISTORY (Ayusin sa login_signup_routes.py)
@auth_bp.route('/get_upload_history')
def get_upload_history():
    if 'user_id' not in session:
        return jsonify([])

    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT filename, upload_date FROM uploads WHERE user_id = %s", (user_id,))
    uploads = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(uploads)



# 🔹 CHECK SESSION ROUTE (Idagdag sa login_signup_routes.py)
@auth_bp.route('/check_session', methods=['GET'])
def check_session():
    if 'user_id' in session:
        return jsonify({'logged_in': True, 'username': session.get('username')}), 200
    return jsonify({'logged_in': False}), 401



