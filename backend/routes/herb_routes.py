from flask import Blueprint, request, jsonify
from db_config import get_db_connection

# Blueprint Initialization
herbs_bp = Blueprint('herbs', __name__)

# ✅ Route to get all herbs
@herbs_bp.route('/', methods=['GET'])
def get_herbs():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM herbs")
    herbs = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(herbs)

# ✅ Route to get a specific herb by ID
@herbs_bp.route('/<int:herb_id>', methods=['GET'])
def get_herb(herb_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM herbs WHERE id = %s", (herb_id,))
    herb = cursor.fetchone()
    cursor.close()
    conn.close()
    if herb:
        return jsonify(herb)
    return jsonify({"message": "Herb not found"}), 404

# ✅ Route to add a new herb (updated fields)
@herbs_bp.route('/', methods=['POST'])
def add_herb():
    data = request.json
    name = data.get("name")
    english_name = data.get("english_name")
    tagalog_name = data.get("tagalog_name")
    bicol_name = data.get("bicol_name")
    benefits = data.get("benefits")
    description = data.get("description", "")

    if not name or not benefits:
        return jsonify({"message": "Name and benefits are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO herbs (name, english_name, tagalog_name, bicol_name, benefits, description)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (name, english_name, tagalog_name, bicol_name, benefits, description))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Herb added successfully!"}), 201
