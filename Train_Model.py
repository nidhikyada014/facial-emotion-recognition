import streamlit as st
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
import os

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first 🔐")
    st.stop()

st.title("🧠 Train Emotion Detection Model")

if st.button("Start Training"):

    with st.spinner("Training in progress... Please wait"):
        st.write("Training started")

        # Load FER2013 CSV
        df = pd.read_csv("fer2013_from_folders.csv")

        X, y = [], []

        for i in range(len(df)):
            pixels = np.array(df['pixels'][i].split(), dtype='float32')
            X.append(pixels)
            y.append(df['emotion'][i])

        X = np.array(X).reshape(-1, 48, 48, 1) / 255.0
        y = tf.keras.utils.to_categorical(y, num_classes=7)

        # Model
        model = Sequential([
            Conv2D(32, (3,3), activation='relu', input_shape=(48,48,1)),
            MaxPooling2D(2,2),
            Conv2D(64, (3,3), activation='relu'),
            MaxPooling2D(2,2),
            Flatten(),
            Dense(128, activation='relu'),
            Dropout(0.5),
            Dense(7, activation='softmax')
        ])

        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )

        # Train (IMPORTANT)
        history = model.fit(
            X, y,
            epochs=10,
            batch_size=64,
            validation_split=0.2,
            verbose=1
        )

        # Save model
        os.makedirs("saved_model", exist_ok=True)
        model.save("saved_model/emotion_model.h5")

        st.success("✅ Training completed & model saved!")
        st.write("Saved at:", os.path.abspath("saved_model/emotion_model.h5"))
        progress = st.progress(0)

class Callback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        progress.progress((epoch+1)/10)