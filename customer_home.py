# import streamlit as st
# import pandas as pd
# import customer_order
# import feedback
# import rewards
# from streamlit_gsheets import GSheetsConnection



# import datetime

# # Establish Google Sheets connection
# conn = st.connection("gsheets", type=GSheetsConnection)

# # styling
# st.markdown(
#     """
#     <style>
#     body {
#         background-color: #f8f8f8; 
#     }
#     .title {
#         color: #3E2723; 
#         font-size: 40px; 
#         font-weight: bold; 
#     }
#     .header {
#         color: #6D4C41; 
#         font-size: 30px; 
#     }
#     .subheader {
#         color: #795548; 
#     }
#     .description {
#         font-style: italic;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# def check_notifications(username):
#     try:
#         # Load notifications from the Google Sheets
#         notifications_data = pd.DataFrame(conn.read(worksheet="Notifications"))

#         # Convert the Timestamp column to datetime format using the correct format
#         notifications_data["Timestamp"] = pd.to_datetime(notifications_data["Timestamp"], format="%Y-%m-%d %H:%M:%S", errors="coerce")
        
#         # Filter notifications for today and where the recipient is Admin
#         today = datetime.datetime.now().date()
#         notifications_data["Timestamp"] = notifications_data["Timestamp"].dt.date
#         today_notifications = notifications_data[
#             (notifications_data["Timestamp"] == today) &
#             (notifications_data["Recipient"] == username)
#         ]

#         if not today_notifications.empty:
#             # Add an expander to show today's notifications
#             with st.sidebar.expander(f"Notifications for {today.strftime('%Y-%m-%d')}"):
#                 for index, notification in today_notifications.iterrows():
#                     st.info(notification["Message"])
#         else:
#             st.sidebar.info("No notifications for today.")

#     except Exception as e:
#         st.sidebar.error(f"Error fetching notifications: {e}")

# def display_menu():
#     # Sample data for drinks sbb takda menu lg
#     # experiment
#     drinks = [
#         {
#             "name": "Latte",
#             #"image": "latte.jpg",  # Path to the image
#             "description": "A creamy latte made with the finest beans.",
#             "price": 3.50,
#         },
#         {
#             "name": "Cappuccino",
#             #"image": "cappuccino.jpg",
#             "description": "Rich espresso topped with foamed milk.",
#             "price": 3.00,
#         },
#         {
#             "name": "Espresso",
#             #"image": "espresso.jpg",
#             "description": "A strong shot of pure coffee.",
#             "price": 2.50,
#         },
#         {
#             "name": "Seasonal Pumpkin Spice Latte",
#             #"image": "pumpkin_spice_latte.jpg",
#             "description": "A seasonal favorite with pumpkin and spice flavors.",
#             "price": 4.00,
#         },
#         {
#             "name": "Mocha",
#             #"image": "mocha.jpg",
#             "description": "Chocolate and espresso combined for a rich treat.",
#             "price": 3.75,
#         },
#         {
#             "name": "Cold Brew",
#             #"image": "cold_brew.jpg",
#             "description": "Smooth and refreshing cold brew coffee.",
#             "price": 3.25,
#         },
#     ]

# # Menu Highlights Section with dummy data sbb menu takda lg
#     st.header("Featured Drinks")

#     # Create an expander for scrolling
#     with st.expander("Display Featured Drinks", expanded=True):
#         # Create a horizontal layout
#         cols = st.columns(3)  # Adjust the number of columns based on your preference

#         # Loop through drinks and display them in columns
#         for i, drink in enumerate(drinks):
#             with cols[i % 3]:  # This will distribute drinks in the created columns
#                 st.subheader(drink["name"])
#                 #st.image(drink["image"], width=150)  # Set the width of the image
#                 st.write(drink["description"])
#                 st.write(f"Price: ${drink['price']:.2f}")  # Format price to 2 decimal places

# def flow(username):

#     user_df = pd.DataFrame(conn.read(worksheet="User"))
#     user_data = user_df[user_df['Username'] == username]
#     first_name = user_data['First Name'].iloc[0]

