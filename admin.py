import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

import admin_orders
import inventory_management
import sales_reporting
import analytics_dashboard
import feedback
import promotions

# Admin Flow Placeholder
def flow():
    st.title("Admin Dashboard")
    st.write("Welcome Admin. Here is your overview.")

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