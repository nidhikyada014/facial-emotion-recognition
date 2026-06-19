import streamlit as st
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
from streamlit_autorefresh import st_autorefresh
import os

st.set_page_config(page_title="Faculty Interview Panel", layout="wide")

st.title("👨‍🏫 AI Interview Monitoring System")

# 🔄 Auto refresh
st_autorefresh(interval=2000, key="refresh")

# -------- LOAD MODEL --------
model = load_model("saved_model/emotion_model.h5")

emotion_labels = ['Angry','Disgust','Fear','Happy','Sad','Surprise','Neutral']

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# 🔥 IMPORTANT: SAME PATH AS STUDENT
student_path = r"z:\\"

img_path = os.path.join(student_path, "student.jpg")
csv_path = os.path.join(student_path, "emotion.csv")

# -------- SCORE FUNCTION --------
def calculate_score(emotions):

    stress_emotions = ['Angry','Fear','Sad','Disgust']
    confident_emotions = ['Happy','Neutral','Surprise']

    stress = sum(1 for e in emotions if e in stress_emotions)
    confident = sum(1 for e in emotions if e in confident_emotions)

    total = stress + confident

    if total == 0:
        return 0, 0

    return round((stress/total)*100,2), round((confident/total)*100,2)


# -------- FACULTY CAMERA --------
class FacultyEmotion(VideoTransformerBase):

    def transform(self, frame):

        img = frame.to_ndarray(format="bgr24")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.1, 5)

        for (x,y,w,h) in faces:

            face = gray[y:y+h, x:x+w]

            try:
                face = cv2.resize(face,(48,48))
            except:
                continue

            roi = face.reshape(1,48,48,1)/255.0

            prediction = model.predict(roi, verbose=0)
            label = emotion_labels[np.argmax(prediction)]

            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.putText(img, label, (x,y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

        return img


st.subheader("📷 Faculty Camera")

webrtc_streamer(
    key="faculty",
    video_transformer_factory=FacultyEmotion
)

# -------- STUDENT DATA --------
st.subheader("🎓 Student Monitoring")

try:
    # IMAGE
    if os.path.exists(img_path):
        img = cv2.imread(img_path)

        if img is not None:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            st.image(img, caption="Student Camera", use_column_width=True)
        else:
            st.warning("Image not updating...")

    else:
        st.warning("Waiting for student image...")

    # CSV
    if os.path.exists(csv_path):

        df = pd.read_csv(csv_path)

        if not df.empty:

            latest_emotion = df.iloc[-1]["emotion"]

            st.success(f"Student Emotion: {latest_emotion}")

            # GRAPH
            st.subheader("📊 Emotion Trend")

            fig, ax = plt.subplots()
            ax.plot(df["emotion"])
            ax.set_title("Emotion Changes")
            ax.set_xlabel("Time")
            ax.set_ylabel("Emotion")

            st.pyplot(fig)

            # SCORE
            st.subheader("🧠 Analysis")

            stress, confidence = calculate_score(df["emotion"])

            col1, col2 = st.columns(2)
            col1.metric("Confidence", f"{confidence}%")
            col2.metric("Stress", f"{stress}%")

            if stress > 60:
                st.warning("⚠️ High Stress Detected")

        else:
            st.warning("No emotion data yet...")

    else:
        st.warning("Waiting for emotion data...")

except Exception as e:
    st.error(f"Error: {e}")