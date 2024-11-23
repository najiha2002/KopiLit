import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# App title and styling
st.set_page_config(
    page_title="KopiLit: Coffee Shop App",
    page_icon="(coffee)"
)

import customer_home
import admin

# Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)
spreadsheet="1zu1v-w6KnpB-Mw6D5_ikwL2jrkmzGT_MF6Dpu-J0Y_I"

# Load users data
@st.cache_data
def load_users_data():
    users_data = conn.read(spreadsheet_id = "1zu1v-w6KnpB-Mw6D5_ikwL2jrkmzGT_MF6Dpu-J0Y_I", worksheet="User")
    return pd.DataFrame(users_data)

# Initialize session state variables
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user_role' not in st.session_state:
    st.session_state['user_role'] = None
if 'username' not in st.session_state:
    st.session_state['username'] = None

# Login flow
def login():
    st.markdown("### 👤 Login to Your Account")
    st.write("Welcome back! Please log in to continue.")

    # Form for login
    with st.form("login_form"):
        user_role = st.selectbox("Login as", ["Customer", "Admin"])
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            users_data = load_users_data()
            user_found = any(
                user.Username == username and user.Password == password and user.Role == user_role
                for user in users_data.itertuples()
            )

            if user_found:
                st.success(f"✅ Logged in as {user_role}")
                st.session_state['logged_in'] = True
                st.session_state['user_role'] = user_role
                st.session_state['username'] = username
                st.rerun()
            else:
                st.error("❌ Invalid username or password. Please try again.")

# Registration flow
def register():
    st.markdown("### ✨ Register as a New Customer")
    st.write("Create your account and enjoy exclusive offers!")

    # Form for registration
    with st.form("register_form"):
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        gender = st.selectbox("Gender", ["Male", "Female"])
        email = st.text_input("Email")
        username = st.text_input("Create Username")
        password = st.text_input("Create Password", type="password")
        submitted = st.form_submit_button("Register")

        if submitted:
            users_data = load_users_data()
            if any(user.Username == username for user in users_data.itertuples()):
                st.error("❌ Username already taken. Please choose a different one.")
            else:
                new_user_data = pd.DataFrame(
                    [
                        {
                            "First Name": first_name,
                            "Last Name": last_name,
                            "Email": email,
                            "Username": username,
                            "Password": password,
                            "Role": "Customer",
                            "Gender": gender
                        }
                    ]
                )
                try:
                    updated_df = pd.concat([users_data, new_user_data], ignore_index=True)
                    conn.update(worksheet="User", data=updated_df)
                    st.success("✅ Registration successful! Please login to continue.")
                    st.cache_data.clear()
                except Exception as e:
                    st.error(f"❌ An error occurred while updating Google Sheets: {e}")

# Main app flow control
if st.session_state['logged_in']:
    # Dashboard for logged-in users
    st.sidebar.title(f"Welcome, {st.session_state['username']}!")
    if st.session_state['user_role'] == "Customer":
        customer_home.flow(st.session_state['username'])
    elif st.session_state['user_role'] == "Admin":
        admin.flow()

    # Logout button in the sidebar
    if st.sidebar.button("Logout"):
        st.session_state['logged_in'] = False
        st.session_state['user_role'] = None
        st.session_state['username'] = None
        st.rerun()
else:
    # Welcome page for non-logged-in users
    image_url = "https://i.ibb.co/rbPn1vt/kopilit.png"  
    # Add the image to the sidebar
    st.sidebar.image(image_url, use_column_width=True)

    st.sidebar.markdown("## ☕ Welcome to KopiLit!")
    st.sidebar.write("Your favorite coffee shop app! Please login or register to get started.")
    
    # Navigation: Login or Register
    flow_selection = st.sidebar.radio("Navigate", ["Login", "Register"])
    if flow_selection == "Login":
        login()
    elif flow_selection == "Register":
        register()
