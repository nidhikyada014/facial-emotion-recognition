import streamlit as st
from tensorflow.keras.models import load_model


# 🔐 Login protection
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first 🔐")
    st.stop()

st.title("📊 Model Information")

# ===== BASIC INFO =====
st.subheader("🔍 Project Overview")
st.write("""
This Facial Emotion Recognition system uses a **Convolutional Neural Network (CNN)**
trained on the **FER2013 dataset** to classify human facial expressions.
""")

# ===== DATASET INFO =====
st.subheader("📁 Dataset Details")
st.markdown("""
- **Dataset Name:** FER2013  
- **Image Size:** 48 × 48 (Grayscale)  
- **Total Classes:** 7  
- **Emotions:** Angry, Disgust, Fear, Happy, Sad, Surprise, Neutral
""")

# ===== MODEL INFO =====
st.subheader("🧠 CNN Model Details")
st.markdown("""
- Input Shape: (48, 48, 1)
- Optimizer: Adam
- Loss Function: Categorical Crossentropy
- Activation Functions: ReLU, Softmax
""")

# ===== LOAD MODEL & SUMMARY =====
st.subheader("📐 Model Architecture")

try:
    model = load_model("saved_model/emotion_model.h5")

    with st.expander("Click to view model summary"):
        summary_list = []
        model.summary(print_fn=lambda x: summary_list.append(x))
        st.text("\n".join(summary_list))

except:
    st.error("Model file not found ❌ Please train the model first.")

# ===== PERFORMANCE =====
st.subheader("📈 Model Performance")
st.markdown("""
- Training Accuracy: ~65–70%  
- Validation Accuracy: ~60–65%  
- Real-time Prediction Speed: ~1 sec/frame
""")

# ===== TECHNOLOGIES =====
st.subheader("🛠 Technologies Used")
st.markdown("""
- Python  
- TensorFlow / Keras  
- OpenCV  
- Streamlit  
- Haar Cascade  
""")

# ===== FOOTER =====
st.markdown("---")
st.caption("Developed as a Mini / Major Project using Deep Learning")