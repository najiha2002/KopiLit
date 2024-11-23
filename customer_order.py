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
    st.title("☕ Customer Order")

    # Coffee menu with emojis
    coffee_menu = {
        "Americano": 3.00,
        "Cappuccino": 3.50,
        "Latte": 4.00,
        "Caramel Macchiato": 4.50
    }

    # Display the menu
    st.markdown("### 📋 Menu")
    for coffee, price in coffee_menu.items():
        st.write(f"{coffee}: **${price:.2f}**")

    # Order selection form
    st.markdown("---")
    st.markdown("### 🛒 Place Your Order")
    coffee_type = st.selectbox("Select your coffee", list(coffee_menu.keys()))
    size = st.selectbox("Select size", ["Small", "Medium", "Large"])
    add_ons = st.multiselect("Select add-ons", ["Extra Sugar", "Milk", "Whipped Cream"])
    quantity = st.number_input("Quantity", min_value=1, step=1)

    # Calculate price based on coffee type and size
    size_multiplier = {"Small": 1, "Medium": 1.5, "Large": 2}
    price = coffee_menu[coffee_type] * size_multiplier[size]

    # Add to cart button
    if st.button("Add to Cart 🛒"):
        st.session_state.cart.append({
            "Coffee Type": coffee_type,
            "Size": size,
            "Add-ons": ', '.join(add_ons),
            "Quantity": quantity,
            "Price": (price * quantity)
        })
        st.success(f"{coffee_type} added to cart!")

    # Display the cart
    st.markdown("---")
    st.markdown("### 🧾 Your Cart")
    if len(st.session_state.cart) == 0:
        st.info("Your cart is empty. Add items to place an order.")
    else:
        total_price = 0
        # Display cart items in a structured format
        for idx, item in enumerate(st.session_state.cart):
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 2, 1, 1])

                # Display item details
                with col1:
                    st.markdown(
                        f"**{item['Coffee Type']}** ({item['Size']})"
                    )
                    st.caption(f"Add-ons: {item['Add-ons'] or 'None'}")
                
                # Quantity
                with col2:
                    st.markdown(f"**Quantity:** {item['Quantity']}")

                # Price
                with col3:
                    st.markdown(f"**Price:** ${item['Price']:.2f}")

                # Remove Button
                with col4:
                    if st.button("❌ Remove", key=f"remove_{idx}"):
                        st.session_state.cart.pop(idx)
                        st.rerun()

                # Accumulate total price
                total_price += item['Price']

        # Promo Code Section inside an Expander
        st.markdown("---")
        with st.expander("🎟️ Apply Promo Code"):
            promo_code = st.text_input("Enter your promo code:")
            discount = 0

            # Check promo code from the Promotion sheet
            try:
                promotion_data = conn.read(worksheet="Promotion")
                promotion_df = pd.DataFrame(promotion_data)
                if promo_code in promotion_df["name"].values:
                    promo_details = promotion_df[promotion_df["name"] == promo_code].iloc[0]
                    discount = promo_details["discount"] / 100 * total_price
                    st.success(f"Promo code applied! You saved ${discount:.2f}.")
                elif promo_code:
                    st.error("Invalid promo code. Please try again.")
            except Exception as e:
                st.error(f"Error fetching promo code data: {e}")


        # Calculate final price after discount
        final_price = total_price - discount
        st.markdown("---")
        st.markdown(f"#### 🏷️ **Total Price: ${final_price:.2f}**")

        # Loyalty Points Calculation
        loyalty_points = int(final_price)  # 1 point per $1 spent
        st.markdown(f"##### 🌟 **Loyalty Points Earned: {loyalty_points} points**")

        # Payment Section inside an Expander
        st.markdown("---")
        with st.expander("💳 Proceed to Payment"):
            st.markdown("### Select Payment Method")

            # Initialize session state for payment method
            if "selected_payment_option" not in st.session_state:
                st.session_state.selected_payment_option = None

            # Payment Method Selection
            payment_option = st.radio(
                "Choose your payment method:",
                ["Credit/Debit Card", "PayPal", "Cash on Delivery"],
                key="payment_method_radio"
            )

            # Save the selected payment option in session state
            if payment_option:
                st.session_state.selected_payment_option = payment_option

            # Show corresponding payment form
            if st.session_state.selected_payment_option == "Credit/Debit Card":
                st.markdown("#### 💳 Enter Card Details")
                card_number = st.text_input("Card Number", key="card_number")
                card_holder = st.text_input("Card Holder Name", key="card_holder")
                expiry_date = st.text_input("Expiry Date (MM/YY)", key="expiry_date")
                cvv = st.text_input("CVV", type="password", key="cvv")

                if st.button("Verify", key="verify_card"):
                        if card_number and card_holder and expiry_date and cvv:
                            st.success(f"Card is valid.")
                            payment = "Card"

            elif st.session_state.selected_payment_option == "PayPal":
                st.markdown("#### 🅿️ Enter PayPal Email")
                paypal_email = st.text_input("PayPal Email", key="paypal_email")
                if st.button("Verify", key="verify_paypal"):
                        if paypal_email:
                            st.success(f"Paypal is valid.")
                            payment = "PayPal"

            elif st.session_state.selected_payment_option == "Cash on Delivery":
                payment = "COD"

        # Place Order button
        if st.button("Place Order ✅"):

            orders_data = conn.read(worksheet="Order")
            orders_df = pd.DataFrame(orders_data)

            # Generate booking details
            timestamp = datetime.datetime.now()
            booking_number = str(random.randint(1000, 9999))
            estimated_time = "5-10 minutes"

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
                    "Quantity": item['Quantity'],
                    "Status": "Pending",
                    "Price": total_price,
                    "Final Price": final_price,
                    "Promo Code": promo_code,
                    "Loyalty Points": loyalty_points,
                    "Payment": st.session_state.selected_payment_option
                })

            new_order_df = pd.DataFrame(new_orders)

            try:
                # Fetch inventory data
                inventory_data = conn.read(worksheet="Inventory")
                inventory_df = pd.DataFrame(inventory_data)
                inventory_dict = {row['Item']: row['Stock'] for _, row in inventory_df.iterrows()}

                # Ingredient requirements
                ingredient_requirements = {
                    "Americano": {"Coffee Beans": 1},
                    "Cappuccino": {"Coffee Beans": 1, "Milk": 0.5},
                    "Latte": {"Coffee Beans": 1, "Milk": 1},
                    "Caramel Macchiato": {"Coffee Beans": 1, "Milk": 1, "Caramel Syrup": 0.5},
                }

                # Calculate total ingredient requirements
                required_ingredients = {}
                for item in st.session_state.cart:
                    coffee_type = item['Coffee Type']
                    quantity = item['Quantity']
                    if coffee_type in ingredient_requirements:
                        for ingredient, amount in ingredient_requirements[coffee_type].items():
                            required_ingredients[ingredient] = required_ingredients.get(ingredient, 0) + amount * quantity

                # Check and update inventory
                for ingredient, required_amount in required_ingredients.items():
                    if inventory_dict.get(ingredient, 0) < required_amount:
                        st.error(f"Not enough {ingredient} in stock to fulfill the order.")
                        return

                for ingredient, required_amount in required_ingredients.items():
                    inventory_dict[ingredient] -= required_amount

                updated_inventory_df = pd.DataFrame(
                    [{"Item": item, "Stock": stock} for item, stock in inventory_dict.items()]
                )
                conn.update(worksheet="Inventory", data=updated_inventory_df)

                # Append orders to sheet
                updated_orders_df = pd.concat([orders_df, new_order_df], ignore_index=True)
                conn.update(worksheet="Order", data=updated_orders_df)
                

                # Clear cart
                st.session_state.cart = []

                # Notify admin about the order
                notification = {
                    "Recipient": "Admin",
                    "Sender": username,
                    "Message": f"New order placed by {username}",
                    "Timestamp": datetime.datetime.now()
                }

                notifications_data = conn.read(worksheet="Notifications")
                notifications_df = pd.DataFrame(notifications_data)
                updated_notifications_df = pd.concat([notifications_df, pd.DataFrame([notification])], ignore_index=True)
                conn.update(worksheet="Notifications", data=updated_notifications_df)
                st.cache_data.clear()
                st.success(
                    f"Order placed successfully! Your booking number is **#{booking_number}**. "
                    f"Estimated preparation time: **{estimated_time}**"
                )

            except Exception as e:
                st.error(f"An error occurred while updating Google Sheets: {e}")
