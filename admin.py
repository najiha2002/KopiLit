import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

import admin_orders
import inventory_management
import sales_reporting
import analytics_dashboard

# Admin Flow Placeholder
def flow():
    st.title("Admin Dashboard")
    st.write("Welcome Admin. Here is your overview.")

    # Sidebar navigation options
    st.sidebar.title(f"Hi, admin!")
   # Admin Sidebar Navigation
    navigation = st.sidebar.selectbox("Navigate", ["Orders", "Inventory Management", "Sales Reporting", "Analytics"])
    
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