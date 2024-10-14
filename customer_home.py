# customer_home.py

import streamlit as st
import pandas as pd
import customer_order
import feedback
from streamlit_gsheets import GSheetsConnection

# Establish Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

def flow(username):
    st.title("Customer Dashboard")
    st.write(f"Welcome, {username}!")

    # Sidebar navigation options
    st.sidebar.title(f"Hi, {username}!")
    navigation = st.sidebar.selectbox("Navigate", ["Home", "Menu", "Orders", "Rewards", "Account"])

    if navigation == "Home":
        st.header("Home")
        st.write("Here are your history orders, ongoing orders, and latest offerings.")

    # to start new order
    elif navigation == "Menu":
        st.header("Menu")
        customer_order.customer_order(username)

    # View current/past orders
    elif navigation == "Orders":
        st.header("Orders")
        orders_data = pd.DataFrame(conn.read(worksheet="Order"))
        user_orders = orders_data[orders_data['Username'] == username]
        st.write(user_orders)

    elif navigation == "Rewards":
        st.header("Rewards")
        # Assuming each order has an 'Amount' column for calculating rewards
        orders_data = pd.DataFrame(conn.read(worksheet="Order"))
        user_orders = orders_data[orders_data['Username'] == username]
        total_points = sum(order.get("Amount", 0) // 10 for order in user_orders.itertuples())
        st.write(f"You have {total_points} reward points.")

    elif navigation == "Account":
        st.header("Account")
        feedback.collect_feedback()

