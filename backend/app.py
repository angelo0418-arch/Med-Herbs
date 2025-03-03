from flask import Flask, request, jsonify, render_template, send_from_directory, url_for
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
import json
import numpy as np
from PIL import Image
import tensorflow as tf  
from datetime import datetime

# 🔹 CONFIG
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ML_MODEL_DIR = os.path.join(BASE_DIR, "../ml_model")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 🔹 LOAD MODEL
MODEL_PATH = os.path.join(ML_MODEL_DIR, "herb_identification_model.h5")
model = tf.keras.models.load_model(MODEL_PATH)

# 🔹 LOAD JSON FILES
with open(os.path.join(ML_MODEL_DIR, "class_indices.json"), 'r') as f:
    class_indices = json.load(f)

with open(os.path.join(ML_MODEL_DIR, "herb_benefits.json"), 'r') as f:
    herb_benefits = json.load(f)

class_names = [class_indices[str(i)] for i in range(len(class_indices))]

# 🔹 IMAGE PREPROCESSING
def preprocess_image(image_path):
    img = Image.open(image_path).resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

# 🔹 PREDICTION FUNCTION
def predict_image(image_path):
    img_array = preprocess_image(image_path)
    prediction = model.predict(img_array)

    predicted_class = np.argmax(prediction)
    confidence = np.max(prediction)

    if confidence < 0.5:
        return "Oops! This doesn't seem to be a herb. Please try again with the correct image.", ""

    herb_name = class_names[predicted_class]
    benefit = herb_benefits.get(herb_name, "No information available.")
    return herb_name, benefit

# 🔹 FLASK APP
app = Flask(__name__)
CORS(app)

# ✅ Inject timestamp para maiwasan ang cache sa static files
@app.context_processor
def inject_time():
    return {'time': datetime.utcnow().timestamp()}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files.get('file')
    if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
        file_path = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
        file.save(file_path)

        herb, benefit = predict_image(file_path)
        return jsonify({'herb': herb, 'benefit': benefit})

    return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=8000)
