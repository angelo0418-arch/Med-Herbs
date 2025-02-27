# tf_inference.py

import os
import tensorflow as tf
import numpy as np
import json
import matplotlib.pyplot as plt
from PIL import Image
import cv2

# === LOAD THE TENSORFLOW MODEL ===
model_path = os.path.abspath("herb_identification_model.h5")
model = tf.keras.models.load_model(model_path)
print("✅ TensorFlow Model Successfully Loaded and Ready for Inference!")

# === LOAD CLASS INDICES MAPPING ===
class_indices_path = os.path.abspath("class_indices.json")
try:
    with open(class_indices_path, 'r') as f:
        class_indices = json.load(f)
except FileNotFoundError:
    print("❌ Error: class_indices.json not found.")
    class_indices = {}

# === IMAGE PREPROCESSING FUNCTION ===
def preprocess_image(image_path, target_size):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Image not found at {image_path}")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, target_size)
    img = img / 255.0  # Normalize to [0, 1]
    img = np.expand_dims(img, axis=0)
    return img

# === LOAD THE TEST IMAGE ===
image_path = os.path.abspath("../predict_images/image.png")  # Palitan ang filename kung iba ang image
input_shape = model.input_shape[1:3]  # Get input shape from model
input_data = preprocess_image(image_path, input_shape)

# === DISPLAY THE PREPROCESSED IMAGE ===
plt.imshow(input_data[0])
plt.title("Preprocessed Image")
plt.axis('off')
plt.show()

# === RUN INFERENCE ===
predictions = model.predict(input_data).flatten()  # Flatten for consistency

# === DISPLAY RAW PREDICTIONS ===
print("\n📊 Raw Model Output:")
print(predictions)

# === APPLY SOFTMAX ===
predictions = tf.nn.softmax(predictions).numpy()

# === DISPLAY SOFTMAX OUTPUT ===
print("\n📊 Softmax Output:")
print(predictions)

# === GET TOP-1 PREDICTION ===
predicted_class = np.argmax(predictions)
class_name = class_indices.get(str(predicted_class), "Unknown Class")
confidence = predictions[predicted_class] * 100

print(f"\n🔍 Predicted Class Index: {predicted_class}")
print(f"🌿 Predicted Herb: {class_name}")
print(f"🎯 Confidence: {confidence:.2f}%")
