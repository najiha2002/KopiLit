import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px

# Establish Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

def analytics():
    st.title("📊 Analytics Dashboard")
    st.write("Real-time insights into current orders, inventory levels, and sales performance.")

    # Load data from Google Sheets
    try:
        sales_data = pd.DataFrame(conn.read(worksheet="Order"))
        inventory_data = pd.DataFrame(conn.read(worksheet="Inventory"))
        user_data = pd.DataFrame(conn.read(worksheet="User"))
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return

    # Filter: Date Range for Sales Data
    st.markdown("### 🗓️ Filter Sales by Date Range")
    if 'Timestamp' in sales_data.columns:
        sales_data['Timestamp'] = pd.to_datetime(sales_data['Timestamp'], errors='coerce')
        min_date = sales_data['Timestamp'].min().date()
        max_date = sales_data['Timestamp'].max().date()
        start_date, end_date = st.date_input(
            "Select Date Range:",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        sales_data = sales_data[(sales_data['Timestamp'].dt.date >= start_date) & (sales_data['Timestamp'].dt.date <= end_date)]
    else:
        st.warning("Timestamp column missing in sales data.")

    st.markdown("---")

    # Total Revenue and Key Metrics
    st.markdown("### 📈 Key Performance Metrics")
    if 'Price' in sales_data.columns:
        completed_sales = sales_data[sales_data['Status'].str.lower() == 'completed']
        completed_sales['Price'] = pd.to_numeric(completed_sales['Price'], errors='coerce')
        total_revenue = completed_sales['Price'].sum()
        total_orders = len(completed_sales)
        avg_order_value = total_revenue / total_orders if total_orders > 0 else 0

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Revenue", f"${total_revenue:.2f}")
        col2.metric("Total Completed Orders", total_orders)
        col3.metric("Average Order Value", f"${avg_order_value:.2f}")

    st.markdown("---")

    # Sales Trend Over Time
    st.markdown("### 📅 Sales Trend Over Time")
    if 'Timestamp' in sales_data.columns and 'Price' in sales_data.columns:
        sales_data['Price'] = pd.to_numeric(sales_data['Price'], errors='coerce')
        sales_data['Date'] = sales_data['Timestamp'].dt.date
        daily_sales = sales_data.groupby('Date')['Price'].sum().reset_index()

        if not daily_sales.empty:
            fig5 = px.line(
                daily_sales,
                x='Date',
                y='Price',
                title='Sales Trend Over Time',
                labels={'Date': 'Date', 'Price': 'Total Revenue'},
                markers=True
            )
            st.plotly_chart(fig5, use_container_width=True)
        else:
            st.info("No sales data available for the selected date range.")

    st.markdown("---")

    # Low Stock Items
    st.markdown("### 🔍 Low Stock Alerts")
    if 'Item' in inventory_data.columns and 'Quantity' in inventory_data.columns:
        inventory_data['Quantity'] = pd.to_numeric(inventory_data['Quantity'], errors='coerce')
        low_stock_items = inventory_data[inventory_data['Quantity'] <= 5]

        if not low_stock_items.empty:
            st.warning("⚠️ The following items are running low on stock:")
            st.dataframe(low_stock_items)
        else:
            st.success("All inventory items are sufficiently stocked.")
    else:
        st.warning("Inventory data is incomplete.")

    st.markdown("---")


    # Heatmap: Popular Coffee Types by Time of Day
    st.markdown("### 🕒 Coffee Popularity by Time of Day")
    if 'Coffee Type' in sales_data.columns and 'Timestamp' in sales_data.columns:
        try:
            # Extract hour from the Timestamp
            sales_data['Timestamp'] = pd.to_datetime(sales_data['Timestamp'], errors='coerce')
            sales_data['Hour'] = sales_data['Timestamp'].dt.hour

            # Group by Coffee Type and Hour
            coffee_time_data = sales_data.groupby(['Coffee Type', 'Hour']).size().reset_index(name='Orders')

            # Ensure Hour is sorted and numeric
            coffee_time_data['Hour'] = coffee_time_data['Hour'].astype(int)

            # Plot the heatmap
            if not coffee_time_data.empty:
                fig6 = px.density_heatmap(
                    coffee_time_data,
                    x='Hour',
                    y='Coffee Type',
                    z='Orders',
                    title='Coffee Popularity by Time of Day',
                    labels={'Hour': 'Hour of Day', 'Coffee Type': 'Type of Coffee', 'Orders': 'Number of Orders'},
                    color_continuous_scale="Blues",
                )
                fig6.update_xaxes(type='category')  # Ensure Hour is treated as discrete
                st.plotly_chart(fig6, use_container_width=True)
            else:
                st.info("No data available to analyze coffee popularity by time of day.")
        except Exception as e:
            st.error(f"Error processing data for coffee popularity heatmap: {e}")


    st.markdown("---")

    # Customer Demographics: Gender and Loyalty Points
    st.markdown("### 🧑‍🤝‍🧑 Customer Demographics")
    if 'Gender' in user_data.columns:
        gender_distribution = user_data['Gender'].value_counts().reset_index()
        gender_distribution.columns = ['Gender', 'Count']

        if not gender_distribution.empty:
            fig7 = px.pie(
                gender_distribution,
                names='Gender',
                values='Count',
                title='Customer Gender Distribution'
            )
            st.plotly_chart(fig7, use_container_width=True)
        else:
            st.info("No gender data available.")

    if 'Loyalty Points' in user_data.columns:
        user_data['Loyalty Points'] = pd.to_numeric(user_data['Loyalty Points'], errors='coerce').fillna(0)
        loyalty_distribution = user_data.groupby('Gender')['Loyalty Points'].mean().reset_index()

        if not loyalty_distribution.empty:
            fig8 = px.bar(
                loyalty_distribution,
                x='Gender',
                y='Loyalty Points',
                title='Average Loyalty Points by Gender',
                labels={'Loyalty Points': 'Average Points', 'Gender': 'Gender'}
            )
            st.plotly_chart(fig8, use_container_width=True)
        else:
            st.info("No loyalty points data available.")
