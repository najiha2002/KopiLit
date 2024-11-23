import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import datetime

# Assuming `conn` is the Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)
spreadsheet = "1zu1v-w6KnpB-Mw6D5_ikwL2jrkmzGT_MF6Dpu-J0Y_I"

def view_orders():
    st.title("📋 Admin Dashboard: Customer Orders")
    st.markdown("Manage and track customer orders efficiently.")

    # Load order data from Google Sheets
    try:
        orders_data = conn.read(spreadsheet_id = spreadsheet, worksheet="Order")  # Replace with your actual worksheet name
        orders_df = pd.DataFrame(orders_data)
        orders_df['Booking Number'] = orders_df['Booking Number'].astype(int)
        

        # Check if there are any orders
        if not orders_df.empty:
            # Display a summary of orders
            total_orders = len(orders_df)
            pending_orders_count = len(orders_df[orders_df["Status"] != "Completed"])
            completed_orders_count = len(orders_df[orders_df["Status"] == "Completed"])

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Orders", total_orders)
            with col2:
                st.metric("Pending Orders", pending_orders_count)
            with col3:
                st.metric("Completed Orders", completed_orders_count)

            # Filter pending orders for updating status
            st.markdown("---")
            st.markdown("### 🕒 Pending Orders")
            pending_orders = orders_df[(orders_df["Status"] != "Completed") & (orders_df["Status"] != "Cancelled")]

            st.dataframe(pending_orders)

            if not pending_orders.empty:
                booking_num = st.selectbox(
                    "Select a Booking Number to update status",
                    pending_orders["Booking Number"].unique(),
                )

                order_details = orders_df[orders_df["Booking Number"] == booking_num]
                st.markdown("#### Order Details")
                st.dataframe(order_details)

                # Select new status for the order
                new_status = st.selectbox(
                    "Change Order Status",
                    ["Pending", "Processing", "Ready for Pickup", "Completed", "Cancelled"],
                    index=["Pending", "Processing", "Ready for Pickup", "Completed", "Cancelled"].index(
                        order_details["Status"].iloc[0]
                    ),
                )

                # Update button to apply changes
                if st.button("Update Status"):
                    # Update the status in the DataFrame
                    orders_df.loc[orders_df["Booking Number"] == booking_num, "Status"] = new_status

                    # Update the Google Sheet with the modified DataFrame
                    try:
                        conn.update(spreadsheet_id = spreadsheet, worksheet="Order", data=orders_df)

                        # Create a new notification for the customer
                        customer_username = order_details["Username"].iloc[0]
                        notification = {
                            "Recipient": customer_username,  # Notify customer
                            "Sender": "Admin",
                            "Message": f"Your order #{booking_num} status has been updated to {new_status}.",
                            "Timestamp": datetime.datetime.now()
                        }

                        notifications_data = conn.read(spreadsheet_id = spreadsheet, worksheet="Notifications")
                        notifications_df = pd.DataFrame(notifications_data)
                        new_notifications_df = pd.concat(
                            [notifications_df, pd.DataFrame([notification])], ignore_index=True
                        )
                        conn.update(spreadsheet_id = spreadsheet, worksheet="Notifications", data=new_notifications_df)

                        st.success("Order status updated and customer notified!")

                        # Clear cache to ensure fresh data on reload
                        st.cache_data.clear()
                        st.rerun()

                    except Exception as e:
                        st.error(f"An error occurred while updating Google Sheets: {e}")
            else:
                st.info("No pending orders at the moment.")

            # Display completed orders
            st.markdown("---")
            st.markdown("### ✅ Completed Orders")
            completed_orders = orders_df[orders_df["Status"] == "Completed"]
            completed_orders ['Formatted Timestamp'] = pd.to_datetime(orders_df["Timestamp"], format='mixed')
            if not completed_orders.empty:
                st.dataframe(completed_orders.sort_values(by='Formatted Timestamp', ascending=False))
            else:
                st.info("No completed orders found.")

        else:
            st.info("No orders found.")

    except Exception as e:
        st.error(f"An error occurred while fetching order data: {e}")
#test