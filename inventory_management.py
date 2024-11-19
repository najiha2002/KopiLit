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


##Working but right now it not real time, so biila tekan button update
##dalm sheet update tpi dia tk display
##
##
# import streamlit as st
# from streamlit_gsheets import GSheetsConnection
# import pandas as pd

# # Create a connection object for Google Sheets
# conn = st.connection("gsheets", type=GSheetsConnection)

# def manage_inventory():
#     st.write("Monitor and update inventory levels here.")

#     # Connect to the "Inventory" worksheet
#     inventory_sheet = conn.read(worksheet="Inventory")  # Adjust to your actual worksheet name
#     inventory_df = pd.DataFrame(inventory_sheet)  # Convert the data to a DataFrame

#     # Ensure the DataFrame has the expected structure (assuming columns 'Item' and 'Stock')
#     if 'Item' in inventory_df.columns and 'Stock' in inventory_df.columns:
#         inventory = {row['Item']: row['Stock'] for _, row in inventory_df.iterrows()}
#     else:
#         st.error("Inventory data does not contain required columns.")
#         return

#     # Display the inventory and allow for manual updates
#     updated_inventory = {}
#     for item, stock in inventory.items():
#         col1, col2 = st.columns([2, 1])  # Adjust column widths for better layout
        
#         with col1:
#             st.write(f"{item}: {stock} units")
        
#         with col2:
#             new_stock = st.number_input(f"Update {item} stock", min_value=0, value=int(stock), key=item)
#             updated_inventory[item] = new_stock

#     # Automatically update display in real-time based on user inputs

#     # Button to update the inventory in Google Sheets
#     if st.button("Update Inventory"):
#         # Create a DataFrame to update the inventory in Google Sheets
#         updated_inventory_df = pd.DataFrame(updated_inventory.items(), columns=['Item', 'Stock'])
        
#         # Update the Google Sheets Inventory worksheet with the updated DataFrame
#         try:
#             conn.update(worksheet="Inventory", data=updated_inventory_df)  # Update the inventory worksheet
#             st.success("Inventory updated successfully!")
#         except Exception as e:
#             st.error(f"An error occurred while updating Google Sheets: {e}")


# manage_inventory()



import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Create a connection object for Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

def fetch_inventory():
    """
    Fetch inventory data from Google Sheets.
    """
    inventory_sheet = conn.read(worksheet="Inventory")  # Adjust to your actual worksheet name
    return pd.DataFrame(inventory_sheet)  # Convert the data to a DataFrame

def manage_inventory():
    st.write("Monitor and update inventory levels here.")

    # Fetch the latest inventory data from Google Sheets
    inventory_df = fetch_inventory()

    # Ensure the DataFrame has the expected structure (assuming columns 'Item' and 'Stock')
    if 'Item' in inventory_df.columns and 'Stock' in inventory_df.columns:
        inventory = {row['Item']: row['Stock'] for _, row in inventory_df.iterrows()}
    else:
        st.error("Inventory data does not contain required columns.")
        return

    # Display the inventory and allow for manual updates
    updated_inventory = {}
    for item, stock in inventory.items():
        col1, col2 = st.columns([2, 1])  # Adjust column widths for better layout
        
        with col1:
            st.write(f"{item}")  # Display only the item name
        
        with col2:
            new_stock = st.number_input(f"Update {item} stock", min_value=0, value=int(stock), key=f"{item}_stock")
            updated_inventory[item] = new_stock

    # Button to update the inventory in Google Sheets
    if st.button("Update Inventory"):
        # Create a DataFrame to update the inventory in Google Sheets
        updated_inventory_df = pd.DataFrame(updated_inventory.items(), columns=['Item', 'Stock'])
        
        # Update the Google Sheets Inventory worksheet with the updated DataFrame
        try:
            conn.update(worksheet="Inventory", data=updated_inventory_df)  # Update the inventory worksheet
            st.success("Inventory updated successfully!")
        except Exception as e:
            st.error(f"An error occurred while updating Google Sheets: {e}")



