import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt
import json
import re


model = load_model('herb_classifier_model.h5')


with open('class_indices.json', 'r') as json_file:
    class_indices = json.load(json_file)
    class_labels = {int(k): re.sub(r'^\d+\s*', '', v) for k, v in class_indices.items()}


def load_and_prepare_image(img_path):
    img = image.load_img(img_path, target_size=(128, 128))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0
    return img_array, img


image_folder = 'C:/Users/ACER/Desktop/System_MedHerbs/predict_images/'


for image_file in os.listdir(image_folder):
    
    if image_file.endswith('.jpg') or image_file.endswith('.png'):
        image_path = os.path.join(image_folder, image_file)
        print(f"\n🔍 Processing Image: {image_file}")

       
        processed_image, display_image = load_and_prepare_image(image_path)

        
        prediction = model.predict(processed_image)
        predicted_class_index = np.argmax(prediction, axis=1)[0]

        
        predicted_herb = class_labels.get(predicted_class_index, "Unknown Herb")

        
        plt.imshow(display_image)
        plt.title(f'Predicted Herb: {predicted_herb}')
        plt.axis('off')
        plt.show()

        
        print(f"✅ Predicted Herb: {predicted_herb}")
