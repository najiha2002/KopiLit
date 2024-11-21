# customer_home.py
# hellor

import streamlit as st
import pandas as pd
import customer_order
import feedback
from streamlit_gsheets import GSheetsConnection

import datetime

# Establish Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

# styling
st.markdown(
    """
    <style>
    body {
        background-color: #f8f8f8; 
    }
    .title {
        color: #3E2723; 
        font-size: 40px; 
        font-weight: bold; 
    }
    .header {
        color: #6D4C41; 
        font-size: 30px; 
    }
    .subheader {
        color: #795548; 
    }
    .description {
        font-style: italic;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def check_notifications(username):
    try:
        # Load notifications from the Google Sheets
        notifications_data = pd.DataFrame(conn.read(worksheet="Notifications"))

        # Convert the Timestamp column to datetime format using the correct format
        notifications_data["Timestamp"] = pd.to_datetime(notifications_data["Timestamp"], format="%Y-%m-%d %H:%M:%S", errors="coerce")
        
        # Filter notifications for today and where the recipient is Admin
        today = datetime.datetime.now().date()
        notifications_data["Timestamp"] = notifications_data["Timestamp"].dt.date
        today_notifications = notifications_data[
            (notifications_data["Timestamp"] == today) &
            (notifications_data["Recipient"] == username)
        ]

        if not today_notifications.empty:
            # Add an expander to show today's notifications
            with st.sidebar.expander(f"Notifications for {today.strftime('%Y-%m-%d')}"):
                for index, notification in today_notifications.iterrows():
                    st.info(notification["Message"])
        else:
            st.sidebar.info("No notifications for today.")

    except Exception as e:
        st.sidebar.error(f"Error fetching notifications: {e}")

def display_menu():
    # Sample data for drinks sbb takda menu lg
    # experiment
    drinks = [
        {
            "name": "Latte",
            #"image": "latte.jpg",  # Path to the image
            "description": "A creamy latte made with the finest beans.",
            "price": 3.50,
        },
        {
            "name": "Cappuccino",
            #"image": "cappuccino.jpg",
            "description": "Rich espresso topped with foamed milk.",
            "price": 3.00,
        },
        {
            "name": "Espresso",
            #"image": "espresso.jpg",
            "description": "A strong shot of pure coffee.",
            "price": 2.50,
        },
        {
            "name": "Seasonal Pumpkin Spice Latte",
            #"image": "pumpkin_spice_latte.jpg",
            "description": "A seasonal favorite with pumpkin and spice flavors.",
            "price": 4.00,
        },
        {
            "name": "Mocha",
            #"image": "mocha.jpg",
            "description": "Chocolate and espresso combined for a rich treat.",
            "price": 3.75,
        },
        {
            "name": "Cold Brew",
            #"image": "cold_brew.jpg",
            "description": "Smooth and refreshing cold brew coffee.",
            "price": 3.25,
        },
    ]

# Menu Highlights Section with dummy data sbb menu takda lg
    st.header("Featured Drinks")

    # Create an expander for scrolling
    with st.expander("Display Featured Drinks", expanded=True):
        # Create a horizontal layout
        cols = st.columns(3)  # Adjust the number of columns based on your preference

        # Loop through drinks and display them in columns
        for i, drink in enumerate(drinks):
            with cols[i % 3]:  # This will distribute drinks in the created columns
                st.subheader(drink["name"])
                #st.image(drink["image"], width=150)  # Set the width of the image
                st.write(drink["description"])
                st.write(f"Price: ${drink['price']:.2f}")  # Format price to 2 decimal places

def flow(username):

    user_df = pd.DataFrame(conn.read(worksheet="User"))
    user_data = user_df[user_df['Username'] == username]
    first_name = user_data['First Name'].iloc[0]

    check_notifications(username)

    image_url = "https://i.ibb.co/rbPn1vt/kopilit.png"  
    # Add the image to the sidebar
    st.sidebar.image(image_url, use_column_width=True)
    
    # Sidebar navigation options
    st.sidebar.title(f"Hi, {first_name}!")
    navigation = st.sidebar.selectbox("Navigate", ["Home", "Menu", "Orders", "Rewards", "Account"])

    if navigation == "Home":
        st.header("Home")
        display_menu()
        

    # to start new order
    elif navigation == "Menu":
        customer_order.customer_order(username)

    # View current/past orders
    elif navigation == "Orders":
        st.header("Orders")
        orders_data = pd.DataFrame(conn.read(worksheet="Order"))
        user_orders = orders_data[orders_data['Username'] == username]
        st.write(user_orders)

    elif navigation == "Rewards":
        st.header("Rewards")
        # Assuming each order has an 'Amount' column for calculating rewards
        orders_data = pd.DataFrame(conn.read(worksheet="Order"))
        user_orders = orders_data[orders_data['Username'] == username]
        total_points = sum(order.get("Amount", 0) // 10 for order in user_orders.itertuples())
        st.write(f"You have {total_points} reward points.")

    elif navigation == "Account":
        st.header("Account")
        feedback.collect_feedback()

#flow("adarisa")

