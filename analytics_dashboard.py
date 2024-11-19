import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px

conn = st.connection("gsheets", type=GSheetsConnection)
# Establish Google Sheets connection
def analytics():
    sales_data = pd.DataFrame(conn.read(worksheet="Order"))
    st.title("Analytics Dashboard")
    st.write("Real-time stats on current orders, inventory levels, and sales.")
    st.write("Total Orders Today: 50")
    st.write("Items Running Low: Coffee Beans, Cups")
    inventory_data = pd.DataFrame(conn.read(worksheet="Inventory"))
    user_data = pd.DataFrame(conn.read(worksheet="User"))

    # Bar Chart of Total Sales by Coffee Type
    if 'Status' in sales_data.columns == 'Completed' :
        # Convert the Price column to numeric, in case it contains string values
        sales_data['Price'] = sales_data.to_numeric(sales_data['Price'], errors='coerce')

        # Group by 'Coffee Type' and sum the 'Price'
        coffee_price_sum = sales_data.groupby('Coffee Type')['Price'].sum().reset_index()

        # Create a bar chart using Plotly
        fig1 = px.bar(coffee_price_sum, x='Coffee Type', y='Price', title='Total Sales by Coffee Type',
                    labels={'Price': 'Total Price', 'Coffee Type': 'Type of Coffee'})

        # Display the bar chart in expander Streamlit
        with st.expander("Total Sales by Coffee type"):
            st.plotly_chart(fig1, use_container_width=True)

    # Bar Chart of Available Inventory Stock Quantity
    if 'Item' in inventory_data.columns and 'Quantity' in inventory_data.columns:
        # Convert the Quantity column to numeric, in case it contains string values
        inventory_data['Quantity'] = pd.to_numeric(inventory_data['Quantity'], errors='coerce')
        
        # Create a bar chart using Plotly
        fig2 = px.bar(inventory_data, x='Item', y='Quantity', title='Stock Inventory Quantity',
                 labels={'Quantity': 'Quantity', 'Item': 'Item'})
        
        # Display the bar chart in Streamlit
        with st.expander("Stock Inventory Quantity"):
            st.plotly_chart(fig2, use_container_width=True)

    
    # Bar Chart of User Preference on Coffee Type (Ordered)


    # Distribution of Customer Gender 


    

    

    
