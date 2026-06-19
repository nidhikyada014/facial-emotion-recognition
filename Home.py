import streamlit as st
 
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first 🔐")
    st.stop()
st.image("https://cdn-icons-png.flaticon.com/512/295/295128.png", width=100)
st.title("Welcome to Facial Emotion App")

st.markdown(
    """
    <h1 style='text-align: center;'>😄 Facial Expression Recognition</h1>
    <p style='text-align: center; font-size:18px;'>
    Real-time emotion detection using Deep Learning & Webcam
    </p>
    """,
    unsafe_allow_html=True
)


st.success("✔ Upload image or use webcam to detect emotions")