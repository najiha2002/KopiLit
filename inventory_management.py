import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Create a connection object for Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)
spreadsheet = "1zu1v-w6KnpB-Mw6D5_ikwL2jrkmzGT_MF6Dpu-J0Y_I"

@st.cache_data
def fetch_inventory():
    """
    Fetch inventory data from Google Sheets.
    """
    inventory_sheet = conn.read(spreadsheet_id = spreadsheet, worksheet="Inventory")  # Adjust to your actual worksheet name
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
            # Clear the cached data to fetch the updated inventory on reload
            st.cache_data.clear()
            st.success("Inventory updated successfully!")
        except Exception as e:
            st.error(f"An error occurred while updating Google Sheets: {e}")



