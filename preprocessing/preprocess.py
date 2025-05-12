# preprocess.py
import os
from PIL import Image

# Function: Check Dataset Classes
def check_dataset_classes(dataset_path):
    if not os.path.exists(dataset_path):
        print(f"❌ Dataset path '{dataset_path}' does not exist.")
        return None
    
    classes = sorted([d for d in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, d))])
    
    print(f"\n✅ Found {len(classes)} classes in '{dataset_path}':\n")
    for i, class_name in enumerate(classes, start=1):
        print(f" {i}. {class_name}")
    
    return set(classes)

# Function: Resize Images Consistently
def resize_images(dataset_path, output_path, image_size=(128, 128), allowed_extensions=('.png', '.jpg', '.jpeg')):
    os.makedirs(output_path, exist_ok=True)

    for root, dirs, files in os.walk(dataset_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file.lower().endswith(allowed_extensions):  
                relative_path = os.path.relpath(root, dataset_path)
                output_folder = os.path.join(output_path, relative_path)
                os.makedirs(output_folder, exist_ok=True)

                output_file_path = os.path.join(output_folder, file)
                try:
                    with Image.open(file_path) as img:
                        img = img.resize(image_size)
                        img = img.convert('RGB')  # Convert to RGB
                        img.save(output_file_path)
                        print(f"✅ Resized: {output_file_path}")
                except Exception as e:
                    print(f"❌ Error resizing {file}: {e}")

# Main Function
def main():
    dataset_root = "../Philippine Medicinal Plant Leaf Dataset"
    output_path = "Resized_Dataset"
    
    train_path = os.path.join(dataset_root, "train")
    val_path = os.path.join(dataset_root, "val")
    test_path = os.path.join(dataset_root, "test")

    print("Checking dataset classes...")
    train_classes = check_dataset_classes(train_path)
    val_classes = check_dataset_classes(val_path)
    test_classes = check_dataset_classes(test_path)

    if train_classes and val_classes and test_classes:
        if train_classes == val_classes == test_classes:
            print("\n✅ All datasets have the same class distribution!")
        else:
            print("\n⚠️ Warning: Mismatch detected in dataset classes!")

    print("\nResizing images...")
    resize_images(dataset_root, output_path)
    print("\n✅ All valid images resized successfully!")

if __name__ == "__main__":
    main()