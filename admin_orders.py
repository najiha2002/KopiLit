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
        
        # Check if there are any orders
        if not orders_df.empty:
            # Display the order data in a table
            st.write("Below are the orders placed by customers:")
            st.dataframe(orders_df)
            
            # Filter by Order ID to update status
            order_id = st.selectbox("Select an Order ID to update status", orders_df["Order ID"].unique())
            order_details = orders_df[orders_df["Order ID"] == order_id]
            st.write("Order Details:", order_details)
            
            # Select new status for the order
            new_status = st.selectbox("Change Order Status", ["Pending", "Completed", "Cancelled"])
            
            # Update button to apply changes
            if st.button("Update Status"):
                # Update the status in the DataFrame
                orders_df.loc[orders_df["Order ID"] == order_id, "Status"] = new_status

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
