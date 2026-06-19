import streamlit as st
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer
import cv2
import numpy as np
from tensorflow.keras.models import load_model

# ------------------ LOGIN CHECK ------------------
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first 🔐")
    st.stop()

st.title("📹 Multiple Face Emotion Detection")

# ------------------ LOAD EMOTION MODEL ------------------
model = load_model('saved_model/emotion_model.h5')
emotion_labels = ['Angry','Disgust','Fear','Happy','Sad','Surprise','Neutral']

# ------------------ LOAD HAAR CASCADE (Built-in OpenCV) ------------------
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# ------------------ VIDEO PROCESSING CLASS ------------------
class EmotionDetector(VideoTransformerBase):
    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect multiple faces
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,   # smaller = more precise detection
            minNeighbors=5,
            minSize=(30, 30)
        )

        # Loop through all detected faces
        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]

            try:
                face = cv2.resize(face, (48, 48))
            except:
                continue

            roi = face.reshape(1, 48, 48, 1) / 255.0

            # Predict emotion
            prediction = model.predict(roi, verbose=0)
            max_index = np.argmax(prediction)
            label = emotion_labels[max_index]
            confidence = np.max(prediction)

            label_text = f"{label} ({confidence:.2f})"

            # Draw rectangle + label
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(
                img,
                label_text,
                (x, y-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )
       
        return img


# ------------------ START CAMERA ------------------
webrtc_streamer(
    key="emotion",
    video_transformer_factory=EmotionDetector
)
