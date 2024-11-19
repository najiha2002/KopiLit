import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

import admin_orders
import inventory_management
import sales_reporting
import analytics_dashboard
import feedback
import promotions

import datetime

# Establish Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

import datetime
import pandas as pd

def check_notifications():
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
            (notifications_data["Recipient"] == "Admin")
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


# Admin Flow Placeholder
def flow():
    st.title("Admin Dashboard")
    st.write("Welcome Admin. Here is your overview.")

    # Check for customer order notifications
    check_notifications()

    # Sidebar navigation options
    st.sidebar.title(f"Hi, admin!")
   # Admin Sidebar Navigation
    navigation = st.sidebar.selectbox("Navigate", ["Orders", "Inventory Management", "Sales Reporting", "Analytics", "Feedback", "Promotions"])
    
    # Conditionally display sections based on navigation selection

    if navigation == "Orders":
        admin_orders.view_orders()
    
    elif navigation == "Inventory Management":
        st.header("Inventory Management")
        inventory_management.manage_inventory()
    
    elif navigation == "Sales Reporting":
        st.header("Sales Reporting")
        sales_reporting.sales_report()
    
    elif navigation == "Analytics":
        st.header("Analytics")
        analytics_dashboard.analytics()
    
    elif navigation == "Customer Feedback":
        st.header("Customer Feedback")
        feedback.view_feedback()

    elif navigation == "Promotions":
        st.header("Manage Promotion")
        promotions.manage_promotions()