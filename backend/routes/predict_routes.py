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
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # ✅ Ensure uploads folder exists
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# ✅ Load ML Model
MODEL_PATH = os.path.join(ML_MODEL_DIR, "herb_identification_model.h5")
try:
    model = tf.keras.models.load_model(MODEL_PATH)
except Exception as e:
    print(f"❌ Model Loading Error: {e}")
    model = None

# ✅ Load Class Labels
LABELS_PATH = os.path.join(ML_MODEL_DIR, "class_indices.json")
BENEFITS_PATH = os.path.join(ML_MODEL_DIR, "herb_benefits.json")

print(f"🔍 Checking if files exist:\n - {LABELS_PATH}\n - {BENEFITS_PATH}")

if not os.path.exists(LABELS_PATH):
    print("❌ class_indices.json not found!")
if not os.path.exists(BENEFITS_PATH):
    print("❌ herb_benefits.json not found!")

# ✅ IMAGE PREPROCESSING FUNCTION
def preprocess_image(image_path):
    img = Image.open(image_path).resize((224, 224))  
    img_array = np.array(img) / 255.0  
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

# ✅ Load Class Labels and Benefits
class_indices = {}
herb_benefits = {}

try:
    with open(LABELS_PATH, "r") as file:
        class_indices = json.load(file)
        print("✅ Loaded class_indices.json successfully!")

    with open(BENEFITS_PATH, "r") as file:
        herb_benefits = json.load(file)
        print("✅ Loaded herb_benefits.json successfully!")
    
    # ✅ Generate class names list from class_indices
    class_names = [class_indices[str(i)] for i in range(len(class_indices))]
    print(f"✅ Loaded class names: {class_names}")
    
except json.JSONDecodeError:
    print("❌ ERROR: One of the JSON files is empty or malformed.")
except FileNotFoundError:
    print("❌ ERROR: JSON file not found. Check the file path!")

# ✅ PREDICTION FUNCTION
def predict_image(image_path):
    img_array = preprocess_image(image_path)
    prediction = model.predict(img_array)

    print(f"🔍 Prediction values: {prediction}")  
    predicted_class = np.argmax(prediction)
    confidence = np.max(prediction)

    print(f"🔍 Confidence: {confidence}")  
    print(f"🔍 Predicted class index: {predicted_class}")  

    if confidence < 0.5:
        print("❌ Prediction confidence too low!")  
        return "❌ Prediction failed. Please try again.", ""
    
    herb_name = class_names[predicted_class]
    benefit = herb_benefits.get(herb_name, "No information available.")
    
    print(f"🔍 Herb Name: {herb_name}, Benefit: {benefit}")  
    return herb_name, benefit

# 🔹 BLUEPRINT SETUP
predict_bp = Blueprint('predict_bp', __name__)

@predict_bp.route('/', methods=['POST'])  
def predict_image_route():  
    print("📌 Received request to /predict")  
    print(f"🔍 DEBUG: Request files - {request.files}")  
    print(f"🔍 DEBUG: Received user_id: {request.form.get('user_id')}")

    if 'file' not in request.files or request.files['file'].filename == '':
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        print("❌ Empty filename")
        return jsonify({"error": "Empty file name"}), 400

    # Secure filename
    filename = secure_filename(file.filename)  # ✅ FIXED!
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file_path = os.path.abspath(file_path)  
    file.save(file_path)
    print(f"✅ File saved at: {file_path}")

    # Predict the image
    herb, benefit = predict_image(file_path)
    if herb == "❌ Prediction failed. Please try again.":
        return jsonify({'warning': herb}), 200  

    # ✅ INSERT INTO DATABASE IF USER IS LOGGED IN
    user_id = request.form.get("user_id")
    if user_id:
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            try:
                user_id = int(user_id)  
            except (TypeError, ValueError):
                return jsonify({"error": "Invalid user_id format"}), 400

            # Check if user exists
            cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
            existing_user = cursor.fetchone()
            if not existing_user:
                return jsonify({"error": "User does not exist in the database."}), 400

            # Insert upload record
            cursor.execute(
                "INSERT INTO uploads (user_id, image_path, predicted_herb) VALUES (%s, %s, %s)",
                (user_id, file_path, herb)
            )
            conn.commit()
            print("✅ Prediction saved to database")
        except Exception as e:
            print(f"❌ Database Error: {e}")
            return jsonify({"error": "Failed to save to database"}), 500
        finally:
            cursor.close()
            conn.close()

    return jsonify({'herb': herb, 'benefit': benefit})