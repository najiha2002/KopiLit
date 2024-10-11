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