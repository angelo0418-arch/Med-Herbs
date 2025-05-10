import os
import sys
import numpy as np
import json
import re
import matplotlib.pyplot as plt
import seaborn as sns
from tensorflow.keras.models import load_model
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from preprocessing.data_loader import load_data  # Absolute import


model = load_model('herb_identification_model.h5')


with open('class_indices.json', 'r') as json_file:
    class_indices = json.load(json_file)
    class_labels = {int(k): v['english_name'] for k, v in class_indices.items()}
    label_names = list(class_labels.values())


_, _, test_data = load_data()
    

loss, accuracy = model.evaluate(test_data)
print(f"\n📊 Test Loss: {loss:.4f}")
print(f"🎯 Test Accuracy: {accuracy * 100:.2f}%")


y_true = test_data.classes  
y_pred_prob = model.predict(test_data)
y_pred = np.argmax(y_pred_prob, axis=1)  


print("\n📊 Classification Report:")
print(classification_report(y_true, y_pred, target_names=label_names))

from sklearn.metrics import f1_score

# Compute weighted F1 score
f1 = f1_score(y_true, y_pred, average='weighted')
print(f"🧪 Weighted F1 Score: {f1:.4f}")



conf_matrix = confusion_matrix(y_true, y_pred)


plt.figure(figsize=(12, 10))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=label_names, yticklabels=label_names)
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')
plt.title('Confusion Matrix')
plt.xticks(rotation=45)
plt.yticks(rotation=45)
plt.tight_layout()


plt.savefig('confusion_matrix.png', dpi=300)
plt.show()


import matplotlib.pyplot as plt
plt.figure(figsize=(12, 12))
for i in range(9):
    plt.subplot(3, 3, i + 1)
    img, label = test_data[i][0][0], y_true[i]
    plt.imshow(img)
    plt.title(f"True: {label_names[label]}\nPred: {label_names[y_pred[i]]}")
    plt.axis('off')

plt.tight_layout()
plt.show()
