from flask import Blueprint, request, jsonify, g
import mysql.connector
import jwt
from functools import wraps
from db_config import get_db_connection

dataset_updates_bp = Blueprint('dataset_updates_bp', __name__)

SECRET_KEY = "your_secret_key"  # Dapat parehas sa login

# ✅ FUNCTION: AUTHENTICATION CHECKER
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            g.user_id = decoded_token['user_id']  # ✅ Gamitin ang `g.user_id`
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(*args, **kwargs)
    return decorated

# ✅ GET: Kunin ang lahat ng dataset updates
@dataset_updates_bp.route('/updates', methods=['GET'])
def get_updates():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM dataset_updates ORDER BY update_time DESC")
    updates = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(updates)

# ✅ POST: Magdagdag ng bagong update (Naka-secure gamit ang JWT)
@dataset_updates_bp.route('/updates', methods=['POST'])
@token_required
def add_update():
    data = request.json
    
    if not data:
        return jsonify({'message': 'No data received!'}), 400  # 🛑 Kung walang data sa request
    
    update_details = data.get('update_details')
    
    if not update_details:
        return jsonify({'message': 'Update details are required'}), 400
    
    updated_by = g.user_id  # ✅ Gamitin ang `g.user_id`
    
    if not updated_by:
        return jsonify({'message': 'User ID is missing from token!'}), 401  # 🛑 Kung wala ang user_id sa token

    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO dataset_updates (updated_by, update_details) VALUES (%s, %s)", (updated_by, update_details))
    db.commit()
    cursor.close()
    db.close()

    return jsonify({'message': 'Update added successfully!'}), 201
