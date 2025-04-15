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
        return "Oops! This doesn't seem to be a herb. Please try again with the correct image.", None, None, None, original_image

    predicted_herb = class_labels.get(predicted_class_index, "Unknown Herb")
    
    # Extracting additional data
    herb_data = class_indices[str(predicted_class_index)]
   
    herb_benefit = herb_benefits.get(predicted_herb, "No available information.")

    
    # Adding additional information for the display
    herb_english_name = herb_data['english_name']
    herb_tagalog_name = herb_data['tagalog_name']
    herb_bicol_name = herb_data['bicol_name']
    herb_description = herb_data['description']
    
    return predicted_herb, herb_benefit, herb_english_name, herb_tagalog_name, herb_bicol_name, herb_description, original_image

# 🔹 PROCESS ALL IMAGES
if __name__ == "__main__":
    for img_file in os.listdir(PREDICT_IMAGES_DIR):
        img_path = os.path.join(PREDICT_IMAGES_DIR, img_file)
        predicted_herb, herb_benefit, english_name, tagalog_name, bicol_name, description, original_image = predict_image(img_path)

        plt.imshow(original_image)
        plt.axis("off")
        plt.title(f"Predicted: {predicted_herb}\n"
                  f"English Name: {english_name}\n"
                  f"Tagalog Name: {tagalog_name}\n"
                  f"Bicol Name: {bicol_name}\n"
                  f"Description: {description}\n"
                  f"Benefits: {herb_benefit}")
        plt.show()

plt.title(f"Predicted: {predicted_herb}", fontsize=14)

# Maglagay ng text sa ibaba ng image
plt.figtext(0.01, -0.12, f"English Name: {english_name}", wrap=True, horizontalalignment='left', fontsize=10)
plt.figtext(0.01, -0.17, f"Tagalog Name: {tagalog_name}", wrap=True, horizontalalignment='left', fontsize=10)
plt.figtext(0.01, -0.22, f"Bicol Name: {bicol_name}", wrap=True, horizontalalignment='left', fontsize=10)
plt.figtext(0.01, -0.27, f"Description: {description}", wrap=True, horizontalalignment='left', fontsize=10)
plt.figtext(0.01, -0.32, f"Benefits: {herb_benefit}", wrap=True, horizontalalignment='left', fontsize=10)
