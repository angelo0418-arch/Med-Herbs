import os
import shutil
import random

def clear_directory(directory):
    """Burahin ang directory kung meron, para magsimula ulit ng split."""
    if os.path.exists(directory):
        shutil.rmtree(directory)
        print(f"🧹 Cleared existing directory: {directory}")

def create_split_folders(base_dir, class_names):
    """Gumawa ng train/val/test folders para sa bawat class."""
    for split in ["train", "val", "test"]:
        for class_name in class_names:
            path = os.path.join(base_dir, split, class_name)
            os.makedirs(path, exist_ok=True)

def split_dataset(source_dir, base_dir, train_ratio=0.7, val_ratio=0.15, test_ratio=0.15, seed=42):
    """Main function para hatiin ang dataset."""
    random.seed(seed)

    # ✅ Hakbang 1: Ilista lahat ng class folders
    class_names = [d for d in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, d))]

    # ✅ Hakbang 2: Burahin ang dating split folders kung meron
    for split in ["train", "val", "test"]:
        clear_directory(os.path.join(base_dir, split))

    # ✅ Hakbang 3: Gumawa ng bagong folders
    create_split_folders(base_dir, class_names)

    # ✅ Hakbang 4: Shuffle at hatiin ang bawat class
    for class_name in class_names:
        class_path = os.path.join(source_dir, class_name)
        images = [img for img in os.listdir(class_path) if os.path.isfile(os.path.join(class_path, img))]
        random.shuffle(images)

        total = len(images)
        n_train = int(train_ratio * total)
        n_val = int(val_ratio * total)

        splits = {
            "train": images[:n_train],
            "val": images[n_train:n_train + n_val],
            "test": images[n_train + n_val:]
        }

        for split_name, file_list in splits.items():
            for file_name in file_list:
                src = os.path.join(class_path, file_name)
                dst = os.path.join(base_dir, split_name, class_name, file_name)
                shutil.copy2(src, dst)

        print(f"✅ '{class_name}': {total} total → {len(splits['train'])} train, {len(splits['val'])} val, {len(splits['test'])} test")

    print("\n🎉 Dataset splitting complete!")

# 🔧 CONFIGURATION
base_dir = r"C:\Users\ACER\Desktop\System_MedHerbs\Philippine Medicinal Plant Leaf Dataset"
source_dir = base_dir  # Kung walang "full_dataset" folder, gamitin ang base_dir


# ⏬ Patakbuhin ang split
split_dataset(source_dir, base_dir)
