import streamlit as st
import datetime
import random
import pandas as pd


def payment_page(conn):
    st.title("💳 Payment Gateway")

    # Retrieve session state variables
    final_price = st.session_state.final_price
    total_price = st.session_state.total_price
    promo_code = st.session_state.promo_code
    loyalty_points = st.session_state.loyalty_points
    cart = st.session_state.cart

    st.markdown(f"### 🏷️ Final Price: **${final_price:.2f}**")
    st.markdown(f"#### 🌟 Loyalty Points Earned: **{loyalty_points} points**")

    # Payment options
    st.markdown("### 🏦 Payment Options")
    payment_option = st.radio("Choose your payment method:", ["Credit/Debit Card", "PayPal", "Cash on Delivery"])

    if payment_option == "Credit/Debit Card":
        st.markdown("#### 💳 Enter Card Details")
        card_number = st.text_input("Card Number")
        card_holder = st.text_input("Card Holder Name")
        expiry_date = st.text_input("Expiry Date (MM/YY)")
        cvv = st.text_input("CVV", type="password")
        if st.button("Pay Now"):
            if card_number and card_holder and expiry_date and cvv:
                st.success(f"Payment of **${final_price:.2f}** successful via Credit/Debit Card!")
                complete_order(conn, payment_option)

    elif payment_option == "PayPal":
        st.markdown("#### 🅿️ Enter PayPal Email")
        paypal_email = st.text_input("PayPal Email")
        if st.button("Pay Now"):
            if paypal_email:
                st.success(f"Payment of **${final_price:.2f}** successful via PayPal!")
                complete_order(conn, payment_option)

    elif payment_option == "Cash on Delivery":
        if st.button("Confirm Order"):
            st.success(f"Order confirmed! Pay **${final_price:.2f}** upon delivery.")
            complete_order(conn, payment_option)


def complete_order(conn, payment_method):
    try:
        # Generate booking details
        timestamp = datetime.datetime.now()
        booking_number = str(random.randint(1000, 9999))
        username = "JohnDoe"  # Replace with actual username logic
        estimated_time = "5-10 minutes"

        # Add order to Google Sheets
        orders_data = conn.read(worksheet="Order")
        orders_df = pd.DataFrame(orders_data)

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
                "Quantity": item['Quantity'],
                "Status": "Paid",
                "Price": st.session_state.total_price,
                "Final Price": st.session_state.final_price,
                "Promo Code": st.session_state.promo_code,
                "Loyalty Points": st.session_state.loyalty_points,
                "Payment Method": payment_method
            })

        new_order_df = pd.DataFrame(new_orders)
        updated_orders_df = pd.concat([orders_df, new_order_df], ignore_index=True)
        conn.update(worksheet="Order", data=updated_orders_df)

        # Update inventory
        inventory_data = conn.read(worksheet="Inventory")
        inventory_df = pd.DataFrame(inventory_data)
        inventory_dict = {row['Item']: row['Stock'] for _, row in inventory_df.iterrows()}

        ingredient_requirements = {
            "Americano": {"Coffee Beans": 1},
            "Cappuccino": {"Coffee Beans": 1, "Milk": 0.5},
            "Latte": {"Coffee Beans": 1, "Milk": 1},
            "Caramel Macchiato": {"Coffee Beans": 1, "Milk": 1, "Caramel Syrup": 0.5},
        }

        # Calculate ingredient requirements based on cart
        required_ingredients = {}
        for item in st.session_state.cart:
            coffee_type = item['Coffee Type']
            quantity = item['Quantity']
            if coffee_type in ingredient_requirements:
                for ingredient, amount in ingredient_requirements[coffee_type].items():
                    required_ingredients[ingredient] = required_ingredients.get(ingredient, 0) + (amount * quantity)

        # Check stock availability
        for ingredient, required_amount in required_ingredients.items():
            if inventory_dict.get(ingredient, 0) < required_amount:
                st.error(f"Not enough {ingredient} in stock to fulfill the order.")
                return

        # Deduct from inventory
        for ingredient, required_amount in required_ingredients.items():
            inventory_dict[ingredient] -= required_amount

        # Save updated inventory to Google Sheets
        updated_inventory_df = pd.DataFrame(
            [{"Item": item, "Stock": stock} for item, stock in inventory_dict.items()]
        )
        conn.update(worksheet="Inventory", data=updated_inventory_df)

        # Notify admin
        notification = {
            "Recipient": "Admin",
            "Sender": username,
            "Message": f"Payment received for order #{booking_number} by {username}.",
            "Timestamp": datetime.datetime.now()
        }

        notifications_data = conn.read(worksheet="Notifications")
        notifications_df = pd.DataFrame(notifications_data)
        updated_notifications_df = pd.concat([notifications_df, pd.DataFrame([notification])], ignore_index=True)
        conn.update(worksheet="Notifications", data=updated_notifications_df)

        # Clear cart and success message
        st.session_state.cart = []
        st.success(
            f"Payment successful! Your order is confirmed. Booking number: **#{booking_number}**. "
            f"Estimated preparation time: **{estimated_time}**."
        )

    except Exception as e:
        st.error(f"An error occurred while completing the order: {e}")
