import os

# ✅ Function: Pagbilang ng Images per Class
def count_images(dataset_path):
    """
    Bilangin ang images sa bawat class directory.
    Args:
        dataset_path (str): Path ng dataset (train, val, test).
    Returns:
        dict: Class name bilang key, at bilang ng images bilang value.
    """
    class_counts = {}
    if not os.path.exists(dataset_path):
        print(f"❌ ERROR: Directory '{dataset_path}' not found.")
        return class_counts
    
    # ✅ Bilangin ang images per class
    for class_name in sorted(os.listdir(dataset_path)):
        class_path = os.path.join(dataset_path, class_name)
        if os.path.isdir(class_path):  # Tiyaking directory (class)
            num_images = len([f for f in os.listdir(class_path) if os.path.isfile(os.path.join(class_path, f))])
            class_counts[class_name] = num_images

    return class_counts

# ✅ Define Dataset Directories
base_dir = r"C:\Users\ACER\Desktop\System_MedHerbs\Philippine Medicinal Plant Leaf Dataset"
train_dir = os.path.join(base_dir, "train")
val_dir = os.path.join(base_dir, "val")
test_dir = os.path.join(base_dir, "test")

# ✅ Check Directory Existence
def check_directory(directory):
    """Check kung existing at hindi empty ang directory."""
    if not os.path.exists(directory):
        print(f"❌ ERROR: Directory '{directory}' not found.")
        return False
    elif not os.listdir(directory):
        print(f"❌ ERROR: Directory '{directory}' is empty.")
        return False
    else:
        print(f"✅ Found and verified directory: {directory}")
        return True

# ✅ Verify Directories
if not all([check_directory(train_dir), check_directory(val_dir), check_directory(test_dir)]):
    raise FileNotFoundError("❌ ERROR: Please check your dataset directories.")

# ✅ Get Image Counts for Each Split
train_counts = count_images(train_dir)
val_counts = count_images(val_dir)
test_counts = count_images(test_dir)

# ✅ Compute Total Images Per Class
all_classes = set(train_counts.keys()) | set(val_counts.keys()) | set(test_counts.keys())
total_counts = {cls: train_counts.get(cls, 0) + val_counts.get(cls, 0) + test_counts.get(cls, 0) for cls in all_classes}

# ✅ Display Dataset Distribution
print(f"\n{'Class Name':<30} {'Train %':<10} {'Val %':<10} {'Test %':<10}")
print("-" * 60)

for cls, total in sorted(total_counts.items(), key=lambda x: int(''.join(filter(str.isdigit, x[0])) or '0')):
    train_pct = (train_counts.get(cls, 0) / total) * 100 if total > 0 else 0
    val_pct = (val_counts.get(cls, 0) / total) * 100 if total > 0 else 0
    test_pct = (test_counts.get(cls, 0) / total) * 100 if total > 0 else 0
    
    # ✅ Print Results
    print(f"{cls:<30} {train_pct:.2f}%     {val_pct:.2f}%     {test_pct:.2f}%")

    # ✅ Check for Warnings
    if not (65 <= train_pct <= 75):
        print(f"⚠️ WARNING: Train set for '{cls}' is out of range (expected ~70%)")
    if not (10 <= val_pct <= 20):
        print(f"⚠️ WARNING: Validation set for '{cls}' is out of range (expected ~15%)")
    if not (10 <= test_pct <= 20):
        print(f"⚠️ WARNING: Test set for '{cls}' is out of range (expected ~15%)")

print("\n✅ Dataset split check completed!")