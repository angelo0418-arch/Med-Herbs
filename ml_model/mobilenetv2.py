from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import regularizers

def build_mobilenetv2_model(num_classes):
    
    base_model = MobileNetV2(input_shape=(128, 128, 3),
                             include_top=False,  
                             weights='imagenet')

    
    base_model.trainable = False

    
    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dense(256, kernel_regularizer=regularizers.l2(0.0001), activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(num_classes, activation='softmax')
    ])

    
    model.compile(optimizer=Adam(learning_rate=0.0001),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    
    model.summary()

    return model
