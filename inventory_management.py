# # Syuk connectkan inventory dgan db dulu (googlesheet)
# # Lepas dh connect db connect dgan order page so kena ada function orderminus (tolak order)
# # Function ni akan dicall oleh page order, pastu run dkat sini utk tolak equal to the amount yg order

# import streamlit as st

# from streamlit_gsheets import GSheetsConnection

# # Assuming `conn` is the Google Sheets connection
# conn = st.connection("gsheets", type=GSheetsConnection)

# def manage_inventory():
#     st.title("Inventory Management")
#     st.write("Monitor and update inventory levels here.")
#     # Inventory display and manual update options
#     inventory = {
#         "Coffee Beans": 100,
#         "Milk": 50,
#         "Sugar": 80,
#         "Cups": 200
#     }
#     for item, stock in inventory.items():
#         st.write(f"{item}: {stock} units")
#         new_stock = st.number_input(f"Update {item} stock", min_value=0, value=stock)
#         inventory[item] = new_stock

#     if st.button("Update Inventory"):
#         st.success("Inventory updated successfully!")

# import streamlit as st
# import pandas as pd
# from streamlit_gsheets import GSheetsConnection

# # Create a connection object for Google Sheets
# conn = st.connection("gsheets", type=GSheetsConnection)

# def manage_inventory():
#     st.title("Inventory Management")
#     st.write("Monitor and update inventory levels here.")

#     # Connect to the "Inventory" worksheet
#     inventory_sheet = conn.read(worksheet="Inventory")  # Change "Inventory" to the name of your inventory worksheet
#     inventory_df = pd.DataFrame(inventory_sheet)  # Convert the data to a DataFrame

#     # Ensure the DataFrame has the expected structure (assuming columns 'Item' and 'Stock')
#     if 'Item' in inventory_df.columns and 'Stock' in inventory_df.columns:
#         inventory = {row['Item']: row['Stock'] for _, row in inventory_df.iterrows()}
#     else:
#         st.error("Inventory data does not contain required columns.")
#         return

#     # Display the inventory and allow for updates
#     for item, stock in inventory.items():
#         st.write(f"{item}: {stock} units")
#         new_stock = st.number_input(f"Update {item} stock", min_value=0, value=int(stock))
#         inventory[item] = new_stock

#     if st.button("Update Inventory"):
#         # Create a DataFrame to update the inventory in Google Sheets
#         updated_inventory_df = pd.DataFrame(inventory.items(), columns=['Item', 'Stock'])
        
#         # Update the Google Sheets Inventory worksheet with the updated DataFrame
#         try:
#             conn.update(worksheet="Inventory", data=updated_inventory_df)  # Update the inventory worksheet
#             st.success("Inventory updated successfully!")
#         except Exception as e:
#             st.error(f"An error occurred while updating Google Sheets: {e}")

# Run the inventory management app

import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# Create a connection object for Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

def manage_inventory():
    st.title("Inventory Management")
    st.write("Monitor and update inventory levels here.")

    # Function to read inventory from Google Sheets
    def get_inventory():
        inventory_sheet = conn.read(worksheet="Inventory")  # Read from the Inventory worksheet
        inventory_df = pd.DataFrame(inventory_sheet)  # Convert the data to a DataFrame
        
        # Ensure the DataFrame has the expected structure (assuming columns 'Item' and 'Stock')
        if 'Item' in inventory_df.columns and 'Stock' in inventory_df.columns:
            return {row['Item']: row['Stock'] for _, row in inventory_df.iterrows()}
        else:
            st.error("Inventory data does not contain required columns.")
            return {}

    # Initial inventory fetch
    inventory = get_inventory()

    # Display the inventory and allow for updates
    for item, stock in inventory.items():
        st.write(f"{item}: {stock} units")
        new_stock = st.number_input(f"Update {item} stock", min_value=0, value=int(stock))
        inventory[item] = new_stock

    if st.button("Update Inventory"):
        # Create a DataFrame to update the inventory in Google Sheets
        updated_inventory_df = pd.DataFrame(inventory.items(), columns=['Item', 'Stock'])
        
        # Update the Google Sheets Inventory worksheet with the updated DataFrame
        try:
            conn.update(worksheet="Inventory", data=updated_inventory_df)  # Update the inventory worksheet
            st.success("Inventory updated successfully!")
            
            # Re-fetch the inventory to reflect changes on the page
            inventory = get_inventory()  # Update the displayed inventory after change

            # Display updated inventory
            st.write("Updated Inventory:")
            for item, stock in inventory.items():
                st.write(f"{item}: {stock} units")
                
        except Exception as e:
            st.error(f"An error occurred while updating Google Sheets: {e}")

# Run the inventory management app
# manage_inventory()

