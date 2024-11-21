import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# Establish Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

def customer_rewards(username):
    st.title("🎉 Rewards Page")

    # Fetch order data from Google Sheets
    try:
        orders_data = conn.read(worksheet="Order")
        orders_df = pd.DataFrame(orders_data)

        # Filter orders for the specific user
        user_orders = orders_df[orders_df["Username"] == username]

        if user_orders.empty:
            st.warning("You have no orders yet.")
            return

        # Calculate total loyalty points for the user
        user_orders["Loyalty Points"] = user_orders["Loyalty Points"].astype(int)
        total_loyalty_points = user_orders["Loyalty Points"].sum()

        st.markdown(f"### 🌟 Hello, {username}!")
        st.markdown(f"#### You have **{total_loyalty_points}** loyalty points!")

    except Exception as e:
        st.error(f"Error fetching order data: {e}")
        return

    st.markdown("---")
    
    # Redeemable Rewards Section
    st.markdown("### 🎁 Redeem Your Rewards")
    rewards_catalog = {
        "Free Coffee (100 points)": 100,
        "Discount Voucher - $5 (200 points)": 200,
        "Discount Voucher - $10 (300 points)": 300,
    }

    for reward, points_required in rewards_catalog.items():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{reward}** - Requires **{points_required} points**")
        with col2:
            if st.button(f"Redeem", key=reward):
                if total_loyalty_points >= points_required:
                    # Deduct points from the user's total
                    total_loyalty_points -= points_required

                    # Update redeemed points in Google Sheets (Optional - depends on implementation)
                    # You can create a "Redeemed Rewards" sheet or column in the `Order` worksheet
                    st.success(f"You have successfully redeemed: {reward}!")
                    st.rerun()  # Refresh page to update points
                else:
                    st.error("You don't have enough points to redeem this reward.")

    st.markdown("---")

    # Order History and Points Earned
    st.markdown("### 🛍️ Order History & Points Earned")
    if not user_orders.empty:
        # Display user orders with loyalty points earned
        user_orders = user_orders[["Booking Number", "Coffee Type", "Quantity", "Final Price", "Loyalty Points"]]
        user_orders.rename(columns={"Final Price": "Total Price"}, inplace=True)
        st.dataframe(user_orders)
    else:
        st.info("No orders found for this account.")
