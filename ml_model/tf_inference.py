import os 
import numpy as np
import json
import tensorflow as tf
import matplotlib.pyplot as plt
from PIL import Image

# === FILE PATHS ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "herb_identification_model.h5")
CLASS_INDICES_PATH = os.path.join(BASE_DIR, "class_indices.json")
HERB_BENEFITS_PATH = os.path.join(BASE_DIR, "herb_benefits.json")
IMAGE_PATH = os.path.abspath(os.path.join(BASE_DIR, "../predict_images/class7_95.jpg"))

# === LOAD MODEL ===
model = tf.keras.models.load_model(MODEL_PATH)
print("✅ Model loaded successfully!")

# === LOAD JSON FILES ===
with open(CLASS_INDICES_PATH, 'r') as f:
    class_indices = json.load(f)

with open(HERB_BENEFITS_PATH, 'r') as f:
    herb_benefits = json.load(f)

class_labels = {int(k): v for k, v in class_indices.items()}

# === IMAGE PREPROCESSING ===
def preprocess_image(image_path):
    img = Image.open(image_path).resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

# === RUN INFERENCE ===
img_array = preprocess_image(IMAGE_PATH)
predictions = model.predict(img_array)
predicted_class_index = np.argmax(predictions)
confidence = np.max(predictions)

# === CHECK CONFIDENCE THRESHOLD ===
if confidence < 0.5:
    print("\nOops! This doesn't seem to be a herb. Please try again with the correct image.")
else:
    predicted_herb = class_labels.get(predicted_class_index, "Unknown Herb")
    herb_benefit = herb_benefits.get(predicted_herb, "No available information.")

    print(f"\n🌿 Predicted Herb: {predicted_herb}")
    print(f"💡 Herb Benefits: {herb_benefit}")
