import streamlit as st
from streamlit_gsheets import GSheetsConnection
import random
import pandas as pd

# Create a connection object
conn = st.connection("gsheets", type=GSheetsConnection)

def customer_order(username):
    st.title("Customer Order")
    coffee_menu = {
        "Americano": 3.00,
        "Cappuccino": 3.50,
        "Latte": 4.00,
        "Caramel Macchiato": 4.50
    }
    st.header("Menu")
    for coffee, price in coffee_menu.items():
        st.write(f"{coffee}: ${price}")

    coffee_type = st.selectbox("Select your coffee", list(coffee_menu.keys()))
    size = st.selectbox("Select size", ["Small", "Medium", "Large"])
    add_ons = st.multiselect("Select add-ons", ["Extra Sugar", "Milk", "Whipped Cream"])

    if st.button("Place Order"):
        orders_data = conn.read(worksheet="Order")
        orders_df = pd.DataFrame(orders_data)

        booking_number = random.randint(1000, 9999)
        estimated_time = "5-10 minutes"
        st.success(f"Order placed successfully! Your booking number is #{booking_number}. Estimated preparation time: {estimated_time}")
        
        # Add order details to Google Sheets with associated username
        new_order = pd.DataFrame(
            [
                {
                    "Username": username,
                    "Order Type": "Order",
                    "Coffee Type": coffee_type,
                    "Size": size,
                    "Add-ons": ', '.join(add_ons),
                    "Booking Number": booking_number,
                    "Status": "Pending"
                }
            ]
        )
        
        try:
            # Append the new order data to the existing orders data
            updated_orders_df = pd.concat([orders_df, new_order], ignore_index=True)
        
            # Update the Google Sheets Order worksheet with the updated DataFrame
            conn.update(worksheet="Order", data=updated_orders_df)
            st.success("Order placed successfully!")
            
            # Optionally clear the cache to ensure fresh data on reload
            st.cache_data.clear()

        except Exception as e:
            st.error(f"An error occurred while updating Google Sheets: {e}")