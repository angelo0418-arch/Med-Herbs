import os

# Function to count images in each class directory
def count_images_in_directory(directory):
    class_counts = {}

    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' not found.")
        return {}

    for class_name in sorted(os.listdir(directory)):
        class_path = os.path.join(directory, class_name)
        if os.path.isdir(class_path) and class_name not in ['test', 'train', 'val']:  # Iwasan ang main dataset folders
            num_images = len([f for f in os.listdir(class_path) if os.path.isfile(os.path.join(class_path, f))])
            class_counts[class_name] = num_images

    return class_counts

# Define dataset directories
base_dir = r"C:\Users\ACER\Desktop\System_MedHerbs\Philippine Medicinal Plant Leaf Dataset"
train_dir = os.path.join(base_dir, "train")
val_dir = os.path.join(base_dir, "val")
test_dir = os.path.join(base_dir, "test")

# Function to count images per class
def count_images(dataset_path):
    class_counts = {}
    if not os.path.exists(dataset_path):
        print(f"Error: Directory '{dataset_path}' not found.")
        return class_counts

    for class_name in os.listdir(dataset_path):
        class_path = os.path.join(dataset_path, class_name)
        if os.path.isdir(class_path):  # Only count directories (classes)
            num_images = len(os.listdir(class_path))
            class_counts[class_name] = num_images
    return class_counts

# Get image counts for each dataset split
train_counts = count_images(train_dir)
val_counts = count_images(val_dir)
test_counts = count_images(test_dir)

# Compute total images per class
total_counts = {cls: train_counts.get(cls, 0) + val_counts.get(cls, 0) + test_counts.get(cls, 0) for cls in train_counts.keys()}

# Compute and display dataset distribution
print(f"{'Class Name':<30} {'Train %':<10} {'Val %':<10} {'Test %':<10}")
print("-" * 60)

for cls, total in sorted(total_counts.items(), key=lambda x: int(''.join(filter(str.isdigit, x[0])))):
    train_pct = (train_counts.get(cls, 0) / total) * 100 if total > 0 else 0
    val_pct = (val_counts.get(cls, 0) / total) * 100 if total > 0 else 0
    test_pct = (test_counts.get(cls, 0) / total) * 100 if total > 0 else 0
    
    # Print results
    print(f"{cls:<30} {train_pct:.2f}%     {val_pct:.2f}%     {test_pct:.2f}%")

    # Check for warnings
    if not (65 <= train_pct <= 75):
        print(f"⚠️ WARNING: Train set for '{cls}' is out of range (expected ~70%)")
    if not (10 <= val_pct <= 20):
        print(f"⚠️ WARNING: Validation set for '{cls}' is out of range (expected ~15%)")
    if not (10 <= test_pct <= 20):
        print(f"⚠️ WARNING: Test set for '{cls}' is out of range (expected ~15%)")

print("\n✅ Dataset split check completed!")
