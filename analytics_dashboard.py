import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px

# Establish Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

def analytics():
    st.title("Analytics Dashboard")
    st.write("Real-time stats on current orders, inventory levels, and sales.")

    # Load data from Google Sheets
    try:
        sales_data = pd.DataFrame(conn.read(worksheet="Order"))
        inventory_data = pd.DataFrame(conn.read(worksheet="Inventory"))
        user_data = pd.DataFrame(conn.read(worksheet="User"))
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return

    # Bar Chart: Total Sales by Coffee Type
    if 'Status' in sales_data.columns and 'Coffee Type' in sales_data.columns and 'Price' in sales_data.columns:
        # Filter for completed orders
        completed_sales = sales_data[sales_data['Status'].str.lower() == 'completed']

        # Convert Price column to numeric
        completed_sales['Price'] = pd.to_numeric(completed_sales['Price'], errors='coerce')

        # Aggregate sales by Coffee Type
        coffee_price_sum = completed_sales.groupby('Coffee Type')['Price'].sum().reset_index()

        # Plot the data
        if not coffee_price_sum.empty:
            fig1 = px.bar(
                coffee_price_sum,
                x='Coffee Type',
                y='Price',
                title='Total Sales by Coffee Type',
                labels={'Price': 'Total Price', 'Coffee Type': 'Type of Coffee'}
            )
            with st.expander("Total Sales by Coffee Type", expanded=True):
                st.plotly_chart(fig1, use_container_width=True)
        else:
            st.info("No sales data available for completed orders.")

    # Bar Chart: Available Inventory Stock Quantity
    if 'Item' in inventory_data.columns and 'Quantity' in inventory_data.columns:
        # Convert Quantity column to numeric
        inventory_data['Quantity'] = pd.to_numeric(inventory_data['Quantity'], errors='coerce')

        # Plot the data
        if not inventory_data.empty:
            fig2 = px.bar(
                inventory_data,
                x='Item',
                y='Quantity',
                title='Stock Inventory Quantity',
                labels={'Quantity': 'Quantity', 'Item': 'Item'}
            )
            with st.expander("Stock Inventory Quantity", expanded=True):
                st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No inventory data available.")

    # Bar Chart: User Preference on Coffee Type (Completed Orders)
    if 'coffee_type' in sales_data.columns and 'quantity' in sales_data.columns and 'status' in sales_data.columns:
        # Filter for completed orders
        completed_orders = sales_data[sales_data['status'].str.lower() == 'completed']

        # Convert quantity column to numeric
        completed_orders['quantity'] = pd.to_numeric(completed_orders['quantity'], errors='coerce')

        # Aggregate coffee preferences
        coffee_preference = completed_orders.groupby('coffee_type')['quantity'].sum().reset_index()

        # Plot the data
        if not coffee_preference.empty:
            fig3 = px.bar(
                coffee_preference,
                x='coffee_type',
                y='quantity',
                title='User Preference on Coffee Type (Completed Orders)',
                labels={'quantity': 'Quantity', 'coffee_type': 'Coffee Type'}
            )
            with st.expander("User Preference on Coffee Type (Completed Orders)", expanded=True):
                st.plotly_chart(fig3, use_container_width=True)
        else:
            st.info("No completed orders available to analyze user preferences.")

    # Distribution of Customer Gender
    if 'Gender' in user_data.columns:
        gender_distribution = user_data['Gender'].value_counts().reset_index()
        gender_distribution.columns = ['Gender', 'Count']

        if not gender_distribution.empty:
            fig4 = px.pie(
                gender_distribution,
                names='Gender',
                values='Count',
                title='Customer Gender Distribution'
            )
            with st.expander("Customer Gender Distribution"):
                st.plotly_chart(fig4, use_container_width=True)
        else:
            st.info("No user data available for gender distribution.")
