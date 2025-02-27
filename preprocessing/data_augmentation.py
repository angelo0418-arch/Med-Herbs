import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array

# ✅ Function: Get Data Generator
def get_data_generator():
    """
    Gumagawa ng ImageDataGenerator para sa training, validation, at testing.
    Returns:
        train_datagen, val_datagen, test_datagen
    """
    # I-setup ang ImageDataGenerator para sa training
    train_datagen = ImageDataGenerator(
        rescale=1./255,  # Ginagawang 0-1 ang pixel values
        rotation_range=20,
        width_shift_range=0.1,
        height_shift_range=0.1,
        shear_range=0.2,
        zoom_range=0.3,
        horizontal_flip=True,
        vertical_flip=True,
        fill_mode='nearest',
        brightness_range=[0.8, 1.2],  # Nag-aadjust ng brightness mula 50% hanggang 150%
    )

    # I-setup ang ImageDataGenerator para sa validation (karaniwan walang augmentation)
    val_datagen = ImageDataGenerator(rescale=1./255)

    # I-setup ang ImageDataGenerator para sa testing (karaniwan walang augmentation)
    test_datagen = ImageDataGenerator(rescale=1./255)

    # ✅ Ibalik ang tatlong data generators
    return train_datagen, val_datagen, test_datagen

# ---------------------------
# ✅ Ipakita ang sample output ng data augmentation:
# Palitan ang 'sample_image.jpg' ng tamang path ng iyong sample image.
sample_image_path = r'C:/Users/ACER/Desktop/System_MedHerbs/Philippine Medicinal Plant Leaf Dataset/test/Moringa oleifera/Class5_2.jpg'
img = load_img(sample_image_path, target_size=(128, 128))  # I-resize sa 128x128
img_array = img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)  # Gawing batch ang image

# Gumawa ng iterator para sa augmented images
train_datagen, _, _ = get_data_generator()  # Tawagin ang get_data_generator
aug_iter = train_datagen.flow(img_array, batch_size=1)

# Ipakita ang 6 sample augmented images
plt.figure(figsize=(12, 6))
for i in range(6):
    augmented_img = next(aug_iter)[0]  # Kumuha ng isang augmented image
    plt.subplot(2, 3, i+1)
    plt.imshow(augmented_img)
    plt.axis('off')
plt.suptitle("Sample Augmented Images", fontsize=16)
plt.show()
