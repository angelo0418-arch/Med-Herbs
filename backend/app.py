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
import logging

# ✅ Import Blueprints
from routes.herb_routes import herbs_bp
from routes.uploads_routes import uploads_bp
from routes.predict_routes import predict_bp
from routes.login_signup_routes import auth_bp


# 🔹 FLASK CONFIG
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "your_fallback_secret_key")  # ✅ Secure secret key
CORS(app)

# 🔹 CONFIGURATION
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ML_MODEL_DIR = os.path.join(BASE_DIR, "../ml_model")
UPLOAD_FOLDER = os.path.abspath(os.path.join(BASE_DIR, 'backend', 'static', 'uploads'))
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 🔹 MYSQL CONFIG
app.config['MYSQL_HOST'] = os.getenv("MYSQL_HOST", "localhost")
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = os.getenv("MYSQL_PASSWORD", "@SorsuBC#404")  # ✅ Secure database password
app.config['MYSQL_DB'] = 'medherbs_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# 🔹 REGISTER BLUEPRINTS
app.register_blueprint(herbs_bp, url_prefix='/herbs')
app.register_blueprint(uploads_bp, url_prefix='/uploads')
app.register_blueprint(predict_bp, url_prefix='/predict')
app.register_blueprint(auth_bp, url_prefix='/auth')


# 🔹 SECURITY CONFIG (Sessions)
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False  # ⚠ Set to True sa production
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# ✅ Inject timestamp para maiwasan ang cache sa static files
@app.context_processor
def inject_time():
    return {'time': datetime.utcnow().timestamp()}

# 🔹 TEST ROUTE
@app.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "Server is running!"})

# 🔹 MAIN ROUTE
@app.route('/')
def index():
    return render_template('index.html')

# 🔹 USER DASHBOARD ROUTE
@app.route('/user_dashboard')
def user_dashboard():
    return render_template('user_dashboard.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)