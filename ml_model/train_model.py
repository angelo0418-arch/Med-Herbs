import sys
import os
sys.path.append(os.path.abspath('..'))
from preprocessing.data_loader import load_data
from mobilenetv2 import build_mobilenetv2_model
import matplotlib.pyplot as plt
from tensorflow.keras.optimizers.experimental import AdamW  
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from sklearn.utils import class_weight
import numpy as np
import json  


train_data, val_data, test_data = load_data()


model = build_mobilenetv2_model(num_classes=train_data.num_classes)


model.compile(optimizer=AdamW(learning_rate=1e-4),  
              loss='categorical_crossentropy',
              metrics=['accuracy'])


early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
checkpoint = ModelCheckpoint('herb_identification_model.h5', monitor='val_loss', save_best_only=True, mode='min')
lr_scheduler = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=4, min_lr=1e-6)   


class_indices = train_data.class_indices
labels = train_data.classes
class_weights = class_weight.compute_class_weight(
    class_weight='balanced',
    classes=np.unique(labels),
    y=labels
)
class_weights_dict = {i: weight for i, weight in enumerate(class_weights)}
print("\n⚖️ Class Weights:", class_weights_dict)


class_indices_sorted = sorted(class_indices.items(), key=lambda x: x[1])
class_names = [item[0] for item in class_indices_sorted]


output_json_file = 'C:/Users/ACER/Desktop/System_MedHerbs/ml_model/class_indices.json'
with open(output_json_file, 'w') as f:
    json.dump({str(i): name for i, name in enumerate(class_names)}, f, indent=4)
print("\n💾 Class indices saved to class_indices.json")


history = model.fit(
    train_data,
    validation_data=val_data,
    epochs=30,
    class_weight=class_weights_dict,
    callbacks=[early_stopping, checkpoint, lr_scheduler]
)


model.save('herb_identification_model.h5')


plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.title('Training and Validation Accuracy')
plt.show()

plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.title('Training and Validation Loss')
plt.show()
