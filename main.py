import streamlit as st
import pandas as pd

import customer_home
import customer_order
import inventory_management
import sales_reporting
import user_authentication
import feedback
import promotions
import analytics_dashboard
import payment
from streamlit_gsheets import GSheetsConnection

st.title("KopiLit: Coffee Shop App")

# Establish Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

# Load users data
@st.cache_data
def load_users_data():
    users_data = conn.read(worksheet="Sheet1")
    return pd.DataFrame(users_data)

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
            if user_role == "Customer":
                customer_home.flow(username)  # Call the function from the new module
            elif user_role == "Admin":
                admin_flow()
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
            # Prepare the new user data (order should match the headers in the sheet)
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
                # Step 4: Update Google Sheets by appending the new row
                updated_df = pd.concat([users_data, new_user_data], ignore_index=True)
                conn.update(worksheet="Sheet1", data=updated_df)  # Ensure to pass the argument in the correct format (single list)
                st.success("Registration successful! Please login to continue.")
                
                # Invalidate cache to ensure fresh data
                st.cache_data.clear()
                
            except Exception as e:
                st.error(f"An error occurred while updating Google Sheets: {e}")

# Sidebar navigation
st.sidebar.title("Coffee Shop Management System")
flow_selection = st.sidebar.radio("Navigate", ["Login", "Register"])
if flow_selection == "Login":
    login()
elif flow_selection == "Register":
    register()

# Seamless Customer Flow
def customer_flow(username):
    st.title("Customer Dashboard")
    st.write("Welcome to your homepage.")
    
    st.header("Home")
    st.write("Here are your history orders, ongoing orders, and latest offerings.")
    
    st.header("Menu")
    customer_order.customer_order(username)
    
    st.header("Orders")
    orders_data = pd.DataFrame(conn.read(worksheet="Orders"))
    user_orders = orders_data[orders_data['Username'] == username]
    st.write(user_orders)
    
    st.header("Rewards")
    total_points = sum(order.get("Amount", 0) // 10 for order in user_orders.itertuples())
    st.write(f"You have {total_points} reward points.")
    
    st.header("Account")
    feedback.collect_feedback()

# Seamless Admin Flow
def admin_flow():
    st.title("Admin Dashboard")
    st.write("Welcome Admin. Here is the business overview.")
    
    st.header("Home")
    sales_reporting.sales_report()
    
    st.header("Orders")
    orders_data = pd.DataFrame(conn.read(worksheet="Orders"))
    st.write(orders_data)
    payment.payment_admin()
    
    st.header("Inventory")
    inventory_management.manage_inventory()
    
    st.header("Promotion")
    promotions.manage_promotions()
    
    st.header("Analytics Dashboard")
    analytics_dashboard.analytics()
    
    st.header("Feedback")
    feedback.view_feedback()
    
    st.header("Account")
    st.write("Manage account settings.")
