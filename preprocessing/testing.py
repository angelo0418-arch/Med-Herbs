import os


# Or check test images
dataset_dir = r"C:\Users\ACER\Desktop\System_MedHerbs\Philippine Medicinal Plant Leaf Dataset\val"


for class_name in os.listdir(dataset_dir):
    class_path = os.path.join(dataset_dir, class_name)
    if os.path.isdir(class_path):
        num_images = len(os.listdir(class_path))
        print(f"{class_name}: {num_images} images")

from PIL import Image
import os

dataset_dir = 'Philippine Medicinal Plant Leaf Dataset'

for root, dirs, files in os.walk(dataset_dir):
    for file in files:
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(root, file)
            try:
                with Image.open(img_path) as img:
                    width, height = img.size
                    pixels = width * height
                    if pixels > 89_478_485:
                        print(f"⚠️ Oversized image: {img_path} ({width}x{height} = {pixels} pixels)")
            except Exception as e:
                print(f"❌ Error reading {img_path}: {e}")
