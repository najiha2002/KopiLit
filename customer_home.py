# customer_dashboard.py

import streamlit as st
import pandas as pd
import customer_order
import feedback
from streamlit_gsheets import GSheetsConnection

# Establish Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

def flow(username):
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
