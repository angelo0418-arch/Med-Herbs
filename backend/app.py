from flask import Flask, request, jsonify, render_template_string
from werkzeug.utils import secure_filename
from flask_cors import CORS  
import os
import numpy as np
from PIL import Image
import tensorflow as tf

app = Flask(__name__)
CORS(app)  


app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}


model = tf.keras.models.load_model('../ml_model/herb_identification_model.h5')


herb_labels = [
     "Aloe barbadensis Miller", "Annona muricata", "Antidesma bunius", "Arachis hypogaea", 
    "Averrhoea bilimbi", "Blumea balsamifera", "Capsicum frutescens", "Carmona retusa", 
    "Centella asiatica", "Citrus aurantiifolia", "Citrus maxima", "Citrus microcarpa", 
    "Citrus sinensis", "Coleus scutellarioides", "Corchorus olitorius", "Curcuma longa", 
    "Euphorbia hirta", "Gliricidia sepium", "Hibiscus rosa-sinensis", "Impatiens balsamina", 
    "Ipomoea batatas", "Jatropha curcas", "Lagerstroemia speciosa", "Leucaena leucocephala", 
    "Mangifera indica", "Manihot esculenta", "Mentha cordifolia Opiz", "Momordica charantia", 
    "Moringa oleifera", "Nerium oleander", "Ocimum basilicum", "Origanum vulgare", 
    "Pandanus amaryllifolius", "Pepromia pellucida", "Phyllanthus niruri", "Premna odorata", 
    "Psidium guajava", "Senna alata", "Tamarindus indica", "Vitex negundo"
] 


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def preprocess_image(image_path):
    img = Image.open(image_path)
    img = img.resize((128, 128))  
    img = np.array(img) / 255.0
    img = np.expand_dims(img, axis=0)
    return img


@app.route('/', methods=['GET', 'POST'])
def index():
    message = None
    prediction = None

    if request.method == 'POST':
        if 'file' not in request.files:
            message = 'No file part in the request'
        else:
            file = request.files['file']

            if file.filename == '':
                message = 'No selected file'
            elif file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)

                
                processed_image = preprocess_image(file_path)

                
                prediction_probs = model.predict(processed_image)
                predicted_class = np.argmax(prediction_probs, axis=1)[0]
                prediction = herb_labels[predicted_class]

                message = f'File uploaded successfully: {filename}'
            else:
                message = 'Invalid file type. Only png, jpg, jpeg are allowed.'

    return render_template_string('''
        <h2>Medicinal Herb Identification System</h2>
        <p>Upload an image to identify the medicinal herb:</p>
        <form method="post" enctype="multipart/form-data">
            <input type="file" name="file" accept="image/png, image/jpeg">
            <button type="submit">Upload Image</button>
        </form>
        {% if message %}
        <p><strong>{{ message }}</strong></p>
        {% endif %}
        {% if prediction %}
        <h3>Prediction Result: {{ prediction }}</h3>
        {% endif %}
    ''', message=message, prediction=prediction)

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    app.run(debug=True, port=8000)
