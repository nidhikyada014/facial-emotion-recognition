import streamlit as st
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras import backend as K
from PIL import Image
import pandas as pd
from mtcnn import MTCNN
import cv2
import os

# --------------------- LOGIN CHECK ---------------------
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first 🔐")
    st.stop()

st.title("📷 Image Emotion Prediction (Any Angle)")

# --------------------- EMOTION MODEL ---------------------
def build_emotion_model():
    """
    Builds the emotion recognition CNN.
    Layer names are left default to avoid duplicates in Streamlit reruns.
    """
    model = Sequential([
        Conv2D(32, (3,3), activation='relu', input_shape=(48,48,1)),
        MaxPooling2D(),
        Conv2D(64, (3,3), activation='relu'),
        MaxPooling2D(),
        Flatten(),
        Dense(128, activation='relu'),
        Dense(7, activation='softmax')
    ])
    return model

# Load model once per session
if "emotion_model" not in st.session_state:
    weights_path = "saved_model/emotion_model_weights.h5"
    if os.path.exists(weights_path):
        K.clear_session()  # Clear old models to avoid duplicate layer names
        model = build_emotion_model()
        model.load_weights(weights_path)
        st.session_state.emotion_model = model
    else:
        st.error("❌ Weights file not found. Run fix_model.py first.")
        st.stop()
else:
    model = st.session_state.emotion_model

emotion_labels = ['Angry','Disgust','Fear','Happy','Sad','Surprise','Neutral']

# --------------------- IMAGE UPLOAD ---------------------
# Session flag to clear file
if "clear_file" not in st.session_state:
    st.session_state.clear_file = False

# Button to clear uploaded image
if st.button("Clear Uploaded Image"):
    st.session_state.clear_file = True

# File uploader (do not assign st.session_state directly!)
uploaded_file = st.file_uploader("Upload Image", type=["jpg","png","jpeg"])

# Handle clearing
if st.session_state.clear_file:
    uploaded_file = None
    st.session_state.clear_file = False

# --------------------- PROCESS UPLOADED IMAGE ---------------------
if uploaded_file is not None:
    # Load and display uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    img = np.array(image)

    # Detect faces using MTCNN
    detector = MTCNN()
    faces = detector.detect_faces(img)

    if len(faces) == 0:
        st.error("❌ No face detected. Make sure the image contains a human face.")
        st.stop()

    # Pick the largest face
    largest_face = max(faces, key=lambda f: f['box'][2]*f['box'][3])
    x, y, w, h = largest_face['box']
    x, y = max(0, x), max(0, y)  # Ensure positive coordinates
    face = img[y:y+h, x:x+w]

    # Preprocess face for emotion model
    gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, (48,48))
    gray = gray.astype("float32") / 255.0
    gray = np.reshape(gray, (1,48,48,1))

    # Predict emotion
    prediction = model.predict(gray, verbose=0)
    label = emotion_labels[np.argmax(prediction)]
    confidence = np.max(prediction) * 100

    st.success(f"Detected Emotion: **{label}** ({confidence:.2f}%)")

    # Show confidence chart
    df = pd.DataFrame({
        "Emotion": emotion_labels,
        "Confidence": prediction[0]
    })
    st.subheader("📊 Emotion Confidence")
    st.bar_chart(df.set_index("Emotion"))
