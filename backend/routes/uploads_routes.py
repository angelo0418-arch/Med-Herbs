import os
import time
from datetime import datetime
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from db_config import get_db_connection
from .predict_routes import predict_image  # ✅ AYOS NA IMPORT

uploads_bp = Blueprint('uploads', __name__)

# 🔹 CONFIGURATION
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "../../uploads")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# ✅ Siguraduhin na may `uploads` folder
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ✅ Function para i-check kung valid ang file type
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 📌 1️⃣ ROUTE PARA SA FILE UPLOAD + SAVE SA DATABASE
@uploads_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        # ✅ Kunin ang `user_id` o `guest_id`
        user_id = request.form.get("user_id")
        guest_id = request.form.get("guest_id")

        # ❌ Error kung sabay silang meron
        if user_id and guest_id:
            return jsonify({"error": "Only one of user_id or guest_id should be provided, not both."}), 400

        if user_id:
            if not user_id.isdigit():
                return jsonify({"error": "Invalid User ID"}), 400
            user_id = int(user_id)

            # ✅ I-check kung umiiral ang user
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
            existing_user = cursor.fetchone()
            cursor.close()
            conn.close()

            if not existing_user:
                return jsonify({"error": "Invalid User ID. User does not exist."}), 400

        elif guest_id:
            guest_id = guest_id.strip()  # linisin kung may extra spaces
            if guest_id == "":
                return jsonify({"error": "Guest ID cannot be empty"}), 400

        else:
            # Auto-generate guest_id gamit ang timestamp kapag wala silang ipinasang guest_id
            guest_id = "guest_" + datetime.now().strftime("%Y%m%d%H%M%S")
        
        # ✅ Predict herb automatically
        scientific_name, english_name, tagalog_name, bicol_name, description, benefit = predict_image(file_path)
        predicted_herb = scientific_name  # 🔁 clarity lang

        # ✅ Save to database
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO uploads 
                (user_id, guest_id, image_path, identified_herb, english_name, tagalog_name, bicol_name, description, herb_benefit)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    user_id if user_id else None,
                    guest_id if guest_id else None,
                    file_path,
                    scientific_name,
                    english_name,
                    tagalog_name,
                    bicol_name,
                    description,
                    benefit
                )
            )

            conn.commit()

            cursor.execute("SELECT LAST_INSERT_ID()")
            upload_id = cursor.fetchone()[0]

        except Exception as e:
            return jsonify({"message": "Database error", "error": str(e)}), 500

        finally:
            cursor.close()
            conn.close()

        return jsonify({
            "message": "File uploaded and saved to database!",
            "upload_id": upload_id,
            "file_path": file_path,
            "predicted_herb": predicted_herb,
            "benefit": benefit
        }), 201

    return jsonify({"error": "Invalid file type"}), 400