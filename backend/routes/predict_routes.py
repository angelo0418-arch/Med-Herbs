from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
import json
import numpy as np
from PIL import Image
import tensorflow as tf
from db_config import get_db_connection  # ✅ Import MySQL connection
from flask import session 

# 🔹 CONFIGURATION
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ML_MODEL_DIR = os.path.join(BASE_DIR, "../../ml_model")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "../static/uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# 🔹 Load ML Model
MODEL_PATH = os.path.join(ML_MODEL_DIR, "herb_identification_model.h5")
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ Model Loading Error: {e}")
    model = None

# 🔹 Load JSON files
LABELS_PATH = os.path.join(ML_MODEL_DIR, "class_indices.json")
BENEFITS_PATH = os.path.join(ML_MODEL_DIR, "herb_benefits.json")

class_indices = {}
herb_benefits = {}

try:
    with open(LABELS_PATH, "r") as file:
        class_indices = json.load(file) 
        print("✅ class_indices.json loaded!")

    with open(BENEFITS_PATH, "r") as file:
        herb_benefits = json.load(file)
        print("✅ herb_benefits.json loaded!")
except Exception as e:
    print(f"❌ Error loading JSON files: {e}")

# 🔹 Preprocess image
def preprocess_image(image_path):
    try:
        img = Image.open(image_path).convert('RGB').resize((224, 224))  # ← dagdag ang .convert('RGB')
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        return img_array
    except Exception as e:
        print(f"❌ Error processing image: {e}")
        return None

# 🔹 Prediction function
def predict_image(image_path):
    img_array = preprocess_image(image_path)
    if img_array is None:
        return None, None, None, None, None, None, "Error processing image."

    prediction = model.predict(img_array)
    confidence = float(np.max(prediction))  # Isa lang dapat ito
    predicted_class = np.argmax(prediction)

    
    if confidence < 0.5:
        return None, None, None, None, None, None, (
            '<span style="color: #d9534f; font-style: italic;">'
            'We could not confidently identify the herb. Please upload a clear image of a medicinal plant.'
            '</span>'
        )

    
    herb_data = class_indices.get(str(predicted_class), {})
    
    scientific_name = herb_data.get("scientific_name", "Unknown")
    english_name = herb_data.get("english_name", "Unknown")
    tagalog_name = herb_data.get("tagalog_name", "Unknown")
    bicol_name = herb_data.get("bicol_name", "Unknown")
    description = herb_data.get("description", "No description.")
    benefit = herb_benefits.get(scientific_name, "No benefits information.")

    return confidence, scientific_name, english_name, tagalog_name, bicol_name, description, benefit


# 🔹 Blueprint setup
predict_bp = Blueprint('predict', __name__)  # Define the Blueprint

@predict_bp.route('/', methods=['POST'])
def predict_image_route():
    print("📌 Received request to /predict")
    
    if 'file' not in request.files or request.files['file'].filename == '':
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    # Predict
    confidence, scientific_name, english_name, tagalog_name, bicol_name, description, benefit = predict_image(file_path)

    if scientific_name is None:
        return jsonify({'warning': benefit}), 200

    # Save to database if user is logged in
    user_id = session.get("user_id")
    guest_id = request.form.get("guest_id")

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Check if user_id is provided, and if it's valid
        if user_id:
            user_id = int(user_id)
            cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
            if not cursor.fetchone():
                return jsonify({"error": "User does not exist in the database."}), 400

        cursor.execute(""" 
            INSERT INTO uploads (
                user_id, guest_id, image_path, 
                identified_herb, english_name, tagalog_name, 
                bicol_name, description, herb_benefit
            ) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            user_id if user_id else None,
            guest_id if guest_id else None,
            file_path,
            scientific_name,
            english_name,
            tagalog_name,
            bicol_name,
            description,
            benefit
        ))

        conn.commit()
        print("✅ Saved prediction to database.")
    except Exception as e:
        print(f"❌ Database Error: {e}")
        return jsonify({"error": "Failed to save to database"}), 500
    finally:
        cursor.close()
        conn.close()

    # Return to frontend
    return jsonify({
        "confidence": f"{confidence * 100:.2f}",  # convert to percent string
        "herb": scientific_name,
        "scientific_name": scientific_name,
        "english_name": english_name,
        "tagalog_name": tagalog_name,
        "bicol_name": bicol_name,
        "description": description,
        "benefit": benefit
    }), 200
    

    
#--------------------------------Routes for upload history-----------------------------------
    
@predict_bp.route('/upload_history', methods=['GET'])
def get_upload_history():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "User not logged in"}), 401

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT identified_herb, english_name, tagalog_name, bicol_name, description, herb_benefit, image_path
            FROM uploads
            WHERE user_id = %s
            ORDER BY uploaded_at DESC
        """, (user_id,))
        uploads = cursor.fetchall()

        # ✅ Baguhin ang image_path sa filename lang
        for upload in uploads:
            filename = os.path.basename(upload['image_path'])  # Extract filename from full path
            upload['image_path'] = filename

        return jsonify(uploads), 200
    except Exception as e:
        print(f"❌ Error fetching upload history: {e}")
        return jsonify({"error": "Failed to fetch upload history"}), 500
    finally:
        cursor.close()
        conn.close()