#     image_url = "https://i.ibb.co/rbPn1vt/kopilit.png"  
#     # Add the image to the sidebar
#     st.sidebar.image(image_url, use_column_width=True)

#     check_notifications(username)
    
#     # Sidebar navigation options
#     st.sidebar.title(f"Hi, {first_name}!")
#     navigation = st.sidebar.selectbox("Navigate", ["Home", "Menu", "Orders", "Rewards", "Account"])

#     if navigation == "Home":
#         st.header("Home")
#         display_menu()
        

#     # to start new order
#     elif navigation == "Menu":
#         customer_order.customer_order(username)

#     # View current/past orders
#     elif navigation == "Orders":
#         st.header("Orders")
#         orders_data = pd.DataFrame(conn.read(worksheet="Order"))
#         user_orders = orders_data[orders_data['Username'] == username]
#         st.write(user_orders)

#     elif navigation == "Rewards":
#         rewards.customer_rewards(username)

#     elif navigation == "Account":
#         st.header("Account")
#         feedback.collect_feedback()

# flow("adarisa")

import streamlit as st
import pandas as pd
import customer_order
import feedback
import rewards
from streamlit_gsheets import GSheetsConnection
import datetime

# Establish Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

def fetch_menu():
    menu_data = pd.DataFrame(conn.read(worksheet = "Menu"))
    return menu_data

