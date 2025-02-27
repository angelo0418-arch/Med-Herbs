import os

def check_dataset_structure(dataset_path):
    subsets = ['train', 'val', 'test']  
    
    for subset in subsets:
        subset_path = os.path.join(dataset_path, subset)
        if not os.path.exists(subset_path):
            print(f"⚠️ Warning: '{subset}' folder not found!")
            continue
        
        class_folders = sorted(os.listdir(subset_path)) 
        num_classes = len(class_folders)
        
        print(f"\n📂 Checking '{subset}' dataset...")
        print(f"✅ Found {num_classes} classes in '{subset}'")
        for class_name in class_folders:
            print(f" - {class_name}")


dataset_folder = r"C:\Users\ACER\Desktop\System_MedHerbs\Philippine Medicinal Plant Leaf Dataset"
check_dataset_structure(dataset_folder)
