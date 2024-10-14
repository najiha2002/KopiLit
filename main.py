import streamlit as st
import pandas as pd

import customer_home  # This is where the customer flow is handled
import admin
from streamlit_gsheets import GSheetsConnection

st.title("KopiLit: Coffee Shop App")

# Establish Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

# Load users data
@st.cache_data
def load_users_data():
    users_data = conn.read(worksheet="User")
    return pd.DataFrame(users_data)

# Initialize session state variables for login state management
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user_role' not in st.session_state:
    st.session_state['user_role'] = None
if 'username' not in st.session_state:
    st.session_state['username'] = None

# Login or Register Flow
def login():
    st.title("Login")
    st.write("Please log in to continue.")
    
    user_role = st.selectbox("Login as", ["Customer", "Admin"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        users_data = load_users_data()
        user_found = any(
            user.Username == username and user.Password == password and user.Role == user_role
            for user in users_data.itertuples()
        )
        
        if user_found:
            st.success(f"Logged in as {user_role}")
            st.session_state['logged_in'] = True
            st.session_state['user_role'] = user_role
            st.session_state['username'] = username
            # Force a page reload to show the dashboard
            st.rerun()
        else:
            st.error("Invalid username or password.")

def register():
    st.title("Register as Customer")
    username = st.text_input("Create Username")
    password = st.text_input("Create Password", type="password")
    
    if st.button("Register"):
        users_data = load_users_data()
        if any(user.Username == username for user in users_data.itertuples()):
            st.error("Username already taken. Please choose a different one.")
        else:
            # Prepare the new user data
            new_user_data = pd.DataFrame(
                [
                    {
                        "Username": username,
                        "Password": password,
                        "Role": "Customer"
                    }  
                ]
            )

            try:
                # Update Google Sheets by appending the new row
                updated_df = pd.concat([users_data, new_user_data], ignore_index=True)
                conn.update(worksheet="User", data=updated_df)  # Ensure to pass the argument in the correct format
                st.success("Registration successful! Please login to continue.")
                
                # Clear the cache to ensure fresh data
                st.cache_data.clear()
                
            except Exception as e:
                st.error(f"An error occurred while updating Google Sheets: {e}")



# Main App Flow Control
if st.session_state['logged_in']:
    # Show the customer or admin dashboard based on user role
    if st.session_state['user_role'] == "Customer":
        customer_home.flow(st.session_state['username'])
    elif st.session_state['user_role'] == "Admin":
        admin.flow()

    # Single logout button in the sidebar
    if st.sidebar.button("Logout"):
        st.session_state['logged_in'] = False
        st.session_state['user_role'] = None
        st.session_state['username'] = None
        st.rerun()

else:
    # Show the login or register page if not logged in
    st.sidebar.title("Coffee Shop Management System")
    flow_selection = st.sidebar.radio("Navigate", ["Login", "Register"])
    if flow_selection == "Login":
        login()
    elif flow_selection == "Register":
        register()