# Styling
st.markdown(
    """
    <style>
    .product-card {
        text-align: center;
        background-color: #fff;
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 20px;
        margin: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .product-card img {
        border-radius: 10px;
        max-width: 100%;
        height: auto;
    }
    .product-title {
        font-size: 18px;
        font-weight: bold;
        color: #6D4C41;
        margin: 10px 0 5px;
    }
    .product-description {
        font-size: 14px;
        color: #795548;
        margin: 5px 0 15px;
    }
    .product-price {
        font-size: 16px;
        color: #3E2723;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .add-to-cart-btn {
        display: inline-block;
        background-color: #6D4C41;
        color: #fff;
        text-decoration: none;
        font-size: 14px;
        padding: 10px 20px;
        border-radius: 5px;
        margin-top: 10px;
    }
    .add-to-cart-btn:hover {
        background-color: #3E2723;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def check_notifications(username):
    try:
        # Load notifications from the Google Sheets
        notifications_data = pd.DataFrame(conn.read(worksheet="Notifications"))

        # Convert the Timestamp column to datetime format
        notifications_data["Timestamp"] = pd.to_datetime(
            notifications_data["Timestamp"], format="%Y-%m-%d %H:%M:%S", errors="coerce"
        )
        
        # Filter notifications for today and where the recipient matches the username
        today = datetime.datetime.now().date()
        notifications_data["Timestamp"] = notifications_data["Timestamp"].dt.date
        today_notifications = notifications_data[
            (notifications_data["Timestamp"] == today) & 
            (notifications_data["Recipient"] == username)
        ]

        if not today_notifications.empty:
            # Add an expander to show today's notifications
            with st.sidebar.expander(f"Notifications for {today.strftime('%Y-%m-%d')}"):
                for _, notification in today_notifications.iterrows():
                    st.info(notification["Message"])
        else:
            st.sidebar.info("No notifications for today.")
    except Exception as e:
        st.sidebar.error(f"Error fetching notifications: {e}")

def display_menu():
    st.header("Featured Menu")

    menu_data = fetch_menu()

    # Create an expander for the menu
    with st.expander("Display Featured Menu", expanded=True):
        # Display menu items in a grid layout
        cols = st.columns(3)  # Adjust the number of columns based on preference
        for index, row in menu_data.iterrows():  # Use the index to ensure unique keys
            # Handle missing images with a placeholder
            image_url = row['Image'] if 'Image' in row and pd.notna(row['Image']) else "https://via.placeholder.com/150"
            with cols[index % 3]:  # Distribute items across columns
                st.markdown(
                    f"""
                    <div class="product-card">
                        <img src="{image_url}" alt="{row['Name']}" style="width: 150px; height: 150px; object-fit: cover; border-radius: 10px;">
                        <div class="product-title">{row['Name']}</div>
                        <div class="product-description">Type: {row['Type']} | Size: {row['Size']}</div>
                        <div class="product-price">Price: RM{row['Price']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                
                # Order button with a unique key
                if st.button(f"Order {row['Name']}", key=f"order-{row['Menu ID']}-{index}"):
                    st.query_params(page="menu")  # Navigate to the menu page

                
def flow(username):
    # Load user data from Google Sheets
    user_df = pd.DataFrame(conn.read(worksheet="User"))
    user_data = user_df[user_df['Username'] == username]
    first_name = user_data['First Name'].iloc[0]

    # Add sidebar branding
    image_url = "https://i.ibb.co/rbPn1vt/kopilit.png"
    st.sidebar.image(image_url, use_column_width=True)

    # Display notifications
    check_notifications(username)

    # Sidebar navigation options
    st.sidebar.title(f"Hi, {first_name}!")
    navigation = st.sidebar.selectbox("Navigate", ["Home", "Menu", "Orders", "Rewards", "Account"])

    if navigation == "Home":
        display_menu()

    elif navigation == "Menu":
        customer_order.customer_order(username)

    elif navigation == "Orders":
        st.header("Your Orders")
        orders_data = pd.DataFrame(conn.read(worksheet="Order"))
        user_orders = orders_data[orders_data['Username'] == username]
        st.write(user_orders)

    elif navigation == "Rewards":
        st.header("Rewards")
        rewards.customer_rewards(username)

    elif navigation == "Account":
        st.header("Your Account")
        feedback.collect_feedback()


import streamlit as st

# Styling
st.markdown(
    """
    <style>
    body {
        background-color: #1b1b1b; /* Dark background */
    }
    .header-section {
        text-align: center;
        color: white;
        padding: 50px 20px;
        font-family: 'Georgia', serif;
    }
    .header-title {
        font-size: 3.5em;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .header-subtitle {
        font-size: 1.5em;
        margin-bottom: 40px;
    }
    .btn-container {
        margin-top: 20px;
    }
    .btn {
        display: inline-block;
        text-decoration: none;
        padding: 10px 25px;
        font-size: 1.1em;
        font-weight: bold;
        color: #1b1b1b;
        background-color: white;
        border: 2px solid white;
        border-radius: 5px;
        margin: 5px;
        transition: all 0.3s ease-in-out;
    }
    .btn:hover {
        background-color: #ffc107; /* Coffee color */
        color: #1b1b1b;
    }
    .stats-container {
        display: flex;
        justify-content: center;
        margin-top: 40px;
        gap: 50px;
    }
    .stats-item {
        text-align: center;
        color: white;
        font-family: 'Arial', sans-serif;
    }
    .stats-item h2 {
        font-size: 2.5em;
        margin: 0;
    }
    .stats-item p {
        font-size: 1em;
        margin: 0;
    }
    .coffee-image {
        text-align: center;
        margin-top: 30px;
    }
    .coffee-image img {
        max-width: 400px;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header Section
st.markdown(
    """
    <div class="header-section">
        <h1 class="header-title">Discover The Art Of Perfect Coffee</h1>
        <p class="header-subtitle">
            Experience the rich and bold flavors of KopiLit's exquisite coffee blends, 
            crafted to awaken your senses and start your day right.
        </p>
        <div class="btn-container">
            <a href="#" class="btn">Order Now</a>
            <a href="#" class="btn">Explore More</a>
        </div>
        <div class="stats-container">
            <div class="stats-item">
                <h2>50+</h2>
                <p>Items of Coffee</p>
            </div>
            <div class="stats-item">
                <h2>20+</h2>
                <p>Orders Running</p>
            </div>
            <div class="stats-item">
                <h2>2k+</h2>
                <p>Happy Customers</p>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Coffee Image Section
st.markdown(
    """
    <div class="coffee-image">
        <img src="https://thumbs.dreamstime.com/b/dynamic-coffee-splash-mug-dark-background-high-speed-capture-droplets-frozen-time-around-white-325109112.jpg" alt="Coffee Splash">
    </div>
    """,
    unsafe_allow_html=True,
)

