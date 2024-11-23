import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px

# Establish Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

spreadsheet = "1zu1v-w6KnpB-Mw6D5_ikwL2jrkmzGT_MF6Dpu-J0Y_I"

def cust_dash(username):
    st.title("📊 Customer Dashboard")

    # Fetch and filter the orders data
    try:
        orders_data = pd.DataFrame(conn.read(spreadsheet_id=spreadsheet, worksheet="Order"))
        user_orders = orders_data[orders_data["Username"] == username]

        if user_orders.empty:
            st.info("No purchase history found.")
            return

        # Display purchase history
        st.header("🛍️ Your Past Orders")
        user_orders_filtered = user_orders.reset_index()
        user_orders_filtered = user_orders_filtered[['Booking Number', 'Timestamp', 'Coffee Type', 'Size', 'Add-ons', 'Status', 'Quantity', 'Final Price', 'Promo Code', 'Loyalty Points']]
        user_orders_filtered.index = user_orders_filtered.index + 1
        st.write(user_orders_filtered)

        # ---- Add visualizations below ----

        # 1. Purchase Trend Over Time
        st.markdown("---")
        st.subheader("📅 Purchase Trend Over Time")
        user_orders["Timestamp"] = pd.to_datetime(user_orders["Timestamp"], format='mixed')
        trend_data = user_orders.groupby(user_orders["Timestamp"].dt.date).size().reset_index(name="Orders")
        trend_fig = px.line(
            trend_data,
            x="Timestamp",
            y="Orders",
            title="Number of Orders Over Time",
            markers=True,
            labels={"Timestamp": "Date", "Orders": "Number of Orders"}
        )
        st.plotly_chart(trend_fig, use_container_width=True)

        # 2. Breakdown of Payment Methods
        st.markdown("---")
        st.subheader("💳 Payment Method Breakdown")
        payment_data = user_orders["Payment"].value_counts().reset_index()
        payment_data.columns = ["Payment Method", "Count"]
        payment_fig = px.pie(
            payment_data,
            names="Payment Method",
            values="Count",
            title="Preferred Payment Methods",
            hole=0.4
        )
        st.plotly_chart(payment_fig, use_container_width=True)

        # 3. Coffee Orders Breakdown
        st.markdown("---")
        st.subheader("☕ Coffee Orders Breakdown")
        coffee_data = user_orders["Coffee Type"].value_counts().reset_index()
        coffee_data.columns = ["Coffee Type", "Count"]
        coffee_fig = px.bar(
            coffee_data,
            x="Coffee Type",
            y="Count",
            color="Coffee Type",
            title="Most Ordered Coffees",
            text="Count"
        )
        coffee_fig.update_traces(textposition="outside")
        coffee_fig.update_layout(showlegend=False)
        st.plotly_chart(coffee_fig, use_container_width=True)

        # 4. Spending Pattern
        st.markdown("---")
        st.subheader("💰 Spending Pattern")
        spending_data = user_orders.groupby(user_orders["Timestamp"].dt.date)["Final Price"].sum().reset_index()
        spending_data.columns = ["Date", "Total Spending"]
        spending_fig = px.area(
            spending_data,
            x="Date",
            y="Total Spending",
            title="Spending Trend Over Time",
            labels={"Date": "Date", "Total Spending": "Amount Spent ($)"}
        )
        st.plotly_chart(spending_fig, use_container_width=True)

    except Exception as e:
        st.error(f"Error loading customer dashboard: {e}")
