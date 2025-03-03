from tensorflow.keras import models, layers, regularizers, initializers
from dropout import add_dropout 

def build_model(num_classes):
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), padding="same", 
                      kernel_initializer=initializers.HeNormal(),
                      kernel_regularizer=regularizers.l2(0.0001), 
                      input_shape=(224, 224, 3)),
        layers.BatchNormalization(),
        layers.Activation('swish'),  
        layers.MaxPooling2D((2, 2)),
        add_dropout(0.3),  

        layers.Conv2D(64, (3, 3), padding="same", 
                      kernel_initializer=initializers.HeNormal(),
                      kernel_regularizer=regularizers.l2(0.0001)),
        layers.BatchNormalization(),
        layers.Activation('swish'),
        layers.MaxPooling2D((2, 2)),
        add_dropout(0.3),

        layers.Conv2D(128, (3, 3), padding="same", 
                      kernel_initializer=initializers.HeNormal(),
                      kernel_regularizer=regularizers.l2(0.0001)),
        layers.BatchNormalization(),
        layers.Activation('swish'),
        layers.MaxPooling2D((2, 2)),
        add_dropout(0.4),

        # Global Average Pooling for Reduced Complexity
        layers.GlobalAveragePooling2D(),

        layers.Dense(128, 
                     kernel_initializer=initializers.HeNormal(),
                     kernel_regularizer=regularizers.l2(0.0001)),
        layers.BatchNormalization(),
        layers.Activation('swish'),
        add_dropout(0.5),

        layers.Dense(num_classes, activation='softmax')
    ])

    # I-print ang summary ng model
    model.summary()

    return model

if __name__ == "__main__":
    model = build_model(num_classes=40)  # Palitan ng tamang bilang ng classes sa dataset mo
