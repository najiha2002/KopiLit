# Syuk connectkan inventory dgan db dulu (googlesheet)
# Lepas dh connect db connect dgan order page so kena ada function orderminus (tolak order)
# Function ni akan dicall oleh page order, pastu run dkat sini utk tolak equal to the amount yg order

import streamlit as st

def manage_inventory():
    st.title("Inventory Management")
    st.write("Monitor and update inventory levels here.")
    # Inventory display and manual update options
    inventory = {
        "Coffee Beans": 100,
        "Milk": 50,
        "Sugar": 80,
        "Cups": 200
    }
    for item, stock in inventory.items():
        st.write(f"{item}: {stock} units")
        new_stock = st.number_input(f"Update {item} stock", min_value=0, value=stock)
        inventory[item] = new_stock

    if st.button("Update Inventory"):
        st.success("Inventory updated successfully!")