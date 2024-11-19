# import streamlit as st
# from streamlit_gsheets import GSheetsConnection
# import random
# import pandas as pd
# import datetime

# # Create a connection object
# conn = st.connection("gsheets", type=GSheetsConnection)

# # Initialize session state for the cart if it doesn't exist
# if 'cart' not in st.session_state:
#     st.session_state.cart = []

# def customer_order(username):
#     st.title("Customer Order")
#     coffee_menu = {
#         "Americano": 3.00,
#         "Cappuccino": 3.50,
#         "Latte": 4.00,
#         "Caramel Macchiato": 4.50
#     }

#     st.header("Menu")
#     for coffee, price in coffee_menu.items():
#         st.write(f"{coffee}: ${price}")

#     coffee_type = st.selectbox("Select your coffee", list(coffee_menu.keys()))
#     size = st.selectbox("Select size", ["Small", "Medium", "Large"])
#     add_ons = st.multiselect("Select add-ons", ["Extra Sugar", "Milk", "Whipped Cream"])
#     quantity = st.number_input("Quantity", min_value=1)

#     # Calculate price based on coffee type and size
#     size_multiplier = {"Small": 1, "Medium": 1.5, "Large": 2}
#     price = coffee_menu[coffee_type] * size_multiplier[size]

#     if st.button("Add to Cart"):
#         st.session_state.cart.append({
#             "Coffee Type": coffee_type,
#             "Size": size,
#             "Add-ons": ', '.join(add_ons),
#             "Quantity": quantity,
#             "Price": (price * quantity)
#         })
#         st.success(f"{coffee_type} added to cart!")

#     st.header("Your Cart")
#     if len(st.session_state.cart) == 0:
#         st.write("Your cart is empty.")
#     else:
#         total_price = 0
#         for idx, item in enumerate(st.session_state.cart):
#             col1, col2 = st.columns([3, 1])
#             with col1:
#                 st.write(f"{item['Coffee Type']} ({item['Size']}), Add-ons: {item['Add-ons']}, Quantity: {item['Quantity']}, Price: ${item['Price']}")
#             with col2:
#                 # Individual remove button for each cart item
#                 if st.button(f"Remove", key=f"remove_{idx}"):
#                     st.session_state.cart.pop(idx)
#                     st.rerun()  # Re-run to update the UI after removal

#             total_price += item['Price']

#         st.write(f"**Total Price: ${total_price:.2f}**")

#         if st.button("Place Order"):
#             orders_data = conn.read(worksheet="Order")
#             orders_df = pd.DataFrame(orders_data)

#             timestamp = datetime.datetime.now()
#             booking_number = str(random.randint(1000, 9999))
#             estimated_time = "5-10 minutes"
#             st.success(f"Order placed successfully! Your booking number is #{booking_number}. Estimated preparation time: {estimated_time}")

#             # Add cart items to Google Sheets
#             new_orders = []
#             for item in st.session_state.cart:
#                 new_orders.append({
#                     "Booking Number": booking_number,
#                     "Timestamp": timestamp,
#                     "Username": username,
#                     "Order Type": "Order",
#                     "Coffee Type": item['Coffee Type'],
#                     "Size": item['Size'],
#                     "Add-ons": item['Add-ons'],
#                     "Quantity": item['Quantity'],
#                     "Status": "Pending",
#                     "Price": total_price
                    
#                 })

#             new_order_df = pd.DataFrame(new_orders)

#             try:
#                 # Append the new orders to the existing orders data
#                 updated_orders_df = pd.concat([orders_df, new_order_df], ignore_index=True)

#                 # Update the Google Sheets Order worksheet with the updated DataFrame
#                 conn.update(worksheet="Order", data=updated_orders_df)
#                 st.success("All items in the cart have been ordered!")

#                 # Clear the cart
#                 st.session_state.cart = []

#                 # Create a new notification for the admin
#                 notification = {
#                     "Recipient": "Admin",  # Notify Admin
#                     "Sender": username,
#                     "Message": f"New order placed by {username}",
#                     "Timestamp": datetime.datetime.now()
#                 }

