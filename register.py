import streamlit as st
import re
from database import create_db, add_user

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

def show_register():

    create_db()

    st.title("📝 Faculty Registration")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    mobile = st.text_input("Mobile Number")
    email = st.text_input("Email")
    dob = st.date_input("Date of Birth")
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Register"):

            if username == "" or password == "" or mobile == "" or email == "":
                st.warning("⚠️ Please fill all fields")
                return

            if not is_valid_email(email):
                st.error("❌ Invalid Email Format")
                return

            if not mobile.isdigit() or len(mobile) != 10:
                st.error("❌ Mobile must be 10 digits")
                return

            result = add_user(
                username,
                password,
                mobile,
                str(dob),
                gender,
                email
            )

            if result == "success":
                st.success("✅ Registration Successful!")
            else:
                st.error("❌ Username already exists")

    with col2:
        if st.button("Back to Login"):
            st.session_state.page = "Login"
            st.experimental_rerun()