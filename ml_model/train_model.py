import sys
import os
import json
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.optimizers.experimental import AdamW  
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from sklearn.utils import class_weight
import logging
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Setup Logging
logging.basicConfig(level=logging.INFO)

# Path Configurations
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, 'ml_model')  # Adjusted to ensure correct path
CLASS_INDICES_FILE = os.path.join(MODEL_DIR, 'class_indices.json')
MODEL_FILE = os.path.join(MODEL_DIR, 'herb_identification_model.h5')

# Ensure preprocessing directory is in the path
sys.path.append(os.path.abspath(BASE_DIR))

# Import necessary modules
from preprocessing.data_loader import load_data
from preprocessing.data_augmentation import get_data_generator
from mobilenetv2 import build_mobilenetv2_model

# Load Dataset
train_data, val_data, test_data = load_data()

# Build Model
model = build_mobilenetv2_model(num_classes=train_data.num_classes)

# Compile Model
model.compile(optimizer=AdamW(learning_rate=1e-4),  
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Callbacks
early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
checkpoint = ModelCheckpoint(
    MODEL_FILE, 
    monitor='val_accuracy', 
    save_best_only=True, 
    mode='max', 
    verbose=1
)
lr_scheduler = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=4, min_lr=1e-6)   

# Class Weights Calculation
class_indices = train_data.class_indices
labels = train_data.classes
class_weights = class_weight.compute_class_weight(
    class_weight='balanced',
    classes=np.unique(labels),
    y=labels
)
class_weights_dict = {i: weight for i, weight in enumerate(class_weights)}
logging.info(f"\n⚖️ Class Weights: {class_weights_dict}")

# Sorting Class Indices
class_indices_sorted = sorted(class_indices.items(), key=lambda x: x[1])
class_names = [item[0] for item in class_indices_sorted]

# Save Class Indices to JSON
os.makedirs(MODEL_DIR, exist_ok=True)
try:
    with open(CLASS_INDICES_FILE, 'w') as f:
        json.dump({str(i): name for i, name in enumerate(class_names)}, f, indent=4)
    logging.info("\n💾 Class indices saved to class_indices.json")
except Exception as e:
    logging.error(f"Failed to save class_indices.json: {e}")

# Model Training
history = model.fit(
    train_data,
    validation_data=val_data,
    epochs=30,
    class_weight=class_weights_dict,
    callbacks=[early_stopping, checkpoint, lr_scheduler]
)

# Save Final Model
try:
    model.save(MODEL_FILE)
    logging.info("\n✅ Model saved successfully.")
except Exception as e:
    logging.error(f"Failed to save model: {e}")

# Visualization of Training History
def plot_metrics(history):
    try:
        plt.figure(figsize=(10, 6))
        plt.plot(history.history['accuracy'], label='Training Accuracy')
        plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
        plt.xlabel('Epochs')
        plt.ylabel('Accuracy')
        plt.legend()
        plt.title('Training and Validation Accuracy')
        plt.grid(True)
        plt.show()

        plt.figure(figsize=(10, 6))
        plt.plot(history.history['loss'], label='Training Loss')
        plt.plot(history.history['val_loss'], label='Validation Loss')
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.legend()
        plt.title('Training and Validation Loss')
        plt.grid(True)
        plt.show()
    except Exception as e:
        logging.error(f"Failed to plot metrics: {e}")

# Plotting Training Metrics
plot_metrics(history)