#                 new_notifications_df = pd.DataFrame([notification])

#                 # Append the notification to the Notifications sheet
#                 notifications_df = pd.DataFrame(conn.read(worksheet="Notifications"))
#                 updated_notifications_df = pd.concat([notifications_df, new_notifications_df], ignore_index=True)
#                 conn.update(worksheet="Notifications", data=updated_notifications_df)
#                 st.success("Order placed and admin notified!")

#                 # Optionally clear the cache to ensure fresh data on reload
#                 st.cache_data.clear()

#             except Exception as e:
#                 st.error(f"An error occurred while updating Google Sheets: {e}")


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
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"{item['Coffee Type']} ({item['Size']}), Add-ons: {item['Add-ons']}, Quantity: {item['Quantity']}, Price: ${item['Price']}")
            with col2:
                # Individual remove button for each cart item
                if st.button(f"Remove", key=f"remove_{idx}"):
                    st.session_state.cart.pop(idx)
                    st.rerun()

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
                    "Quantity": item['Quantity'],
                    "Status": "Pending",
                    "Price": total_price
                })

            new_order_df = pd.DataFrame(new_orders)

            try:
                # Fetch the latest inventory data
                inventory_data = conn.read(worksheet="Inventory")
                inventory_df = pd.DataFrame(inventory_data)
                inventory_dict = {row['Item']: row['Stock'] for _, row in inventory_df.iterrows()}

                # Define ingredient requirements for each coffee type
                ingredient_requirements = {
                    "Americano": {"Coffee Beans": 1},
                    "Cappuccino": {"Coffee Beans": 1, "Milk": 0.5},
                    "Latte": {"Coffee Beans": 1, "Milk": 1},
                    "Caramel Macchiato": {"Coffee Beans": 1, "Milk": 1, "Caramel Syrup": 0.5},
                }

                # Calculate total ingredient requirements based on the cart
                required_ingredients = {}
                for item in st.session_state.cart:
                    coffee_type = item['Coffee Type']
                    quantity = item['Quantity']
                    if coffee_type in ingredient_requirements:
                        for ingredient, amount in ingredient_requirements[coffee_type].items():
                            required_ingredients[ingredient] = required_ingredients.get(ingredient, 0) + amount * quantity

                # Check if inventory is sufficient
                for ingredient, required_amount in required_ingredients.items():
                    if inventory_dict.get(ingredient, 0) < required_amount:
                        st.error(f"Not enough {ingredient} in stock to fulfill the order.")
                        return

                # Deduct ingredients from inventory
                for ingredient, required_amount in required_ingredients.items():
                    inventory_dict[ingredient] -= required_amount

                # Update the inventory in Google Sheets
                updated_inventory_df = pd.DataFrame(
                    [{"Item": item, "Stock": stock} for item, stock in inventory_dict.items()]
                )
                conn.update(worksheet="Inventory", data=updated_inventory_df)

                # Append the new orders to the existing orders data
                updated_orders_df = pd.concat([orders_df, new_order_df], ignore_index=True)

                # Update the Google Sheets Order worksheet with the updated DataFrame
                conn.update(worksheet="Order", data=updated_orders_df)
                st.success("All items in the cart have been ordered!")

                # Clear the cart
                st.session_state.cart = []

                # Create a new notification for the admin
                notification = {
                    "Recipient": "Admin",  # Notify Admin
                    "Sender": username,
                    "Message": f"New order placed by {username}",
                    "Timestamp": datetime.datetime.now()
                }

                new_notifications_df = pd.DataFrame([notification])

                # Append the notification to the Notifications sheet
                notifications_df = pd.DataFrame(conn.read(worksheet="Notifications"))
                updated_notifications_df = pd.concat([notifications_df, new_notifications_df], ignore_index=True)
                conn.update(worksheet="Notifications", data=updated_notifications_df)
                st.success("Order placed and admin notified!")

                # Optionally clear the cache to ensure fresh data on reload
                st.cache_data.clear()

            except Exception as e:
                st.error(f"An error occurred while updating Google Sheets: {e}")
