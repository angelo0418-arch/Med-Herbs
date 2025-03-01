import sys
import os
from .data_augmentation import get_data_generator
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ✅ Global Setting: Madaling Baguhin ang Batch Size Dito
BATCH_SIZE = 16  # Mas mababang batch size para bawas memory usage

# ✅ Function: Pag-check ng Dataset Directory
def check_directory(directory):
    """Check if the directory exists and is not empty."""
    if not os.path.exists(directory):
        print(f"❌ ERROR: Directory '{directory}' does not exist.")
        return False
    elif not os.listdir(directory):
        print(f"❌ ERROR: Directory '{directory}' is empty.")
        return False
    else:
        print(f"✅ Found and verified directory: {directory}")
        return True

# ✅ Function: Load Dataset Using ImageDataGenerator
def load_data():
    # Base Directory: Philippine Medicinal Plant Leaf Dataset
    BASE_DIR = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'Philippine Medicinal Plant Leaf Dataset')
    )

    # Define Dataset Directories
    train_dir = os.path.join(BASE_DIR, 'train')
    val_dir = os.path.join(BASE_DIR, 'val')
    test_dir = os.path.join(BASE_DIR, 'test')

    # Directory Verification
    if not all([check_directory(train_dir), check_directory(val_dir), check_directory(test_dir)]):
        raise FileNotFoundError("❌ ERROR: Please check your dataset directories.")
    
    # ✅ Tawagin ang get_data_generator
    train_datagen, val_datagen, test_datagen = get_data_generator()

    # ✅ Load Training Data
    train_data = train_datagen.flow_from_directory(
        train_dir, 
        target_size=(224, 224),  # Ginawang Consistent ang target_size
        class_mode='categorical', 
        batch_size=BATCH_SIZE,
        shuffle=True
    )

    # ✅ Load Validation Data
    val_data = val_datagen.flow_from_directory(
        val_dir, 
        target_size=(224, 224),  # Ginawang Consistent ang target_size
        class_mode='categorical', 
        batch_size=BATCH_SIZE,
        shuffle=False
    )

    # ✅ Load Test Data
    test_data = test_datagen.flow_from_directory(
        test_dir, 
        target_size=(224, 224),  # Ginawang Consistent ang target_size
        class_mode='categorical', 
        batch_size=BATCH_SIZE,
        shuffle=False
    )

    # ✅ Display Dataset Summary and Class Mappings
    print("\n🔎 DATASET SUMMARY 🔍")
    print(f"Training Samples: {train_data.samples}")
    print(f"Validation Samples: {val_data.samples}")
    print(f"Test Samples: {test_data.samples}")
    print("\n📊 Class Indices:", train_data.class_indices)

    # ✅ Display Sample Batch for Verification
    image_batch, label_batch = next(iter(train_data))
    print("\n🖼️ Sample Image Batch Shape:", image_batch.shape)
    print("🏷️ Sample Label Batch Shape:", label_batch.shape)

    # ✅ Return Data Generators
    return train_data, val_data, test_data
