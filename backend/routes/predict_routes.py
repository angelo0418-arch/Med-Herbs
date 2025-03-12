from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
import json
import numpy as np
from PIL import Image
import tensorflow as tf  
from db_config import get_db_connection  # ✅ Import MySQL connection

# 🔹 CONFIGURATION
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ML_MODEL_DIR = os.path.join(BASE_DIR, "../../ml_model")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "../../uploads")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# ✅ Load ML Model
MODEL_PATH = os.path.join(ML_MODEL_DIR, "herb_identification_model.h5")
model = tf.keras.models.load_model(MODEL_PATH)

# ✅ Load Class Labels
LABELS_PATH = os.path.join(ML_MODEL_DIR, "class_indices.json")
with open(LABELS_PATH, "r") as file:
    class_indices = json.load(file)

class_names = [class_indices[str(i)] for i in range(len(class_indices))]

# ✅ Load Herb Benefits
BENEFITS_PATH = os.path.join(ML_MODEL_DIR, "herb_benefits.json")
with open(BENEFITS_PATH, "r") as file:
    herb_benefits = json.load(file)

# ✅ IMAGE PREPROCESSING FUNCTION
def preprocess_image(image_path):
    img = Image.open(image_path).resize((224, 224))  
    img_array = np.array(img) / 255.0  
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

# ✅ PREDICTION FUNCTION
def predict_image(image_path):
    img_array = preprocess_image(image_path)
    prediction = model.predict(img_array)

    predicted_class = np.argmax(prediction)
    confidence = np.max(prediction)

    if confidence < 0.5:
        return "❌ Prediction failed. Please try again.", ""

    herb_name = class_names[predicted_class]
    benefit = herb_benefits.get(herb_name, "No information available.")
    return herb_name, benefit

# 🔹 BLUEPRINT SETUP
predict_bp = Blueprint('predict', __name__)

# 🔹 PREDICT ROUTE (with DATABASE INSERT)
@predict_bp.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        herb, benefit = predict_image(file_path)

        if herb == "❌ Prediction failed. Please try again.":
            return jsonify({'warning': herb})

        # ✅ INSERT INTO DATABASE
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO uploads (user_id, image_path, predicted_herb) VALUES (%s, %s, %s)",
                (1, file_path, herb)  # ⚠️ Palitan ang `1` ng actual `user_id` kung meron
            )
            conn.commit()
        except Exception as e:
            print(f"❌ Database Error: {e}")  # Debug log
            return jsonify({"error": "Failed to save to database"}), 500
        finally:
            cursor.close()
            conn.close()

        return jsonify({'herb': herb, 'benefit': benefit})

    return jsonify({"error": "Invalid file format"}), 400
