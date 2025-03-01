from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.utils import class_weight
import numpy as np

# Define the path to your training data
train_data_dir = 'C:/Users/ACER/Desktop/System_MedHerbs/Philippine Medicinal Plant Leaf Dataset/train' # Palitan ito sa tamang directory ng iyong dataset

# Define the ImageDataGenerator for the training data
train_datagen = ImageDataGenerator(rescale=1./255)

# Create a data generator for training data
train_data = train_datagen.flow_from_directory(
    train_data_dir,  # Path to your dataset
    target_size=(224, 224),
    batch_size=32,
    class_mode='binary'  # O 'categorical' kung maraming klase
)

# Get the class labels from the generator
labels = train_data.classes

# Compute class weights
class_weights = class_weight.compute_class_weight(class_weight='balanced',
                                                  classes=np.unique(labels),
                                                  y=labels)

# Convert the class weights to a dictionary for easier use
class_weights_dict = dict(enumerate(class_weights))

# Print the computed class weights
print("Class Weights:", class_weights_dict)
