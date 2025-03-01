import json

# Load class_indices.json
with open('C:/Users/ACER/Desktop/System_MedHerbs/ml_model/class_indices.json', 'r') as f:
    class_indices = json.load(f)

# Load herb_benefits.json
with open('C:/Users/ACER/Desktop/System_MedHerbs/ml_model/herb_benefits.json', 'r') as f:
    herb_benefits = json.load(f)

# Extract herb names from class_indices in order
class_names = [class_indices[str(i)] for i in range(len(class_indices))]
benefit_names = list(herb_benefits.keys())

# Check if all class names have corresponding benefits
missing_benefits = [name for name in class_names if name not in benefit_names]

if missing_benefits:
    print("Warning: Kulang sa herb_benefits.json ang:", missing_benefits)
else:
    print("Lahat ng herbs ay may corresponding benefits.")
