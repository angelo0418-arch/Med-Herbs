import os
import numpy as np
import json
import re
import cv2
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# 🔹 FILE PATHS
MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_FILE = os.path.join(MODEL_DIR, "herb_identification_model.h5")
CLASS_INDICES_FILE = os.path.join(MODEL_DIR, "class_indices.json")
HERB_BENEFITS_FILE = os.path.join(MODEL_DIR, "herb_benefits.json")
PREDICT_IMAGES_DIR = os.path.abspath(os.path.join(MODEL_DIR, "..", "predict_images"))

# 🔹 LOAD MODEL
model = load_model(MODEL_FILE)
print("✅ Model successfully loaded.")

# 🔹 LOAD CLASS INDICES & HERB BENEFITS
with open(CLASS_INDICES_FILE, 'r') as f:
    class_indices = json.load(f)
class_labels = {int(k): v for k, v in class_indices.items()}

with open(HERB_BENEFITS_FILE, 'r') as f:
    herb_benefits = json.load(f)

# 🔹 IMAGE PREPROCESSING
def load_and_prepare_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array, img

# 🔹 PREDICTION FUNCTION
def predict_image(image_path):
    processed_image, original_image = load_and_prepare_image(image_path)
    prediction = model.predict(processed_image)

    predicted_class_index = np.argmax(prediction)
    confidence = np.max(prediction)

    if confidence < 0.5:
        return "Oops! This doesn't seem to be a herb. Please try again with the correct image.", None, original_image

    predicted_herb = class_labels.get(predicted_class_index, "Unknown Herb")
    herb_benefit = herb_benefits.get(predicted_herb, "No available information.")
    return predicted_herb, herb_benefit, original_image

# 🔹 PROCESS ALL IMAGES
if __name__ == "__main__":
    for img_file in os.listdir(PREDICT_IMAGES_DIR):
        img_path = os.path.join(PREDICT_IMAGES_DIR, img_file)
        predicted_herb, herb_benefit, original_image = predict_image(img_path)

        plt.imshow(original_image)
        plt.axis("off")
        plt.title(f"Predicted: {predicted_herb}\nBenefits: {herb_benefit}")
        plt.show()

        print(f"\n🌿 **Predicted Herb:** {predicted_herb}")
        print(f"💡 **Herb Benefits:** {herb_benefit}")
