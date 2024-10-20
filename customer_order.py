# Syuk buat order, so bila orang order nnti dkat stock tolak

import streamlit as st
from streamlit_gsheets import GSheetsConnection
import random
import pandas as pd
import datetime

# Create a connection object
conn = st.connection("gsheets", type=GSheetsConnection)

# Initialize session state for the cart if it doesn't exist
if 'cart' not in st.session_state:
    st.session_state.cart = []

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
    quantity = st.number_input("Quantity", min_value=1)

    # Calculate price based on coffee type and size
    size_multiplier = {"Small": 1, "Medium": 1.5, "Large": 2}
    price = coffee_menu[coffee_type] * size_multiplier[size]

    if st.button("Add to Cart"):
        st.session_state.cart.append({
            "Coffee Type": coffee_type,
            "Size": size,
            "Add-ons": ', '.join(add_ons),
            "Quantity": quantity,
            "Price": (price * quantity)
        })
        st.success(f"{coffee_type} added to cart!")

    st.header("Your Cart")
    if len(st.session_state.cart) == 0:
        st.write("Your cart is empty.")
    else:
        total_price = 0
        for idx, item in enumerate(st.session_state.cart):
            st.write(f"{idx + 1}. {item['Coffee Type']} ({item['Size']}), Add-ons: {item['Add-ons']}, Price: ${item['Price']}")
            total_price += item['Price']

        st.write(f"**Total Price: ${total_price:.2f}**")

        if st.button("Place Order"):
            orders_data = conn.read(worksheet="Order")
            orders_df = pd.DataFrame(orders_data)

            timestamp = datetime.datetime.now()
            booking_number = str(random.randint(1000, 9999))
            estimated_time = "5-10 minutes"
            st.success(f"Order placed successfully! Your booking number is #{booking_number}. Estimated preparation time: {estimated_time}")

            # Add cart items to Google Sheets
            new_orders = []
            for item in st.session_state.cart:
                new_orders.append({
                    "Booking Number": booking_number,
                    "Timestamp": timestamp,
                    "Username": username,
                    "Order Type": "Order",
                    "Coffee Type": item['Coffee Type'],
                    "Size": item['Size'],
                    "Add-ons": item['Add-ons'],
                    "Status": "Pending"
                })

            new_order_df = pd.DataFrame(new_orders)

            try:
                # Append the new orders to the existing orders data
                updated_orders_df = pd.concat([orders_df, new_order_df], ignore_index=True)

                # Update the Google Sheets Order worksheet with the updated DataFrame
                conn.update(worksheet="Order", data=updated_orders_df)
                st.success("All items in the cart have been ordered!")

                # Clear the cart
                st.session_state.cart = []

                # Optionally clear the cache to ensure fresh data on reload
                st.cache_data.clear()

            except Exception as e:
                st.error(f"An error occurred while updating Google Sheets: {e}")
