import streamlit as st
from database import login_user, create_db
import register

create_db()

# SESSION
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "Login"


# LOGIN
def login():

    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Login"):

            if username == "" or password == "":
                st.warning("⚠️ Please fill all fields")
                return

            result = login_user(username, password)

            if result:
                st.session_state.logged_in = True
                st.success("Login successful ✅")
                st.experimental_rerun()
            else:
                st.error("New user?..Please Rgestration First")

    with col2:
        if st.button("New User?? Click Here For Register"):
            st.session_state.page = "Register"
            st.experimental_rerun()


# LOGOUT
def logout():
    st.session_state.logged_in = False
    st.session_state.page = "Login"
    st.experimental_rerun()


# MAIN
if not st.session_state.logged_in:

    if st.session_state.page == "Login":
        login()

    elif st.session_state.page == "Register":
        register.show_register()

else:
    st.sidebar.success("Logged in Successfully ✅")

    if st.sidebar.button("Logout"):
        logout()

    st.title("😊 Facial Emotion Recognition App")

    st.write("Welcome! You are logged in successfully.")

    st.markdown("---")

    st.subheader("📌 Features")
    st.write("""
    ✔ Image Emotion Detection  
    ✔ Webcam Emotion Detection  
    ✔ Student Monitoring  
    ✔ Faculty Dashboard  
    """)