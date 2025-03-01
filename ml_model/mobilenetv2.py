from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import regularizers
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau

def build_mobilenetv2_model(num_classes, 
                            input_shape=(224, 224, 3), 
                            learning_rate=1e-4, 
                            dropout_rate=0.5, 
                            fine_tune_at=100):
    try:
        print("\n🚀 Loading MobileNetV2 base model...")

        # Load Pretrained MobileNetV2
        base_model = MobileNetV2(input_shape=input_shape,
                                 include_top=False,
                                 weights='imagenet')
        
        # Fine-tune upper layers
        for layer in base_model.layers[:fine_tune_at]:
            layer.trainable = False
        for layer in base_model.layers[fine_tune_at:]:
            layer.trainable = True
        print("✅ MobileNetV2 loaded and fine-tuned.")

        # Add Custom Layers
        model = models.Sequential([
            base_model,
            layers.GlobalAveragePooling2D(),
            layers.BatchNormalization(),
            layers.Dense(256, kernel_regularizer=regularizers.l2(0.0001), activation='relu'),
            layers.Dropout(dropout_rate),
            layers.Dense(num_classes, activation='softmax')
        ])
        print("✅ Custom layers added.")

        # Compile Model
        model.compile(optimizer=Adam(learning_rate=learning_rate),
                      loss='categorical_crossentropy',
                      metrics=['accuracy'])
        
        # Model Summary
        print("\n🔍 Model Summary:")
        model.summary()

        print("\n✅ Model compiled successfully.")
        return model
    
    except Exception as e:
        print(f"\n❌ Error occurred while building model: {e}")
        return None


# Optional: Define Callbacks
def get_callbacks(patience=5):
    early_stopping = EarlyStopping(monitor='val_loss', patience=patience, restore_best_weights=True)
    lr_scheduler = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=3, min_lr=1e-6)
    print("\n🔔 Callbacks set.")
    return [early_stopping, lr_scheduler]

# Example Usage
if __name__ == '__main__':
    print("\n🚀 Building and Compiling Model...")
    model = build_mobilenetv2_model(num_classes=5)
    if model:
        print("\n✅ Model is ready for training.")
    else:
        print("\n❌ Model building failed.")
