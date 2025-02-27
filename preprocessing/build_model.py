from tensorflow.keras import models, layers, regularizers
from dropout import add_dropout  # Import Dropout function

def build_model(num_classes):
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), padding="same", kernel_regularizer=regularizers.l2(0.0001), input_shape=(128, 128, 3)),
        layers.BatchNormalization(),
        layers.Activation('relu'),
        layers.MaxPooling2D((2, 2)),
        add_dropout(0.5),  # Tumawag ng Dropout function mula sa dropout.py

        layers.Conv2D(64, (3, 3), padding="same", kernel_regularizer=regularizers.l2(0.0001)),
        layers.BatchNormalization(),
        layers.Activation('relu'),
        layers.MaxPooling2D((2, 2)),
        add_dropout(0.5),

        layers.Conv2D(128, (3, 3), padding="same", kernel_regularizer=regularizers.l2(0.0001)),
        layers.BatchNormalization(),
        layers.Activation('relu'),
        layers.MaxPooling2D((2, 2)),
        add_dropout(0.5),

        # Gumamit ng GlobalAveragePooling2D sa halip ng Flatten para sa mas mababang complexity
        layers.GlobalAveragePooling2D(),

        layers.Dense(128, kernel_regularizer=regularizers.l2(0.0001)),
        layers.BatchNormalization(),
        layers.Activation('relu'),
        add_dropout(0.5),

        layers.Dense(num_classes, activation='softmax')
    ])

    # I-print ang summary ng model
    model.summary()

    return model

if __name__ == "__main__":
    model = build_model(num_classes=40)  # Palitan ng tamang bilang ng classes sa dataset mo

