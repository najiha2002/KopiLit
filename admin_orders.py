# admin_orders.py

import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# Assuming `conn` is the Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

def view_orders():
    st.header("Customer Orders")
    
    # Load order data from Google Sheets
    try:
        orders_data = conn.read(worksheet="Order")  # Replace "Order" with your actual worksheet name
        orders_df = pd.DataFrame(orders_data)
        orders_df = orders_df.sort_values(by="Timestamp", ascending=False)
        
        # Check if there are any orders
        if not orders_df.empty:
            # Display the order data in a table
            st.write("Below are the orders placed by customers:")
            st.dataframe(orders_df)
            pending_orders = orders_df[orders_df["Status"] != "Completed"]
            
            # Filter by Order ID to update status
            booking_num = st.selectbox("Select a Booking Number to update status", pending_orders["Booking Number"].unique())
            order_details = orders_df[orders_df["Booking Number"] == booking_num]
            st.write("Order Details:", order_details)
            
            # Select new status for the order
            new_status = st.selectbox("Change Order Status", ["Pending", "Processing", "Ready for Pickup", "Completed", "Cancelled"])
            
            # Update button to apply changes
            if st.button("Update Status"):
                # Update the status in the DataFrame
                orders_df.loc[orders_df["Booking Number"] == booking_num, "Status"] = new_status

                # Update the Google Sheet with the modified DataFrame
                try:
                    conn.update(worksheet="Order", data=orders_df)
                    st.success("Order status updated successfully!")
                    
                    # Optionally clear cache to ensure fresh data on reload
                    st.cache_data.clear()
                
                except Exception as e:
                    st.error(f"An error occurred while updating Google Sheets: {e}")
        
        else:
            st.info("No orders found.")
    
    except Exception as e:
        st.error(f"An error occurred while fetching order data: {e}")
