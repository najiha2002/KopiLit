# customer_home.py

import streamlit as st
import pandas as pd
import customer_order
import feedback
from streamlit_gsheets import GSheetsConnection

import datetime

# Establish Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

def check_notifications(username):
    try:
        # Load notifications from the Google Sheets
        notifications_data = pd.DataFrame(conn.read(worksheet="Notifications"))

        # Convert the Timestamp column to datetime format using the correct format
        notifications_data["Timestamp"] = pd.to_datetime(notifications_data["Timestamp"], format="%Y-%m-%d %H:%M:%S", errors="coerce")
        
        # Filter notifications for today and where the recipient is Admin
        today = datetime.datetime.now().date()
        notifications_data["Timestamp"] = notifications_data["Timestamp"].dt.date
        today_notifications = notifications_data[
            (notifications_data["Timestamp"] == today) &
            (notifications_data["Recipient"] == username)
        ]

        if not today_notifications.empty:
            # Add an expander to show today's notifications
            with st.sidebar.expander(f"Notifications for {today.strftime('%Y-%m-%d')}"):
                for index, notification in today_notifications.iterrows():
                    st.info(notification["Message"])
        else:
            st.sidebar.info("No notifications for today.")

    except Exception as e:
        st.sidebar.error(f"Error fetching notifications: {e}")

def flow(username):

    user_df = pd.DataFrame(conn.read(worksheet="User"))
    user_data = user_df[user_df['Username'] == username]
    first_name = user_data['First Name'].iloc[0]

    check_notifications(username)
    
    st.title("Customer Dashboard")
    st.write(f"Welcome, {first_name}!")

    # Sidebar navigation options
    st.sidebar.title(f"Hi, {first_name}!")
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

