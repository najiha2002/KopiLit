# main.py
import streamlit as st
import customer_order
import inventory_management
import sales_reporting
import user_authentication
import feedback
import promotions
import analytics_dashboard
import payment
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.title("KopiLit: Coffee Shop App")
#st.set_page_config(page_title="KopiLit: Coffee Shop App", layout="wide")

# Create a connection object
conn = st.connection("gsheets", type=GSheetsConnection)

# Caching function for reading Google Sheets data
@st.cache_data(ttl=60)
def load_users_data():
    return conn.read()

# Login or Register Flow
def login():
    st.title("Login")
    st.write("Please log in to continue.")
    
    user_role = st.selectbox("Login as", ["Customer", "Admin"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        # Validate user from Google Sheets
        users_data = load_users_data()
        user_found = any(user.Username == username and user.Password == password and user.Role == user_role for user in users_data.itertuples())
        st.write(users_data.itertuples())
        
        if user_found:
            st.success(f"Logged in as {user_role}")
            if user_role == "Customer":
                customer_flow(username)
            elif user_role == "Admin":
                admin_flow()
        else:
            st.error("Invalid username or password.")

def register():
    st.title("Register as Customer")
    username = st.text_input("Create Username")
    password = st.text_input("Create Password", type="password")
    
    if st.button("Register"):
        # Check if username already exists
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
                load_users_data.clear()
                
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
    
    # Home
    st.header("Home")
    st.write("Here are your history orders, ongoing orders, and latest offerings.")
    
    # Menu
    st.header("Menu")
    st.write("View our menu and start ordering.")
    customer_order.customer_order(username)
    
    # Orders
    st.header("Orders")
    st.write("View your incoming and past orders.")
    st.write("Earn points with every order - 10 points per RM10 spent!")
    st.write("Here is your order history:")
    orders_data = conn.read()
    user_orders = orders_data[orders_data['Username'] == username]
    st.write(user_orders)
    
    # Rewards
    st.header("Rewards")
    st.write("Check your points and redeem rewards.")
    # Placeholder for rewards calculation based on orders
    total_points = sum(order.get("Amount", 0) // 10 for order in user_orders.itertuples())
    st.write(f"You have {total_points} reward points.")
    
    # Account
    st.header("Account")
    st.write("Manage your settings and provide feedback.")
    feedback.collect_feedback()

# Seamless Admin Flow
def admin_flow():
    st.title("Admin Dashboard")
    st.write("Welcome Admin. Here is the business overview.")
    
    # Home
    st.header("Home")
    st.write("Sales reporting, overall status, and new orders notifications.")
    sales_reporting.sales_report()
    
    # Orders
    st.header("Orders")
    st.write("List all orders of the coffee shop.")
    orders_data = conn.read()
    st.write(orders_data)
    payment.payment_admin()
    
    # Inventory
    st.header("Inventory")
    st.write("Manage inventory and update stock levels.")
    inventory_management.manage_inventory()
    
    # Promotion
    st.header("Promotion")
    st.write("Create and manage promotions for specific or all customers.")
    promotions.manage_promotions()
    
    # Analytics Dashboard
    st.header("Analytics Dashboard")
    st.write("View real-time stats on current orders, inventory levels, and sales.")
    analytics_dashboard.analytics()
    
    # Feedback
    st.header("Feedback")
    st.write("View customer feedback.")
    feedback.view_feedback()
    
    # Account
    st.header("Account")
    st.write("Manage account settings.")