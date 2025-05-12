import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np


model = load_model('herb_identification_model.h5')


test_data_dir = 'C:\\Users\\ACER\\Desktop\\System_MedHerbs\\Philippine Medicinal Plant Leaf Dataset\\test'
img_height, img_width = 224, 224  
batch_size = 16


test_datagen = ImageDataGenerator(rescale=1./255)

test_generator = test_datagen.flow_from_directory(
    test_data_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical',  
    shuffle=False 
)


loss, accuracy = model.evaluate(test_generator)
print(f'\nTest Loss: {loss:.4f}')
print(f'Test Accuracy: {accuracy:.4f}')


import matplotlib.pyplot as plt


predictions = model.predict(test_generator)
predicted_classes = np.argmax(predictions, axis=1)
true_classes = test_generator.classes
class_labels = list(test_generator.class_indices.keys())


plt.figure(figsize=(12, 12))
for i in range(9):
    plt.subplot(3, 3, i + 1)
    img, label = test_generator[i][0][0], true_classes[i]
    plt.imshow(img)
    plt.title(f"True: {class_labels[label]}\nPred: {class_labels[predicted_classes[i]]}")
    plt.axis('off')

plt.tight_layout()
plt.show()