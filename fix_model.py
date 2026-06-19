from tensorflow.keras.models import load_model
import os

model_path = "saved_model/emotion_model.h5"
weights_path = "saved_model/emotion_model_weights.h5"

if os.path.exists(model_path):
    # Load original model (even with duplicate names)
    model = load_model(model_path, compile=False)

    # Save only weights
    model.save_weights(weights_path)
    print(f"✅ Weights saved to {weights_path}")
else:
    print("❌ Original model not found!")
