from flask import Flask, request, jsonify, render_template, session
from werkzeug.utils import secure_filename
from flask_cors import CORS
from flask_mysqldb import MySQL
import bcrypt
import os
import json
import numpy as np
from PIL import Image
import tensorflow as tf  
from datetime import datetime

# 🔹 CONFIGURATION
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ML_MODEL_DIR = os.path.join(BASE_DIR, "../ml_model")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 🔹 FLASK CONFIG
app = Flask(__name__)
app.secret_key = "10000"  # Palitan ito ng mas secure na key
CORS(app)

# 🔹 MYSQL CONFIG
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Palitan ayon sa MySQL mo
app.config['MYSQL_PASSWORD'] = '@FaithGeloJohnVic#404'  # Ilagay ang MySQL password mo
app.config['MYSQL_DB'] = 'medherbs_user'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

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
        return "❌ Prediction failed. Please try again.", ""

    herb_name = class_names[predicted_class]
    benefit = herb_benefits.get(herb_name, "No information available.")
    return herb_name, benefit

# ✅ Inject timestamp para maiwasan ang cache sa static files
@app.context_processor
def inject_time():
    return {'time': datetime.utcnow().timestamp()}

# 🔹 ROUTES

@app.route('/')
def index():
    return render_template('index.html')

# 🔹 SIGNUP ROUTE
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'Please fill in all fields'}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users (Username, Email_address, hashed_password) VALUES (%s, %s, %s)", 
                (username, email, hashed_password))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Account created successfully!'})

# 🔹 LOGIN ROUTE
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Please enter both email and password'}), 400

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE Email_address = %s", (email,))
    user = cur.fetchone()
    cur.close()

    if user and bcrypt.checkpw(password.encode('utf-8'), user['hashed_password'].encode('utf-8')):
        session['loggedin'] = True
        session['user_id'] = user['user_id']
        session['username'] = user['Username']
        return jsonify({'message': 'Login successful', 'username': user['Username']})
    else:
        return jsonify({'error': 'Invalid email or password'}), 401

# 🔹 LOGOUT ROUTE
@app.route('/logout')
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'})

# 🔹 PREDICT IMAGE ROUTE
@app.route('/predict', methods=['POST'])
def predict():
    file = request.files.get('file')
    if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
        file_path = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
        file.save(file_path)

        herb, benefit = predict_image(file_path)

        if herb == "❌ Prediction failed. Please try again.":
            return jsonify({'warning': herb})

        if herb not in class_names:
            return jsonify({'warning': "❌ Prediction failed. Please try again."})

        return jsonify({'herb': herb, 'benefit': benefit})

    return jsonify({'error': 'Invalid file type'}), 400

# 🔹 PROTECTED DASHBOARD
@app.route('/dashboard')
def dashboard():
    if 'loggedin' not in session:
        return jsonify({'error': 'Unauthorized access'}), 401
    return jsonify({'message': f'Welcome {session["username"]}! This is your dashboard.'})

if __name__ == '__main__':
    app.run(debug=True, port=8000)
