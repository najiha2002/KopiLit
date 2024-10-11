import streamlit as st
from streamlit_gsheets import GSheetsConnection
import random

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
        booking_number = random.randint(1000, 9999)
        estimated_time = "5-10 minutes"
        st.success(f"Order placed successfully! Your booking number is #{booking_number}. Estimated preparation time: {estimated_time}")
        
        # Add order details to Google Sheets with associated username
        new_order = {
            "Username": username,
            "Order Type": "Order",
            "Coffee Type": coffee_type,
            "Size": size,
            "Add-ons": ', '.join(add_ons),
            "Booking Number": booking_number,
            "Status": "Pending"
        }
        conn.write(new_order)