import streamlit as st 
from streamlit_gsheets import GSheetsConnection
import pandas as pd

import user_authentication

# Create a connection object for Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

def view_order():
    st.title("☕ Past Orders")
    st.write("---")  # Add a horizontal line for better separation

    st.subheader("View your past order details below:")

    # Connect to the "Order" worksheet
    order_sheet = conn.read(worksheet="Order")  # Adjust to your actual worksheet name
    order_df = pd.DataFrame(order_sheet)  # Convert the data to a DataFrame

    # Ensure the DataFrame has the expected structure
    if 'Username' in order_df.columns and 'Status' in order_df.columns:
        # Filter for the logged-in user and completed orders
        user_orders = order_df[
            (order_df['Username'] == user_authentication.username) &
            (order_df['Status'] == 'Completed')
        ]

        if not user_orders.empty:
            st.success("Here are your completed orders:")
            
            # Display order details
            for index, order in user_orders.iterrows():
                st.write(f"### 📝 Order No.: {order['Booking Number']}")
                st.write(f"**Coffee Type**: {order['Coffee Type']}")
                st.write(f"**Quantity**: {order['Quantity']}")
                st.write(f"**Total Price**: ${order['Price']:.2f}")
                st.write("---")  # Separator for each order
        else:
            st.warning("You don't have any completed orders yet.")
    else:
        st.error("The data structure is not as expected. Please check the Google Sheet.")
