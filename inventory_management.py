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
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Create a connection object for Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

def manage_inventory():
    st.write("Monitor and update inventory levels here.")

    # Connect to the "Inventory" worksheet
    inventory_sheet = conn.read(worksheet="Inventory")  # Adjust to your actual worksheet name
    inventory_df = pd.DataFrame(inventory_sheet)  # Convert the data to a DataFrame

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
            st.write(f"{item}: {stock} units")
        
        with col2:
            new_stock = st.number_input(f"Update {item} stock", min_value=0, value=int(stock), key=item)
            updated_inventory[item] = new_stock

    # Automatically update display in real-time based on user inputs

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




# test 22

# import streamlit as st
# from streamlit_gsheets import GSheetsConnection
# import pandas as pd

# # Create a connection object for Google Sheets
# conn = st.connection("gsheets", type=GSheetsConnection)

# def manage_inventory():
#     st.title("Inventory Management")
#     st.write("Monitor and update inventory levels here.")

#     # Connect to the "Inventory" worksheet
#     inventory_sheet = conn.read(worksheet="Inventory")  # Adjust to your actual worksheet name
#     inventory_df = pd.DataFrame(inventory_sheet)  # Convert the data to a DataFrame

#     # Ensure the DataFrame has the expected structure (assuming columns 'Item' and 'Stock')
#     if 'Item' in inventory_df.columns and 'Stock' in inventory_df.columns:
#         # Initialize session state for original inventory if it doesn't exist
#         if 'inventory' not in st.session_state:
#             st.session_state.inventory = {row['Item']: row['Stock'] for _, row in inventory_df.iterrows()}
#     else:
#         st.error("Inventory data does not contain required columns.")
#         return

#     # Display the current inventory without immediate changes
#     updated_inventory = {}
#     for item, stock in st.session_state.inventory.items():
#         col1, col2 = st.columns([2, 1])  # Adjust column widths for better layout
        
#         with col1:
#             st.write(f"{item}: {stock} units")
        
#         with col2:
#             new_stock = st.number_input(f"Update {item} stock", min_value=0, value=int(stock), key=f"update_{item}")
#             updated_inventory[item] = new_stock

#     # Button to update the inventory in Google Sheets
#     if st.button("Update Inventory"):
#         # Update the session state with the updated inventory values
#         st.session_state.inventory.update(updated_inventory)

#         # Create a DataFrame to update the inventory in Google Sheets
#         updated_inventory_df = pd.DataFrame(st.session_state.inventory.items(), columns=['Item', 'Stock'])
        
#         # Update the Google Sheets Inventory worksheet with the updated DataFrame
#         try:
#             conn.update(worksheet="Inventory", data=updated_inventory_df)  # Update the inventory worksheet
#             st.success("Inventory updated successfully!")
#         except Exception as e:
#             st.error(f"An error occurred while updating Google Sheets: {e}")


# # TNOR WORLKINGGG
# import streamlit as st
# from streamlit_gsheets import GSheetsConnection
# import pandas as pd

# # Create a connection object for Google Sheets
# conn = st.connection("gsheets", type=GSheetsConnection)

# # Initialize session state for inventory update status
# if 'updated' not in st.session_state:
#     st.session_state['updated'] = False

# def manage_inventory():
#     st.title("Inventory Management")
#     st.write("Monitor and update inventory levels here.")

#     def load_inventory():
#         # Connect to the "Inventory" worksheet
#         inventory_sheet = conn.read(worksheet="Inventory")  # Adjust to your actual worksheet name
#         inventory_df = pd.DataFrame(inventory_sheet)  # Convert the data to a DataFrame
        
#         # Ensure the DataFrame has the expected structure (assuming columns 'Item' and 'Stock')
#         if 'Item' in inventory_df.columns and 'Stock' in inventory_df.columns:
#             inventory = {row['Item']: row['Stock'] for _, row in inventory_df.iterrows()}
#             return inventory_df, inventory
#         else:
#             st.error("Inventory data does not contain required columns.")
#             return None, None

#     # Load the current inventory, checking if the data has been updated
#     if not st.session_state['updated']:
#         inventory_df, inventory = load_inventory()
#     else:
#         inventory_df, inventory = load_inventory()
#         st.session_state['updated'] = False  # Reset after the data has been updated and reloaded

#     if inventory is None:
#         return  # Stop execution if data is invalid

#     # Display the inventory and allow for manual updates
#     updated_inventory = {}
#     for item, stock in inventory.items():
#         col1, col2 = st.columns([2, 1])  # Adjust column widths for better layout
        
#         with col1:
#             st.write(f"{item}: {stock} units")
        
#         with col2:
#             new_stock = st.number_input(f"Update {item} stock", min_value=0, value=int(stock), key=item)
#             updated_inventory[item] = new_stock

#     # Button to update the inventory in Google Sheets
#     if st.button("Update Inventory"):
#         # Create a DataFrame to update the inventory in Google Sheets
#         updated_inventory_df = pd.DataFrame(updated_inventory.items(), columns=['Item', 'Stock'])
        
#         # Update the Google Sheets Inventory worksheet with the updated DataFrame
#         try:
#             conn.update(worksheet="Inventory", data=updated_inventory_df)  # Update the inventory worksheet
#             st.success("Inventory updated successfully!")
            
#             # Set session state to trigger reload of updated data
#             st.session_state['updated'] = True

#         except Exception as e:
#             st.error(f"An error occurred while updating Google Sheets: {e}")

