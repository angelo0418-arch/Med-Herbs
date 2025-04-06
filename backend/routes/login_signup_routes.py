from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from db_config import get_db_connection
import jwt
import datetime
import bcrypt
import mysql.connector

# ✅ Gumawa ng `auth_bp` Blueprint
auth_bp = Blueprint('auth_bp', __name__)

# 🔑 SECRET KEY para sa JWT
SECRET_KEY = "your_secret_key"  # Palitan ito ng mas secure na key!

# ✅ LOGIN ROUTE (Session + JWT)
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
    
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
        # ✅ Gumawa ng session-based login
        session['user_id'] = user['id']
        session['username'] = user['username']

        # ✅ Gumawa ng JWT token
        token = jwt.encode({
            'user_id': user['id'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Expire sa 1 hour
        }, SECRET_KEY, algorithm="HS256")

        return jsonify({'message': 'Login successful', 'token': token, 'status': 'success'}), 200
    else:
        return jsonify({'error': 'Invalid email or password'}), 401  # Unauthorized

# ✅ SIGNUP ROUTE
@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'All fields are required'}), 400

    # ✅ Hash ang password gamit ang bcrypt
# ✅ Hash ang password gamit ang bcrypt
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


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

# ✅ LOGOUT ROUTE
@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()  # Linisin ang session para ma-log out ang user
    return jsonify({'success': True}), 200

# ✅ GET UPLOAD HISTORY
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

# ✅ CHECK SESSION & JWT AUTHENTICATION
@auth_bp.route('/check_session', methods=['GET'])
def check_session():
    # 🔹 Kung may session, ibalik ang user info
    if 'user_id' in session:
        return jsonify({'logged_in': True, 'username': session.get('username')}), 200
    
    # 🔹 Kung walang session, tingnan kung may valid JWT token
    token = request.headers.get('Authorization')
    if token:
        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return jsonify({'logged_in': True, 'user_id': decoded['user_id']}), 200
        except jwt.ExpiredSignatureError:
            return jsonify({'logged_in': False, 'error': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'logged_in': False, 'error': 'Invalid token'}), 401
    
    return jsonify({'logged_in': False}), 401