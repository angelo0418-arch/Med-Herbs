import os
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

        # ✅ Kunin ang `user_id`
        try:
            user_id = request.form.get("user_id")
            
            if not user_id or not user_id.isdigit():
                return jsonify({"error": "Invalid User ID"}), 400
            
            user_id = int(user_id)  # Convert to integer

            # ✅ I-check kung ang user ay umiiral sa `users` table bago mag-insert
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
            existing_user = cursor.fetchone()
            
            if not existing_user:
                return jsonify({"error": "Invalid User ID. User does not exist."}), 400
        
        except ValueError:
            return jsonify({"error": "Invalid User ID"}), 400
        
        finally:
            cursor.close()
            conn.close()

        # ✅ Predict herb automatically
        predicted_herb, benefit = predict_image(file_path)

        # 🔹 LOGGING PARA SA DEBUGGING
        print(f"📸 File Path: {file_path}")
        print(f"🧑‍💻 User ID: {user_id}")
        print(f"🌿 Predicted Herb: {predicted_herb}")

        # ✅ Save to database
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            # I-check muna kung may existing user_id sa users table
            cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
            existing_user = cursor.fetchone()

            if not existing_user:
                return jsonify({"error": "User does not exist in the database."}), 400

            # Kapag valid, saka lang mag-insert
            cursor.execute(
                "INSERT INTO uploads (user_id, image_path, predicted_herb) VALUES (%s, %s, %s)",
                (user_id, file_path, herb)
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
