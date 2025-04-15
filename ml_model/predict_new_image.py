import os
import numpy as np
import json
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
try:
    model = load_model(MODEL_FILE)
    print("✅ Model successfully loaded.")
except Exception as e:
    print(f"❌ Failed to load model: {e}")
    exit(1)

# 🔹 LOAD CLASS INDICES & HERB BENEFITS
try:
    with open(CLASS_INDICES_FILE, 'r') as f:
        class_indices = json.load(f)
        scientific_name_map = {int(k): v['scientific_name'] for k, v in class_indices.items()}

    with open(HERB_BENEFITS_FILE, 'r') as f:
        herb_benefits = json.load(f)

    print("✅ JSON files loaded successfully.")
except Exception as e:
    print(f"❌ Error loading JSON files: {e}")
    exit(1)

# 🔹 IMAGE PREPROCESSING
def load_and_prepare_image(img_path):
    try:
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        return img_array, img
    except Exception as e:
        print(f"❌ Error processing image {img_path}: {e}")
        return None, None

# 🔹 PREDICTION FUNCTION
def predict_image(image_path):
    processed_image, original_image = load_and_prepare_image(image_path)
    if processed_image is None:
        return "Invalid image file.", None, None, None, None, None, None

    prediction = model.predict(processed_image)
    predicted_class_index = int(np.argmax(prediction))
    confidence = float(np.max(prediction))

    if confidence < 0.5:
        return "Oops! This doesn't seem to be a herb. Please try again with the correct image.", None, None, None, None, None, original_image

    predicted_herb = scientific_name_map.get(predicted_class_index, "Unknown Herb")
    herb_data = class_indices.get(str(predicted_class_index), {})

    return (
        predicted_herb,
        herb_benefits.get(predicted_herb, "No available information."),
        herb_data.get("english_name", "N/A"),
        herb_data.get("tagalog_name", "N/A"),
        herb_data.get("bicol_name", "N/A"),
        herb_data.get("description", "No description."),
        original_image
    )

# 🔹 PROCESS IMAGES IN FOLDER
if __name__ == "__main__":
    for img_file in os.listdir(PREDICT_IMAGES_DIR):
        img_path = os.path.join(PREDICT_IMAGES_DIR, img_file)
        print(f"\n📷 Processing {img_file}...")

        result = predict_image(img_path)

        if result[1] is None:
            print(f"⚠️ Skipped: {result[0]}")
            continue

        predicted_herb, benefit, english, tagalog, bicol, description, original_image = result

        print(f"✅ Prediction: {predicted_herb}")
        print(f"📌 English: {english} | Tagalog: {tagalog} | Bicol: {bicol}")
        print(f"📋 Description: {description}")
        print(f"🌿 Benefits: {benefit}")

        plt.imshow(original_image)
        plt.axis("off")
        plt.title(f"Predicted: {predicted_herb}", fontsize=14)
        plt.figtext(0.01, -0.12, f"English Name: {english}", wrap=True, fontsize=10)
        plt.figtext(0.01, -0.17, f"Tagalog Name: {tagalog}", wrap=True, fontsize=10)
        plt.figtext(0.01, -0.22, f"Bicol Name: {bicol}", wrap=True, fontsize=10)
        plt.figtext(0.01, -0.27, f"Description: {description}", wrap=True, fontsize=10)
        plt.figtext(0.01, -0.32, f"Benefits: {benefit}", wrap=True, fontsize=10)
        plt.show()
