import streamlit as st

def authentication():
    st.title("User Authentication")
    st.write("Log in to access additional features.")
    # Placeholder for login/signup features
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Log In"):
        st.success("Logged in successfully!")